#!/usr/bin/env python3
"""Scan G-records for RI field positioning issues (column 22 check)."""

file = r'd:\X\ND\ENSDF\A35\Cl35\new\Cl35_34s_p_g.ens'

with open(file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find G-records where column 22 is NOT a space
# Column 22 should be space separator, RI should start at column 23
problematic = []
for i, line in enumerate(lines):
    if line.startswith(' 35CL  G ') and len(line) > 22:
        col22 = line[21]  # Column 22 (0-indexed = 21)
        # Column 22 should be space. If it's a digit or letter, RI is shifted left
        if col22 != ' ':
            # Extract RI field area (columns 23-29) to show what's there
            ri_area = line[22:29] if len(line) > 29 else line[22:]
            problematic.append((i+1, line.rstrip(), col22, ri_area))

print(f'Total G-records with non-space at column 22: {len(problematic)}')
print('=' * 80)
if len(problematic) > 0:
    print(f'Showing first 10 of {len(problematic)} issues:\n')
    for num, line, col22_char, ri_area in problematic[:10]:
        print(f'Line {num:4d}: col22="{col22_char}" | RI area (23-29)=[{ri_area}]')
        print(f'             {line[:60]}...')
        print()
else:
    print('[OK] All G-records have mandatory space at column 22')
