# -*- coding: utf-8 -*-
"""Regenerate replacements.json with correct $ (not \\$) in new cG lines."""
import json

lines = open('A34/Cl34/new/Cl34_33s_p_g.ens', encoding='latin-1').readlines()

def ri_field(v):
    return v.ljust(7)

def dri_field(v):
    return v.ljust(2)

# (G_line_1based, cG_line_1based, new_ri, new_dri, new_cg_text, new_2cg_text)
cases = [
 (1286, 1287, '23.7', '24', 'weighted average of 23.5 {I24} (1977Da02) and 39 {I22} (1969Gr29).', 'Other: 23 (1983Wa27).'),
 (1288, 1289, '17.0', '74', 'weighted average of 14.7 {I74} (1977Da02) and 22 {I11} (1969Gr29).', 'Other: 15 (1983Wa27), 28 (1964Gl04).'),
 (1312, 1313, '13.6', '59', 'weighted average of 11.8 {I59} (1977Da02) and 17 {I8} (1969Gr29).', 'Other: 9.4 (1983Wa27).'),
 (1321, 1322, '79', '8', 'weighted average of 74 {I8} (1977Da02) and 100 {I17} (1969Gr29).', 'Other: 85 (1983Wa27), 70 (1964Gl04).'),
 (1351, 1352, '18.0', '18', 'weighted average of 18.2 {I18} (1977Da02) and 17 {I4} (1969Gr29).', 'Other: 19 (1983Wa27), 22 (1964Gl04).'),
 (1356, 1357, '6.8', '38', 'weighted average of 8.0 {I41} (1977Da02) and 5.7 {I38} (1969Gr29).', 'Other: 10 (1983Wa27), 22 (1964Gl04).'),
 (1358, 1359, '12.5', '40', 'weighted average of 9.1 {I46} (1977Da02) and 15 {I4} (1969Gr29).', 'Other: 9.8 (1983Wa27), 14 (1964Gl04).'),
 (None, 1361, None, None, 'weighted average of 25.0 {I25} (1977Da02) and 25 {I4} (1969Gr29).', 'Other: 23 (1983Wa27), 18 (1964Gl04).'),
 (1368, 1369, '10.7', '40', 'weighted average of 10.2 {I52} (1977Da02) and 11 {I4} (1969Gr29).', 'Other: 11 (1983Wa27).'),
 (1370, 1371, '20.1', '21', 'weighted average of 20.5 {I21} (1977Da02) and 15.1 {I76} (1969Gr29).', 'Other: 24 (1983Wa27), 28 (1964Gl04).'),
 (1388, 1389, '8.4', '38', 'weighted average of 7.3 {I38} (1977Da02) and 26 {I15} (1969Gr29).', 'Other: 13 (1983Wa27), 19 (1964Gl04).'),
 (1398, 1399, '49', '5', 'weighted average of 48 {I5} (1977Da02) and 56 {I17} (1969Gr29).', 'Other: 49 (1983Wa27), 100 (1964Gl04).'),
 (1523, 1524, '1.80', '80', 'weighted average of 1.59 {I80} (1977Da02) and 6.2 {I37} (1969Gr29).', 'Other: 1.4 (1983Wa27), 23 (1964Gl04).'),
 (None, 1526, None, None, 'weighted average of 11.1 {I11} (1977Da02) and 11.1 {I13} (1969Gr29).', 'Other: 9.9 (1983Wa27), 19 (1964Gl04).'),
 (1528, 1529, '1.2', '12', 'weighted average of 0.79 {I40} (1977Da02) and 4.9 {I13} (1969Gr29).', None),
 (1556, 1557, '20.4', '21', 'weighted average of 20.5 {I21} (1977Da02) and 19 {I7} (1969Gr29).', 'Other: 17 (1983Wa27).'),
 (1568, 1569, '34', '4', 'weighted average of 36 {I4} (1977Da02) and 31 {I5} (1969Gr29).', 'Other: 41 (1983Wa27), 28 (1964Gl04).'),
 (1570, 1571, '16.5', '18', 'weighted average of 18.2 {I18} (1977Da02) and 11.3 {I32} (1969Gr29).', 'Other: 16 (1983Wa27).'),
 (1616, 1617, '23.5', '24', 'weighted average of 24.1 {I24} (1977Da02) and 21 {I5} (1969Gr29).', 'Other: 21 (1983Wa27), 40 (1964Gl04).'),
 (1626, 1627, '11.2', '23', 'weighted average of 10.3 {I52} (1977Da02) and 11.4 {I23} (1969Gr29).', 'Other: 9.1 (1983Wa27).'),
 (1632, 1633, '25.6', '23', 'weighted average of 31.0 {I31} (1977Da02) and 22.7 {I23} (1969Gr29).', 'Other: 22 (1983Wa27).'),
 (1636, 1637, '36.5', '53', 'weighted average of 48 {I5} (1977Da02) and 34.1 {I23} (1969Gr29).', 'Other: 42 (1983Wa27), 60 (1964Gl04).'),
 (1640, 1641, '46', '5', 'weighted average of 52 {I5} (1977Da02) and 39 {I5} (1969Gr29).', 'Other: 42 (1983Wa27).'),
]

replacements = []
errors = 0
for c in cases:
    g_line, cg_line, new_ri, new_dri, new_cg_text, new_2cg_text = c
    cg_idx = cg_line - 1

    old_cg = lines[cg_idx]

    # Build new cG line with literal $ (not escaped)
    new_cg_full = ' 34CL cG RI$' + new_cg_text + '\n'

    if new_2cg_text:
        new_after = new_cg_full + ' 34CL2cG ' + new_2cg_text + '\n'
    else:
        new_after = new_cg_full

    if g_line:
        g_idx = g_line - 1
        old_g = lines[g_idx]
        new_g = old_g[:22] + ri_field(new_ri) + dri_field(new_dri) + old_g[31:]
        if len(new_g.rstrip('\n')) != 80:
            print('ERROR: new G line length %d (not 80) for G=%s' % (len(new_g.rstrip('\n')), g_line))
            errors += 1
        old_str = old_g + old_cg
        new_str = new_g + new_after
    else:
        old_str = old_cg
        new_str = new_after

    replacements.append({'old': old_str, 'new': new_str, 'g': g_line, 'cg': cg_line})

print('Total cases:', len(replacements))
print('Errors:', errors)

# Verify all old strings exist in file
file_content = open('A34/Cl34/new/Cl34_33s_p_g.ens', encoding='latin-1').read()
missing = 0
for i, r in enumerate(replacements):
    if r['old'] not in file_content:
        print('MISSING case %d G=%s cG=%s' % (i+1, r['g'], r['cg']))
        missing += 1
print('Missing:', missing)

# Save to JSON
with open('.github/temp/replacements2.json', 'w', encoding='latin-1') as f:
    json.dump(replacements, f, ensure_ascii=False, indent=2)
print('Saved to .github/temp/replacements2.json')
