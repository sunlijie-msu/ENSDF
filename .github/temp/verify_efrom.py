"""Verify all 10 cG E$From comment insertions."""
with open('A34/Cl34/new/Cl34_adopted.ens', 'r') as f:
    lines = f.readlines()

targets = {
    'G 314.64':  ('314.64', 'E$From {+32}S'),
    'G 461.00':  ('461.00', 'E$From {+32}S'),
    'G 1740.2':  ('1740.2', 'E$From {+32}S'),
    'G 204.58':  ('204.58', 'E$From {+32}S'),
    'G 519.22':  ('519.22', 'E$From {+32}S'),
    'G 564.67':  ('564.67', 'E$From {+32}S'),
    'G 769.25':  ('769.25', 'E$From {+32}S'),
    'G 1426.7':  ('1426.7', 'E$From {+32}S'),
    'G 1224.1':  ('1224.1', 'E$From {+24}Mg'),
    'G 4677.4':  ('4677.4', 'E$From {+24}Mg'),
}

all_ok = True
for label, (energy, pattern) in targets.items():
    found_g = False
    for i, l in enumerate(lines):
        if '  G ' + energy in l and l[0:5].strip():
            found_g = True
            found_e = False
            for j in range(i, min(len(lines), i+6)):
                if pattern in lines[j]:
                    found_e = True
                    efrom_line = lines[j].rstrip()
                    efrom_lineno = j+1
                    break
            if found_e:
                print(f'OK  {label}: line {efrom_lineno}: {efrom_line}')
            else:
                print(f'FAIL {label}: E$From comment NOT FOUND in next 6 lines!')
                all_ok = False
                for j in range(i, min(len(lines), i+6)):
                    print(f'  {j+1}: {lines[j].rstrip()}')
            break
    if not found_g:
        print(f'FAIL {label}: G-record not found!')
        all_ok = False

print()
print('All OK!' if all_ok else 'ERRORS FOUND!')

# Count total E$From(3He) and E$From(Mg) lines
n_3he = sum(1 for l in lines if 'cG E$From {+32}S' in l)
n_mg  = sum(1 for l in lines if 'cG E$From {+24}Mg' in l)
print(f'Total cG E$From(3He): {n_3he}')
print(f'Total cG E$From(Mg): {n_mg}')
