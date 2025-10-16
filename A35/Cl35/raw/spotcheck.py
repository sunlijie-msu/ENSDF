#!/usr/bin/env python3
"""Perform random spot-check validation of ENSDF data"""

import csv
import random

# Read CSV
with open('2001VO24.csv', 'r') as f:
    reader = csv.reader(f)
    rows = list(reader)

# Extract Exi values
exi_row = rows[2]
exi_values = []
exi_col_indices = []
for col_idx in range(2, len(exi_row)):
    val = exi_row[col_idx].strip()
    if val and val != 'Exi':
        exi_values.append(int(val))
        exi_col_indices.append(col_idx)

# Extract transitions
transitions = {}
for row_idx in range(3, len(rows)-1):
    row = rows[row_idx]
    exf_label = row[0].strip()
    exf_val = row[1].strip()
    
    if exf_label == 'Exf' and exf_val:
        exf = int(exf_val)
        for col_idx, exi in zip(exi_col_indices, exi_values):
            if col_idx < len(row):
                br_str = row[col_idx].strip()
                if br_str:
                    br = int(br_str)
                    if exi not in transitions:
                        transitions[exi] = {}
                    transitions[exi][exf] = br

# Read ENSDF file
with open('2001VO24.ens', 'r') as f:
    ens_lines = f.readlines()

# Select 6 random transitions for spot-check (~5% of 85)
all_transitions = []
for exi in transitions:
    for exf in transitions[exi]:
        all_transitions.append((exi, exf, transitions[exi][exf]))

random.seed(42)  # For reproducibility
samples = random.sample(all_transitions, min(6, len(all_transitions)))
samples.sort()

print("RANDOM SPOT-CHECK VALIDATION (5% sample = 6 entries)")
print("="*80)
print()

# Verify each sample
all_ok = True
for sample_idx, (exi, exf, br) in enumerate(samples, 1):
    egamma = exi - exf
    exi_mev = exi / 1000.0
    
    # Find in ENSDF file
    found_l = False
    found_g = False
    
    for i, line in enumerate(ens_lines):
        if len(line) >= 19:
            type_field = line[7:8]
            energy_field = line[9:19].strip()
            
            # Look for matching L-record
            if type_field == 'L' and energy_field:
                try:
                    file_energy = float(energy_field)
                    if abs(file_energy - exi_mev) < 0.001:
                        found_l = True
                        l_line = i + 1
                        
                        # Now look for corresponding G-records
                        for j in range(i+1, len(ens_lines)):
                            next_line = ens_lines[j]
                            if len(next_line) >= 19:
                                next_type = next_line[7:8]
                                
                                # Stop if we hit next L-record
                                if next_type == 'L':
                                    break
                                
                                # Check G-records
                                if next_type == 'G':
                                    g_energy_field = next_line[9:19].strip()
                                    ri_field = next_line[23:29].strip()
                                    
                                    if g_energy_field and ri_field:
                                        try:
                                            file_egamma = float(g_energy_field)
                                            file_ri = int(ri_field)
                                            
                                            if abs(file_egamma - egamma) < 0.001 and file_ri == br:
                                                found_g = True
                                                g_line = j + 1
                                        except:
                                            pass
                except:
                    pass
            
            if found_l and found_g:
                break
    
    # Report result
    print(f"Sample {sample_idx}:")
    print(f"  CSV Source: Exi={exi} keV, Exf={exf} keV, BR={br}")
    print(f"  Calculated: Egamma={egamma} keV, L record E={exi_mev} MeV")
    
    if found_l and found_g:
        print(f"  ✓ FOUND in file: L-record at line {l_line}, G-record at line {g_line}")
        print(f"    File values: L {exi_mev}, G {egamma} RI {br}")
    else:
        print(f"  ✗ NOT FOUND in file")
        all_ok = False
    print()

print("="*80)
if all_ok:
    print("✓ SPOT-CHECK PASSED: All 6 random samples verified successfully!")
else:
    print("✗ SPOT-CHECK FAILED: Some samples not found or incorrect")
