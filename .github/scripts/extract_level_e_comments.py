#!/usr/bin/env python3
"""Extract E$ weighted average comments for levels with ({+16}O,|ap|g) data"""

file = r'A35/Cl35/new/Cl35_adopted.ens'
with open(file, 'r', encoding='latin-1') as f:
    lines = f.readlines()

# Find L-records and their associated cL E$ comments
current_level = None
level_data = []

for i, line in enumerate(lines):
    # Check if it's an L-record
    if line[7:8] == 'L' and line[0:5].strip():
        # Store previous level if it had (+16O,|ap|g) data
        if current_level and '({+16}O,|ap|g)' in ''.join(current_level['comments']):
            level_data.append(current_level)
        
        # Start new level
        current_level = {
            'line_num': i+1,
            'l_record': line[:80],
            'energy': line[9:19].strip(),
            'unc': line[19:21].strip(),
            'comments': []
        }
    elif current_level and 'cL E$weighted average' in line:
        # This is an E$ weighted average comment for current level
        # Collect all continuation lines
        comment_lines = [line[:80]]
        j = i + 1
        while j < len(lines) and 'cL' in lines[j][5:8]:
            comment_lines.append(lines[j][:80])
            j += 1
        current_level['comments'] = comment_lines

# Don't forget the last level
if current_level and '({+16}O,|ap|g)' in ''.join(current_level['comments']):
    level_data.append(current_level)

print(f'Found {len(level_data)} levels with ({{+16}}O,|ap|g) data in E$ comments')
print('='*80)
for data in level_data:
    print(f'\nLevel at line {data["line_num"]}: E = {data["energy"]} ± {data["unc"]} keV')
    for comment in data['comments']:
        print(comment.rstrip())
