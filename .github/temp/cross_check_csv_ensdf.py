#!/usr/bin/env python3
"""
Cross-check 2019LI41_isomer.csv against Si34_beta_decay_23.2_ms.ens
"""

import csv, io, re, sys

# --- 1. Parse CSV source ---
csv_str = open('A34/Si34/raw/2019LI41_isomer.csv', encoding='utf-8').read()
csv_str = csv_str.replace('\u2212', '-')  # Unicode minus → regular hyphen
csv_str = csv_str.replace('\u200b', '')   # zero-width spaces

reader = csv.reader(io.StringIO(csv_str))
header = next(reader)
print('HEADER:', header)

csv_levels = []  # list of dicts
csv_gammas = []  # list of dicts
current_level = None

for row in reader:
    cells = [c.strip() for c in row]
    ei, jpi, ib, eg, ig, ef = (cells[:6] if len(cells) >= 6 else
                                cells + [''] * (6 - len(cells)))
    if ei:
        current_level = {'Ei': ei, 'Jp': jpi, 'Ib': ib}
        csv_levels.append(current_level)
    if eg:
        csv_gammas.append({'parent_Ei': current_level['Ei'],
                           'Eg': eg, 'Ig': ig, 'Ef': ef})

print('\n=== CSV LEVELS ===')
for l in csv_levels:
    print('  Ei=%s  Jp=%s  Ib=%s' % (l['Ei'].ljust(15), l['Jp'].ljust(6), l['Ib'].ljust(8)))

print('\n=== CSV GAMMAS ===')
for g in csv_gammas:
    print('  Parent=%s  Eg=%s  Ig=%s  Ef=%s' % (
        g['parent_Ei'].ljust(12), g['Eg'].ljust(12),
        g['Ig'].ljust(8), g['Ef'].ljust(8)))

# --- 2. Parse ENSDF target ---
ens_lines = open('A34/Si34/new/Si34_beta_decay_23.2_ms.ens', encoding='utf-8').readlines()

def parse_ens_val_unc(val, unc, limit_char=None):
    """Extract value and uncertainty string from ENSDF L/G/B record fields."""
    v = val.strip()
    u = unc.strip() if unc else ''
    q = '?' if limit_char and limit_char.strip() == '?' else ''
    return v, u, q

ens_levels = []
ens_gammas = []
ens_betas = []

i = 0
while i < len(ens_lines):
    line = ens_lines[i].rstrip('\n')
    # Skip short lines
    if len(line) < 8:
        i += 1
        continue
    
    c6 = line[5] if len(line) > 5 else ' '
    c7 = line[6] if len(line) > 6 else ' '
    c8 = line[7] if len(line) > 7 else ' '
    
    # Only match non-continuation records (c6 is blank)
    if c6 != ' ':
        i += 1
        continue
    
    if c8 == 'L' and c7 == ' ':
        # L-record
        e_val = line[9:19].strip() if len(line) > 19 else ''
        e_unc = line[19:21].strip() if len(line) > 21 else ''
        jp = line[22:39].strip() if len(line) > 39 else ''
        q_flag = line[79] if len(line) > 79 else ' '
        
        ens_levels.append({
            'line_num': i + 1,
            'E': e_val,
            'DE': e_unc,
            'JP': jp,
            'Q': q_flag
        })
        
    elif c8 == 'G' and c7 == ' ':
        # G-record - find parent level (last L-record)
        parent = ens_levels[-1]['E'] if ens_levels else '?'
        e_val = line[9:19].strip() if len(line) > 19 else ''
        e_unc = line[19:21].strip() if len(line) > 21 else ''
        ri_val = line[22:29].strip() if len(line) > 29 else ''
        ri_unc = line[29:31].strip() if len(line) > 31 else ''
        
        ens_gammas.append({
            'line_num': i + 1,
            'parent_E': parent,
            'E': e_val,
            'DE': e_unc,
            'RI': ri_val,
            'DRI': ri_unc
        })
        
    elif c8 == 'B' and c7 == ' ':
        # B-record
        ib_val = line[9:19].strip() if len(line) > 19 else ''
        ib_unc = line[19:21].strip() if len(line) > 21 else ''
        logft_val = line[22:39].strip() if len(line) > 39 else ''
        logft_unc = line[39:49].strip() if len(line) > 49 else ''
        
        # Find parent level
        parent = ens_levels[-1]['E'] if ens_levels else '?'
        ens_betas.append({
            'line_num': i + 1,
            'parent_E': parent,
            'IB': ib_val,
            'DIB': ib_unc,
            'LOGF': logft_val,
            'DLOGF': logft_unc
        })
    
    i += 1

# --- 3. Compare ---
print('\n\n========== CROSS-CHECK REPORT ==========')

# Match levels by Ei
print('\n--- LEVEL COMPARISON ---')
print('%-15s %-15s %-8s %-15s %-8s %s' %
      ('CSV_Ei', 'ENS_E', 'CSV_Jp', 'ENS_JP', 'CSV_Ib', 'ENS_IB'))
print('-' * 80)

csv_level_map = {}
for l in csv_levels:
    # Parse Ei without uncertainty
    m = re.match(r'([\d.]+)', l['Ei'])
    if m:
        csv_level_map[m.group(1)] = l

level_matches = 0
level_issues = []
for el in ens_levels:
    e_match = None
    for csv_e, csv_l in csv_level_map.items():
        csv_e_clean = csv_e
        if abs(float(el['E']) - float(csv_e_clean)) < 0.5:
            e_match = csv_l
            break
    if e_match:
        level_matches += 1
        print('%-15s %-15s %-8s %-15s %-8s' %
              (e_match['Ei'].ljust(15), el['E'].ljust(15),
               e_match['Jp'].ljust(8), el['JP'].ljust(15),
               e_match['Ib'].ljust(8), '?' ))
    else:
        level_issues.append(el['E'])
        print('! MISMATCH: ENS level E=%s (line %d) not in CSV' %
              (el['E'], el['line_num']))

for csv_e, csv_l in csv_level_map.items():
    found = False
    for el in ens_levels:
        if abs(float(csv_e) - float(el['E'])) < 0.5:
            found = True
            break
    if not found:
        print('! MISMATCH: CSV level Ei=%s not found in ENS' % csv_e)

print('\nMatched: %d/%d ENS levels' % (level_matches, len(ens_levels)))
print('Matched: %d/%d CSV levels' % (len(csv_levels) - sum(1 for c in csv_level_map.values() 
    if not any(abs(float(c.keys() if isinstance(c,dict) else '')) for c in [])), len(csv_levels)))
