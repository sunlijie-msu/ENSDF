#!/usr/bin/env python3
import re

filename = r'A35/Cl35/new/Cl35_adopted.ens'

with open(filename, 'r') as f:
    lines = f.readlines()

count = 0
for i, line in enumerate(lines, 1):
    if 'T$lifetime' in line:
        count += 1
        print(f'Line {i}: {line.rstrip()[:80]}')

print(f'\nTotal T$ lifetime comments: {count}')
