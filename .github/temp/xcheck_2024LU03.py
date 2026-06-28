#!/usr/bin/env python3
import re

# Read and clean source
text = open('A34/Si34/raw/2024LU03.md', encoding='utf-8').read()
text = text.replace('\u2212','-').replace('\u2013','-').replace('\u200b','')

# Extract table rows
lines = text.split('\n')
table_start = False
src_levels = []
src_gammas = []
current_level = None

for line in lines:
    if 'E_initial_level' in line:
        table_start = True
        continue
    if not table_start: continue
    stripped = line.strip()
    if not stripped.startswith('|'): continue
    if '---' in stripped: continue
    
    parts = [p.strip() for p in stripped.split('|')]
    if len(parts) < 5: continue
    
    ei_raw = parts[1].replace('**','')
    jpi = parts[2].replace('**','')
    eg_raw = parts[3].replace('**','')
    ig_raw = parts[4].replace('**','')
    
    if ei_raw:
        m = re.match(r'([\d.]+)(?:\((\d+)\))?', ei_raw)
        if m:
            current_level = {'Ei_val':float(m.group(1)), 'Ei_raw':ei_raw, 'Jpi':jpi}
            src_levels.append(current_level)
    
    if eg_raw:
        m_eg = re.match(r'([\d.]+)(?:\((\d+)\))?', eg_raw)
        m_ig = re.match(r'([\d.]+)(?:\((\d+)\))?', ig_raw) if ig_raw else None
        src_gammas.append({
            'parent_Ei': current_level['Ei_val'],
            'parent_raw': current_level['Ei_raw'],
            'Eg_raw': eg_raw, 'Eg_val': float(m_eg.group(1)) if m_eg else None,
            'Eg_unc': m_eg.group(2) if m_eg and m_eg.group(2) else '',
            'Ig_raw': ig_raw, 'Ig_val': m_ig.group(1) if m_ig else '',
            'Ig_unc': m_ig.group(2) if m_ig and m_ig.group(2) else '',
        })

# Parse ENSDF
ens_lines = open('A34/Si34/new/Si34_beta_decay_mixed.ens').readlines()
ens_levels = []
ens_gammas = []
parent_e = None
parent_jpi = ''
for i, line in enumerate(ens_lines, 1):
    l = line.rstrip('\n')
    if len(l) < 9: continue
    if l[5] != ' ' or l[6] != ' ': continue
    typ = l[7]
    if typ == 'L':
        e_str = l[9:19].strip()
        try: parent_e = float(e_str)
        except: parent_e = None
        parent_jpi = l[22:39].strip()
        ens_levels.append({'E':parent_e, 'E_str':e_str, 'Jpi':parent_jpi, 'line':i})
    elif typ == 'G':
        ens_gammas.append({
            'line':i, 'parent_E':parent_e,
            'Eg_str':l[9:19].strip(), 'DE_str':l[19:21].strip(),
            'RI_str':l[22:29].strip(), 'DRI_str':l[29:31].strip(),
        })

# Match function
def match_ens(sg):
    for eg in ens_gammas:
        if eg['parent_E'] is None or sg['parent_Ei'] is None: continue
        if abs(eg['parent_E'] - sg['parent_Ei']) > 2.0: continue
        try: e_dist = abs(float(eg['Eg_str']) - sg['Eg_val'])
        except: continue
        if e_dist < 0.01:
            return eg
    return None

print('%-4s %-14s %-4s %-10s %-4s %-12s %-8s %-4s %s' % ('#','SRC_Eg','DE','ENS_Eg','DE','SRC_Ig','ENS_RI','DRI','STATUS'))
print('-'*85)

mismatches = []
for idx, sg in enumerate(src_gammas):
    eg = match_ens(sg)
    if eg is None:
        print('%-4d %-14s %-4s %-10s %-4s %-12s %-8s %-4s NO MATCH' % (
            idx+1, sg['Eg_raw'], sg['Eg_unc'], '???', '??', sg['Ig_raw'], '???', '??'))
        mismatches.append((idx+1, sg['Eg_raw'], sg['parent_raw'], 'NO ENSDF MATCH'))
        continue
    
    e_ok = abs(float(eg['Eg_str'])-sg['Eg_val'])<0.005
    de_ok = eg['DE_str'].strip() == sg['Eg_unc']
    ri_ok = eg['RI_str'] == sg['Ig_val']
    dri_ok = eg['DRI_str'].strip() == sg['Ig_unc']
    all_ok = e_ok and de_ok and ri_ok and dri_ok
    
    status = 'OK' if all_ok else 'MIS'
    print('%-4d %-14s %-4s %-10s %-4s %-12s %-8s %-4s %s' % (
        idx+1, sg['Eg_raw'], sg['Eg_unc'], eg['Eg_str'], eg['DE_str'].strip(),
        sg['Ig_raw'], eg['RI_str'], eg['DRI_str'].strip(), status))
    if not all_ok:
        issues = []
        if not e_ok: issues.append('Eg')
        if not de_ok: issues.append('DE')
        if not ri_ok: issues.append('RI')
        if not dri_ok: issues.append('DRI')
        mismatches.append((idx+1, sg['Eg_raw'], sg['Ig_raw'], ','.join(issues),
            'SRC:Eg=%s(%s) Ig=%s(%s) ENS:Eg=%s(%s) RI=%s(%s)' % (
                sg['Eg_raw'],sg['Eg_unc'],sg['Ig_raw'],sg['Ig_unc'],
                eg['Eg_str'],eg['DE_str'],eg['RI_str'],eg['DRI_str'])))

# Level Jpi compare
print()
print('LEVEL Jpi COMPARISON')
jpi_mismatches = []
for sl in src_levels:
    match = None
    for el in ens_levels:
        if el['E'] is None: continue
        if abs(el['E'] - sl['Ei_val']) < 2.0:
            match = el; break
    if match:
        ok = sl['Jpi'] == match['Jpi']
        print('  SRC Ei=%12s Jpi=%-6s  ENS Ei=%8s Jpi=%-6s  %s' % (
            sl['Ei_raw'],sl['Jpi'],match['E_str'],match['Jpi'],'OK' if ok else 'MIS'))
        if not ok:
            jpi_mismatches.append((sl['Ei_raw'], sl['Jpi'], match['Jpi']))
    else:
        print('  SRC Ei=%12s Jpi=%-6s  ENS: NO MATCH' % (sl['Ei_raw'],sl['Jpi']))

print()
print('TOTAL: %d gammas, %d mismatches' % (len(src_gammas), len(mismatches)))
print('Jpi mismatches: %d' % len(jpi_mismatches))
for m in mismatches:
    print('  G%d: %s -> %s' % (m[0], m[1], m[-1]))
for m in jpi_mismatches:
    print('  Jpi: SRC=%s(%s) ENS=%s' % m)
