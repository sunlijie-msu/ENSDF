#!/usr/bin/env python3
"""
Analyze 2001VO24 CSV matrix to extract ALL 80+ gamma transitions
with CORRECT Egamma values (Egamma = Exi - Exf)

CSV Structure:
Row 0: ['', 'Ep', '', '832', '1212', ...] (probe energies - not used)
Row 1: ['', '', '', '', '', ...] (blank row)
Row 2: ['', 'Exi', '5645', '7179', '7547', '7838', '8207', '8216', '8381', '8484', '8893', '8907', '9081', '']
Row 3+: ['Exf', value, RI1, RI2, RI3, ..., Exf_duplicate]
        Column 0: 'Exf' label
        Column 1: Exf value
        Columns 2-12: RI values for each Exi
"""

import csv

# Read CSV
csv_path = "A35/Cl35/raw/2001VO24.csv"
data = []
with open(csv_path, 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        data.append(row)

print("=" * 100)
print("ANALYSIS OF 2001VO24 CSV MATRIX - CORRECT PARSING")
print("=" * 100)
print()

# Parse Exi values from row 2, columns 2-12
exi_values = []
for col in range(2, len(data[2])):
    val = data[2][col].strip()
    if val:
        try:
            exi_values.append((col, float(val)))
        except ValueError:
            pass

print(f"Exi (initial state) values:")
for col, exi in exi_values:
    print(f"  Column {col}: Exi = {exi}")
print(f"Total initial states: {len(exi_values)}")
print()

# Parse data rows (starting from row 3)
print("=" * 100)
print("ALL GAMMA TRANSITIONS FROM CSV MATRIX")
print("=" * 100)
print()

transitions_list = []  # (Exi, Egamma, RI, Exf)

for row_idx in range(3, len(data)):
    row = data[row_idx]
    
    # Column 1 contains Exf value
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
                    egamma = exi - exf  # CRITICAL: Egamma = Exi - Exf
                    
                    transitions_list.append((exi, egamma, ri, exf))
                except ValueError:
                    pass

print(f"Total transitions extracted: {len(transitions_list)}")
print()

# Sort by Exi first, then by Egamma (ascending energy)
transitions_list.sort(key=lambda x: (x[0], x[1]))

# Display organized by Exi
current_exi = None
count_by_exi = {}

print(f"{'Exi':<8} {'Egamma':<10} {'RI':<8} {'Exf':<8} {'Calculation':<20}")
print("-" * 60)

for exi, egamma, ri, exf in transitions_list:
    if exi != current_exi:
        current_exi = exi
        count_by_exi[exi] = 0
    count_by_exi[exi] += 1
    calc = f"{exi:.0f}-{exf:.0f}"
    print(f"{exi:<8.0f} {egamma:<10.1f} {ri:<8.1f} {exf:<8.0f} {calc:<20}")

print()
print("=" * 100)
print("SUMMARY BY INITIAL STATE (Exi)")
print("=" * 100)
for exi in sorted(count_by_exi.keys()):
    print(f"Exi = {exi:<8.0f} : {count_by_exi[exi]:>3} transitions")

print()
print(f"TOTAL: {len(transitions_list)} transitions")
print()

# Specific analysis of L 7547 transitions
print("=" * 100)
print("SPECIFIC ANALYSIS: L 7547 TRANSITIONS (the 'absolutely wrong' case)")
print("=" * 100)
print()

l7547_transitions = [(eg, ri, exf) for exi, eg, ri, exf in transitions_list if exi == 7547]
print(f"Found {len(l7547_transitions)} transitions from L 7547:")
print(f"{'Egamma (keV)':<15} {'RI':<10} {'Exf (keV)':<15} {'Calculation':<20}")
print("-" * 70)
for egamma, ri, exf in sorted(l7547_transitions, key=lambda x: x[0]):
    calc = f"7547 - {exf:.0f} = {egamma:.1f}"
    print(f"{egamma:<15.1f} {ri:<10.1f} {exf:<15.0f} {calc:<20}")

# Find G 7070 specifically
print()
print(f"Looking for Egamma≈7070 transitions from Exi=7547:")
for exi, egamma, ri, exf in transitions_list:
    if exi == 7547 and abs(egamma - 7070) < 0.5:
        print(f"  FOUND: Egamma={egamma:.1f}, RI={ri:.1f}, Exf={exf:.0f}")
        print(f"  Calculation: {exi:.0f} - {exf:.0f} = {egamma:.1f}")
