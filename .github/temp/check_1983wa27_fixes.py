s = open(r'd:\X\ND\ENSDF\A34\Cl34\new\Cl34_33s_p_g.ens').read()
checks = [
    ('Ep=546',  '0.7 {I3} (1983Wa27)'),
    ('Ep=639',  '0.06 {I3} (1983Wa27)'),
    ('Ep=1029', '1.1 {I3} (1983Wa27)'),
    ('Ep=1057', '1.8 {I5} (1983Wa27)'),
    ('Ep=1097', '1.4 {I3} (1983Wa27)'),
    ('Ep=1165', '3.3 {I7} (1983Wa27)'),
    ('Ep=1215', '2.2 {I9} (1983Wa27)'),
    ('Ep=1386', '0.6 {I3} (1983Wa27)'),
    ('Ep=1644', '0.7 {I3} (1983Wa27)'),
    ('Ep=1698', '0.2 {I1} (1983Wa27)'),
    ('Ep=1762', '2.1 {I5} (1983Wa27)'),
    ('Ep=1843', '0.8 {I3} (1983Wa27)'),
    ('Ep=976',  '1.0 {I3} (1983Wa27)'),
    ('Ep=1158', '0.4 {I2} (1983Wa27)'),
    ('Ep=1997', '1.7 {I4} (1983Wa27)'),
]
all_ok = True
for label, search in checks:
    status = 'OK' if search in s else 'MISSING'
    if status == 'MISSING':
        all_ok = False
    print(f'{label}: {status}')
print()
print('All OK!' if all_ok else 'Some entries are MISSING!')
