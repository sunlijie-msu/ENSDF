"""
Build replacement pairs for remaining Ep merges (REPs 08-30) and
wg splits (REPs 31-34), reading from CURRENT file state.
Uses content-based line finding instead of hardcoded line numbers.
"""
import json

content = open(r'd:\X\ND\ENSDF\A34\Cl34\new\Cl34_33s_p_g.ens', 'rb').read().decode('ascii')
lines = content.split('\r\n')
CRLF = '\r\n'

def find_line(unique_substring):
    """Find index (0-based) of the first line containing the substring."""
    for i, line in enumerate(lines):
        if unique_substring in line:
            return i
    return None

def L_by_content(unique_substring):
    """Return the full 80-char line containing the unique substring."""
    i = find_line(unique_substring)
    if i is None:
        raise ValueError(f'NOT FOUND: {repr(unique_substring)}')
    return lines[i]

def L_next(unique_substring, offset=1):
    """Return the line at offset from the line containing unique_substring."""
    i = find_line(unique_substring)
    if i is None:
        raise ValueError(f'NOT FOUND: {repr(unique_substring)}')
    return lines[i + offset]

EP = '$E(p)(lab)='
WG = '$|w|g='

# REP 08: L6228.5: 3-line merge (1044-1046 in orig, now shifted)
# Pattern: first line contains 1118.5, second has 1119.6, third has 34CL2cL
rep08_L0 = L_by_content('E(p)(lab)=1118.5 {I3} (1983Wa27)')
rep08_L1 = L_next('E(p)(lab)=1118.5 {I3} (1983Wa27)', 1)
rep08_L2 = L_next('E(p)(lab)=1118.5 {I3} (1983Wa27)', 2)

# REP 09: L6273.1: 2-line merge: 1164.5 + 1165
rep09_L0 = L_by_content('E(p)(lab)=1164.5 {I13} (1977Da02)')
rep09_L1 = L_next('E(p)(lab)=1164.5 {I13} (1977Da02)', 1)

# REP 10: L6322.3: 2-line merge: 1215.2 + 1214
rep10_L0 = L_by_content('E(p)(lab)=1215.2 {I13} (1977Da02)')
rep10_L1 = L_next('E(p)(lab)=1215.2 {I13} (1977Da02)', 1)

# REP 11: L6361.3: 2-line merge: 1255.4 + 1255
rep11_L0 = L_by_content('E(p)(lab)=1255.4 {I13} (1977Da02)')
rep11_L1 = L_next('E(p)(lab)=1255.4 {I13} (1977Da02)', 1)

# REP 12: L6369.8: 2-line merge: 1264.4 + 1266.4
rep12_L0 = L_by_content('E(p)(lab)=1264.4 {I2} (1983Wa27)')
rep12_L1 = L_next('E(p)(lab)=1264.4 {I2} (1983Wa27)', 1)

# REP 13: L6441.5: 2-line merge: 1338.4 + 1336.8
rep13_L0 = L_by_content('E(p)(lab)=1338.4 {I14} (1977Da02)')
rep13_L1 = L_next('E(p)(lab)=1338.4 {I14} (1977Da02)', 1)

# REP 14: L6450.5: 2-line merge: 1347.3 + 1348.9
rep14_L0 = L_by_content('E(p)(lab)=1347.3 {I2} (1983Wa27)')
rep14_L1 = L_next('E(p)(lab)=1347.3 {I2} (1983Wa27)', 1)

# REP 15: L6479.2: 2-line merge: 1376.9 + 1373.1
rep15_L0 = L_by_content('E(p)(lab)=1376.9 {I14} (1977Da02)')
rep15_L1 = L_next('E(p)(lab)=1376.9 {I14} (1977Da02)', 1)

# REP 16: L6488.3: 2-line merge: 1386.3 + 1383.0
rep16_L0 = L_by_content('E(p)(lab)=1386.3 {I14} (1977Da02)')
rep16_L1 = L_next('E(p)(lab)=1386.3 {I14} (1977Da02)', 1)

# REP 17: L6547.8: 2-line merge: 1447.6 + 1445.0
rep17_L0 = L_by_content('E(p)(lab)=1447.6 {I15} (1977Da02)')
rep17_L1 = L_next('E(p)(lab)=1447.6 {I15} (1977Da02)', 1)

# REP 18: L6576.1: 2-line merge: 1476.8 + 1473.8
rep18_L0 = L_by_content('E(p)(lab)=1476.8 {I15} (1977Da02)')
rep18_L1 = L_next('E(p)(lab)=1476.8 {I15} (1977Da02)', 1)

# REP 19: L6626.2: 2-line merge: 1528.4 + 1524.0
rep19_L0 = L_by_content('E(p)(lab)=1528.4 {I15} (1977Da02)')
rep19_L1 = L_next('E(p)(lab)=1528.4 {I15} (1977Da02)', 1)

# REP 20: L6640.91: 2-line merge (cL+2cL): 1543.49;1543.6;1545.4 + ...
rep20_L0 = L_by_content('E(p)(lab)=1543.49 {I5} (1994Li20); 1543.6 {I2} (1983Wa27); 1545.4')
rep20_L1 = L_next('E(p)(lab)=1543.49 {I5} (1994Li20); 1543.6 {I2} (1983Wa27); 1545.4', 1)

# REP 21: L6724.2: single-line with semicolons: 1630.3;1626.5
rep21_L0 = L_by_content('E(p)(lab)=1630.3 {I16} (1977Da02); 1626.5 {I20} (1973An13)')

# REP 22: L6738.4: 2-line merge: 1644.0 + 1640.2
rep22_L0 = L_by_content('E(p)(lab)=1644.0 {I16} (1977Da02)')
rep22_L1 = L_next('E(p)(lab)=1644.0 {I16} (1977Da02)', 1)

# REP 23: L6798.4: 2-line merge: 1705.9 + 1703.2
rep23_L0 = L_by_content('E(p)(lab)=1705.9 {I16} (1977Da02)')
rep23_L1 = L_next('E(p)(lab)=1705.9 {I16} (1977Da02)', 1)

# REP 24: L6807.9: 2-line merge: 1715.6 + 1713.8
rep24_L0 = L_by_content('E(p)(lab)=1715.6 {I16} (1977Da02)')
rep24_L1 = L_next('E(p)(lab)=1715.6 {I16} (1977Da02)', 1)

# REP 25: L6829.8: 2-line merge: 1738.2 + 1734.3
rep25_L0 = L_by_content('E(p)(lab)=1738.2 {I14} (1977Da02)')
rep25_L1 = L_next('E(p)(lab)=1738.2 {I14} (1977Da02)', 1)

# REP 26: L6871.0: 2-line merge: 1780.7 + 1782.2
rep26_L0 = L_by_content('E(p)(lab)=1780.7 {I3} (1983Wa27)')
rep26_L1 = L_next('E(p)(lab)=1780.7 {I3} (1983Wa27)', 1)

# REP 27: L6887.9: 2-line merge: 1798.1 + 1799.3;1796.4
rep27_L0 = L_by_content('E(p)(lab)=1798.1 {I3} (1983Wa27)')
rep27_L1 = L_next('E(p)(lab)=1798.1 {I3} (1983Wa27)', 1)

# REP 28: L6901.7: 2-line merge: 1812.3 + 1813.4;1809.5
rep28_L0 = L_by_content('E(p)(lab)=1812.3 {I3} (1983Wa27)')
rep28_L1 = L_next('E(p)(lab)=1812.3 {I3} (1983Wa27)', 1)

# REP 29: L7059.0: 2-line merge: 1974.4 + 1974;1975.3
rep29_L0 = L_by_content('E(p)(lab)=1974.4 {I3} (1983Wa27)')
rep29_L1 = L_next('E(p)(lab)=1974.4 {I3} (1983Wa27)', 1)

# REP 30: L7078.92: single-line with semicolons: 1994.86;1997.2
rep30_L0 = L_by_content('E(p)(lab)=1994.86 {I7} (1994Li20); 1997.2 {I18} (1977Da02)')

# Batch C: |w|g splits
rep31_L0 = L_by_content('w|g=0.60 {I30} (1964Gl04); 3.6 {I5} (1977Da02)')
rep32_L0 = L_by_content('w|g=0.21 {I11} (1964Gl04); 0.9 {I3} (1977Da02)')
rep33_L0 = L_by_content('w|g=2.5 {I8} (1977Da02); 0.23 {I12} (1964Gl04)')
rep34_L0 = L_by_content('w|g=8 {I2} (1992Ka39); 8 {I2} (1977Da02)')

# Build replacement list
reps = [
    # REP 08: L6228.5
    (rep08_L0+CRLF+rep08_L1+CRLF+rep08_L2,
     ' 34CL cL '+EP+'1119 {I2} (1964Gl04), 1119.6 {I12} (1977Da02), 1118.5 {I3} (1983Wa27). Other: 1121 (1971Hy02).'),

    # REP 09: L6273.1
    (rep09_L0+CRLF+rep09_L1,
     ' 34CL cL '+EP+'1165 {I2} (1964Gl04) and 1164.5 {I13} (1977Da02).'),

    # REP 10: L6322.3
    (rep10_L0+CRLF+rep10_L1,
     ' 34CL cL '+EP+'1214 {I2} (1964Gl04) and 1215.2 {I13} (1977Da02).'),

    # REP 11: L6361.3
    (rep11_L0+CRLF+rep11_L1,
     ' 34CL cL '+EP+'1255 {I2} (1964Gl04) and 1255.4 {I13} (1977Da02).'),

    # REP 12: L6369.8
    (rep12_L0+CRLF+rep12_L1,
     ' 34CL cL '+EP+'1266 {I2} (1964Gl04), 1266.4 {I13} (1977Da02), 1264.4 {I2} (1983Wa27).'),

    # REP 13: L6441.5
    (rep13_L0+CRLF+rep13_L1,
     ' 34CL cL '+EP+'1336.8 {I15} (1973An13) and 1338.4 {I14} (1977Da02).'),

    # REP 14: L6450.5
    (rep14_L0+CRLF+rep14_L1,
     ' 34CL cL '+EP+'1346.5 {I15} (1973An13), 1348.9 {I14} (1977Da02), 1347.3 {I2} (1983Wa27).'),

    # REP 15: L6479.2
    (rep15_L0+CRLF+rep15_L1,
     ' 34CL cL '+EP+'1373.1 {I15} (1973An13) and 1376.9 {I14} (1977Da02).'),

    # REP 16: L6488.3
    (rep16_L0+CRLF+rep16_L1,
     ' 34CL cL '+EP+'1383.0 {I15} (1973An13) and 1386.3 {I14} (1977Da02).'),

    # REP 17: L6547.8
    (rep17_L0+CRLF+rep17_L1,
     ' 34CL cL '+EP+'1445.0 {I15} (1973An13) and 1447.6 {I15} (1977Da02).'),

    # REP 18: L6576.1
    (rep18_L0+CRLF+rep18_L1,
     ' 34CL cL '+EP+'1473.8 {I15} (1973An13) and 1476.8 {I15} (1977Da02).'),

    # REP 19: L6626.2
    (rep19_L0+CRLF+rep19_L1,
     ' 34CL cL '+EP+'1524.0 {I20} (1973An13) and 1528.4 {I15} (1977Da02).'),

    # REP 20: L6640.91
    (rep20_L0+CRLF+rep20_L1,
     ' 34CL cL '+EP+'1542.0 {I20} (1973An13), 1545.4 {I15} (1977Da02), 1543.6 {I2} (1983Wa27), 1543.49 {I5} (1994Li20). Other: 1542 (1975Ke11).'),

    # REP 21: L6724.2
    (rep21_L0,
     ' 34CL cL '+EP+'1626.5 {I20} (1973An13) and 1630.3 {I16} (1977Da02).'),

    # REP 22: L6738.4
    (rep22_L0+CRLF+rep22_L1,
     ' 34CL cL '+EP+'1640.2 {I20} (1973An13) and 1644.0 {I16} (1977Da02).'),

    # REP 23: L6798.4
    (rep23_L0+CRLF+rep23_L1,
     ' 34CL cL '+EP+'1703.2 {I20} (1973An13) and 1705.9 {I16} (1977Da02).'),

    # REP 24: L6807.9
    (rep24_L0+CRLF+rep24_L1,
     ' 34CL cL '+EP+'1713.8 {I20} (1973An13) and 1715.6 {I16} (1977Da02).'),

    # REP 25: L6829.8
    (rep25_L0+CRLF+rep25_L1,
     ' 34CL cL '+EP+'1734.3 {I20} (1973An13) and 1738.2 {I14} (1977Da02).'),

    # REP 26: L6871.0
    (rep26_L0+CRLF+rep26_L1,
     ' 34CL cL '+EP+'1782.2 {I16} (1977Da02) and 1780.7 {I3} (1983Wa27).'),

    # REP 27: L6887.9
    (rep27_L0+CRLF+rep27_L1,
     ' 34CL cL '+EP+'1796.4 {I20} (1973An13), 1799.3 {I16} (1977Da02), 1798.1 {I3} (1983Wa27).'),

    # REP 28: L6901.7
    (rep28_L0+CRLF+rep28_L1,
     ' 34CL cL '+EP+'1809.5 {I20} (1973An13), 1813.4 {I16} (1977Da02), 1812.3 {I3} (1983Wa27).'),

    # REP 29: L7059.0
    (rep29_L0+CRLF+rep29_L1,
     ' 34CL cL '+EP+'1975.3 {I18} (1977Da02), 1974.4 {I3} (1983Wa27), 1974 {I1} (1992Ka39).'),

    # REP 30: L7078.92
    (rep30_L0,
     ' 34CL cL '+EP+'1997.2 {I18} (1977Da02) and 1994.86 {I7} (1994Li20).'),

    # REP 31: |w|g split line 976 area
    (rep31_L0,
     ' 34CL cL '+WG+'0.60 {I30} (1964Gl04)'+CRLF+' 34CL cL '+WG+'3.6 {I5} (1977Da02)'),

    # REP 32: |w|g split line 1047 area
    (rep32_L0,
     ' 34CL cL '+WG+'0.21 {I11} (1964Gl04)'+CRLF+' 34CL cL '+WG+'0.9 {I3} (1977Da02)'),

    # REP 33: |w|g split line 1151 area (reorder year)
    (rep33_L0,
     ' 34CL cL '+WG+'0.23 {I12} (1964Gl04)'+CRLF+' 34CL cL '+WG+'2.5 {I8} (1977Da02)'),

    # REP 34: |w|g split line 1683 area (reorder year)
    (rep34_L0,
     ' 34CL cL '+WG+'8 {I2} (1977Da02)'+CRLF+' 34CL cL '+WG+'8 {I2} (1992Ka39)'),
]

# Verify all found
print('=== VERIFICATION ===')
all_ok = True
for i, (old, new) in enumerate(reps, start=8):
    found = old in content
    print(f'[{i:02d}] FOUND={found} old_len={len(old)} new_len={len(new)}')
    if not found:
        all_ok = False
        print(f'  MISSING! old starts: {repr(old[:70])}')

print()
print('ALL FOUND:', all_ok)

# Write to JSON
out = [{'old': old, 'new': new} for old, new in reps]
with open(r'd:\X\ND\ENSDF\.github\temp\replacements2.json', 'w', encoding='ascii') as f:
    json.dump(out, f, indent=2, ensure_ascii=False)
print('Written replacements2.json with', len(out), 'entries')
