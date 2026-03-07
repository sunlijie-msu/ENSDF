"""
Generate exact old/new replacement strings for E(p)(lab) reformatting
in Cl34_33s_p_g.ens.
RULES:
 - One cL line per level for all Ep values
 - Values with uncertainty: main combined line, sorted ascending year
 - Values WITHOUT uncertainty: appended as 'Other: ...'
 - Two values: use 'and'; three+: use commas
 - Each |w|g on separate cL line (|w|g splits handled separately)
 - End with period
OUTPUT: exact (old_block, new_block) pairs as Python repr strings
"""

import re

FILEPATH = r'd:\X\ND\ENSDF\A34\Cl34\new\Cl34_33s_p_g.ens'

with open(FILEPATH, newline='') as f:
    content = f.read()

# File uses CRLF
lines = content.split('\r\n')

def pad80(s):
    """Pad string to 80 chars."""
    return s.ljust(80)

def show_block(label, linerange, old_lines, new_lines):
    old_block = '\r\n'.join(old_lines)
    new_block = '\r\n'.join(new_lines)
    print(f'\n=== {label} (lines {linerange}) ===')
    print('OLD:')
    for l in old_lines:
        print(f'  |{l}|')
    print('NEW:')
    for l in new_lines:
        print(f'  |{l}|')
    print(f'OLD repr: {repr(old_block)}')
    print(f'NEW repr: {repr(new_block)}')

# Helper to get exact line content
def L(n):  # 1-based
    return lines[n-1]

# ============================================================
# COMPLEX MERGES: levels with multiple Ep lines to combine
# ============================================================

# Level 5635.7: lines 627-628
# Values: 507.6 {I2} (1983Wa27), 507 {I1} (1964Gl04), 507.1 {I10} (1959Ku79)
# Sort by year: 1959, 1964, 1983
new627 = pad80(' 34CL cL $E(p)(lab)=507.1 {I10} (1959Ku79), 507 {I1} (1964Gl04), 507.6 {I2} (1983Wa27).')
show_block('L 5635.7', '627-628', [L(627), L(628)], [new627])

# Level 5852.8: lines 787-788
# Values: 731.4 {I3} (1983Wa27), 731 {I1} (1964Gl04)
# Sort by year: 1964, 1983
new787 = pad80(' 34CL cL $E(p)(lab)=731 {I1} (1964Gl04) and 731.4 {I3} (1983Wa27).')
show_block('L 5852.8', '787-788', [L(787), L(788)], [new787])

# Level 6088.91: lines 863-864 (already partially combined with 2cL)
# Values: 974.61 {I4} (1994Li20), 974.83 {I16} (1983Ra04), 976 {I2} (1964Gl04)
# Sort by year: 1964, 1983, 1994
new863 = pad80(' 34CL cL $E(p)(lab)=976 {I2} (1964Gl04), 974.83 {I16} (1983Ra04), 974.61 {I4} (1994Li20).')
show_block('L 6088.91', '863-864', [L(863), L(864)], [new863])

# Level 6136.2: lines 882-883
# Values: 1023.4 {I11} (1977Da02), 1023 {I2} (1964Gl04)
# Sort by year: 1964, 1977
new882 = pad80(' 34CL cL $E(p)(lab)=1023 {I2} (1964Gl04) and 1023.4 {I11} (1977Da02).')
show_block('L 6136.2', '882-883', [L(882), L(883)], [new882])

# Level 6141.7: lines 904-905
# Values: 1029.1 {I11} (1977Da02), 1029 {I2} (1964Gl04)
# Need to check line 905
show_block('L 6141.7 check', '904-905', [L(904), L(905)], [])

# Level 6169.1: lines 926-927
# Values: 1057.3 {I11} (1977Da02) [has unc], 1058 (1971Hy02) [NO unc -> Other], 1057 {I2} (1964Gl04) [has unc]
# With unc sorted by year: 1964, 1977. Other: 1971
new926 = pad80(' 34CL cL $E(p)(lab)=1057 {I2} (1964Gl04), 1057.3 {I11} (1977Da02). Other: 1058 (1971Hy02).')
show_block('L 6169.1', '926-927', [L(926), L(927)], [new926])

# Level 6181.1: lines 974-975
# Values: 1069.7 {I2} (1983Wa27), 1071.1 {I11} (1977Da02), 1071 {I2} (1964Gl04)
# Sort by year: 1964, 1977, 1983
new974 = pad80(' 34CL cL $E(p)(lab)=1071 {I2} (1964Gl04), 1071.1 {I11} (1977Da02), 1069.7 {I2} (1983Wa27).')
show_block('L 6181.1', '974-975', [L(974), L(975)], [new974])

# Level 6207.1: lines 1002-1004 (special: corrupted line 1004)
# Values: 1096.5 {I12} (1977Da02) [has unc], 1098 (1973An13,1971Hy02) [NO unc -> Other], 1096 {I2} (1964Gl04) [has unc]
# With unc sorted by year: 1964, 1977. Other: 1971Hy02, 1973An13
new1002 = pad80(' 34CL cL $E(p)(lab)=1096 {I2} (1964Gl04), 1096.5 {I12} (1977Da02). Other: 1098 (1971Hy02,1973An13).')
new1004 = pad80(' 34CL cL $|w|g=0.29 {I15} (1964Gl04)')
show_block('L 6207.1', '1002-1004', [L(1002), L(1003), L(1004)], [new1002, new1004])

# Level 6228.5: lines 1044-1046 (has 2cL continuation)
# Values: 1118.5 {I3} (1983Wa27), 1119.6 {I12} (1977Da02), 1121 (1971Hy02) [NO unc -> Other], 1119 {I2} (1964Gl04)
# With unc sorted by year: 1964, 1977, 1983. Other: 1971Hy02
new1044 = pad80(' 34CL cL $E(p)(lab)=1119 {I2} (1964Gl04), 1119.6 {I12} (1977Da02), 1118.5 {I3} (1983Wa27). Other: 1121 (1971Hy02).')
show_block('L 6228.5', '1044-1046', [L(1044), L(1045), L(1046)], [new1044])

# Level 6273.1: lines 1087-1088 (need to check line 1088)
show_block('L 6273.1 check', '1087-1088', [L(1087), L(1088)], [])

# Level 6322.3: lines 1111-1112
# Values: 1215.2 {I13} (1977Da02), 1214 {I2} (1964Gl04)
# Sort by year: 1964, 1977
new1111 = pad80(' 34CL cL $E(p)(lab)=1214 {I2} (1964Gl04) and 1215.2 {I13} (1977Da02).')
show_block('L 6322.3', '1111-1112', [L(1111), L(1112)], [new1111])

# Level 6361.3: lines 1138-1139
# Values: 1255.4 {I13} (1977Da02), 1255 {I2} (1964Gl04)
# Sort by year: 1964, 1977
new1138 = pad80(' 34CL cL $E(p)(lab)=1255 {I2} (1964Gl04) and 1255.4 {I13} (1977Da02).')
show_block('L 6361.3', '1138-1139', [L(1138), L(1139)], [new1138])

# Level 6369.8: lines 1149-1150
# Values: 1264.4 {I2} (1983Wa27), 1266.4 {I13} (1977Da02), 1266 {I2} (1964Gl04)
# Sort by year: 1964, 1977, 1983
new1149 = pad80(' 34CL cL $E(p)(lab)=1266 {I2} (1964Gl04), 1266.4 {I13} (1977Da02), 1264.4 {I2} (1983Wa27).')
show_block('L 6369.8', '1149-1150', [L(1149), L(1150)], [new1149])

# Level 6441.5: lines 1203-1204
# Values: 1338.4 {I14} (1977Da02), 1336.8 {I15} (1973An13)
# Sort by year: 1973, 1977
new1203 = pad80(' 34CL cL $E(p)(lab)=1336.8 {I15} (1973An13) and 1338.4 {I14} (1977Da02).')
show_block('L 6441.5', '1203-1204', [L(1203), L(1204)], [new1203])

# Level 6450.5: lines 1215-1216
# Values: 1347.3 {I2} (1983Wa27), 1348.9 {I14} (1977Da02), 1346.5 {I15} (1973An13)
# Sort by year: 1973, 1977, 1983
new1215 = pad80(' 34CL cL $E(p)(lab)=1346.5 {I15} (1973An13), 1348.9 {I14} (1977Da02), 1347.3 {I2} (1983Wa27).')
show_block('L 6450.5', '1215-1216', [L(1215), L(1216)], [new1215])

# Level 6479.2: lines 1239-1240
# Values: 1376.9 {I14} (1977Da02), 1373.1 {I15} (1973An13)
# Sort by year: 1973, 1977
new1239 = pad80(' 34CL cL $E(p)(lab)=1373.1 {I15} (1973An13) and 1376.9 {I14} (1977Da02).')
show_block('L 6479.2', '1239-1240', [L(1239), L(1240)], [new1239])

# Level 6488.3: lines 1249-1250
# Values: 1386.3 {I14} (1977Da02), 1383.0 {I15} (1973An13)
# Sort by year: 1973, 1977
new1249 = pad80(' 34CL cL $E(p)(lab)=1383.0 {I15} (1973An13) and 1386.3 {I14} (1977Da02).')
show_block('L 6488.3', '1249-1250', [L(1249), L(1250)], [new1249])

# Level 6547.8: lines 1274-1275
# Values: 1447.6 {I15} (1977Da02), 1445.0 {I15} (1973An13)
# Sort by year: 1973, 1977
new1274 = pad80(' 34CL cL $E(p)(lab)=1445.0 {I15} (1973An13) and 1447.6 {I15} (1977Da02).')
show_block('L 6547.8', '1274-1275', [L(1274), L(1275)], [new1274])

# Level 6576.1: lines 1288-1289
# Values: 1476.8 {I15} (1977Da02), 1473.8 {I15} (1973An13)
# Sort by year: 1973, 1977
new1288 = pad80(' 34CL cL $E(p)(lab)=1473.8 {I15} (1973An13) and 1476.8 {I15} (1977Da02).')
show_block('L 6576.1', '1288-1289', [L(1288), L(1289)], [new1288])

# Level 6626.2: need to check line 1310-1311
show_block('L 6626.2 check', '1310-1311', [L(1310), L(1311)], [])

# Level 6640.91: lines 1331-1332 (already partial with 2cL)
# Values: 1543.49 {I5} (1994Li20), 1543.6 {I2} (1983Wa27), 1545.4 {I15} (1977Da02), 1542 (1975Ke11) [NO unc -> Other], 1542.0 {I20} (1973An13)
# With unc sorted by year: 1973, 1977, 1983, 1994. Other: 1975Ke11
new1331 = pad80(' 34CL cL $E(p)(lab)=1542.0 {I20} (1973An13), 1545.4 {I15} (1977Da02), 1543.6 {I2} (1983Wa27), 1543.49 {I5} (1994Li20). Other: 1542 (1975Ke11).')
show_block('L 6640.91', '1331-1332', [L(1331), L(1332)], [new1331])

# Level 6724.2: line 1408 (two values on one line separated by semicolon)
# Values: 1630.3 {I16} (1977Da02), 1626.5 {I20} (1973An13)
# Sort by year: 1973, 1977
new1408 = pad80(' 34CL cL $E(p)(lab)=1626.5 {I20} (1973An13) and 1630.3 {I16} (1977Da02).')
show_block('L 6724.2', '1408', [L(1408)], [new1408])

# Level 6738.4: lines 1425-1426 (need to check exact lines)
show_block('L 6738.4 check', '1425-1426', [L(1425), L(1426)], [])

# Level 6798.4: check
show_block('L 6798.4 check', '1449-1450', [L(1449), L(1450)], [])

# Level 6807.9: check
show_block('L 6807.9 check', '1466-1467', [L(1466), L(1467)], [])

# Level 6829.8: check
show_block('L 6829.8 check', '1479-1480', [L(1479), L(1480)], [])

# Level 6871.0: user's example
show_block('L 6871.0 check', '1535-1536', [L(1535), L(1536)], [])

# Level 6887.9: has semicoloned line 
show_block('L 6887.9 check', '1548-1549', [L(1548), L(1549)], [])

# Level 6901.7: has semicoloned line
show_block('L 6901.7 check', '1565-1566', [L(1565), L(1566)], [])

# Level 7059.0: has semicoloned Ep
show_block('L 7059.0 check', '1689-1690', [L(1689), L(1690)], [])

# Level 7078.92: has semicoloned Ep
show_block('L 7078.92 check', '1702-1703', [L(1702), L(1703)], [])
