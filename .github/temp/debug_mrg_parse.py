#!/usr/bin/env python3
"""Debug script to understand mrg file structure."""

import re

mrg_path = r'A34\Cl34\raw\1977DA02_1983WA27.mrg'

with open(mrg_path, 'r') as f:
    lines = f.readlines()

# Find LEVEL lines with * and calculate total count
level_count = 0
for i, l in enumerate(lines):
    if ' LEVEL' in l and '*' in l and '34CL  L' in l:
        level_count += 1

print(f'Total LEVEL headers in mrg: {level_count}')
print()

# Show first 10 LEVEL lines
level_found = 0
for i, l in enumerate(lines):
    if ' LEVEL' in l and '*' in l and '34CL  L' in l:
        level_found += 1
        idx = l.find('34CL  L')
        energy_str = l[idx+7:idx+20].strip()
        print(f'LEVEL #{level_found} (line {i+1}): energy=\"{energy_str}\"')
        print(f'  Full line: {repr(l[:80])}')
        if level_found >= 10:
            break

print()

# Find where 3982 and 6136 energies are
for i, l in enumerate(lines):
    if '3982' in l or '6136' in l:
        if '34CL' in l:
            print(f'Line {i+1}: {repr(l[:90])}')
