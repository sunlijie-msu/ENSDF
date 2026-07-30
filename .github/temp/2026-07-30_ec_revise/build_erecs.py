"""Build and validate E-records and L-records for S34 EC decay."""
import subprocess, sys

def ruler(line):
    r = subprocess.run([sys.executable, '.github/scripts/ensdf_1line_ruler.py', '--line', line],
                       capture_output=True, text=True)
    return r.returncode

def build_L(E_str, DE_str, J_str):
    line = (
        ' 34S   L ' +
        E_str.ljust(10)[:10] +
        DE_str.ljust(2)[:2] +
        ' ' + J_str.ljust(17)[:17] +
        ' ' * 41
    )
    return line

def build_E(IB_str, DIB_str, IE_str, DIE_str, LOGFT_str, DFT_str, TI_str, DTI_str):
    line = (
        ' 34S   E ' +
        ' ' * 10 +  # E endpoint
        '  ' +      # DE
        ' ' +       # col 22
        IB_str.ljust(7)[:7] +
        DIB_str.ljust(2)[:2] +
        IE_str.ljust(8)[:8] +
        DIE_str.ljust(2)[:2] +
        ' ' +       # col 42
        LOGFT_str.ljust(7)[:7] +
        DFT_str.ljust(6)[:6] +
        ' ' * 9 +   # cols 56-64
        TI_str.ljust(10)[:10] +
        DTI_str.ljust(2)[:2] +
        ' ' +       # C
        '  ' +      # UN
        ' '         # Q
    )
    return line

# Test existing E record
print('=== Existing E record ===')
existing = ' 34S   E              99.9208 8 0.0792  8 3.4844812                  100        '
rc = ruler(existing)
print('Existing E: len=' + str(len(existing)) + ' ' + ('OK' if rc == 0 else 'FAIL'))

# Build new E records
print()
print('=== New E records ===')
erecs = [
    ('0.006',  'LT', '', '', '4.0', 'GT', '0.006',  'LT'),
    ('0.002',  'LT', '', '', '',    '',   '0.002',  'LT'),
    ('0.003',  'LT', '', '', '',    '',   '0.003',  'LT'),
    ('0.0009', 'LT', '', '', '',    '',   '0.0009', 'LT'),
]
results = []
for ib, dib, ie, die, logft, dft, ti, dti in erecs:
    line = build_E(ib, dib, ie, die, logft, dft, ti, dti)
    rc = ruler(line)
    ok = rc == 0
    results.append((line, ok))
    print('E IB=' + ib.ljust(7) + ' DIB=' + dib.ljust(2) + ' LOGFT=' + logft.ljust(6) + ' DFT=' + dft.ljust(2) + ' len=' + str(len(line)) + ' ' + ('OK' if ok else 'FAIL'))

print()
print('=== L records ===')
lrecs = [
    ('3910', '', '0+'),
    ('4070', '', '1+'),
    ('5230', '', '0+'),
    ('5380', '', '1+'),
]
for e, de, j in lrecs:
    line = build_L(e, de, j)
    rc = ruler(line)
    ok = rc == 0
    results.append((line, ok))
    print('L E=' + e.ljust(6) + ' J=' + j.ljust(3) + ' len=' + str(len(line)) + ' ' + ('OK' if ok else 'FAIL'))

all_ok = all(r[1] for r in results)
print()
print('All pass: ' + str(all_ok))

# Print generated lines for copy-paste
if all_ok:
    print()
    print('=== GENERATED LINES ===')
    for line, ok in results:
        print(line)
