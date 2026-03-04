from pathlib import Path
lines = Path('ENSDF_Mass_Chain_Evaluations.md').read_text(encoding='utf-8').splitlines()
data_rows = []
for ln in lines:
    if not ln.startswith('| ') or ln.startswith('|---'):
        continue
    p = [x.strip() for x in ln.strip('|').split('|')]
    if len(p) == 4 and p[0].isdigit():
        data_rows.append((int(p[0]), ln))

print(f'Total data rows: {len(data_rows)}')
if data_rows:
    print(f'Min A: {data_rows[0][0]}')
    print(f'Max A: {data_rows[-1][0]}')
    print()
    print('Last 10 rows:')
    for a, ln in data_rows[-10:]:
        print(repr(ln))
    print()
    # Find rows near 224
    print('Rows around A=220-228:')
    for a, ln in data_rows:
        if 218 <= a <= 230:
            print(repr(ln))
