import csv, bisect
rows = list(csv.DictReader(open(r'XUNDL/2026LIAA_CV10930_71As_Table_I.csv', encoding='utf-8-sig')))

def norm(s):
    return (s or '').replace('\u2212', '-').strip()

# canonical registry from Ei rows
canon = {}
for r in rows:
    ei = float(norm(r['Ei (keV)']))
    J = norm(r['I\u03c0i (Initial Spin-Parity)'])
    canon.setdefault(ei, set()).add(J)

keys = sorted(canon)

def find(Ef):
    # nearest canonical within 1.0 keV
    pos = bisect.bisect_left(keys, Ef)
    best, bd = None, 1e9
    for c in keys[max(0,pos-1):pos+1]:
        d = abs(c - Ef)
        if d < bd:
            bd, best = d, c
    return (best, bd) if best is not None and bd <= 1.0 else (None, bd)

print('FULL J-PI OCCURRENCE SCAN (paren-sensitive):')
print('row  Ei      Eγ      Ef      Jpf          canonical J          residual  verdict')
issues = []
for idx, r in enumerate(rows, 1):
    Ei = float(norm(r['Ei (keV)']))
    Eg = float(norm(r['E\u03b3 (keV)']))
    Ef = Ei - Eg
    Jpf = norm(r['I\u03c0f (Final Spin-Parity)'])
    best, bd = find(Ef)
    if best is None:
        # ground state check
        if abs(Ef) < 1.0:
            verdict = 'OK(gs)' if Jpf == '5/2-' else '??gs'
        else:
            verdict = 'NO-LVL'
        print('%3d %-7s %-7s %-7s %-10s %-15s %-8s %s' % (idx, norm(r['Ei (keV)']), norm(r['E\u03b3 (keV)']), '%.1f' % Ef, Jpf, '-', '%.1f' % bd, verdict))
        continue
    canJ = canon[best]
    # J must be identical string (paren-sensitive)
    if Jpf in canJ:
        verdict = 'OK'
    else:
        verdict = 'MISMATCH'
        issues.append((idx, Ef, best, Jpf, canJ))
    print('%3d %-7s %-7s %-7s %-10s %-15s %-8s %s' % (idx, norm(r['Ei (keV)']), norm(r['E\u03b3 (keV)']), '%.1f' % Ef, Jpf, ','.join(sorted(canJ)), '%.1f' % bd, verdict))

print()
print('=== MISMATCHES (all) ===')
for it in issues:
    print('row %d: Ef=%.1f -> canonical %.1f %s ; table Jpf=%s' % (it[0], it[1], it[2], it[4], it[3]))
