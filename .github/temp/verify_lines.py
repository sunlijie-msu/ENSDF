"""Dry-run: verify line numbers and content before applying fixes"""
from pathlib import Path

ENS_FILE = Path(r"A34\Cl34\new\Cl34_adopted.ens")

with open(ENS_FILE, encoding='utf-8') as f:
    lines = f.readlines()

# All lines to check: (lineno, expected_stripped_prefix)
checks = [
    (243,  ' 34CL cL J$1697|g'),
    (244,  ' 34CL2cL 146 level.'),
    (627,  ' 34CL cL J$3500|g'),
    (628,  ' 34CL2cL level.'),
    (639,  ' 34CL cL J$1502|g'),
    (663,  ' 34CL cL J$3330|g'),
    (814,  ' 34CL cL J$725|g'),
    (836,  ' 34CL cL J$4300.0|g'),
    (982,  ' 34CL cL J$1224.1|g'),
    (983,  ' 34CL2cL 3+, 146 level.'),
    (1027, ' 34CL cL J$2681|g'),
    (1054, ' 34CL3cL 4810.5|g'),
    (1174, ' 34CL2cL transition 1786.6'),
    (1209, ' 34CL cL J$primary transition 1330|g'),
    (1223, ' 34CL2cL 1977.0|g'),
    (1310, ' 34CL cL J$primary transitions 5762.8'),
    (1327, ' 34CL2cL transition 5638.6'),
    (2273, ' 34CL cL J$1935.0|g'),
    (2476, ' 34CL cL J$2384|g'),
    (2517, ' 34CL cL J$2487.4|g'),
    (2683, ' 34CL cL J$2840|g'),
    (2904, ' 34CL cL J$4077|g'),
    (2910, ' 34CL cL J$3381|g'),
]

all_ok = True
for lineno, prefix in checks:
    actual = lines[lineno-1].rstrip('\n')
    if actual.startswith(prefix):
        print(f'OK  Line {lineno:5d}: {actual[:60]}')
    else:
        print(f'FAIL Line {lineno:5d}: expected prefix {prefix!r}')
        print(f'          actual: {actual[:70]!r}')
        all_ok = False

print()
print('All OK!' if all_ok else 'SOME FAILURES - check line numbers')
