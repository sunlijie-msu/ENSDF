import csv
import re
from pathlib import Path

csv_path = Path(r'd:\X\ND\ENSDF\A34\Cl34\raw\1983WA27_Unbound.csv')
rows = list(csv.reader(csv_path.open(newline='')))

expected_ei = {
    '447':'5576.9','508':'5635.7','546':'5672.9','639':'5763.2','662':'5785.5','683':'5805.9',
    '731':'5852.8','777':'5897.2','822':'5940.8','914':'6030.0','976':'6088.91','1023':'6136.2',
    '1029':'6141.7','1057':'6169.0','1070':'6181.27','1097':'6207.1','1119':'6228.5','1158':'6266.5',
    '1165':'6273.3','1215':'6322.3','1264':'6369.8','1347':'6450.4','1386':'6488.3','1448':'6547.8',
    '1477':'6576.1','1528':'6626.2','1544':'6640.91','1629':'6724.2','1644':'6737.9','1698':'6790.8',
    '1706':'6798.4','1738':'6829.8','1752':'6842.7','1762':'6852.4','1781':'6871.0','1798':'6887.9',
    '1812':'6901.7','1829':'6917.9','1843':'6931.5','1974':'7059.0','1997':'7078.92'
}

# Tokens that should no longer appear as shorthand in Other Ef.
converted_tokens = {
    '2.18','2.38','2.58','2.61','2.72','3.13','3.33','3.38','3.55','3.60','3.63','3.65','3.66',
    '3.77','3.79','3.94','3.96','3.98','4.08','4.14','4.15','4.33','4.35','4.42','4.45','4.46','4.52',
    '4.606','4.610','4.64','4.70','4.72','4.82','4.94','4.96','5.00','5.17','5.39','5.54'
}
unresolved = {'4.61','13.80'}

failures = []
for row in rows[2:]:
    if len(row) < 2:
        continue
    eplab = row[0]
    ei = row[1]
    if eplab in expected_ei and ei != expected_ei[eplab]:
        failures.append(f'Ei mismatch {eplab}: expected {expected_ei[eplab]} got {ei}')

last_col = '\n'.join(row[-1] for row in rows[2:] if row)
for token in converted_tokens:
    if re.search(rf'(?<!\d){re.escape(token)}\(', last_col):
        failures.append(f'unconverted token remains: {token}(')
for token in unresolved:
    if not re.search(rf'(?<!\d){re.escape(token)}\(', last_col):
        failures.append(f'unresolved token missing unexpectedly: {token}(')

print(f'Total Ei rows checked: {len(expected_ei)}')
print(f'Failures: {len(failures)}')
for item in failures[:50]:
    print('FAIL:', item)

print('\nSpot-check rows:')
for eplab in ['447','1215','1843','1974']:
    row = next(r for r in rows[2:] if r and r[0] == eplab)
    print(eplab, 'Ei=', row[1], 'Other=', row[-1])
