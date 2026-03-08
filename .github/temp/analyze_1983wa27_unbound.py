import csv
import re
from pathlib import Path

csv_path = Path(r'd:\X\ND\ENSDF\A34\Cl34\raw\1983WA27_Unbound.csv')
ens_path = Path(r'd:\X\ND\ENSDF\A34\Cl34\new\Cl34_33s_p_g.ens')

rows = list(csv.reader(csv_path.open(newline='')))
ens_lines = ens_path.read_text(encoding='ascii').splitlines()

l_energies = []
for line in ens_lines:
    if len(line) >= 10 and line[5:8] == '  L':
        energy = line[9:19].strip()
        if energy:
            try:
                value = float(energy)
            except ValueError:
                continue
            l_energies.append((energy, value))

# unique by displayed energy string preserving order
seen = set()
uniq = []
for e, v in l_energies:
    if e not in seen:
        seen.add(e)
        uniq.append((e, v))

rounded_ei = [row[1] for row in rows[2:] if row and len(row) > 1]
print('Ei mappings:')
for ei in rounded_ei:
    try:
        target = float(ei)
    except ValueError:
        continue
    matches = []
    for e, v in uniq:
        if abs(v - target) < 1.0:
            matches.append(e)
    print(f'{ei}: {matches[:10]}')

print('\nOther Ef token mappings:')
# collect unique numeric tokens in last col
num_tokens = set()
for row in rows[2:]:
    if not row:
        continue
    last = row[-1]
    for token in re.findall(r'(?<!unknown Ef \()\b\d+(?:\.\d+)?(?=\()', last):
        num_tokens.add(token)
for token in sorted(num_tokens, key=float):
    t = float(token)
    matches = []
    for e, v in uniq:
        if abs(v/1000.0 - t) < 0.006:
            matches.append(e)
    print(f'{token}: {matches[:10]}')
