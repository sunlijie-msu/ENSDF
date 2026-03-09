mrg_lines = open(r'd:\X\ND\ENSDF\A34\Cl34\raw\1977DA02_1983WA27.mrg', encoding='utf-8').readlines()

samples = [
    ('950.77', '3.9'),   # known LT
    ('1696.9', '100'),   # known numeric
    ('2034.7', '100.0'), # known
    ('665.7', '100'),    # 1977Da02
]

for line in mrg_lines:
    raw = line.rstrip('\n')
    if '--->' not in raw:
        continue
    for e_target, ri_target in samples:
        if e_target in raw and '34CL  G' in raw:
            # find where the ENSDF record starts
            idx = raw.find(' 34CL  G')
            if idx < 0:
                idx = raw.find('34CL  G')
            if idx >= 0:
                print(f"E={e_target}: record_start={idx}, len={len(raw)}")
                # print key chars
                for off in range(0, 35):
                    print(f"  {idx+off:3d}[{off:2d}]: {repr(raw[idx+off])}")
                break
