#!/usr/bin/env python3
"""Quick check if the 4 'remaining' lines are actually fixed."""

file = r'd:\X\ND\ENSDF\A35\Cl35\new\Cl35_34s_p_g.ens'
lines_to_check = {
    1254: '7899.1',
    1300: '7970.2',
    1331: '7987.8',
    1353: '7995.6'
}

with open(file, 'r', encoding='utf-8') as f:
    all_lines = f.readlines()

print('Verifying 4 supposedly remaining lines:')
print('=' * 80)
for line_num, energy in lines_to_check.items():
    line = all_lines[line_num - 1]  # Convert to 0-indexed
    if line.strip():
        col22_char = line[21] if len(line) > 21 else '?'
        status = '[OK]' if col22_char == ' ' else '[NEEDS FIX]'
        print(f'Line {line_num:4d}: {status} col22="{col22_char}" | {line.rstrip()}')
        print(f'             Length: {len(line.rstrip())} chars')
