#!/usr/bin/env python3
"""Generate exact replacement pairs for all RI=100 weighted-average comments."""
import re

with open(r'd:\X\ND\ENSDF\A34\Cl34\raw\1977DA02_1983WA27.adp', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 1-indexed comment line numbers, has_2cg flag
# (Verified by grep: lines containing cG RI$weighted average of 100 and 100)
cases = [
    (34, True),
    (49, False),
    (64, False),
    (74, True),
    (101, True),
    (112, False),
    (148, False),
    (157, False),
    (170, False),
    (175, False),
    (224, False),
    (238, True),
    (252, True),
    (265, False),
    (294, True),
    (302, False),
    (319, False),
    (347, False),
    (373, False),
    (384, False),
    (397, False),
]

replacements = []
for cline, has_2cg in cases:
    # Lines are 0-indexed
    g_line = lines[cline - 2]   # G record
    c_line = lines[cline - 1]   # comment line

    # Extract 1977Da02 value
    m = re.search(r'of (\d+\.?\d* \{I\d+\}) \(1977Da02\)', c_line)
    if not m:
        print(f'ERROR line {cline}: cannot parse 1977Da02 value from: {c_line.strip()}')
        continue
    da_val = m.group(1)

    # Build old string
    old = g_line + c_line
    if has_2cg:
        old += lines[cline]  # 2cG line (0-indexed: cline = line after comment)

    # Build new string: G record unchanged + new comment
    new_comment = f' 34CL cG RI$other: {da_val} (1977Da02)\n'
    new = g_line + new_comment

    replacements.append((cline, old, new))
    print(f'OK cline={cline}: {repr(da_val)}')

# Write the modified file
full_text = ''.join(lines)
for cline, old, new in replacements:
    if old not in full_text:
        print(f'ERROR cline={cline}: oldString not found in file!')
        continue
    count = full_text.count(old)
    if count != 1:
        print(f'WARNING cline={cline}: oldString appears {count} times!')
    full_text = full_text.replace(old, new, 1)

with open(r'd:\X\ND\ENSDF\A34\Cl34\raw\1977DA02_1983WA27.adp', 'w', encoding='utf-8') as f:
    f.write(full_text)

print(f'\nDone! Applied {len(replacements)} replacements.')
