import sys
DOLLAR = chr(36)

da02 = [
    ('1023.4','11','0.6','2'), ('1029.1','11','0.9','5'),
    ('1057.3','11','1.5','7'), ('1071.1','11','3.6','5'),
    ('1096.5','12','2.2','10'), ('1109.0','12','0.10','6'),
    ('1119.6','12','0.9','3'), ('1157.7','13','0.2','1'),
    ('1164.5','13','2.7','10'), ('1215.2','13','1.9','7'),
    ('1255.4','13','0.4','2'), ('1266.4','13','2.5','8'),
    ('1277.1','14','0.3','1'), ('1295.0','14','0.2','1'),
    ('1338.4','14','0.2','1'), ('1348.9','14','0.9','3'),
    ('1376.9','14','0.2','1'), ('1386.3','14','0.8','3'),
    ('1426.7','15','0.2','1'), ('1447.6','15','1.6','5'),
    ('1476.8','15','0.6','2'), ('1484.5','15','0.4','2'),
    ('1528.4','15','0.2','1'), ('1545.4','15','3.8','6'),
    ('1599.3','16','0.4','2'), ('1607.3','16','0.3','2'),
    ('1625.2','16','0.3','1'), ('1630.3','16','0.9','4'),
    ('1644.0','16','0.5','2'), ('1698.0','16','0.6','3'),
    ('1705.9','16','4.0','25'), ('1715.6','16','0.10','7'),
    ('1738.2','14','0.6','3'), ('1751.5','14','1.8','10'),
    ('1762.1','14','2.3','7'), ('1782.2','16','1.6','8'),
    ('1799.3','16','2.0','6'), ('1813.4','16','2.8','9'),
    ('1829.0','17','11','2'), ('1843.0','17','0.8','5'),
    ('1890.3','17','0.5','2'), ('1900','0','1.7','10'),
    ('1966.7','18','0.3','2'), ('1975.3','18','8','2'),
    ('1997.2','18','4.4','20'),
]

filepath = r'A34\Cl34\new\Cl34_33s_p_g.ens'
with open(filepath, newline='') as f:
    lines = f.readlines()
content = ''.join(lines)

# Special: Ep=1545.4 EP is split across cL (line 1371) and 2cL (line 1372)
L1371 = lines[1370].rstrip('\r\n')
L1372 = lines[1371].rstrip('\r\n')
ep1545_split = ('1545.4' in L1371) and ('{I15} (1977Da02)' in L1372)
print('=== Ep=1545.4 split-line check ===')
print('  L1371 ends: |%s|' % L1371[-12:])
print('  L1372 start: |%s|' % L1372[:40])
print('  1545.4 in L1371: %s' % ('1545.4' in L1371))
print('  {I15} (1977Da02) in L1372: %s' % ('{I15} (1977Da02)' in L1372))
print('  => ep1545_split = %s' % ep1545_split)
print()

pass_count = 0
fail_count = 0
fails = []

for ep, dep, wg, dwg in da02:
    # EP patterns
    if dep == '0':
        ep_strict = DOLLAR + 'E(p)(lab)=' + ep + ' (1977Da02)'
        ep_flex   = ep + ' (1977Da02)'
    else:
        ep_strict = DOLLAR + 'E(p)(lab)=' + ep + ' {I' + dep + '} (1977Da02)'
        ep_flex   = ep + ' {I' + dep + '} (1977Da02)'
    # WG patterns
    wg_strict = DOLLAR + '|w|g=' + wg + ' {I' + dwg + '} (1977Da02)'
    wg_flex   = wg + ' {I' + dwg + '} (1977Da02)'

    # Determine OK/FAIL
    if ep == '1545.4':
        ep_ok = ep1545_split
        ep_how = 'split-line'
    elif ep_strict in content:
        ep_ok = True
        ep_how = 'strict'
    elif ep_flex in content:
        ep_ok = True
        ep_how = 'flex'
    else:
        ep_ok = False
        ep_how = 'MISS'

    if wg_strict in content:
        wg_ok = True
        wg_how = 'strict'
    elif wg_flex in content:
        wg_ok = True
        wg_how = 'flex'
    else:
        wg_ok = False
        wg_how = 'MISS'

    if ep_ok and wg_ok:
        pass_count += 1
        print('PASS  Ep=%-8s EP=%-10s WG=%-10s' % (ep, ep_how, wg_how))
    else:
        fail_count += 1
        fails.append((ep, ep_ok, wg_ok, ep_how, wg_how))
        print('FAIL  Ep=%-8s EP=%-10s WG=%-10s' % (ep, ep_how if ep_ok else 'MISS', wg_how if wg_ok else 'MISS'))
        if not ep_ok:
            print('     EP strict: %s' % ep_strict)
            print('     EP flex:   %s' % ep_flex)
        if not wg_ok:
            print('     WG strict: %s' % wg_strict)
            print('     WG flex:   %s' % wg_flex)

print()
print('='*50)
print('FINAL: %d/45 PASS, %d FAIL' % (pass_count, fail_count))
if fail_count == 0:
    print('ALL 45 Da02 ENTRIES VERIFIED CORRECT.')
