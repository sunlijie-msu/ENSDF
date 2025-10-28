import csv
import sys

csv_file = r'd:\X\ND\ENSDF\A35\Cl35\raw\2001VO24.csv'

# Read CSV
with open(csv_file, 'r') as f:
    lines = f.readlines()

# Extract header row with Exi values (line 3, 0-indexed as 2)
exi_line = lines[2].strip()
exi_values = [x.strip() for x in exi_line.split(',')]
# Exi values start at column index 2
exi_list = []
for i in range(2, min(len(exi_values), 14)):
    if exi_values[i].isdigit():
        exi_list.append(int(exi_values[i]))

print("=" * 90)
print("CSV ANALYSIS: 2001VO24.csv - COMPREHENSIVE EXTRACTION")
print("=" * 90)
print(f"\nLevel Energies (Exi) found in order: {exi_list}")
print(f"Total levels: {len(exi_list)}\n")

# Parse all transitions using correct column mapping
transitions_by_exi = {}
for exi in exi_list:
    transitions_by_exi[exi] = []

# Process data rows
for line_num, line in enumerate(lines, start=1):
    line = line.strip()
    if not line or 'Exf' not in line[:4]:
        continue
    
    parts = [x.strip() for x in line.split(',')]
    
    # Extract Exf value
    exf_part = parts[0]
    if exf_part == 'Exf' or not exf_part.startswith('Exf'):
        continue
    
    try:
        exf = int(exf_part[3:]) if len(exf_part) > 3 else None
        if exf is None:
            continue
    except ValueError:
        continue
    
    # Extract intensities for each Exi
    for col_idx, exi in enumerate(exi_list):
        csv_col = col_idx + 2  # Account for first 2 columns (empty, Exi label)
        if csv_col < len(parts) and parts[csv_col].strip().isdigit():
            intensity = int(parts[csv_col].strip())
            if intensity > 0:
                egamma = exi - exf
                if egamma > 0:  # Only positive gamma energies
                    transitions_by_exi[exi].append((egamma, intensity, exf))

# Display all transitions sorted by level
print("\n" + "=" * 90)
print("ALL TRANSITIONS FROM CSV (sorted by Exi, then by Egamma):")
print("=" * 90)

total_gammas = 0
for exi in exi_list:
    if transitions_by_exi[exi]:
        trans_sorted = sorted(transitions_by_exi[exi], key=lambda x: x[0])
        print(f"\n*** Level Exi = {exi} keV ***")
        for egamma, intensity, exf in trans_sorted:
            print(f"    G-record: Egamma = {egamma:5d}  RI = {intensity:3d}  (Exf = {exf})")
            total_gammas += 1

print("\n" + "=" * 90)
print(f"TOTAL GAMMA TRANSITIONS: {total_gammas}")
print("=" * 90)
