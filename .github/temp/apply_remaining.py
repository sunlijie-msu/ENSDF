"""
Apply remaining 27 replacements from replacements2.json.
All old strings verified FOUND=True before this script runs.
"""
import json

with open(r'd:\X\ND\ENSDF\.github\temp\replacements2.json', 'r', encoding='ascii') as f:
    reps = json.load(f)

raw_bytes = open(r'd:\X\ND\ENSDF\A34\Cl34\new\Cl34_33s_p_g.ens', 'rb').read()
content = raw_bytes.decode('ascii')
original_lines = len(content.split('\r\n'))

errors = []
for i, r in enumerate(reps, start=8):
    old = r['old']
    new = r['new']
    if old not in content:
        errors.append(f'[{i:02d}] NOT FOUND')
        continue
    count = content.count(old)
    if count > 1:
        errors.append(f'[{i:02d}] AMBIGUOUS: found {count} times')
        continue
    content = content.replace(old, new, 1)
    print(f'[{i:02d}] Applied')

if errors:
    print('\nERRORS:')
    for e in errors:
        print(' ', e)
    print('\nFile NOT written due to errors.')
else:
    final_lines = len(content.split('\r\n'))
    print(f'\nOriginal lines: {original_lines}, Final lines: {final_lines}, Delta: {final_lines - original_lines}')
    with open(r'd:\X\ND\ENSDF\A34\Cl34\new\Cl34_33s_p_g.ens', 'wb') as f:
        f.write(content.encode('ascii'))
    print('File written successfully.')
