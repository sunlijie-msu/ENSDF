import csv
from pathlib import Path

csv_path = Path(r'd:\X\ND\ENSDF\A34\Cl34\raw\1983WA27_Bound.csv')
ens_path = Path(r'd:\X\ND\ENSDF\A34\Cl34\raw\1983WA27.ens')

expected = {
    '146': '146.4',
    '461': '461.0',
    '666': '665.6',
    '1230': '1230.33',
    '1887': '1887.31',
    '2158': '2157.90',
    '2181': '2181.10',
    '2376': '2375.7',
    '2580': '2580.4',
    '2611': '2611.05',
    '2721': '2721.1',
    '3129': '3129.13',
    '3334': '3334.0',
    '3383': '3383.3',
    '3545': '3545.07',
    '3600': '3600.27',
    '3632': '3631.8',
    '3646': '3646.3',
    '3660': '3660.0',
    '3774': '3773.84',
    '3792': '3791.7',
    '3940': '3940.1',
    '3964': '3964.1',
    '3984': '3983.5',
    '4076': '4076.3',
    '4140': '4139.8',
    '4148': '4147.8',
    '4326': '4325.91',
    '4354': '4354.3',
    '4417': '4417.4',
    '4447': '4446.6',
    '4461': '4461.4',
    '4516': '4515.8',
    '4639': '4638.9',
    '4696': '4695.7',
    '4717': '4717.4',
    '4825': '4824.5',
    '4942': '4941.9',
    '4957': '4957.3',
    '4996': '4995.6',
    '5172': '5171.6',
    '5387': '5386.8',
    '5541': '5540.8',
}

with csv_path.open(newline='') as f:
    rows = list(csv.reader(f))

header = rows[1]
row_labels = [row[0] for row in rows[2:]]

checks = []
checks.append(('header 146.4', header[2] == '146.4'))
checks.append(('header 461.0', header[3] == '461.0'))
checks.append(('header 665.6', header[4] == '665.6'))
checks.append(('header 1230.33', header[5] == '1230.33'))
checks.append(('header 1887.31', header[6] == '1887.31'))
checks.append(('header 2157.90', header[7] == '2157.90'))
checks.append(('header 2181.10', header[8] == '2181.10'))
checks.append(('header 2375.7', header[9] == '2375.7'))
checks.append(('header 2721.1', header[10] == '2721.1'))

for old, new in expected.items():
    checks.append((f'row {new}', new in row_labels))
    checks.append((f'old row {old} removed', old not in row_labels))

checks.append(('row 4606 unchanged', '4606' in row_labels))
checks.append(('row 4610 unchanged', '4610' in row_labels))

failed = [name for name, ok in checks if not ok]
print(f'Total checks: {len(checks)}')
print(f'Failed: {len(failed)}')
for name in failed:
    print('FAIL:', name)

print('\nRandom spot-check sample:')
for old in ['1230', '3632', '4447', '4639', '5541']:
    print(f'{old} -> {expected[old]} | present={expected[old] in row_labels}')
