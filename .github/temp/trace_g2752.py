#!/usr/bin/env python3
"""Manually trace one 'Other:' example: G 2752.7 with Other: <7.8."""

mrg_path = r'A34\Cl34\raw\1977DA02_1983WA27.mrg'

with open(mrg_path, 'r') as f:
    lines = f.readlines()

# Looking for G energies near 2752-2753 measured by 1983Wa27 (dataset B)
print('=== Tracing Example: G 2752.7 with Other: <7.8 (1983Wa27) ===\n')
print('Question: If the adp says this gamma is from 1977Da02 (1.82, DRI=91)')
print('and Other: <7.8 from 1983Wa27, is that correct?\n')

print('Searching in mrg for G 2752-2753 from 1983Wa27 (dataset B):\n')

for i, line in enumerate(lines):
    if '275' in line and '1983Wa27' in line and 'G' in line:
        print(f'Line {i+1}: {line.rstrip()[:120]}')

print('\n\nAlso searching for G 2752-2753 from 1977DA02 (dataset A):\n')
for i, line in enumerate(lines):
    if '275' in line and '1977DA02' in line and 'G' in line:
        print(f'Line {i+1}: {line.rstrip()[:120]}')

print('\n\nAll GAMMA headers with 275 in energy:')
for i, line in enumerate(lines):
    if line.startswith(' GAMMA-') and '275' in line:
        print(f'Line {i+1}: {line.rstrip()[:120]}')
