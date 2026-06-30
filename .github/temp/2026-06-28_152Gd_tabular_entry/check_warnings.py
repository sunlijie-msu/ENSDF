"""Cross-check formatcheck.fmt warnings against markdown Table I."""
import re, os

# Parse all warnings from formatcheck.fmt text (embedded below)
warnings = [
    (127, 1808.22, 490.98, 1317.24, 1318.52),
    (129, 1808.22, 1051.98, 756.24, 755.55),
    (147, 1915.41, 596.00, 1319.41, 1318.52),
    (180, 2133.42, 818.17, 1315.25, 1314.69),
    (352, 2729.35, 1411.50, 1317.84, 1318.52),
    (362, 2733.86, 2388.90, 344.94, 344.37),
    (365, 2742.94, 1634.60, 1108.33, 1109.38),
    (456, 2981.31, 2224.66, 756.63, 755.55),
    (484, 3012.23, 1902.30, 1109.92, 1109.38),
    (520, 3088.65, 2157.19, 931.44, 930.73),
    (521, 3088.65, 2333.77, 754.86, 755.55),
    (586, 3231.98, 1918.40, 1313.57, 1314.69),
    (588, 3231.98, 2475.17, 756.79, 755.55),
    (660, 3324.81, 2570.39, 754.40, 755.55),
    (704, 3369.61, 2440.22, 929.37, 930.73),
    (729, 3400.33, 3056.50, 343.80, 344.37),
    (820, 3508.80, 2577.36, 931.42, 930.73),
    (858, 3567.53, 2445.6, 1121.9, 1123.34),
    (916, 3635.52, 2880.82, 754.67, 755.55),
]

# Parse combined markdown
md_path = r'd:\X\ND\ENSDF\XUNDL\2026OSAA_CT11035_152Gd_Table_I.md'
with open(md_path, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')
markdown_data = {}  # (Ei, Eg) -> Ef
current_ei = None
for line in lines:
    s = line.strip()
    if not s.startswith('|'): continue
    if '$E_i$' in s and '$J^\\pi_i$' in s: continue
    if s.count(':---') >= 3: continue
    parts = s.split('|')
    if parts and parts[0]=='': parts=parts[1:]
    if parts and parts[-1]=='': parts=parts[:-1]
    cells = [c.strip() for c in parts]
    while len(cells) < 9: cells.append('')
    ei_raw = cells[0].replace('\u2212','-')
    eg_raw = cells[2].replace('\u2212','-')
    ef_raw = cells[4].replace('\u2212','-')
    if ei_raw:
        m = re.match(r'([\d.]+)\s*\((\d+)\)', ei_raw)
        current_ei = m.group(1) if m else ei_raw
    m_eg = re.match(r'([\d.]+)\s*\((\d+)\)', eg_raw) if eg_raw else None
    eg_val = m_eg.group(1) if m_eg else eg_raw
    m_ef = re.match(r'([\d.]+)\s*\((\d+)\)', ef_raw) if ef_raw else None
    ef_val = m_ef.group(1) if m_ef else ef_raw
    if eg_val and ef_val and current_ei:
        try:
            key = (float(current_ei), float(eg_val))
            markdown_data[key] = float(ef_val)
        except:
            pass

print('Cross-checking {} warnings against markdown...'.format(len(warnings)))
print()
print('| # | FMT Line | Ei | Eg | Calc FL | Assigned FL | Markdown Ef | Match? |')
print('|---|----------|-----|-----|---------|-------------|-------------|--------|')

all_match = True
for i, (fmt_line, ei, eg, calc_fl, assigned_fl) in enumerate(warnings, 1):
    key = (ei, eg)
    md_ef = markdown_data.get(key)
    if md_ef is None:
        # Try fuzzy match
        for k, v in markdown_data.items():
            if abs(k[0]-ei) < 0.01 and abs(k[1]-eg) < 0.01:
                md_ef = v
                break
    
    if md_ef is None:
        match_str = 'NOT FOUND in MD!'
        all_match = False
    elif abs(md_ef - assigned_fl) < 0.01:
        match_str = 'YES'
    elif abs(md_ef - calc_fl) < 0.01:
        match_str = 'Matches calc FL (not assigned)'
    else:
        match_str = 'NO - MD Ef={}'.format(md_ef)
        all_match = False
    
    print('| {} | {} | {} | {} | {} | {} | {} | {} |'.format(
        i, fmt_line, ei, eg, calc_fl, assigned_fl,
        md_ef if md_ef else '?', match_str))

print()
if all_match:
    print('ALL MATCH: Every assigned FL matches markdown Ef.')
else:
    print('MISMATCHES FOUND - see above.')
