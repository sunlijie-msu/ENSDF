#!/usr/bin/env python3
"""
Parse CSV as proper ENSDF transaction matrix: 
each cell (Exi, Exf, RI) = one gamma transition with Egamma = Exi - Exf
"""

import csv

csv_file = r'd:\X\ND\ENSDF\A35\Cl35\raw\2001VO24.csv'

# Parse CSV
with open(csv_file) as f:
    reader = csv.reader(f)
    lines = list(reader)

# Extract header row with Exi values (line 3 = index 2... wait, let me check index)
# Line "Exi,5645,7179,..." has Exi values starting at column 2
# Let me search for the line that starts with ",Exi,"
exi_line_idx = None
for idx, line in enumerate(lines):
    if line and line[0] == '' and len(line) > 1 and line[1] == 'Exi':
        exi_line_idx = idx
        break

if exi_line_idx is None:
    print("ERROR: Could not find Exi header line")
    exit(1)

exi_line = lines[exi_line_idx]  # e.g., ['', 'Exi', '5645', '7179', ...]
exi_values = []
exi_cols = {}
for col_idx, val in enumerate(exi_line[2:], start=2):  # Skip first two columns (empty, 'Exi')
    try:
        exi = int(val)
        exi_values.append(exi)
        exi_cols[exi] = col_idx
    except:
        pass

print(f"Found {len(exi_values)} levels (Exi): {sorted(exi_values)}")
print()

# Parse transaction matrix: for each data row, extract Exf and all (Exf, Exi, RI) combinations
transitions = {}  # grouped by Exi: {Exi: [(Egamma, RI), ...]}

for exi in exi_values:
    transitions[exi] = []

# Skip header lines and process data rows (start from exi_line_idx + 1 onward)
for row_idx in range(exi_line_idx + 1, len(lines)):
    row = lines[row_idx]
    if not row or len(row) < 2:  # Skip empty rows or rows without enough columns
        continue
    
    # Format is: ['Exf', '0', '', '38', ...]  where row[1] is the Exf value
    if row[0] != 'Exf':  # Skip rows that don't start with 'Exf'
        continue
    
    try:
        exf = int(row[1])  # Exf value is at index 1
    except (ValueError, IndexError):
        continue
    
    # For each Exi, the RI value is at column index = exi_cols[exi]
    for exi in exi_values:
        col_idx = exi_cols[exi]
        if col_idx < len(row):
            ri_str = row[col_idx].strip()
            if ri_str:  # Skip empty cells
                try:
                    ri = int(ri_str)
                    egamma = exi - exf
                    if egamma > 0:  # Only positive energies
                        transitions[exi].append((egamma, ri))
                except ValueError:
                    pass

# Sort gammas within each level by ascending energy
for exi in transitions:
    transitions[exi].sort()

print("=" * 80)
print("AUTHORITATIVE TRANSACTION MATRIX FROM CSV")
print("=" * 80)
print()

total_gammas = 0
for exi in sorted(transitions.keys()):
    gammas = transitions[exi]
    print(f"Exi={exi:5d} keV: {len(gammas):2d} gammas", end='')
    if gammas:
        print(f" → {gammas}")
    else:
        print()
    total_gammas += len(gammas)

print()
print(f"TOTAL GAMMAS: {total_gammas}")
print()

# Verify structure
print("=" * 80)
print("VERIFICATION: Egamma = Exi - Exf")
print("=" * 80)
for exi in sorted(transitions.keys())[:3]:  # Show first 3 levels
    print(f"\nLevel Exi={exi}:")
    for egamma, ri in transitions[exi][:3]:  # Show first 3 gammas
        exf = exi - egamma
        print(f"  Egamma={egamma:4d} keV (Exf={exf:4d}), RI={ri}")
