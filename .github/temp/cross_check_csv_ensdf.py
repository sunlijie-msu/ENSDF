#!/usr/bin/env python3
"""
Cross-check 2024LU03.md vs Si34_beta_decay_mixed.ens
Focus: Eg, DE, Ig(RI), DRI, gamma placement, level Jpi
"""
import csv, io, re

# ---------- Parse 2024LU03.md source ----------
text = open('A34/Si34/raw/2024LU03.md', encoding='utf-8').read()

# Extract table rows (lines with | at start after "E_initial" header)
lines = text.split('\n')
table_start = False
table_rows = []
for line in lines:
    if 'E_initial_level' in line:
        table_start = True
        continue
    if not table_start: continue
    if line.strip().startswith('|') and '---' not in line:
        parts = [c.strip() for c in line.split('|')]
        if len(parts) >= 2:
            table_rows.append(parts)

# Build levels and gammas from markdown table
# Column mapping (0-indexed after split):
# 1=E_init, 2=Jpi_i, 3=Eg, 4=Igamma, 5=Jpi_f, 6=BR, 7=BR_2019Li41

src_levels = []
src_gammas = []
current_level = None

for parts in table_rows:
    if len(parts) < 5: continue
    ei_raw = parts[1].replace('**','').strip()
    jpi = parts[2].replace('**','').strip()
    eg_raw = parts[3].replace('**','').strip()
    ig_raw = parts[4].replace('**','').strip()
    
    if ei_raw and ei_raw != '':  # new level
        # Parse Ei: "3325.7(2)" -> val=3325.7, unc=2
        m = re.match(r'([\d.]+)(?:\((\d+)\))?', ei_raw)
        ei_val = float(m.group(1)) if m else None
        ei_unc = m.group(2) if m and m.group(2) else ''
        current_level = {'Ei_val': ei_val, 'Ei_raw': ei_raw, 'Jpi': jpi}
        src_levels.append(current_level)
    
    if eg_raw:
        # Parse Eg
        m_eg = re.match(r'([\d.]+)(?:\((\d+)\))?', eg_raw)
        eg_val = float(m_eg.group(1)) if m_eg else None
        eg_unc = m_eg.group(2) if m_eg and m_eg.group(2) else ''
        # Parse Ig
        m_ig = re.match(r'([\d.]+)(?:\((\d+)\))?', ig_raw)
        ig_val = m_ig.group(1) if m_ig else ''
        ig_unc = m_ig.group(2) if m_ig and m_ig.group(2) else ''
        
        src_gammas.append({
            'parent_Ei': current_level['Ei_val'],
            'parent_Ei_raw': current_level['Ei_raw'],
            'Eg_raw': eg_raw,
            'Eg_val': eg_val,
            'Eg_unc': eg_unc,
            'Ig_raw': ig_raw,
            'Ig_val': ig_val,
            'Ig_unc': ig_unc,
        })

print('=== SOURCE LEVELS (%d) ===' % len(src_levels))
for l in src_levels:
    print('  Ei=%12s  Jpi=%s' % (l['Ei_raw'], l['Jpi']))
print()
print('=== SOURCE GAMMAS (%d) ===' % len(src_gammas))
for g in src_gammas:
    print('  Parent=%10s  Eg=%12s  Ig=%s' % (g['parent_Ei_raw'], g['Eg_raw'], g['Ig_raw']))

# ---------- Parse ENSDF target ----------
ens_lines = open('A34/Si34/new/Si34_beta_decay_mixed.ens').readlines()

ens_levels = []
ens_gammas = []
parent_e = None
parent_jpi = ''
for i, line in enumerate(ens_lines, 1):
    l = line.rstrip('\n')
    if len(l) < 9: continue
    if l[5] != ' ' or l[6] != ' ': continue  # skip continuations
    typ = l[7]
    if typ == 'L':
        e_str = l[9:19].strip()
        if e_str and (e_str[0].isdigit() or e_str[0] == '.'):
            parent_e = float(e_str)
        else:
            parent_e = None
        parent_jpi = l[22:39].strip()
        ens_levels.append({'E': parent_e, 'E_str': e_str, 'Jpi': parent_jpi, 'line': i})
    elif typ == 'G':
        ens_gammas.append({
            'line': i, 'parent_E': parent_e,
            'Eg_str': l[9:19].strip(), 'DE_str': l[19:21].strip(),
            'RI_str': l[22:29].strip(), 'DRI_str': l[29:31].strip(),
        })

print()
print('=== ENSDF LEVELS (%d) ===' % len(ens_levels))
for el in ens_levels:
    print('  Line%3d: E=%10s  Jpi=%s' % (el['line'], el['E_str'], el['Jpi']))
print()
print('=== ENSDF GAMMAS (%d) ===' % len(ens_gammas))
for eg in ens_gammas:
    print('  Line%3d: Parent_E=%8s  Eg=%8s  DE=%3s  RI=%8s  DRI=%3s' % (
        eg['line'], str(eg['parent_E']), eg['Eg_str'], eg['DE_str'], eg['RI_str'], eg['DRI_str']))

# ---------- Match and Compare ----------
def match_ens_gamma(src_g):
    """Match source gamma to ENSDF gamma by parent level + Eg"""
    src_p = src_g['parent_Ei']
    src_eg = src_g['Eg_val']
    if src_p is None or src_eg is None: return None
    best, best_dist = None, 9999
    for eg in ens_gammas:
        if eg['parent_E'] is None: continue
        p_dist = abs(eg['parent_E'] - src_p)
        try: e_dist = abs(float(eg['Eg_str']) - src_eg)
        except: continue
        if p_dist < 1.5 and e_dist < 0.5:
            return eg  # tolerant match
    return None

print()
print('='*90)
print('GAMMA CROSS-CHECK REPORT')
print('='*90)
print('%-4s %-14s %-5s %-10s %-5s %-12s %-8s %-5s %s' % (
    '#','SRC_Eg','DE','ENS_Eg','DE','SRC_Ig','ENS_RI','DRI','STATUS'))
print('-'*90)

mismatches = []
for idx, sg in enumerate(src_gammas):
    eg = match_ens_gamma(sg)
    if eg is None:
        mismatches.append((idx+1, sg['Eg_raw'], sg['parent_Ei_raw'], 'NO MATCH in ENSDF'))
        print('%-4d %-14s %-5s %-10s %-5s %-12s %-8s %-5s NO MATCH' % (
            idx+1, sg['Eg_raw'], sg['Eg_unc'], '???', '??', sg['Ig_raw'], '???', '??'))
        continue
    
    # Compare
    eg_ok = abs(float(eg['Eg_str']) - sg['Eg_val']) < 0.005
    de_ok = eg['DE_str'].strip() == sg['Eg_unc']
    ri_ok = eg['RI_str'] == sg['Ig_val']
    dri_ok = eg['DRI_str'].strip() == sg['Ig_unc']
    
    all_ok = eg_ok and de_ok and ri_ok and dri_ok
    status = 'OK' if all_ok else 'MIS'
    issues = []
    if not eg_ok: issues.append('Eg')
    if not de_ok: issues.append('DE')
    if not ri_ok: issues.append('RI')
    if not dri_ok: issues.append('DRI')
    
    print('%-4d %-14s %-5s %-10s %-5s %-12s %-8s %-5s %s%s' % (
        idx+1, sg['Eg_raw'], sg['Eg_unc'], eg['Eg_str'], eg['DE_str'].strip(),
        sg['Ig_raw'], eg['RI_str'], eg['DRI_str'].strip(),
        status, ' (%s)'%','.join(issues) if issues else ''))
    
    if not all_ok:
        mismatches.append((idx+1, sg['Eg_raw'], sg['Ig_raw'], ','.join(issues),
            'SRC: Eg=%s(%s) Ig=%s(%s)  ENS: Eg=%s(%s) RI=%s(%s)' % (
                sg['Eg_raw'], sg['Eg_unc'], sg['Ig_raw'], sg['Ig_unc'],
                eg['Eg_str'], eg['DE_str'], eg['RI_str'], eg['DRI_str'])))

# ---------- Compare Level Jpi ----------
print()
print('='*90)
print('LEVEL Jpi COMPARISON')
print('='*90)
for sl in src_levels:
    # Find ENSDF level
    match = None
    for el in ens_levels:
        if el['E'] is None: continue
        if abs(el['E'] - sl['Ei_val']) < 1.5:
            match = el
            break
    if match:
        jpi_ok = sl['Jpi'] == match['Jpi']
        print('  SRC: Ei=%12s Jpi=%-6s  ENS: Ei=%8s Jpi=%-6s  %s' % (
            sl['Ei_raw'], sl['Jpi'], match['E_str'], match['Jpi'], 'OK' if jpi_ok else 'MIS'))
        if not jpi_ok:
            mismatches.append((0, sl['Ei_raw'], '', 'Jpi', 'SRC=%s ENS=%s' % (sl['Jpi'], match['Jpi'])))
    else:
        print('  SRC: Ei=%12s Jpi=%-6s  ENS: NO MATCH' % (sl['Ei_raw'], sl['Jpi']))
        mismatches.append((0, sl['Ei_raw'], '', 'Jpi', 'No ENSDF level match'))

# ---------- Summary ----------
print()
print('='*90)
print('SUMMARY: %d gammas checked, %d mismatches' % (len(src_gammas), len([m for m in mismatches if m[0] > 0])))
print('Level Jpi mismatches: %d' % len([m for m in mismatches if m[0] == 0]))
for m in mismatches:
    if m[0] == 0:
        print('  Jpi: SRC=%s -> %s' % (m[1], m[-1]))
    else:
        print('  G%d: %s  %s' % (m[0], m[3], m[-1]))


