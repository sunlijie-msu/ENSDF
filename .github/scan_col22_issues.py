#!/usr/bin/env python3
"""Comprehensive scan for L-records with column 22 issues."""

file = r'd:\X\ND\ENSDF\A35\Cl35\new\Cl35_34s_p_g.ens'

with open(file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find L-records where column 22 (index 21) is NOT a space and NOT a digit (DE uncertainty)
problematic = []
for i, line in enumerate(lines):
    if line.startswith(' 35CL  L ') and len(line) > 21:
        col22 = line[21]
        # Column 22 should be space. If it's a digit (0-9), it's part of DE field (cols 20-21)
        # If it's J-π character (letter, paren, etc.), that's the problem
        if col22 != ' ' and col22 not in '0123456789':
            problematic.append((i+1, line.rstrip(), col22))

print(f'Total L-records with non-space at column 22: {len(problematic)}')
print('=' * 80)
for num, line, col22_char in problematic:
    print(f'Line {num:4d}: col22="{col22_char}" | {line[:70]}')
