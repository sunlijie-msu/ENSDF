import csv
rows = list(csv.DictReader(open(r'XUNDL/2026LIAA_CV10930_71As_Table_I.csv', encoding='utf-8-sig')))

def norm(s):
    return (s or '').replace('\u2212', '-').strip()

def show(idx):
    r = rows[idx - 1]
    Ei = float(norm(r['Ei (keV)']))
    Eg = float(norm(r['E\u03b3 (keV)']))
    print('row %d: Ei=%s Eγ=%s -> Ef=%.1f | Jpi=%s Jpf=%s | M=%s' % (
        idx, norm(r['Ei (keV)']), norm(r['E\u03b3 (keV)']), Ei - Eg,
        norm(r['I\u03c0i (Initial Spin-Parity)']), norm(r['I\u03c0f (Final Spin-Parity)']),
        norm(r['Multipolarity'])))

print('=== Report items ===')
for idx in [43, 59, 63, 49, 90, 77]:
    show(idx)

print()
print('=== My extra flags (check if genuine) ===')
show(71)

print()
print('=== Canonical J for involved final levels ===')
canon = {}
for r in rows:
    ei = norm(r['Ei (keV)'])
    canon.setdefault(ei, set()).add(norm(r['I\u03c0i (Initial Spin-Parity)']))
for ei in ['2792.7', '3236.9', '2688.6', '3494.5', '5072.9', '3788.6']:
    print('canonical', ei, sorted(canon.get(ei, [])))
