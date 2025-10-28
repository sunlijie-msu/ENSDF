#!/usr/bin/env python3
"""
Filter 2001VO24 transitions to only those with valid Exf (in ENS levels)
"""

import csv

# Read CSV
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

# Read ENS levels
ens_path = "A35/Cl35/raw/2001VO24.ens"
ens_levels = set()
with open(ens_path, 'r') as f:
    for line in f:
        if len(line) < 20:
            continue
        record_type = line[7:8].strip()
        if record_type == 'L':
            energy_str = line[9:19].strip()
            try:
                energy = float(energy_str)
                ens_levels.add(energy)
            except ValueError:
                pass

print(f"Valid ENS levels: {sorted(ens_levels)}")
print()

# Extract transitions with VALID Exf only
valid_transitions = []  # (Exi, Egamma, RI, Exf)
invalid_transitions = []  # (Exi, Egamma, RI, Exf) - Exf NOT in ENS

for row_idx in range(3, len(data)):
    row = data[row_idx]
    exf_str = row[1].strip()
    if not exf_str:
        continue
    
    try:
        exf = float(exf_str)
    except ValueError:
        continue
    
    # Parse RI values for each Exi column
    for col, exi in exi_values:
        if col < len(row):
            ri_str = row[col].strip()
            
            if ri_str and ri_str != "0":
                try:
                    ri = float(ri_str)
                    egamma = exi - exf
                    
                    if exf in ens_levels:
                        valid_transitions.append((exi, egamma, ri, exf))
                    else:
                        invalid_transitions.append((exi, egamma, ri, exf))
                except ValueError:
                    pass

print("=" * 100)
print("TRANSITION VALIDATION RESULTS")
print("=" * 100)
print()
print(f"Valid transitions (Exf in ENS levels): {len(valid_transitions)}")
print(f"Invalid transitions (Exf NOT in ENS levels): {len(invalid_transitions)}")
print(f"Total from CSV: {len(valid_transitions) + len(invalid_transitions)}")
print()

print("INVALID TRANSITIONS (should be REMOVED or marked questionable):")
print(f"{'Exi':<10} {'Egamma':<10} {'RI':<8} {'Exf (NOT IN ENS)':<15}")
print("-" * 60)
for exi, egamma, ri, exf in sorted(invalid_transitions):
    print(f"{exi:<10.0f} {egamma:<10.1f} {ri:<8.1f} {exf:<15.0f}")

print()
print("=" * 100)
print("G 7070 SPECIFIC CASE")
print("=" * 100)

for exi, egamma, ri, exf in invalid_transitions:
    if exi == 7547 and abs(egamma - 7070) < 0.1:
        print(f"FOUND G 7070: Exi=7547, Egamma=7070, RI={ri}, Exf={exf}")
        print(f"Status: INVALID - Exf={exf} is NOT in ENS level scheme")
        print(f"Action: This transition should be REMOVED from 2001VO24.ens")

print()
print("=" * 100)
print("RECOMMENDATION")
print("=" * 100)
print(f"""
The current 2001VO24.ens contains transitions to non-existent levels.

Current approach in ENS file:
  - ALL 85 transitions from CSV are included
  - Some reference Exf values NOT in adopted scheme

Recommended approach:
  - KEEP only {len(valid_transitions)} valid transitions (Exf in ENS levels)
  - REMOVE {len(invalid_transitions)} invalid transitions (Exf NOT in ENS levels)
  - This includes removing G 7070 (7547 → 477, where 477 is NOT a level)

This explains why the user said "G 7070 is absolutely wrong" - it's not that
the energy calculation is wrong, but that 477 keV is not a real level!
""")
