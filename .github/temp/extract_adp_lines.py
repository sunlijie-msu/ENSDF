#!/usr/bin/env python3
with open(r'd:\X\ND\ENSDF\A34\Cl34\raw\1977DA02_1983WA27.adp', 'r', encoding='utf-8') as f:
    lines = f.readlines()

cases = [
    (37, True),
    (52, False),
    (67, False),
    (77, True),
    (104, True),
    (115, False),
    (151, False),
    (160, False),
    (173, False),
    (178, False),
    (227, False),
    (241, True),
    (255, True),
    (268, False),
    (297, True),
    (305, False),
    (322, False),
    (350, False),
    (376, False),
    (387, False),
    (400, False),
]

for ln, has_2cg in cases:
    old_line = lines[ln-1]
    print(f'--- Line {ln} has_2cg={has_2cg} ---')
    print(repr(old_line))
    if has_2cg:
        print(repr(lines[ln]))
