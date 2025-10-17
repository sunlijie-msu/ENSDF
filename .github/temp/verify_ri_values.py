#!/usr/bin/env python3
"""
Verify RI values in Cl35_34s_p_g.ens cG comments against 2001VO24.ens
Check for mismatches and report needed corrections
"""

import re
from collections import defaultdict

print("=" * 80)
print("STEP 1: Build complete mapping from 2001VO24.ens")
print("=" * 80)

# Parse 2001VO24.ens: Exi -> [(Eg, RI)]
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
                    ri = int(ri_field) if ri_field.isdigit() else ri_field
                    exi_to_gammas_2001[current_exi].append((eg, ri))
            except:
                pass

print(f"Parsed {len(exi_to_gammas_2001)} levels with {sum(len(g) for g in exi_to_gammas_2001.values())} gammas from 2001VO24.ens")

print("\n" + "=" * 80)
print("STEP 2: Read Cl35_34s_p_g.ens and extract cG RI comments")
print("=" * 80)

with open('A35/Cl35/new/Cl35_34s_p_g.ens', 'r') as f:
    lines = f.readlines()

# Find all G-records and their following cG RI$ comments
g_records_with_comments = []  # [(g_line_idx, eg, cg_line_idx, cg_text, exi_context)]

current_level_exi = None
for i, line in enumerate(lines):
    if len(line) > 8:
        record_type = line[7:8] if len(line) > 7 else ''
        
        # Track current level
        if record_type == 'L':
            try:
                e_field = line[9:19].strip()
                if e_field:
                    current_level_exi = float(e_field)
            except:
                pass
        
        # Process G-records
        elif record_type == 'G' and current_level_exi is not None:
            try:
                eg_field = line[9:19].strip()
                if eg_field:
                    eg = float(eg_field)
                    
                    # Check if next line is cG RI$ comment
                    cg_line_idx = i + 1
                    cg_text = None
                    if cg_line_idx < len(lines):
                        cg_line = lines[cg_line_idx]
                        if 'cG' in cg_line and 'RI$' in cg_line:
                            cg_text = cg_line.rstrip('\n')
                    
                    g_records_with_comments.append((i, eg, cg_line_idx, cg_text, current_level_exi))
            except:
                pass

print(f"Found {len(g_records_with_comments)} G-records")
g_with_ri = sum(1 for _, _, _, cg, _ in g_records_with_comments if cg is not None)
print(f"  {g_with_ri} have cG RI$ comments")
print(f"  {len(g_records_with_comments) - g_with_ri} are missing cG RI$ comments")

print("\n" + "=" * 80)
print("STEP 3: Verify RI values match")
print("=" * 80)

mismatches = []
missing_ri = []
correct_ri = []

for g_line_idx, eg_cl35, cg_line_idx, cg_text, exi_cl35 in g_records_with_comments:
    # Find best matching Exi in 2001
    best_exi_match = None
    best_exi_dist = float('inf')
    for exi_2001 in exi_to_gammas_2001.keys():
        dist = abs(exi_2001 - exi_cl35)
        if dist < best_exi_dist and dist < 2:
            best_exi_dist = dist
            best_exi_match = exi_2001
    
    if best_exi_match is None:
        # Can't find matching level
        if cg_text:
            print(f"Line {g_line_idx}: G {eg_cl35:7.1f} @ Exi {exi_cl35:7.1f} - NO MATCHING Exi IN 2001VO24")
        continue
    
    # Find best matching Eg in 2001
    gammas_2001 = exi_to_gammas_2001[best_exi_match]
    best_eg_match = None
    best_eg_dist = float('inf')
    best_ri_2001 = None
    
    for eg_2001, ri_2001 in gammas_2001:
        dist = abs(eg_2001 - eg_cl35)
        if dist < best_eg_dist and dist < 1:
            best_eg_dist = dist
            best_eg_match = eg_2001
            best_ri_2001 = ri_2001
    
    if best_eg_match is None:
        # No matching gamma
        if cg_text:
            print(f"Line {g_line_idx}: G {eg_cl35:7.1f} - NO MATCHING GAMMA IN 2001VO24 (closest Exi was {best_exi_match})")
        else:
            missing_ri.append((g_line_idx, eg_cl35, cg_line_idx, exi_cl35, None, None))
        continue
    
    # Check RI value in cG comment
    if cg_text is None:
        # Missing cG RI comment
        missing_ri.append((g_line_idx, eg_cl35, cg_line_idx, exi_cl35, best_eg_match, best_ri_2001))
        print(f"Line {g_line_idx}: G {eg_cl35:7.1f} - MISSING cG RI comment (should be RI${best_ri_2001} from 2001VO24)")
    else:
        # Extract RI value from cG comment
        # Format: " 35CL cG RI$from 1976Me12. Other: X from 2001Vo24."
        ri_match = re.search(r'Other:\s*(\d+)', cg_text)
        if ri_match:
            ri_in_comment = int(ri_match.group(1))
            if ri_in_comment == best_ri_2001:
                correct_ri.append((g_line_idx, eg_cl35, cg_line_idx, best_ri_2001))
                # print(f"Line {g_line_idx}: G {eg_cl35:7.1f} - ✓ Correct RI={best_ri_2001}")
            else:
                mismatches.append((g_line_idx, eg_cl35, cg_line_idx, cg_text, ri_in_comment, best_ri_2001))
                print(f"Line {g_line_idx}: G {eg_cl35:7.1f} - ❌ MISMATCH! cG has RI={ri_in_comment} but 2001VO24 has RI={best_ri_2001}")
        else:
            print(f"Line {g_line_idx}: G {eg_cl35:7.1f} - CANNOT PARSE RI from cG: {cg_text}")

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"✓ Correct RI values: {len(correct_ri)}")
print(f"❌ Mismatched RI values: {len(mismatches)}")
print(f"⚠ Missing RI values: {len(missing_ri)}")

if mismatches:
    print("\nMismatched RI values (need fixing):")
    for g_line_idx, eg, cg_line_idx, cg_text, ri_wrong, ri_correct in mismatches:
        print(f"  Line {g_line_idx}: G {eg:7.1f} - has {ri_wrong}, should be {ri_correct}")

if missing_ri:
    print(f"\nMissing RI values (need adding): {len(missing_ri)} gammas")
    # Show first 5
    for i, (g_line_idx, eg, cg_line_idx, exi, eg_2001, ri_2001) in enumerate(missing_ri[:5]):
        if ri_2001 is not None:
            print(f"  Line {g_line_idx}: G {eg:7.1f} - add RI${ri_2001} from 2001VO24")
        else:
            print(f"  Line {g_line_idx}: G {eg:7.1f} - NO 2001VO24 counterpart")
    if len(missing_ri) > 5:
        print(f"  ... and {len(missing_ri) - 5} more")
