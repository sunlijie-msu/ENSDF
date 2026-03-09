#!/usr/bin/env python3
"""
Manually verify all ~23 'Other:' values in adp against mrg source data.
Direct approach: for each cG line with 'Other:', extract the quoted value
and check if the mrg file actually has that value for the stated dataset.
"""

import re

ADP_FILE = r'A34\Cl34\raw\1977DA02_1983WA27.adp'
MRG_FILE = r'A34\Cl34\raw\1977DA02_1983WA27.mrg'

# Read adp file
with open(ADP_FILE, 'r') as f:
    adp_lines = f.readlines()

# Find all cG lines with 'Other:' 
other_lines = []
for i, line in enumerate(adp_lines):
    if 'cG RI$' in line and 'Other:' in line:
        other_lines.append((i+1, line.rstrip()))

print(f'Found {len(other_lines)} "Other:" lines in adp\n')

# For each Other: line, manually construct what we're looking for
# Example: ' 34CL cG RI$from 1983Wa27. Other: 100 (1977Da02).'
#   => This gamma's RI is from 1983Wa27 (dataset B)
#   => Other dataset (1977Da02 = dataset A) has RI value 100

for line_no, line_text in other_lines:
    print(f'L{line_no}: {line_text[:100]}')
    
    # Extract the quoted value and the stated dataset
    # Pattern: 'Other: VALUE {I...} (DATASET).' or just 'Other: VALUE (DATASET).'
    match = re.search(r'Other:\s*([\d<>\.]+)(?:\s*\{I[^}]*\})?\s*\((\d{4}[A-Z]{2}\d{2})\)', line_text)
    if not match:
        print(f'  ❌ Could not parse Other: format')
        continue
    
    quoted_value = match.group(1)
    quoted_dataset = match.group(2)
    
    # Extract which dataset this gamma is from (the 'from' part)
    from_match = re.search(r'from\s+(\d{4}[A-Z]{2}\d{2})', line_text)
    if not from_match:
        print(f'  ❌ Could not parse "from" dataset')
        continue
    
    from_dataset = from_match.group(1)
    
    print(f'  From: {from_dataset}, Other: {quoted_value} ({quoted_dataset})')
    
    # Now look at the preceding G record to get the gamma energy
    g_line = None
    for j in range(line_no-2, max(0, line_no-10), -1):  # Look back a few lines
        if adp_lines[j].strip().startswith('34CL  G'):
            g_line = adp_lines[j].rstrip()
            break
    
    if g_line:
        # Extract G energy
        g_energy_str = g_line[10:20].strip()
        print(f'  G energy in adp: {g_energy_str}')
    else:
        print(f'  ⚠️  Could not find preceding G record')
    
    print()

print('\nNOTE: Full verification requires mrg file matching - this shows what we\'re looking for.')
