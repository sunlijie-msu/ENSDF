#!/usr/bin/env python3
"""
Simple debug: Count G and L records in ENS file
"""

ens_path = "A35/Cl35/raw/2001VO24.ens"

l_count = 0
g_count = 0

with open(ens_path, 'r') as f:
    for line_num, line in enumerate(f, 1):
        if len(line) < 10:
            continue
        
        if line[7:8] == 'L':
            l_count += 1
            print(f"Line {line_num}: L-record, energy = {line[9:19].strip()}")
        elif line[7:8] == 'G':
            g_count += 1
            print(f"Line {line_num}: G-record, Egamma = {line[9:19].strip()}, RI = {line[22:29].strip()}")

print()
print(f"Total L-records: {l_count}")
print(f"Total G-records: {g_count}")
