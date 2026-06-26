#!/usr/bin/env python3
"""
Cross-check 2019LI41_isomer.csv vs Si34_beta_decay_23.2_ms.ens
Focus: Eg, DE, Ig, DRI, gamma placement
"""
import csv, io, re

# ---------- Parse CSV ----------
raw = open('A34/Si34/raw/2019LI41_isomer.csv', encoding='utf-8').read()
raw = raw.replace('\u2212','-').replace('\u200b','')
reader = csv.reader(io.StringIO(raw))
next(reader)

csv_gammas = []
cur_level_ei = None
for row in reader:
    cells = [c.strip() for c in row]
    ei, jpi, ib, eg, ig, ef = (cells[:6] if len(cells)>=6 else cells+['']*(6-len(cells)))
    if ei:
        m = re.match(r'([\d.]+)', ei)
        cur_level_ei = float(m.group(1)) if m else None
    if eg:
        m_eg = re.match(r'([\d.]+)(?:\((\w+)\))?', eg)
        eg_val = float(m_eg.group(1)) if m_eg else None
        eg_unc = m_eg.group(2) if m_eg and m_eg.group(2) else ''
        m_ig = re.match(r'([\d.]+)\((\d+)\)', ig) if ig else None
        ig_val = m_ig.group(1) if m_ig else ''
        ig_unc = m_ig.group(2) if m_ig else ''
        m_ef = re.match(r'([\d.]+)', ef) if ef else None
        ef_val = float(m_ef.group(1)) if m_ef else None
        csv_gammas.append({
            'parent_Ei': cur_level_ei, 'Eg_raw': eg, 'Eg_val': eg_val, 'Eg_unc': eg_unc,
            'Ig_raw': ig, 'Ig_val': ig_val, 'Ig_unc': ig_unc,
            'Ef_val': ef_val
        })

# ---------- Parse ENSDF ----------
lines = open('A34/Si34/new/Si34_beta_decay_23.2_ms.ens').readlines()
ens_levels = []
ens_gammas = []
parent_e = None
for i, line in enumerate(lines, 1):
    l = line.rstrip('\n')
    if len(l) < 9: continue
    if l[5] != ' ' or l[6] != ' ': continue
    typ = l[7]
    if typ == 'L':
        e_str = l[9:19].strip()
        if e_str and e_str[0].isdigit():
            try: parent_e = float(e_str)
            except: parent_e = None
        else:
            parent_e = None
        ens_levels.append((parent_e, i))
    elif typ == 'G':
        ens_gammas.append({
            'line': i, 'parent_E': parent_e,
            'Eg_str': l[9:19].strip(), 'DE_str': l[19:21].strip(),
            'RI_str': l[22:29].strip(), 'DRI_str': l[29:31].strip(),
        })

# ---------- Match ----------
def match_gamma(csv_g):
    best, best_dist = None, 9999
    csv_p = csv_g['parent_Ei']
    csv_eg = csv_g['Eg_val']
    for eg in ens_gammas:
        if eg['parent_E'] is None: continue
        if csv_p is None: continue
        p_dist = abs(eg['parent_E'] - csv_p)
        try: e_dist = abs(float(eg['Eg_str']) - csv_eg)
        except: continue
        if p_dist < 3.0 and e_dist < 0.01:
            return eg  # tolerant match (GLSC fit shifts levels)
    return None

# ---------- Report ----------
print("%3s %12s %6s %12s %6s %10s %8s %6s %10s" % ('#','CSV_Eg','EgUnc','ENS_Eg','DE','CSV_Ig','ENS_RI','DRI','STATUS'))
print('-'*85)
mismatches = []
for idx, cg in enumerate(csv_gammas):
    eg = match_gamma(cg)
    if eg is None:
        print("%3d %12s %6s %12s %6s %10s %8s %6s %10s" % (idx+1, cg['Eg_raw'], cg['Eg_unc'], '???', '??', cg['Ig_raw'], '???', '??', 'MISSING'))
        mismatches.append((idx+1, cg['Eg_raw'], cg['Ig_raw'], 'MISSING in ENSDF'))
        continue
    
    eg_ok = abs(float(eg['Eg_str']) - cg['Eg_val']) < 0.005
    de_ok = (eg['DE_str'].strip() == cg['Eg_unc']) or (cg['Eg_unc'] == 'E0' and eg['DE_str'].strip() == '')
    ri_ok = eg['RI_str'] == cg['Ig_val']
    dri_ok = eg['DRI_str'].strip() == cg['Ig_unc']
    
    # Special: E0 gamma has intensity in TI not RI
    if cg['Eg_unc'] == 'E0':
        ri_ok = True
        dri_ok = True
    
    all_ok = eg_ok and de_ok and ri_ok and dri_ok
    status = 'OK' if all_ok else ''
    issues = []
    if not eg_ok: issues.append('Eg')
    if not de_ok: issues.append('DE')
    if not ri_ok: issues.append('RI')
    if not dri_ok: issues.append('DRI')
    
    print("%3d %12s %6s %12s %6s %10s %8s %6s %10s" % (
        idx+1, cg['Eg_raw'], cg['Eg_unc'], eg['Eg_str'], eg['DE_str'].strip(),
        cg['Ig_raw'], eg['RI_str'], eg['DRI_str'].strip(),
        all_ok and 'OK' or 'MISMATCH'
    ))
    if not all_ok:
        mismatches.append((idx+1, cg['Eg_raw'], cg['Ig_raw'], ','.join(issues),
                          'CSV: Eg=%s(%s) Ig=%s(%s) vs ENS: Eg=%s(%s) RI=%s(%s)' % (
                              cg['Eg_raw'], cg['Eg_unc'], cg['Ig_raw'], cg['Ig_unc'],
                              eg['Eg_str'], eg['DE_str'], eg['RI_str'], eg['DRI_str'])))

print()
print('TOTAL GAMMAS: CSV=%d  ENSDF=%d' % (len(csv_gammas), len(ens_gammas)))
print('MISMATCHES: %d' % len(mismatches))
for m in mismatches:
    print('  #%d %s' % (m[0], m[-1]))

