#!/usr/bin/env python3
"""Temporary script to analyze problematic G-record lines - reads from actual file"""

# Read actual lines from file
with open('A35/Cl35/new/Cl35_34s_p_g.ens', 'r') as f:
    all_lines = f.readlines()

# Extract lines 322-325 (user's examples, 0-based index 321-324)
lines = [
    all_lines[321].rstrip('\n\r'),
    all_lines[322].rstrip('\n\r'),
    all_lines[323].rstrip('\n\r'),
    all_lines[324].rstrip('\n\r')
]

print('EXACT FIELD ANALYSIS OF ACTUAL FILE LINES 322-325:')
print('=' * 80)

for idx, line in enumerate(lines, 322):
    energy = line[9:19].strip()
    de_field = line[19:21]
    col22 = line[21] if len(line) > 21 else '?'
    ri_field = line[22:29] if len(line) > 22 else '?'
    dri_field = line[29:31] if len(line) > 29 else '?'
    col32 = line[31] if len(line) > 31 else '?'
    m_field = line[32:41] if len(line) > 32 else '?'
    
    print(f'\nLine {idx}: Energy {energy}')
    print(f'  Cols 20-21 (DE):    [{de_field}]')
    print(f'  Col 22 (SPACE):     [{col22}] = {repr(col22)}')
    print(f'  Cols 23-29 (RI):    [{ri_field}]')
    print(f'  Cols 30-31 (DRI):   [{dri_field}]')
    print(f'  Col 32 (SPACE):     [{col32}] = {repr(col32)}')
    print(f'  Cols 33-41 (M):     [{m_field}]')
    
    # Analysis
    errors = []
    if col22 != ' ':
        errors.append(f'Col 22 is {repr(col22)} instead of SPACE')
    if ri_field.strip() and ri_field[0] == ' ':
        errors.append('RI field not LEFT-JUSTIFIED (starts with space)')
    if dri_field.strip() and dri_field[0] == ' ':
        errors.append(f'DRI field has leading space: [{dri_field}]')
    if col32 != ' ' and col32 != '?':
        errors.append(f'Col 32 is {repr(col32)} instead of SPACE')
    if m_field != '?' and m_field.strip() and m_field[0] == ' ':
        errors.append(f'M field not LEFT-JUSTIFIED at col 33: [{m_field}]')
    
    if errors:
        print('  ERRORS:')
        for err in errors:
            print(f'    - {err}')
    else:
        print('  OK!')
