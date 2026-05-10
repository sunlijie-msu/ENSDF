#!/usr/bin/env python3
# Read and inspect the ENSDF file structure 
with open('XUNDL/2026BAAA_CR11022_209Po.ens', 'r') as f:
    lines = f.readlines()

# Find PN line
pn_idx = None
for i, line in enumerate(lines):
    if ' PN' in line or 'PN' in line:
        pn_idx = i
        break

print(f"PN line at index {pn_idx} (line {pn_idx + 1})")
print("\nLines around first G-record (with column ruler):")
print("Col:  123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890")

# Show lines from PN to first several G-records
for i in range(pn_idx, min(pn_idx + 20, len(lines))):
    line = lines[i]
    print(f"Line {i+1:3d}: {line.rstrip()[:90]}")
    if i > pn_idx and i < pn_idx + 15:
        rec_type = line[7] if len(line) > 7 else '?'
        if rec_type == 'L':
            print(f"         ➜ L-RECORD: E({line[9:19]}), DE({line[19:21]}), Jpi({line[22:39]})")
        elif rec_type == 'G':
            print(f"         ➜ G-RECORD: E({line[9:19]}), DE({line[19:21]}), RI({line[22:29]}), DRI({line[29:31]}), M({line[32:41]})")
        elif rec_type == 'c':
            print(f"         ➜ COMMENT: {line[6:10]}{line[9:50]}")
