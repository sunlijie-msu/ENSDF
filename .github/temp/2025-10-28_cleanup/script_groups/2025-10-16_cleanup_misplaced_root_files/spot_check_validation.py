#!/usr/bin/env python3
"""
Random spot-check validation of 2001VO24.ens against CSV source data
"""

import csv
import random

# Read CSV and build transition map
csv_path = "A35/Cl35/raw/2001VO24.csv"
data = []
with open(csv_path, 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        data.append(row)

# Parse Exi values from row 2
exi_values = []
for col in range(2, len(data[2])):
    val = data[2][col].strip()
    if val:
        try:
            exi_values.append((col, float(val)))
        except ValueError:
            pass

# Extract all transitions from CSV
csv_transitions = {}  # {Exi: {Exf: RI}}
for row_idx in range(3, len(data)):
    row = data[row_idx]
    exf_str = row[1].strip()
    if not exf_str:
        continue
    try:
        exf = float(exf_str)
    except ValueError:
        continue
    
    for col, exi in exi_values:
        if col < len(row):
            ri_str = row[col].strip()
            if ri_str and ri_str != "0":
                try:
                    ri = float(ri_str)
                    if exi not in csv_transitions:
                        csv_transitions[exi] = {}
                    csv_transitions[exi][exf] = ri
                except ValueError:
                    pass

# Read ENS file and extract transitions
ens_path = "A35/Cl35/raw/2001VO24.ens"
ens_transitions = {}  # {Exi: {Egamma: RI}}
current_level = None

with open(ens_path, 'r') as f:
    for line in f:
        if len(line) < 20:
            continue
        record_type = line[7:8].strip()
        
        if record_type == 'L':
            energy_str = line[9:19].strip()
            try:
                current_level = float(energy_str)
                if current_level not in ens_transitions:
                    ens_transitions[current_level] = {}
            except ValueError:
                pass
        
        elif record_type == 'G' and current_level:
            energy_str = line[9:19].strip()
            ri_str = line[22:29].strip()
            try:
                egamma = float(energy_str)
                ri = float(ri_str)
                if current_level not in ens_transitions:
                    ens_transitions[current_level] = {}
                ens_transitions[current_level][egamma] = ri
            except ValueError:
                pass

print("=" * 100)
print("RANDOM SPOT-CHECK VALIDATION: 2001VO24.ens vs CSV")
print("=" * 100)
print()

# Convert to list for sampling
all_csv_transitions = []
for exi, exf_dict in csv_transitions.items():
    for exf, ri in exf_dict.items():
        egamma = exi - exf
        all_csv_transitions.append((exi, egamma, ri, exf))

# Random sample (5% of total, minimum 5)
sample_size = max(5, len(all_csv_transitions) // 20)
sample = random.sample(all_csv_transitions, min(sample_size, len(all_csv_transitions)))

print(f"Total transitions in CSV: {len(all_csv_transitions)}")
print(f"Sample size (5%): {sample_size}")
print(f"Sampled: {len(sample)} transitions")
print()

errors = 0
successes = 0

print(f"{'Exi':<10} {'Egamma (CSV)':<18} {'Egamma (ENS)':<18} {'RI (CSV)':<12} {'RI (ENS)':<12} {'Status':<15}")
print("-" * 100)

for exi, egamma_calc, ri_csv, exf in sorted(sample):
    # Find corresponding ENS record
    found = False
    if exi in ens_transitions:
        for ens_egamma, ens_ri in ens_transitions[exi].items():
            if abs(ens_egamma - egamma_calc) < 0.1 and abs(ens_ri - ri_csv) < 0.1:
                status = "OK: MATCH"
                found = True
                successes += 1
                print(f"{exi:<10.0f} {egamma_calc:<18.1f} {ens_egamma:<18.1f} {ri_csv:<12.1f} {ens_ri:<12.1f} {status:<15}")
                break
    
    if not found:
        status = "ERROR: MISMATCH"
        errors += 1
        print(f"{exi:<10.0f} {egamma_calc:<18.1f} {'NOT FOUND':<18} {ri_csv:<12.1f} {'NOT FOUND':<12} {status:<15}")

print()
print("=" * 100)
print("SPOT-CHECK RESULTS")
print("=" * 100)
print(f"OK - Successful matches: {successes}")
print(f"ERROR - Errors found: {errors}")
print()

if errors == 0:
    print("SUCCESS: All sampled transitions match between CSV and ENS!")
else:
    print(f"ERROR: {errors} mismatches found. File requires review.")
