import os
os.chdir(r"D:\X\ND\ENSDF")

lines_ens = open('A34/Cl34/new/Cl34_33s_p_g.ens','r').readlines()
lines_src = open('A34/Cl34/raw/1971HY02.ens','r').readlines()

spot_targets = [
    ('2034.6', '100 {I14}', 2034.6),
    ('3507.1', '100 {I12}', 3507.1),
    ('1589.7', '6.0 {I20}', 1589.7),
    ('3987.7', '16 {I6}', 3987.7),
    ('6228.01', '1.60 {I80}', 6228.01),
]

print('Spot check: 5 of 40 Phase 5 changes (12.5% sample)')
print()
all_pass = True
for ge, expected_cg, approx in spot_targets:
    found_cg = False
    cg_line = 'NOT FOUND'
    for n, ln in enumerate(lines_ens):
        if ('G '+ge) in ln and ln[7:9] == 'G ':
            for k in range(n, min(len(lines_ens), n+7)):
                if expected_cg in lines_ens[k]:
                    found_cg = True
                    cg_line = lines_ens[k].rstrip()[:75]
                    break
            break

    found_src = False
    src_ri = 'N/A'
    src_dri = 'N/A'
    for ln in lines_src:
        if len(ln) >= 19 and ln[7:9] == 'G ':
            src_e = ln[9:19].strip()
            try:
                if abs(float(src_e) - approx) < 2.0:
                    found_src = True
                    src_ri = ln[22:29].strip()
                    src_dri = ln[29:31].strip()
                    break
            except Exception:
                pass

    status = 'PASS' if found_cg else 'FAIL'
    if not found_cg:
        all_pass = False
    print(f'{status}: G={ge}')
    print(f'  Adopted cG text: {cg_line}')
    if found_src:
        print(f'  Source 1971HY02: RI={src_ri}, DRI={src_dri}')
    else:
        print(f'  Source 1971HY02: NOT FOUND (approx {approx})')
    print()

if all_pass:
    print('ALL SPOT CHECKS PASSED (5/5)')
else:
    print('SOME SPOT CHECKS FAILED')
