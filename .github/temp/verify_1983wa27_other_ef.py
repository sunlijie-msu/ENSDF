import csv
from pathlib import Path

csv_path = Path(r'd:\X\ND\ENSDF\A34\Cl34\raw\1983WA27_Bound.csv')
with csv_path.open(newline='') as f:
    rows = list(csv.reader(f))

expected = {
    '4139.8': '2.5804(19+/-3)',
    '4717.4': '2.61105(10+/-3)',
    '4824.5': '3.60027(31+/-2); 3.6318(4+/-1)',
    '5386.8': '3.60027(100)',
    '5540.8': '3.54507(36+/-5); 3.60027(64+/-5)',
}
unknown_expected = {
    '3646.3': 'unknown Ef (25   )',
    '3773.84': 'unknown Ef (23%)',
    '3791.7': 'unknown Ef (15%)',
    '4325.91': 'unknown Ef (20%)',
    '4941.9': 'unknown Ef (30%)',
    '4995.6': 'unknown Ef (30%)',
}

row_map = {row[0]: row[-1] for row in rows[2:]}
failed = []
for level, value in expected.items():
    if row_map.get(level) != value:
        failed.append((level, value, row_map.get(level)))
for level, value in unknown_expected.items():
    if row_map.get(level) != value:
        failed.append((level, value, row_map.get(level)))

print(f'Total checks: {len(expected) + len(unknown_expected)}')
print(f'Failed: {len(failed)}')
for level, exp, got in failed:
    print(f'FAIL {level}: expected={exp!r} got={got!r}')

print('\nSpot-check values:')
for level in ['4139.8', '4717.4', '4824.5', '5386.8', '5540.8']:
    print(level, '->', row_map[level])
