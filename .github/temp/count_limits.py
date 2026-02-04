#!/usr/bin/env python3
import re

filename = r'A35/Cl35/new/Cl35_adopted.ens'

with open(filename, 'r') as f:
    lines = f.readlines()

limits_count = 0
exact_count = 0

for i, line in enumerate(lines, 1):
    if 'T$lifetime' in line:
        if '|t<' in line or '|t>' in line:
            limits_count += 1
            print(f'Line {i}: {line.rstrip()[:75]}')
        else:
            exact_count += 1

print(f'\nTotal T$ comments: {limits_count + exact_count}')
print(f'  With exact lifetime: {exact_count}')
print(f'  With limits (<, >): {limits_count}')
