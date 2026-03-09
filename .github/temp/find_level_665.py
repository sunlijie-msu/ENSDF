#!/usr/bin/env python3
"""Find L 665.7 in mrg and check what gammas are under it."""

mrg_path = r'A34\Cl34\raw\1977DA02_1983WA27.mrg'

with open(mrg_path, 'r') as f:
    lines = f.readlines()

# Find the L 665.7 level
for i, line in enumerate(lines):
    if ' LEVEL' in line and '*' in line and '665.7' in line:
        print(f'Found L 665.7 at line {i+1}')
        print(line.rstrip())
        print()
        
        # Show next 20 lines
        for j in range(i+1, min(i+21, len(lines))):
            l = lines[j].rstrip()
            if l.startswith('-' * 20):
                break
            print(f'{j+1}: {l[:100]}')  # Limit output width
        break
