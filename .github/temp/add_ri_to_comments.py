#!/usr/bin/env python3
"""
Add RI (relative intensity) values from 2001VO24.ens to cG comments in Cl35_34s_p_g.ens
Matching gammas by energy with tolerance of 1 keV
"""

import re
from collections import defaultdict

# Step 1: Parse 2001VO24.ens to build Exi -> [(Eg, RI)] mapping
print("=" * 70)
print("PARSING 2001VO24.ens")
print("=" * 70)

exi_to_gammas_2001 = defaultdict(list)
current_exi = None

with open('A35/Cl35/raw/2001VO24.ens', 'r') as f:
    for line in f:
        if len(line) < 9:
            continue
        
        # ENSDF format: NUCID(1-5), CONT(6), space(7), TYPE(8)
        record_type = line[7:8] if len(line) > 7 else ''
        
        # Check for L-record
        if record_type == 'L':
            try:
                e_field = line[9:19].strip()
                if e_field:
                    current_exi = float(e_field)
                    print(f"Found Exi = {current_exi} keV")
            except:
                pass
        
        # Check for G-record
        elif record_type == 'G' and current_exi is not None:
            try:
                eg_field = line[9:19].strip()
                ri_field = line[22:29].strip()
                if eg_field and ri_field:
                    eg = float(eg_field)
                    ri = int(ri_field) if ri_field.isdigit() else ri_field
                    exi_to_gammas_2001[current_exi].append((eg, ri))
                    print(f"  G {eg:7.1f} keV, RI = {ri}")
            except Exception as e:
                pass

# Step 2: Read Cl35_34s_p_g.ens and find corresponding levels
print("\n" + "=" * 70)
print("ANALYZING Cl35_34s_p_g.ens")
print("=" * 70)

with open('A35/Cl35/new/Cl35_34s_p_g.ens', 'r') as f:
    lines = f.readlines()

# Find all L-records in Cl35_34s_p_g.ens
cl35_levels = []
for i, line in enumerate(lines):
    if len(line) > 8 and line[0:6] == ' 35CL ' and line[7:8] == 'L':
        try:
            e_field = line[9:19].strip()
            if e_field:
                exi_cl35 = float(e_field)
                cl35_levels.append((exi_cl35, i))
        except:
            pass

print(f"Found {len(cl35_levels)} L-records in Cl35_34s_p_g.ens")

# Step 3: Build matching: For each Exi in 2001, find closest in Cl35
print("\n" + "=" * 70)
print("MATCHING LEVELS")
print("=" * 70)

matched_levels = []
for exi_2001 in sorted(exi_to_gammas_2001.keys()):
    # Find closest Exi in Cl35
    best_match = None
    best_distance = float('inf')
    
    for exi_cl35, line_idx in cl35_levels:
        distance = abs(exi_2001 - exi_cl35)
        if distance < best_distance and distance < 2:  # 2 keV tolerance
            best_distance = distance
            best_match = (exi_cl35, line_idx)
    
    if best_match:
        print(f"2001VO24: Exi {exi_2001:7.1f} → Cl35: Exi {best_match[0]:7.1f} (Δ={best_distance:.1f} keV) @ line {best_match[1]}")
        matched_levels.append((exi_2001, best_match, exi_to_gammas_2001[exi_2001]))
    else:
        print(f"2001VO24: Exi {exi_2001:7.1f} → NO MATCH FOUND")

# Step 4: For each matched level, build gamma matching table
print("\n" + "=" * 70)
print("BUILDING GAMMA MATCHING TABLE")
print("=" * 70)

updates_needed = defaultdict(list)  # line_num -> [(eg_cl35, ri_from_2001)]

for exi_2001, (exi_cl35, level_line_idx), gammas_2001 in matched_levels:
    print(f"\nMatching gammas for Exi {exi_2001:7.1f} (Cl35 line {level_line_idx}):")
    
    # Collect all G-records following this L-record
    g_records = []
    i = level_line_idx + 1
    while i < len(lines):
        line = lines[i]
        # Stop if we hit next L-record
        if len(line) > 8 and line[0:6] == ' 35CL ' and line[7:8] == 'L':
            break
        # Collect G-records
        if len(line) > 8 and line[0:6] == ' 35CL ' and line[7:8] == 'G':
            try:
                eg_field = line[9:19].strip()
                if eg_field:
                    eg = float(eg_field)
                    g_records.append((eg, i))
            except:
                pass
        i += 1
    
    # Match gammas from 2001 to Cl35
    for eg_2001, ri_2001 in gammas_2001:
        best_match = None
        best_distance = float('inf')
        
        for eg_cl35, g_line_idx in g_records:
            distance = abs(eg_2001 - eg_cl35)
            if distance < best_distance and distance < 1:  # 1 keV tolerance for gammas
                best_distance = distance
                best_match = (eg_cl35, g_line_idx)
        
        if best_match:
            eg_cl35, g_line_idx = best_match
            print(f"  2001: G {eg_2001:7.1f} RI={ri_2001} → Cl35: G {eg_cl35:7.1f} (Δ={best_distance:.1f} keV) @ line {g_line_idx}")
            updates_needed[g_line_idx].append((eg_cl35, ri_2001))
        else:
            print(f"  2001: G {eg_2001:7.1f} RI={ri_2001} → NO MATCH FOUND")

# Step 5: Apply updates
print("\n" + "=" * 70)
print("APPLYING UPDATES TO CG COMMENTS")
print("=" * 70)

updates_applied = 0
for g_line_idx in sorted(updates_needed.keys()):
    matches = updates_needed[g_line_idx]
    if not matches:
        continue
    
    eg_cl35, ri_2001 = matches[0]  # Use first match
    
    # Check if cG RI comment already exists
    cg_line_idx = g_line_idx + 1
    if cg_line_idx < len(lines) and lines[cg_line_idx].strip().startswith(' 35CL cG RI$'):
        # Already has RI comment - check if it needs revision
        current_ri = lines[cg_line_idx]
        print(f"Line {g_line_idx}: G {eg_cl35:7.1f} - EXISTING cG RI: {current_ri.strip()}")
    else:
        # Need to add cG RI comment
        print(f"Line {g_line_idx}: G {eg_cl35:7.1f} - ADD cG RI${ri_2001} from 2001VO24")
        updates_applied += 1

print(f"\nTotal updates needed: {updates_applied}")

# Summary
print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print(f"Matched levels: {len(matched_levels)} / {len(exi_to_gammas_2001)}")
print(f"G-records ready for update: {len(updates_needed)}")
print(f"Estimated cG comments to add/revise: {updates_applied}")
