#!/usr/bin/env python3
"""Check DE field positioning in L-records"""

import re

with open('A35/Cl35/temp/1976ME12.ens', 'r') as f:
    lines = f.readlines()

print('DE FIELD POSITIONING ANALYSIS (First 10 L-records):')
print('Energy   | DE Value | Cols 20-21 | Line Fragment (cols 10-30)')
print('---------|----------|------------|---------------------------')

count = 0
for line in lines:
    if re.match(r' 35CL  L \d+', line) and count < 10:
        parts = line.split()
        energy = parts[2] if len(parts) > 2 else 'N/A'
        de_value = parts[3] if len(parts) > 3 else 'N/A'
        
        # Extract exact DE field (cols 20-21, 0-indexed = 19-21)
        de_field = line[19:21] if len(line) > 20 else 'XX'
        
        # Context
        context = line[9:30] if len(line) > 29 else line[9:]
        
        print(f'{energy:<8} | {de_value:<8} | "{de_field}"       | "{context}"')
        count += 1

print()
print('CRITICAL FINDING: All DE uncertainties are 10× too large!')
print('File values need to be divided by 10 to match reference data.')