import re, random

random.seed(42)

target_lines = [914, 953, 975, 991, 1004, 1047, 1115, 1143, 1195, 1222, 1246, 1284, 1334, 1371, 1394, 1424, 1459, 1497, 1552, 1582, 1602, 1632, 1637, 1662, 1695, 1726, 1751, 1774, 1799, 1830, 1851, 1880, 1910, 1946, 1979, 2007, 2027, 2055, 2075, 2116, 2148, 2166, 2183, 2204, 2240, 2247, 2272]
old_vals = [2.5, 0.4, 0.3, 0.1, 0.5, 0.3, 1.1, 2.9, 1.1, 0.5, 1.4, 2.4, 3.1, 1.2, 1.4, 0.9, 1.6, 1.3, 8.7, 0.5, 1.3, 0.1, 1.0, 0.7, 1.0, 1.3, 2.3, 2.6, 3.4, 0.9, 3.0, 1.3, 2.5, 3.6, 1.1, 1.5, 2.1, 0.7, 6.0, 4.7, 1.9, 1.9, 1.7, 2.4, 3.0, 1.7, 4.6]
factor = 2.21052631579
n = len(target_lines)
sample_size = max(3, int(0.05 * n) + 1)
sample = random.sample(range(n), sample_size)

with open(r'd:\X\ND\ENSDF\A35\Cl35\new\Cl35_34s_p_g.ens', 'r') as f:
    lines = f.readlines()

print('5%% Random Spot Check (%d of %d samples)' % (sample_size, n))
print()
all_pass = True
for idx in sample:
    ln = target_lines[idx]
    old_val = old_vals[idx]
    expected_new = round(old_val / factor, 2)
    expected_str = '%.2f' % expected_new

    line_content = lines[ln-1].rstrip('\r\n')
    m = re.search(r'\|w\|g[=(]\(?([0-9.]+)\)? eV \(1973Fa07\)', line_content)
    actual_str = m.group(1) if m else 'NOT FOUND'

    status = 'PASS' if actual_str == expected_str else 'FAIL'
    if status != 'PASS':
        all_pass = False
    computed = old_val / factor
    print('[%s] Line %d: old=%s / factor = %.6f -> expected=%s, actual=%s' % (
        status, ln, old_val, computed, expected_str, actual_str))
    print('  Line: %s' % line_content.strip()[:65])
    print()

if all_pass:
    print('All %d spot checks: PASS' % sample_size)
else:
    print('FAILURES DETECTED!')
