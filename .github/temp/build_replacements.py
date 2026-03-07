"""Build exact replacement pairs for Ep comment reformatting."""
import json

content = open(r'd:\X\ND\ENSDF\A34\Cl34\new\Cl34_33s_p_g.ens', 'rb').read().decode('ascii')
lines = content.split('\r\n')
def L(n): return lines[n-1]
CRLF = '\r\n'

EP = '$E(p)(lab)='
WG = '$|w|g='

reps = [
    # [00] L5635.7: merge 627-628, year order 1959,1964,1983
    (L(627)+CRLF+L(628),
     ' 34CL cL ' + EP + '507.1 {I10} (1959Ku79), 507 {I1} (1964Gl04), 507.6 {I2} (1983Wa27).'),

    # [01] L5852.8: merge 787-788, year order 1964,1983
    (L(787)+CRLF+L(788),
     ' 34CL cL ' + EP + '731 {I1} (1964Gl04) and 731.4 {I3} (1983Wa27).'),

    # [02] L6088.91: merge 863-864 (cL+2cL), year order 1964,1983,1994
    (L(863)+CRLF+L(864),
     ' 34CL cL ' + EP + '976 {I2} (1964Gl04), 974.83 {I16} (1983Ra04), 974.61 {I4} (1994Li20).'),

    # [03] L6136.2: merge 882-883, year order 1964,1977
    (L(882)+CRLF+L(883),
     ' 34CL cL ' + EP + '1023 {I2} (1964Gl04) and 1023.4 {I11} (1977Da02).'),

    # [04] L6141.7: merge 904-905, year order 1964,1977
    (L(904)+CRLF+L(905),
     ' 34CL cL ' + EP + '1029 {I2} (1964Gl04) and 1029.1 {I11} (1977Da02).'),

    # [05] L6169.1: merge 926-927, year order 1964,1977, Other 1971
    (L(926)+CRLF+L(927),
     ' 34CL cL ' + EP + '1057 {I2} (1964Gl04), 1057.3 {I11} (1977Da02). Other: 1058 (1971Hy02).'),

    # [06] L6181.1: merge 974-975, year order 1964,1977,1983
    (L(974)+CRLF+L(975),
     ' 34CL cL ' + EP + '1071 {I2} (1964Gl04), 1071.1 {I11} (1977Da02), 1069.7 {I2} (1983Wa27).'),

    # [07] L6207.1: merge 1002-1004 (3 lines), year order 1964,1977, Other 1971+1973, keep wg line
    (L(1002)+CRLF+L(1003)+CRLF+L(1004),
     ' 34CL cL ' + EP + '1096 {I2} (1964Gl04), 1096.5 {I12} (1977Da02). Other: 1098 (1971Hy02,1973An13).'
     + CRLF +
     ' 34CL cL ' + WG + '0.29 {I15} (1964Gl04)'),

    # [08] L6228.5: merge 1044-1046 (3 lines), year order 1964,1977,1983, Other 1971
    (L(1044)+CRLF+L(1045)+CRLF+L(1046),
     ' 34CL cL ' + EP + '1119 {I2} (1964Gl04), 1119.6 {I12} (1977Da02), 1118.5 {I3} (1983Wa27). Other: 1121 (1971Hy02).'),

    # [09] L6273.1: merge 1087-1088, year order 1964,1977
    (L(1087)+CRLF+L(1088),
     ' 34CL cL ' + EP + '1165 {I2} (1964Gl04) and 1164.5 {I13} (1977Da02).'),

    # [10] L6322.3: merge 1111-1112, year order 1964,1977
    (L(1111)+CRLF+L(1112),
     ' 34CL cL ' + EP + '1214 {I2} (1964Gl04) and 1215.2 {I13} (1977Da02).'),

    # [11] L6361.3: merge 1138-1139, year order 1964,1977
    (L(1138)+CRLF+L(1139),
     ' 34CL cL ' + EP + '1255 {I2} (1964Gl04) and 1255.4 {I13} (1977Da02).'),

    # [12] L6369.8: merge 1149-1150, year order 1964,1977,1983
    (L(1149)+CRLF+L(1150),
     ' 34CL cL ' + EP + '1266 {I2} (1964Gl04), 1266.4 {I13} (1977Da02), 1264.4 {I2} (1983Wa27).'),

    # [13] L6441.5: merge 1203-1204, year order 1973,1977
    (L(1203)+CRLF+L(1204),
     ' 34CL cL ' + EP + '1336.8 {I15} (1973An13) and 1338.4 {I14} (1977Da02).'),

    # [14] L6450.5: merge 1215-1216, year order 1973,1977,1983
    (L(1215)+CRLF+L(1216),
     ' 34CL cL ' + EP + '1346.5 {I15} (1973An13), 1348.9 {I14} (1977Da02), 1347.3 {I2} (1983Wa27).'),

    # [15] L6479.2: merge 1239-1240, year order 1973,1977
    (L(1239)+CRLF+L(1240),
     ' 34CL cL ' + EP + '1373.1 {I15} (1973An13) and 1376.9 {I14} (1977Da02).'),

    # [16] L6488.3: merge 1249-1250, year order 1973,1977
    (L(1249)+CRLF+L(1250),
     ' 34CL cL ' + EP + '1383.0 {I15} (1973An13) and 1386.3 {I14} (1977Da02).'),

    # [17] L6547.8: merge 1274-1275, year order 1973,1977
    (L(1274)+CRLF+L(1275),
     ' 34CL cL ' + EP + '1445.0 {I15} (1973An13) and 1447.6 {I15} (1977Da02).'),

    # [18] L6576.1: merge 1288-1289, year order 1973,1977
    (L(1288)+CRLF+L(1289),
     ' 34CL cL ' + EP + '1473.8 {I15} (1973An13) and 1476.8 {I15} (1977Da02).'),

    # [19] L6626.2: merge 1310-1311, year order 1973,1977
    (L(1310)+CRLF+L(1311),
     ' 34CL cL ' + EP + '1524.0 {I20} (1973An13) and 1528.4 {I15} (1977Da02).'),

    # [20] L6640.91: merge 1331-1332 (cL+2cL), year order 1973,1977,1983,1994, Other 1975
    (L(1331)+CRLF+L(1332),
     ' 34CL cL ' + EP + '1542.0 {I20} (1973An13), 1545.4 {I15} (1977Da02), 1543.6 {I2} (1983Wa27), 1543.49 {I5} (1994Li20). Other: 1542 (1975Ke11).'),

    # [21] L6724.2: single line 1408 with semicolons
    (L(1408),
     ' 34CL cL ' + EP + '1626.5 {I20} (1973An13) and 1630.3 {I16} (1977Da02).'),

    # [22] L6738.4: merge 1425-1426, year order 1973,1977
    (L(1425)+CRLF+L(1426),
     ' 34CL cL ' + EP + '1640.2 {I20} (1973An13) and 1644.0 {I16} (1977Da02).'),

    # [23] L6798.4: merge 1448-1449, year order 1973,1977
    (L(1448)+CRLF+L(1449),
     ' 34CL cL ' + EP + '1703.2 {I20} (1973An13) and 1705.9 {I16} (1977Da02).'),

    # [24] L6807.9: merge 1465-1466, year order 1973,1977
    (L(1465)+CRLF+L(1466),
     ' 34CL cL ' + EP + '1713.8 {I20} (1973An13) and 1715.6 {I16} (1977Da02).'),

    # [25] L6829.8: merge 1474-1475, year order 1973,1977
    (L(1474)+CRLF+L(1475),
     ' 34CL cL ' + EP + '1734.3 {I20} (1973An13) and 1738.2 {I14} (1977Da02).'),

    # [26] L6871.0: merge 1531-1532, year order 1977,1983
    (L(1531)+CRLF+L(1532),
     ' 34CL cL ' + EP + '1782.2 {I16} (1977Da02) and 1780.7 {I3} (1983Wa27).'),

    # [27] L6887.9: merge 1563-1564 (1564 has semicolons), year order 1973,1977,1983
    (L(1563)+CRLF+L(1564),
     ' 34CL cL ' + EP + '1796.4 {I20} (1973An13), 1799.3 {I16} (1977Da02), 1798.1 {I3} (1983Wa27).'),

    # [28] L6901.7: merge 1584-1585 (1585 has semicolons), year order 1973,1977,1983
    (L(1584)+CRLF+L(1585),
     ' 34CL cL ' + EP + '1809.5 {I20} (1973An13), 1813.4 {I16} (1977Da02), 1812.3 {I3} (1983Wa27).'),

    # [29] L7059.0: merge 1681-1682 (1682 has semicolons), year order 1977,1983,1992
    (L(1681)+CRLF+L(1682),
     ' 34CL cL ' + EP + '1975.3 {I18} (1977Da02), 1974.4 {I3} (1983Wa27), 1974 {I1} (1992Ka39).'),

    # [30] L7078.92: single line 1712 with semicolons, year order 1977,1994
    (L(1712),
     ' 34CL cL ' + EP + '1997.2 {I18} (1977Da02) and 1994.86 {I7} (1994Li20).'),
]

# Batch C: |w|g splits
wg_reps = [
    # line 976
    (L(976), ' 34CL cL ' + WG + '0.60 {I30} (1964Gl04)' + CRLF + ' 34CL cL ' + WG + '3.6 {I5} (1977Da02)'),
    # line 1047
    (L(1047), ' 34CL cL ' + WG + '0.21 {I11} (1964Gl04)' + CRLF + ' 34CL cL ' + WG + '0.9 {I3} (1977Da02)'),
    # line 1151 (reorder year: 1964 before 1977)
    (L(1151), ' 34CL cL ' + WG + '0.23 {I12} (1964Gl04)' + CRLF + ' 34CL cL ' + WG + '2.5 {I8} (1977Da02)'),
    # line 1683 (reorder year: 1977 before 1992)
    (L(1683), ' 34CL cL ' + WG + '8 {I2} (1977Da02)' + CRLF + ' 34CL cL ' + WG + '8 {I2} (1992Ka39)'),
]

all_reps = reps + wg_reps

# Verify all old strings found
print('=== VERIFICATION ===')
all_ok = True
for i, (old, new) in enumerate(all_reps):
    found = old in content
    print(f'[{i:02d}] FOUND={found} old_len={len(old)} new_len={len(new)}')
    if not found:
        all_ok = False
        print(f'  MISSING! Starts with: {repr(old[:60])}')

print()
print('ALL FOUND:', all_ok)

# Write to JSON
out = [{'old': old, 'new': new} for old, new in all_reps]
with open(r'd:\X\ND\ENSDF\.github\temp\replacements.json', 'w', encoding='ascii') as f:
    json.dump(out, f, indent=2, ensure_ascii=False)
print('Written replacements.json with', len(out), 'entries')
