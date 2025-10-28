#!/usr/bin/env python3
"""
Spot-check: Verify that 10+ randomly selected new RI$ cG lines match the 2001VO24 RI values
"""

import re

# Parse 2001VO24.ens to get the 83 gammas with their RI values
with open('A35/Cl35/raw/2001VO24.ens') as f:
    vo24_lines = f.readlines()

# Extract all G-records from 2001VO24
ri_from_vo24 = []
for line in vo24_lines:
    if len(line) > 8 and line[7:8] == 'G':
        eg_str = line[9:19].strip()
        ri_str = line[22:29].strip()
        if ri_str and ri_str not in ['', 'B', 'V']:
            try:
                eg = float(eg_str)
                ri = int(ri_str.split()[0]) if ri_str[0].isdigit() else 0
                ri_from_vo24.append((eg, ri, line[:79]))
            except:
                pass

print(f"✓ Parsed {len(ri_from_vo24)} gammas from 2001VO24.ens with RI values")

# Parse Cl35_34s_p_g.ens
with open('A35/Cl35/new/Cl35_34s_p_g.ens') as f:
    cl35_lines = f.readlines()

# Find the 34 new cG RI$ lines (they were inserted after specific G-records)
# These lines contain " cG RI$" pattern
new_cg_ri_lines = []
for i, line in enumerate(cl35_lines):
    if len(line) > 8 and 'cG' in line[6:9] and 'RI$' in line[9:15]:
        # Extract the RI value
        ri_match = re.search(r'RI\$(\d+)', line)
        if ri_match:
            ri_val = int(ri_match.group(1))
            # Find the previous G-record (should be within 5 lines)
            for j in range(max(0, i-5), i):
                if len(cl35_lines[j]) > 8 and cl35_lines[j][7:8] == 'G':
                    eg_str = cl35_lines[j][9:19].strip()
                    try:
                        eg = float(eg_str)
                        new_cg_ri_lines.append((eg, ri_val, i+1, cl35_lines[j][:60]))
                    except:
                        pass
                    break

print(f"✓ Found {len(new_cg_ri_lines)} new cG RI$ lines in Cl35_34s_p_g.ens")

# Spot check: Verify 10 random samples
import random
if len(new_cg_ri_lines) > 10:
    samples = random.sample(new_cg_ri_lines, 10)
else:
    samples = new_cg_ri_lines

print(f"\nSpot Check (sample of {len(samples)}):")
matches = 0
mismatches = 0

for eg_cl35, ri_cl35, line_num, g_record in samples:
    # Find this gamma in 2001VO24 (within 1 keV tolerance)
    found = False
    for eg_vo24, ri_vo24, _ in ri_from_vo24:
        if abs(eg_cl35 - eg_vo24) < 1.0:  # 1 keV tolerance
            if ri_cl35 == ri_vo24:
                print(f"  ✓ Line {line_num}: Egamma {eg_cl35:.1f} RI${ri_cl35} matches 2001VO24")
                matches += 1
            else:
                print(f"  ❌ Line {line_num}: Egamma {eg_cl35:.1f} RI${ri_cl35} MISMATCH (expected RI${ri_vo24})")
                mismatches += 1
            found = True
            break
    if not found:
        print(f"  ⚠ Line {line_num}: Egamma {eg_cl35:.1f} not found in 2001VO24")

print(f"\nSpot Check Summary:")
print(f"  ✓ Matches: {matches}/{len(samples)}")
print(f"  ❌ Mismatches: {mismatches}/{len(samples)}")

if mismatches == 0:
    print(f"\n✅ SUCCESS: All sampled RI values match 2001VO24!")
else:
    print(f"\n⚠ WARNING: {mismatches} mismatches detected!")
