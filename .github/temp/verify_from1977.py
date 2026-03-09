with open(r'd:\X\ND\ENSDF\A34\Cl34\raw\1977DA02_1983WA27.adp', encoding='utf-8') as f:
    lines = f.readlines()

print('=== Three changed cases ===')
for i, line in enumerate(lines, 1):
    if 'from 1977Da02. Other:' in line:
        g_line = lines[i-2].rstrip()
        c_line = lines[i-1].rstrip()
        print(f'  G:  {g_line}')
        print(f'  cG: {c_line}')
        print()

print('=== Summary ===')
n_from = sum(1 for l in lines if 'from 1977Da02. Other:' in l)
n_other = sum(1 for l in lines if 'cG RI' in l and 'other: 100' in l)
print(f'from 1977Da02. Other: count = {n_from}  (expected 3)')
print(f'other: 100 count = {n_other}  (expected 22-3=19)')
