#!/usr/bin/env python3
"""
Comprehensive check: Compare CSV Exf values with ENS L-records
Check EVERY transition in ENS against CSV source data
"""

import csv

# Read CSV
csv_path = "A35/Cl35/raw/2001VO24.csv"
data = []
with open(csv_path, 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        data.append(row)

# Parse Exi and build CSV transition map
exi_values = []
for col in range(2, len(data[2])):
    val = data[2][col].strip()
    if val:
        try:
            exi_values.append((col, float(val)))
        except ValueError:
            pass

csv_exf_set = set()
csv_transitions_map = {}  # (Exi, Exf) -> RI

for row_idx in range(3, len(data)):
    row = data[row_idx]
    exf_str = row[1].strip()
    if not exf_str:
        continue
    
    try:
        exf = float(exf_str)
        csv_exf_set.add(exf)
    except ValueError:
        continue
    
    for col, exi in exi_values:
        if col < len(row):
            ri_str = row[col].strip()
            if ri_str and ri_str != "0":
                try:
                    ri = float(ri_str)
                    csv_transitions_map[(exi, exf)] = ri
                except ValueError:
                    pass

print("=" * 100)
print("CSV DATA")
print("=" * 100)
print(f"CSV Exi values: {sorted([e[1] for e in exi_values])}")
print(f"CSV Exf values ({len(csv_exf_set)} unique): {sorted(csv_exf_set)}")
print(f"Total transitions in CSV: {len(csv_transitions_map)}")
print()

# Read ENS file
ens_path = "A35/Cl35/raw/2001VO24.ens"
ens_levels = {}  # Exi -> list of (Egamma, RI)
ens_exf_to_egamma = {}  # {Exi: {Egamma: RI}}
current_level = None

with open(ens_path, 'r') as f:
    for line_num, line in enumerate(f, 1):
        if len(line) < 20:
            continue
        
        # ENSDF record type is at column 8 (index 7), but check for both 'L' and 'G' in positions 7-8
        record_type = line[7:9].strip()  # Get both positions to be sure
        
        if 'L' in record_type:
            energy_str = line[9:19].strip()
            try:
                current_level = float(energy_str)
                ens_levels[current_level] = []
                if current_level not in ens_exf_to_egamma:
                    ens_exf_to_egamma[current_level] = {}
            except ValueError:
                pass
        
        elif 'G' in record_type and current_level is not None:
            energy_str = line[9:19].strip()
            ri_str = line[22:29].strip()
            try:
                egamma = float(energy_str)
                ri = float(ri_str)
                ens_levels[current_level].append((egamma, ri, line_num))
                ens_exf_to_egamma[current_level][egamma] = ri
            except ValueError:
                pass

print("=" * 100)
print("ENS FILE DATA")
print("=" * 100)
print(f"ENS Exi values (levels): {sorted(ens_levels.keys())}")
print(f"ENS L-records: {len(ens_levels)}")

total_g_records = sum(len(gammas) for gammas in ens_levels.values())
print(f"ENS G-records: {total_g_records}")
print()

# Verify each ENS transition against CSV
print("=" * 100)
print("VERIFICATION: Each ENS transition vs CSV")
print("=" * 100)
print()

errors = []
matches = []

for exi in sorted(ens_levels.keys()):
    for egamma, ri, line_num in sorted(ens_levels[exi], key=lambda x: x[0]):
        # Calculate Exf from Egamma = Exi - Exf
        exf = exi - egamma
        
        # Check if this (Exi, Exf, RI) exists in CSV
        if (exi, exf) in csv_transitions_map:
            csv_ri = csv_transitions_map[(exi, exf)]
            if abs(csv_ri - ri) < 0.01:
                matches.append((exi, egamma, ri, exf))
            else:
                errors.append(f"Line {line_num}: Exi={exi}, Egamma={egamma}, RI={ri} - CSV has RI={csv_ri} (MISMATCH)")
        else:
            errors.append(f"Line {line_num}: Exi={exi}, Egamma={egamma}, RI={ri}, Exf={exf} - NOT IN CSV!")

print(f"Matching transitions: {len(matches)}")
print(f"Errors/mismatches: {len(errors)}")
print()

if errors:
    print("ERRORS FOUND:")
    for error in errors[:20]:  # Show first 20 errors
        print(f"  {error}")
    if len(errors) > 20:
        print(f"  ... and {len(errors) - 20} more errors")
