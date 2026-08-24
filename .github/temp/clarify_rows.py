import csv
rows = list(csv.DictReader(open(r'XUNDL/2026LIAA_CV10930_71As_Table_I.csv', encoding='utf-8-sig')))

def norm(s):
    return (s or '').replace('\u2212', '-').strip()

print('=== Row 77 explanation ===')
r = rows[76]
Ei = float(norm(r['Ei (keV)']))
Eg = float(norm(r['E\u03b3 (keV)']))
print('row 77: Ei=%s Eγ=%s -> Ef=%.1f Jpi=%s Jpf=%s' % (Ei, Eg, Ei - Eg, norm(r['I\u03c0i (Initial Spin-Parity)']), norm(r['I\u03c0f (Final Spin-Parity)'])))

print()
print('=== Rows 23, 25, 66 (borderline residual) ===')
for idx in [23, 25, 66]:
    r = rows[idx - 1]
    Ei = float(norm(r['Ei (keV)']))
    Eg = float(norm(r['E\u03b3 (keV)']))
    print('row %d: Ei=%s Eγ=%s -> Ef=%.1f Jpi=%s Jpf=%s' % (idx, Ei, Eg, Ei - Eg, norm(r['I\u03c0i (Initial Spin-Parity)']), norm(r['I\u03c0f (Final Spin-Parity)'])))

print()
print('=== canonical levels near those Ef ===')
for name, ef in [('row23->', 1798.8), ('row25->', 1395.5), ('row66->', 3787.6), ('row77->', 3788.7)]:
    print(name, 'Ef=%.1f' % ef)
