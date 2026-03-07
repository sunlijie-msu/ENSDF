"""
Generate exact replacement strings for ALL E(p)(lab) reformatting edits.
Output: exact multiline replacement pairs with CRLF line endings.
This script does NOT modify any .ens file.
"""

FILEPATH = r'd:\X\ND\ENSDF\A34\Cl34\new\Cl34_33s_p_g.ens'

with open(FILEPATH, newline='') as f:
    content = f.read()

lines = content.split('\r\n')

def L(n):  # 1-based line access
    return lines[n-1]

def pad80(s):
    return s.ljust(80)

def join_lines(*lnums):
    """Join lines by CRLF (matching file format)."""
    return '\r\n'.join(L(n) for n in lnums)

def show(label, old_block, new_block):
    print(f"\n# {label}")
    print(f"OLD = {repr(old_block)}")
    print(f"NEW = {repr(new_block)}")
    # Verify old_block is actually in the file
    if old_block in content:
        print(f"# FOUND in file: YES")
    else:
        print(f"# FOUND in file: NO - CHECK THIS!")

# =========================================================
# BATCH 1: Complex multi-line merges
# =========================================================

# L 5635.7: lines 627-628 → 1 line
show('L 5635.7 (627-628)',
    join_lines(627, 628),
    pad80(' 34CL cL $E(p)(lab)=507.1 {I10} (1959Ku79), 507 {I1} (1964Gl04), 507.6 {I2} (1983Wa27).'))

# L 5852.8: lines 787-788 → 1 line
show('L 5852.8 (787-788)',
    join_lines(787, 788),
    pad80(' 34CL cL $E(p)(lab)=731 {I1} (1964Gl04) and 731.4 {I3} (1983Wa27).'))

# L 6088.91: lines 863-864 → 1 line (removes 2cL)
show('L 6088.91 (863-864)',
    join_lines(863, 864),
    pad80(' 34CL cL $E(p)(lab)=976 {I2} (1964Gl04), 974.83 {I16} (1983Ra04), 974.61 {I4} (1994Li20).'))

# L 6136.2: lines 882-883 → 1 line
show('L 6136.2 (882-883)',
    join_lines(882, 883),
    pad80(' 34CL cL $E(p)(lab)=1023 {I2} (1964Gl04) and 1023.4 {I11} (1977Da02).'))

# L 6141.7: lines 904-905 → 1 line
show('L 6141.7 (904-905)',
    join_lines(904, 905),
    pad80(' 34CL cL $E(p)(lab)=1029 {I2} (1964Gl04) and 1029.1 {I11} (1977Da02).'))

# L 6169.1: lines 926-927 → 1 line (1058 has no unc → Other)
show('L 6169.1 (926-927)',
    join_lines(926, 927),
    pad80(' 34CL cL $E(p)(lab)=1057 {I2} (1964Gl04), 1057.3 {I11} (1977Da02). Other: 1058 (1971Hy02).'))

# L 6181.1: lines 974-975 → 1 line
show('L 6181.1 (974-975)',
    join_lines(974, 975),
    pad80(' 34CL cL $E(p)(lab)=1071 {I2} (1964Gl04), 1071.1 {I11} (1977Da02), 1069.7 {I2} (1983Wa27).'))

# L 6207.1: lines 1002-1004 → 2 lines (Ep merged + extract wg from corrupted line)
# 1098 (1973An13,1971Hy02) has no unc → Other: both refs
new_ep_6207 = pad80(' 34CL cL $E(p)(lab)=1096 {I2} (1964Gl04), 1096.5 {I12} (1977Da02). Other: 1098 (1971Hy02,1973An13).')
new_wg_6207 = pad80(' 34CL cL $|w|g=0.29 {I15} (1964Gl04)')
show('L 6207.1 (1002-1004)',
    join_lines(1002, 1003, 1004),
    new_ep_6207 + '\r\n' + new_wg_6207)

# L 6228.5: lines 1044-1046 → 1 line (removes 2cL)
# 1121 (1971Hy02) has no unc → Other
show('L 6228.5 (1044-1046)',
    join_lines(1044, 1045, 1046),
    pad80(' 34CL cL $E(p)(lab)=1119 {I2} (1964Gl04), 1119.6 {I12} (1977Da02), 1118.5 {I3} (1983Wa27). Other: 1121 (1971Hy02).'))

# L 6273.1: lines 1087-1088 → 1 line
show('L 6273.1 (1087-1088)',
    join_lines(1087, 1088),
    pad80(' 34CL cL $E(p)(lab)=1165 {I2} (1964Gl04) and 1164.5 {I13} (1977Da02).'))

# L 6322.3: lines 1111-1112 → 1 line
show('L 6322.3 (1111-1112)',
    join_lines(1111, 1112),
    pad80(' 34CL cL $E(p)(lab)=1214 {I2} (1964Gl04) and 1215.2 {I13} (1977Da02).'))

# L 6361.3: lines 1138-1139 → 1 line
show('L 6361.3 (1138-1139)',
    join_lines(1138, 1139),
    pad80(' 34CL cL $E(p)(lab)=1255 {I2} (1964Gl04) and 1255.4 {I13} (1977Da02).'))

# L 6369.8: lines 1149-1150 → 1 line
show('L 6369.8 (1149-1150)',
    join_lines(1149, 1150),
    pad80(' 34CL cL $E(p)(lab)=1266 {I2} (1964Gl04), 1266.4 {I13} (1977Da02), 1264.4 {I2} (1983Wa27).'))

# L 6441.5: lines 1203-1204 → 1 line
show('L 6441.5 (1203-1204)',
    join_lines(1203, 1204),
    pad80(' 34CL cL $E(p)(lab)=1336.8 {I15} (1973An13) and 1338.4 {I14} (1977Da02).'))

# L 6450.5: lines 1215-1216 → 1 line
show('L 6450.5 (1215-1216)',
    join_lines(1215, 1216),
    pad80(' 34CL cL $E(p)(lab)=1346.5 {I15} (1973An13), 1348.9 {I14} (1977Da02), 1347.3 {I2} (1983Wa27).'))

# L 6479.2: lines 1239-1240 → 1 line
show('L 6479.2 (1239-1240)',
    join_lines(1239, 1240),
    pad80(' 34CL cL $E(p)(lab)=1373.1 {I15} (1973An13) and 1376.9 {I14} (1977Da02).'))

# L 6488.3: lines 1249-1250 → 1 line
show('L 6488.3 (1249-1250)',
    join_lines(1249, 1250),
    pad80(' 34CL cL $E(p)(lab)=1383.0 {I15} (1973An13) and 1386.3 {I14} (1977Da02).'))

# L 6547.8: lines 1274-1275 → 1 line
show('L 6547.8 (1274-1275)',
    join_lines(1274, 1275),
    pad80(' 34CL cL $E(p)(lab)=1445.0 {I15} (1973An13) and 1447.6 {I15} (1977Da02).'))

# L 6576.1: lines 1288-1289 → 1 line
show('L 6576.1 (1288-1289)',
    join_lines(1288, 1289),
    pad80(' 34CL cL $E(p)(lab)=1473.8 {I15} (1973An13) and 1476.8 {I15} (1977Da02).'))

# L 6626.2: lines 1310-1311 → 1 line
show('L 6626.2 (1310-1311)',
    join_lines(1310, 1311),
    pad80(' 34CL cL $E(p)(lab)=1524.0 {I20} (1973An13) and 1528.4 {I15} (1977Da02).'))

# L 6640.91: lines 1331-1332 → 1 line (removes 2cL, 1542 (1975Ke11) → Other)
show('L 6640.91 (1331-1332)',
    join_lines(1331, 1332),
    pad80(' 34CL cL $E(p)(lab)=1542.0 {I20} (1973An13), 1545.4 {I15} (1977Da02), 1543.6 {I2} (1983Wa27), 1543.49 {I5} (1994Li20). Other: 1542 (1975Ke11).'))

# L 6724.2: line 1408 (single semicoloned line → reformat to "and")
show('L 6724.2 (1408)',
    L(1408),
    pad80(' 34CL cL $E(p)(lab)=1626.5 {I20} (1973An13) and 1630.3 {I16} (1977Da02).'))

# L 6738.4: lines 1425-1426 → 1 line
show('L 6738.4 (1425-1426)',
    join_lines(1425, 1426),
    pad80(' 34CL cL $E(p)(lab)=1640.2 {I20} (1973An13) and 1644.0 {I16} (1977Da02).'))

# L 6798.4: lines 1448-1449 → 1 line
show('L 6798.4 (1448-1449)',
    join_lines(1448, 1449),
    pad80(' 34CL cL $E(p)(lab)=1703.2 {I20} (1973An13) and 1705.9 {I16} (1977Da02).'))

# L 6807.9: lines 1465-1466 → 1 line
show('L 6807.9 (1465-1466)',
    join_lines(1465, 1466),
    pad80(' 34CL cL $E(p)(lab)=1713.8 {I20} (1973An13) and 1715.6 {I16} (1977Da02).'))

# L 6829.8: lines 1474-1475 → 1 line
show('L 6829.8 (1474-1475)',
    join_lines(1474, 1475),
    pad80(' 34CL cL $E(p)(lab)=1734.3 {I20} (1973An13) and 1738.2 {I14} (1977Da02).'))

# L 6871.0: lines 1531-1532 → 1 line
show('L 6871.0 (1531-1532)',
    join_lines(1531, 1532),
    pad80(' 34CL cL $E(p)(lab)=1782.2 {I16} (1977Da02) and 1780.7 {I3} (1983Wa27).'))

# L 6887.9: lines 1563-1564 → 1 line (1564 has semicolons: 1799.3 (1977), 1796.4 (1973))
show('L 6887.9 (1563-1564)',
    join_lines(1563, 1564),
    pad80(' 34CL cL $E(p)(lab)=1796.4 {I20} (1973An13), 1799.3 {I16} (1977Da02), 1798.1 {I3} (1983Wa27).'))

# L 6901.7: lines 1584-1585 → 1 line (1585 has semicolons: 1813.4 (1977), 1809.5 (1973))
show('L 6901.7 (1584-1585)',
    join_lines(1584, 1585),
    pad80(' 34CL cL $E(p)(lab)=1809.5 {I20} (1973An13), 1813.4 {I16} (1977Da02), 1812.3 {I3} (1983Wa27).'))

# L 7059.0: lines 1681-1682 → 1 line (1682 has semicolons: 1974 (1992Ka39), 1975.3 (1977Da02))
show('L 7059.0 (1681-1682)',
    join_lines(1681, 1682),
    pad80(' 34CL cL $E(p)(lab)=1975.3 {I18} (1977Da02), 1974.4 {I3} (1983Wa27), 1974 {I1} (1992Ka39).'))

# L 7078.92: line 1712 (single semicoloned line → reformat to "and")
show('L 7078.92 (1712)',
    L(1712),
    pad80(' 34CL cL $E(p)(lab)=1997.2 {I18} (1977Da02) and 1994.86 {I7} (1994Li20).'))

print("\n\n# =========================================================")
print("# BATCH 2: Split multi-value |w|g lines")
print("# =========================================================")

# Line 976: split |w|g
show('|w|g split line 976',
    L(976),
    pad80(' 34CL cL $|w|g=0.60 {I30} (1964Gl04)') + '\r\n' + pad80(' 34CL cL $|w|g=3.6 {I5} (1977Da02)'))

# Line 1047: split |w|g
show('|w|g split line 1047',
    L(1047),
    pad80(' 34CL cL $|w|g=0.21 {I11} (1964Gl04)') + '\r\n' + pad80(' 34CL cL $|w|g=0.9 {I3} (1977Da02)'))

# Line 1151: split |w|g (year order: 1964, 1977)
show('|w|g split line 1151',
    L(1151),
    pad80(' 34CL cL $|w|g=0.23 {I12} (1964Gl04)') + '\r\n' + pad80(' 34CL cL $|w|g=2.5 {I8} (1977Da02)'))

# Line 1683: split |w|g (year order: 1977, 1992)
show('|w|g split line 1683',
    L(1683),
    pad80(' 34CL cL $|w|g=8 {I2} (1977Da02)') + '\r\n' + pad80(' 34CL cL $|w|g=8 {I2} (1992Ka39)'))
