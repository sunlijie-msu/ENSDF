import csv
rows = list(csv.DictReader(open(r'XUNDL/2026LIAA_CV10930_71As_Table_I.csv', encoding='utf-8-sig')))

def norm(s):
    return (s or '').replace('\u2212', '-').strip()

# Report flagged rows: 2, 12, 30, 91
for idx in [2, 12, 30, 91]:
    r = rows[idx - 1]
    print('row %d: Ei=%s Eg=%s Jpi=%s Jpf=%s Iγ=%s ADO=%s Ap=%s M=%s' % (
        idx, norm(r['Ei (keV)']), norm(r['E\u03b3 (keV)']),
        norm(r['I\u03c0i (Initial Spin-Parity)']), norm(r['I\u03c0f (Final Spin-Parity)']),
        norm(r['I\u03b3 (Relative Intensity)']), norm(r['ADO ratio']), norm(r['Ap value']),
        norm(r['Multipolarity'])))

print()
print('Physics analysis:')
# g#2: 870.4 5/2- -> 147.2 3/2-  (dJ=1) M1+E2, ADO=1.08
print('g#2: 870.4 (5/2-) -> 147.2 (3/2-), dJ=1, M1+E2')
print('  Rule: dJ=1 (stretched dipole) -> R~0.8; measured 1.08(0.12)')
print('  M1+E2 with E2 admixture: ADO depends on mixing ratio; 1.08 is intermediate')
print()
# g#12: 1467.8 7/2- -> 0 5/2-, dJ=1, (M1+E2), ADO=1.07
print('g#12: 1467.8 (7/2-) -> 0.0 (5/2-), dJ=1, (M1+E2)')
print('  Rule: dJ=1 -> R~0.8; measured 1.07(0.12)')
print('  Same mixed-transition caveat')
print()
# g#30: 2415.7 13/2+ -> 1713.9 13/2+, dJ=0, (M1+E2), ADO=1.12, POL=+0.14
print('g#30: 2415.7 (13/2+) -> 1713.9 (13/2+), dJ=0, (M1+E2)')
print('  Rule: dJ=0 (unstretched dipole) -> R~1.3; measured 1.12(0.07)  [consistent-ish]')
print('  POL=+0.14 with M1+E2: M1+E2 has E2 admixture')
print('  Rule says positive POL = electric. M1+E2 is mixed; if E2 dominates, positive POL ok')
print()
# g#91: 6359.5 29/2+ -> 5021.1 25/2+, dJ=2, (E2), ADO=1.59
print('g#91: 6359.5 (29/2+) -> 5021.1 (25/2+), dJ=2, (E2)')
print('  Rule: dJ=2 (stretched quadrupole) -> R~1.3; measured 1.59(0.13)')
print('  1.59 vs 1.3: within 2 sigma? diff=0.29, unc=0.13 -> 2.2 sigma, marginal')
