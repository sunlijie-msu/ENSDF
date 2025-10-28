#!/usr/bin/env python3
"""
Scan for G-records where multipolarity (M field) does NOT start at column 33.

ENSDF G-Record Format:
  Column 32: SPACE (separator after DRI)
  Columns 33-41: M field (multipolarity) - must be LEFT-JUSTIFIED at column 33
"""

input_file = r"d:\X\ND\ENSDF\A35\Cl35\new\Cl35_34s_p_g.ens"

with open(input_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

issues = []

for i, line in enumerate(lines):
    if not line.startswith(' 35CL  G '):
        continue
    
    if len(line) < 42:
        continue
    
    # Column 32 (index 31) - should be space
    # Column 33 (index 32) - multipolarity should start here
    col32 = line[31] if len(line) > 31 else ' '
    col33 = line[32] if len(line) > 32 else ' '
    m_field = line[32:41] if len(line) > 41 else ''
    
    # If M field has content and col33 is NOT space (meaning M starts before col 33)
    if m_field.strip() and col32 != ' ':
        issues.append((i+1, line, col32, m_field))

print(f"Total G-records with M field NOT starting at column 33: {len(issues)}")
print()

if issues:
    print(f"Showing first 10 of {len(issues)} issues:")
    for line_num, line, col32, m_field in issues[:10]:
        print(f"Line {line_num:4d}: col32={repr(col32)} | M field (33-41)=[{m_field}]")
        print(f"             {line.rstrip()}")
        print()
else:
    print("All M fields correctly positioned at column 33!")
