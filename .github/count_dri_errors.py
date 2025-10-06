#!/usr/bin/env python3
"""Count DRI field formatting errors"""

with open('A35/Cl35/new/Cl35_34s_p_g.ens', 'r') as f:
    lines = f.readlines()

dri_errors = []
for i, line in enumerate(lines, 1):
    line_stripped = line.rstrip('\n\r')
    
    # Only G-records
    if len(line_stripped) < 31:
        continue
    if not (line_stripped[7] == 'G' and line_stripped[5] == ' ' and line_stripped[6] == ' '):
        continue
    
    # Check DRI field (cols 30-31, 0-based 29:31)
    dri_field = line_stripped[29:31]
    
    # DRI has content but starts with space = not LEFT-JUSTIFIED
    if dri_field.strip() and dri_field[0] == ' ':
        dri_errors.append((i, line_stripped, dri_field))

print(f'Total DRI field errors: {len(dri_errors)}')
print(f'\nFirst 20 examples:')
for line_num, line_content, dri_value in dri_errors[:20]:
    col32 = line_content[31] if len(line_content) > 31 else '?'
    print(f'  Line {line_num}: DRI=[{dri_value}], col32=[{col32}]')
