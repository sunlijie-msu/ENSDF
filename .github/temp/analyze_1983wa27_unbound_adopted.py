import csv
from pathlib import Path

csv_path = Path(r'd:\X\ND\ENSDF\A34\Cl34\raw\1983WA27_Unbound.csv')
ens_path = Path(r'd:\X\ND\ENSDF\A34\Cl34\new\Cl34_adopted.ens')

rows = list(csv.reader(csv_path.open(newline='')))
ens_lines = ens_path.read_text(encoding='ascii').splitlines()

energies = []
for line in ens_lines:
    if len(line) >= 10 and line[5:8] == '  L':
        energy = line[9:19].strip()
        if energy:
            try:
                value = float(energy)
            except ValueError:
                continue
            energies.append((energy, value))

seen = set()
uniq = []
for e, v in energies:
    if e not in seen:
        seen.add(e)
        uniq.append((e, v))

rounded_ei = [row[1] for row in rows[2:] if row and len(row) > 1]
print('Ei adopted mappings:')
for ei in rounded_ei:
    t = float(ei)
    matches = [e for e,v in uniq if abs(v - t) < 1.0]
    print(f'{ei}: {matches[:10]}')

print('\n4.606/4.610 matches:')
for token in [4.606, 4.610, 13.80]:
    matches = [e for e,v in uniq if abs(v/1000.0 - token) < 0.006]
    print(token, matches[:20])
