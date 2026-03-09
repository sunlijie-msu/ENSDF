#!/usr/bin/env python3
import re

with open(r'd:\X\ND\ENSDF\A34\Cl34\raw\1977DA02_1983WA27.adp', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 1-indexed comment line numbers, has_2cg flag
cases = [
    (37, True),
    (52, False),
    (67, False),
    (77, True),
    (104, True),
    (115, False),
    (151, False),
    (160, False),
    (173, False),
    (178, False),
    (227, False),
    (241, True),
    (255, True),
    (268, False),
    (297, True),
    (305, False),
    (322, False),
    (350, False),
    (376, False),
    (387, False),
    (400, False),
]

for cline, has_2cg in cases:
    g_line = lines[cline - 2]   # G record (0-indexed: cline-2)
    c_line = lines[cline - 1]   # comment line (0-indexed: cline-1)
    
    # Extract 1977Da02 value from comment
    m = re.search(r'of (\d+\.?\d*(?:E\d+)? \{I\d+\}) \(1977Da02\)', c_line)
    if not m:
        print(f'ERROR line {cline}: cannot parse 1977Da02 value')
        print('  LINE:', repr(c_line))
        continue
    da_val = m.group(1)

    # Build old string (with exact trailing spaces)
    old = g_line + c_line
    if has_2cg:
        old += lines[cline]  # 0-indexed: cline is the 2cG line

    # Build new string
    new_comment = f' 34CL cG RI$other: {da_val} (1977Da02)\n'
    new = g_line + new_comment

    print(f'Case cline={cline}: {repr(da_val)} -> new={repr(new_comment.strip())}')
    # Check old uniqueness
    full_text = ''.join(lines)
    count = full_text.count(c_line.rstrip())
    if count != 1:
        print(f'  WARNING: comment line appears {count} times!')
