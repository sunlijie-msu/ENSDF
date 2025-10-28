#!/usr/bin/env python3
"""
COMPREHENSIVE ENS vs CSV COMPARISON
Compare every G-record in ENS against CSV source data
"""

import csv

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

print(f"CSV Exi values: {[exi for _, exi in exi_values]}")
print()

# Build CSV transition map: {(Exi, Exf): RI}
csv_trans_map = {}
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
                    csv_trans_map[(exi, exf)] = ri
                except ValueError:
                    pass

print(f"Total CSV transitions: {len(csv_trans_map)}")
print()

# Read ENS file and extract G-records
ens_path = "A35/Cl35/raw/2001VO24.ens"
ens_gammas = []  # (Exi, Egamma, RI_from_ens, line_num, full_line)
current_exi = None

with open(ens_path, 'r') as f:
    for line_num, line in enumerate(f, 1):
        if len(line) < 20:
            continue
        record_type = line[7:8].strip()
        
        if record_type == 'L':
            energy_str = line[9:19].strip()
            try:
                current_exi = float(energy_str)
            except ValueError:
                pass
        
        elif record_type == 'G' and current_exi is not None:
            energy_str = line[9:19].strip()
            # RI value appears to be in columns 20+ (in DE field position)
            # Extract everything after energy
            rest = line[19:].strip()
            try:
                egamma = float(energy_str)
                # Try to parse RI from rest of line
                ri_parts = rest.split()
                if ri_parts:
                    ri_ens = float(ri_parts[0])
                    ens_gammas.append((current_exi, egamma, ri_ens, line_num, line.rstrip()))
            except ValueError:
                pass

print(f"Total ENS G-records: {len(ens_gammas)}")
print()

# Compare each ENS G-record with CSV
print("=" * 120)
print("ENS vs CSV COMPARISON")
print("=" * 120)
print()

matches = 0
mismatches = 0
missing_in_csv = 0

print(f"{'Line':<6} {'Exi':<8} {'Egamma':<10} {'RI_ENS':<10} {'Status':<20} {'Exf (calc)':<10} {'RI_CSV':<10} {'Match?':<10}")
print("-" * 120)

for exi_ens, egamma_ens, ri_ens, line_num, full_line in ens_gammas:
    # Calculate what Exf should be: Exf = Exi - Egamma
    exf_calc = exi_ens - egamma_ens
    
    # Check if this transition exists in CSV
    if (exi_ens, exf_calc) in csv_trans_map:
        ri_csv = csv_trans_map[(exi_ens, exf_calc)]
        
        # Check if RI matches
        if abs(ri_ens - ri_csv) < 0.1:
            status = "MATCH"
            match_result = "OK"
            matches += 1
        else:
            status = "RI MISMATCH"
            match_result = "ERROR"
            mismatches += 1
    else:
        status = "NOT IN CSV"
        ri_csv = None
        match_result = "ERROR"
        missing_in_csv += 1
    
    ri_csv_str = f"{ri_csv:.1f}" if ri_csv is not None else "N/A"
    print(f"{line_num:<6} {exi_ens:<8.0f} {egamma_ens:<10.1f} {ri_ens:<10.1f} {status:<20} {exf_calc:<10.0f} {ri_csv_str:<10} {match_result:<10}")

print()
print("=" * 120)
print("SUMMARY")
print("=" * 120)
print(f"Matches (ENS matches CSV): {matches}")
print(f"RI mismatches: {mismatches}")
print(f"Missing in CSV: {missing_in_csv}")
print(f"Total ENS records: {len(ens_gammas)}")
print()

if missing_in_csv > 0:
    print("ERROR: Some ENS records do not appear in CSV!")
    print("These transitions should be REMOVED or investigated!")
