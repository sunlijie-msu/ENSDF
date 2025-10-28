#!/usr/bin/env python3
"""
Systematic identification of missing RI values to add to Cl35_34s_p_g.ens
Based on 2001VO24.ens data
"""

import re
from collections import defaultdict

# Parse 2001VO24 data
exi_to_gammas_2001 = defaultdict(list)
current_exi = None

with open('A35/Cl35/raw/2001VO24.ens', 'r') as f:
    for line in f:
        if len(line) < 9:
            continue
        record_type = line[7:8] if len(line) > 7 else ''
        
        if record_type == 'L':
            try:
                e_field = line[9:19].strip()
                if e_field:
                    current_exi = float(e_field)
            except:
                pass
        elif record_type == 'G' and current_exi is not None:
            try:
                eg_field = line[9:19].strip()
                ri_field = line[22:29].strip()
                if eg_field and ri_field:
                    eg = float(eg_field)
                    ri = int(ri_field)
                    exi_to_gammas_2001[current_exi].append((eg, ri))
            except:
                pass

print("=" * 80)
print("2001VO24 DATA (for reference)")
print("=" * 80)
for exi in sorted(exi_to_gammas_2001.keys()):
    gammas = exi_to_gammas_2001[exi]
    print(f"\nExi {exi}: {len(gammas)} gammas")
    for eg, ri in sorted(gammas):
        print(f"  G {eg:7.1f} RI={ri}")

# Now read Cl35 file and identify levels
level_matches = [
    (7178.6, 7179.0),   # Exi 7179 → Cl35 7178.6
    (7548.9, 7547.0),   # Exi 7547 → Cl35 7548.9
    (7837.2, 7838.0),   # Exi 7838 → Cl35 7837.2
    (8208.2, 8207.0),   # Exi 8207 → Cl35 8208.2
    (8216.3, 8216.0),   # Exi 8216 → Cl35 8216.3
    (8381.8, 8381.0),   # Exi 8381 → Cl35 8381.8
    (8484.4, 8484.0),   # Exi 8484 → Cl35 8484.4
    (8893.3, 8893.0),   # Exi 8893 → Cl35 8893.3
    (8906.8, 8907.0),   # Exi 8907 → Cl35 8906.8
    (9081.4, 9081.0),   # Exi 9081 → Cl35 9081.4
]

with open('A35/Cl35/new/Cl35_34s_p_g.ens', 'r') as f:
    lines = f.readlines()

print("\n" + "=" * 80)
print("GAMMAS IN CL35 NEEDING RI VALUES FROM 2001VO24")
print("=" * 80)

additions_needed = []

for cl_exi, vo24_exi in level_matches:
    if vo24_exi not in exi_to_gammas_2001:
        print(f"\nExi {vo24_exi} NOT in 2001VO24")
        continue
    
    gammas_2001 = exi_to_gammas_2001[vo24_exi]
    
    # Find Cl35 L-record
    l_line_num = None
    for i, line in enumerate(lines):
        if len(line) > 8 and line[7:8] == 'L':
            try:
                e_str = line[9:19].strip()
                if e_str and abs(float(e_str) - cl_exi) < 0.5:
                    l_line_num = i
                    break
            except:
                pass
    
    if l_line_num is None:
        print(f"\nCL35 Exi {cl_exi} NOT FOUND")
        continue
    
    print(f"\nExi {vo24_exi} (CL35 Exi {cl_exi} @ line {l_line_num+1}):")
    
    # Scan G-records following this L-record until next L
    i = l_line_num + 1
    gamma_count = 0
    missing_count = 0
    while i < len(lines):
        line = lines[i]
        if len(line) >= 9:
            # Col 6=continuation, Col 7 = 'c' for comment or space, Col 8 = record type
            # Format: "NUCID CONT TYPE" where CONT is char 6, TYPE is char 7-8
            cont = line[5:6] if len(line) > 5 else ' '
            c_flag = line[6:7] if len(line) > 6 else ' '
            rec_type = line[7:8] if len(line) > 7 else ' '
            
            # Stop at next L-record (column 7-8 = 'L')
            if rec_type == 'L' and c_flag != 'c':
                break
            
            # Process G-records (column 7-8 = 'G' and not a comment line)
            if rec_type == 'G' and c_flag != 'c':
                gamma_count += 1
                try:
                    eg_str = line[9:19].strip()
                    if eg_str:
                        eg_cl35 = float(eg_str)
                        
                        # Find matching gamma in 2001
                        best_match = None
                        best_dist = float('inf')
                        for eg_2001, ri_2001 in gammas_2001:
                            dist = abs(eg_2001 - eg_cl35)
                            if dist < best_dist and dist < 1:
                                best_dist = dist
                                best_match = (eg_2001, ri_2001)
                        
                        # Check if next line is cG RI$
                        has_ri = False
                        if i + 1 < len(lines):
                            cg_line = lines[i+1]
                            if 'cG' in cg_line and 'RI$' in cg_line:
                                if '2001Vo24' in cg_line or '2001VO24' in cg_line:
                                    has_ri = True
                        
                        if best_match and not has_ri:
                            eg_2001, ri_2001 = best_match
                            print(f"  Line {i+1}: G {eg_cl35:7.1f} → needs RI${ri_2001} from 2001VO24")
                            missing_count += 1
                            additions_needed.append((i, eg_cl35, ri_2001))
                except:
                    pass
        i += 1
    
    print(f"  Total gammas: {gamma_count}, Missing RI: {missing_count}")

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"Total gammas needing RI additions: {len(additions_needed)}")
for i, (line_num, eg, ri) in enumerate(additions_needed[:10]):
    print(f"  {i+1}. Line {line_num+1}: G {eg:7.1f} → add RI${ri}")
if len(additions_needed) > 10:
    print(f"  ... and {len(additions_needed)-10} more")
