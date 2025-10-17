#!/usr/bin/env python3
"""
Extract ONLY the 11 valid transitions (Exf in ENS levels) and show the corrected ENS structure
"""

import csv

# Read CSV
csv_path = "A35/Cl35/raw/2001VO24.csv"
data = []
with open(csv_path, 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        data.append(row)

# Parse Exi values
exi_values = []
for col in range(2, len(data[2])):
    val = data[2][col].strip()
    if val:
        try:
            exi_values.append((col, float(val)))
        except ValueError:
            pass

# Valid ENS levels
ens_levels = {0.0, 1219.0, 5645.0, 7179.0, 7547.0, 7838.0, 8207.0, 8216.0, 8381.0, 8484.0, 8893.0, 8907.0, 9081.0}

# Extract ONLY valid transitions
valid_transitions = {}  # {Exi: [(Egamma, RI, Exf), ...]}

for row_idx in range(3, len(data)):
    row = data[row_idx]
    exf_str = row[1].strip()
    if not exf_str:
        continue
    
    try:
        exf = float(exf_str)
    except ValueError:
        continue
    
    if exf not in ens_levels:
        continue  # Skip invalid Exf
    
    for col, exi in exi_values:
        if col < len(row):
            ri_str = row[col].strip()
            
            if ri_str and ri_str != "0":
                try:
                    ri = float(ri_str)
                    egamma = exi - exf
                    
                    if exi not in valid_transitions:
                        valid_transitions[exi] = []
                    valid_transitions[exi].append((egamma, ri, exf))
                except ValueError:
                    pass

print("=" * 100)
print("CORRECTED 2001VO24.ens STRUCTURE - VALID TRANSITIONS ONLY")
print("=" * 100)
print()

# Generate corrected ENS format
print("Header section:")
print(" 35CL    2001Vo24                      2001Vo24")
print(" 35CL cL S$LABEL=E{-p}(lab) (keV)")
print(" 35CL PN")
print()

# Group transitions by Exi and output
all_data = []
for exi in sorted(valid_transitions.keys()):
    transitions = sorted(valid_transitions[exi], key=lambda x: x[0])  # Sort by Egamma
    
    # Create L-record (probe energy from current ENS)
    # Map Exi to probe energies from ENS file
    exi_to_probe = {
        5645.0: "832",
        7179.0: "832",
        7547.0: "1212",
        7838.0: "1510",
        8207.0: "1891",
        8216.0: "1900",
        8381.0: "2070",
        8484.0: "2176",
        8893.0: "2597",
        8907.0: "2611",
        9081.0: "2791"
    }
    
    probe = exi_to_probe.get(exi, "")
    
    print(f" 35CL  L {exi:<6.0f}{' ' * (17-len(str(int(exi))))} {probe:>6} 1")
    
    for egamma, ri, exf in transitions:
        # Format as ENSDF G-record
        # Columns: NUCID(1-5), TYPE(8), E(10-19), DE(20-21), RI(23-29), DRI(30-31)
        print(f" 35CL  G {egamma:<6.1f}      {int(ri):<6}")

print()
print("=" * 100)
print("TRANSITION SUMMARY")
print("=" * 100)

total_valid = 0
for exi in sorted(valid_transitions.keys()):
    count = len(valid_transitions[exi])
    total_valid += count
    print(f"Exi = {exi:<8.0f}: {count:>2} transitions")

print()
print(f"TOTAL VALID TRANSITIONS: {total_valid}")
print(f"REMOVED (invalid Exf): {85 - total_valid}")
