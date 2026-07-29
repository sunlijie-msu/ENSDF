"""Build and validate ENSDF lines for S34 beta decay revision."""
import subprocess, sys

def ruler(line):
    r = subprocess.run([sys.executable, '.github/scripts/ensdf_1line_ruler.py', '--line', line],
                       capture_output=True, text=True)
    return r.returncode

def build_B(IB_str, DIB_str, LOGFT_str, DLOGFT_str):
    line = (
        ' 34S   B ' +
        ' '*10 +  # E 10-19
        '  ' +    # DE 20-21
        ' ' +     # col 22
        IB_str.ljust(7)[:7] +
        DIB_str.ljust(2)[:2] +
        ' '*10 +  # cols 32-41
        LOGFT_str.ljust(8)[:8] +
        DLOGFT_str.ljust(6)[:6] +
        ' '*21 +  # cols 56-76
        ' ' +     # col 77
        '  ' +    # cols 78-79
        ' '       # col 80
    )
    return line

def build_G(E_str, DE_str, RI_str, DRI_str, M_str, MR_str='', DMR_str=''):
    line = (
        ' 34S   G ' +
        E_str.ljust(10)[:10] +
        DE_str.ljust(2)[:2] +
        ' ' +     # col 22
        RI_str.ljust(7)[:7] +
        DRI_str.ljust(2)[:2] +
        ' ' +     # col 32
        M_str.ljust(9)[:9] +
        MR_str.ljust(8)[:8] +
        DMR_str.ljust(6)[:6] +
        ' '*7 +   # CC 56-62
        '  ' +    # DCC 63-64
        ' '*10 +  # TI 65-74
        '  ' +    # DTI 75-76
        ' ' +     # C 77
        '  ' +    # cols 78-79
        ' '       # Q 80
    )
    return line

def build_L(E_str, DE_str, J_str):
    line = (
        ' 34S   L ' +
        E_str.ljust(10)[:10] +
        DE_str.ljust(2)[:2] +
        ' ' +     # col 22
        J_str.ljust(17)[:17] +
        ' '*41    # cols 40-80
    )
    return line

def cG(line_text):
    """Build a cG comment line."""
    return (' 34S  cG ' + line_text).ljust(80)[:80]

def cB(line_text):
    return (' 34S  cB ' + line_text).ljust(80)[:80]

# === TEST ALL LINES ===
all_ok = True

print('B-records:')
for IB, DIB, LOGFT, DLOGFT in [('84.8','21','5.159','12'),('14.8','20','4.93','6'),
    ('0.045','17','5.98','17'),('0.111','23','5.38','9'),('0.31','6','4.88','9')]:
    line = build_B(IB, DIB, LOGFT, DLOGFT)
    rc = ruler(line)
    ok = rc == 0
    if not ok: all_ok = False
    print(f'  B IB={IB:>7} len={len(line)} {"OK" if ok else "FAIL"}')
    if not ok:
        print(f'    {repr(line)}')

print('\nG-records:')
grecs = [
    ('2127.3','','100.0','3','E2','',''),
    ('3303.5','','0.12','LT','','',''),
    ('1787','1','0.3','1','E2','',''),
    ('1947.1','15','0.28','10','M1+E2','+1.3','+9-32'),
    ('4073.4','15','0.46','6','D','',''),
    ('1987.2','10','1.0','2','M1+E2','-0.40','5'),
    ('4114.0','15','1.2','2','E2','',''),
    ('1318.5','','0.21','LT','','',''),
    ('2560.0','','0.11','LT','','',''),
    ('1571.5','','1.0','LT','','',''),
    ('4891','','0.08','LT','','',''),
]
for E, DE, RI, DRI, M, MR, DMR in grecs:
    line = build_G(E, DE, RI, DRI, M, MR, DMR)
    rc = ruler(line)
    ok = rc == 0
    if not ok: all_ok = False
    print(f'  G E={E:>10} len={len(line)} {"OK" if ok else "FAIL"}')
    if not ok:
        print(f'    {repr(line)}')

print('\nL-records:')
lrecs = [
    ('2127.4','2','2+'),
    ('3303.7','3',''),
    ('3914.2','6','0+'),
    ('4073.0','10','1+'),
    ('4114.5','6','2+'),
    ('4622.2','6',''),
    ('4687.5','6',''),
    ('4875.2','6',''),
    ('4891','3',''),
]
for E, DE, J in lrecs:
    line = build_L(E, DE, J)
    rc = ruler(line)
    ok = rc == 0
    if not ok: all_ok = False
    print(f'  L E={E:>10} len={len(line)} {"OK" if ok else "FAIL"}')
    if not ok:
        print(f'    {repr(line)}')

print(f'\nAll pass: {all_ok}')
