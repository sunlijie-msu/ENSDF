#!/usr/bin/env python3
"""
Add missing RI$ cG comments to 58 gammas in Cl35_34s_p_g.ens
Based on verification output showing which gammas need RI values
"""

import re

# Mapping of (line_number) -> RI value to add
# From verification output, format: Line XXXX: G YYYY.Y - MISSING cG RI comment (should be RI$Z from 2001VO24)
missing_ri_additions = {
    # Exi 7838 (9 missing)
    1512: ('G  2239.2', 1),
    1514: ('G  3660.9', 28),
    1515: ('G  3665.3', 3),
    1516: ('G  3779.6', 2),
    1517: ('G  3895.9', 1),
    1519: ('G  4835.9', 4),
    1520: ('G  6075.4', 2),
    1521: ('G  6618.9', 37),
    1522: ('G  7838.1', 21),
    
    # Exi 8207 (2 missing)
    2041: ('G  3446.3', 1),  # Wait, needs check - line offset
    
    # Exi 8381 (11 missing)
    2228: ('G  3611.7', 1),
    2329: ('G  3603.2', 7),
    2330: ('G  3859.8', 1),
    2331: ('G  4516.8', 1),
    2332: ('G  4565.6', 5),
    2333: ('G  5481.2', 7),
    2334: ('G  5790.0', 20),
    2335: ('G  5838.2', 3),
    2336: ('G  6720.7', 46),
    2337: ('G  8483.3', 4),
    
    # Exi 8484 (10 missing)
    2329: ('G  3603.2', 7),
    2330: ('G  3859.8', 1),
    2331: ('G  4516.8', 1),
    2332: ('G  4565.6', 5),
    2333: ('G  5481.2', 7),
    2334: ('G  5790.0', 20),
    2335: ('G  5838.2', 3),
    2336: ('G  6720.7', 46),
    2337: ('G  8483.3', 4),
    
    # Exi 8893 (7 missing)
    2652: ('G  3293.4', 1),
    2654: ('G  4779.3', 9),
    2655: ('G  4950.0', 4),
    2656: ('G  5729.8', 29),
    2657: ('G  6198.8', 37),
    2658: ('G  7129.5', 19),
    2659: ('G  8892.1', 1),
    
    # Exi 8907 (6 missing)
    2679: ('G  3261.0', 2),
    2681: ('G  3321.0', 4),
    2684: ('G  4136.7', 6),
    2685: ('G  4963.5', 15),
    
    # Exi 9081 (10 missing)
    2756: ('G  3357.7', 1),
    2757: ('G  4200.2', 1),
    2761: ('G  4903.1', 2),
    2762: ('G  4907.6', 2),
    2763: ('G  5162.5', 9),
    2766: ('G  5917.9', 6),
    2767: ('G  6386.9', 2),
    2768: ('G  6435.1', 1),
    2769: ('G  7317.6', 16),
    2772: ('G  9080.1', 60),
}

print("This script would systematically add missing RI values")
print(f"Total entries to process: {len(missing_ri_additions)}")

# Read current file
with open('A35/Cl35/new/Cl35_34s_p_g.ens', 'r') as f:
    lines = f.readlines()

# For each missing RI, insert a cG line after the G-record
# This is complex because we need to:
# 1. Find the G-record at the expected line
# 2. Check if it already has a cG comment
# 3. If not, insert one
# 4. If yes, update it

print("\nSample validation (first 5 entries):")
for i, (line_num, (g_record, ri_value)) in enumerate(list(missing_ri_additions.items())[:5]):
    if line_num < len(lines):
        actual_line = lines[line_num].rstrip('\n')
        g_match = g_record.split()[1]
        if g_match in actual_line:
            print(f"  Line {line_num}: ✓ Found {g_record} → needs RI${ri_value}")
        else:
            print(f"  Line {line_num}: ✗ Expected {g_record} but found {actual_line[:40]}")

print("\nWARNING: This is a complex operation with many entries.")
print("Recommend using incremental approach: add one level at a time with verification.")
