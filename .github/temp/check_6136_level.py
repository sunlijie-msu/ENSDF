#!/usr/bin/env python3
"""Check if 6136 is an adopted level or only dataset-specific."""

mrg_path = r'A34\Cl34\raw\1977DA02_1983WA27.mrg'

with open(mrg_path, 'r') as f:
    lines = f.readlines()

# Find all LEVEL headers
level_headers = []
for i, line in enumerate(lines):
    if ' LEVEL' in line and '*' in line and '34CL  L' in line:
        # Extract energy
        idx = line.find('34CL  L')
        energy_str = line[idx+7:].strip()
        tokens = energy_str.split()
        energy = tokens[0] if tokens else 'unknown'
        level_headers.append((i+1, float(energy) if tokens and tokens[0].replace('.','').isdigit() else None))

print(f'Total LEVEL headers: {len(level_headers)}\n')
print('Last 10 LEVEL energies:')
for line_no, energy in level_headers[-10:]:
    print(f'  Line {line_no}: E={energy}')

print(f'\nIs 6136 an adopted level?')
for line_no, e in level_headers:
    if e and abs(e - 6136) < 1:
        print(f'  YES - Found at line {line_no}')
        break
else:
    print(f'  NO - 6136 is NOT an adopted level header')
    print(f'  Highest adopted level: {level_headers[-1][1]} keV')
