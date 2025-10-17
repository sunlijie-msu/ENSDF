#!/usr/bin/env python3
"""
Analyze 2001VO24.csv to extract all transitions using the physics formula Egamma = Exi - Exf
"""

csv_file = r'd:\X\ND\ENSDF\A35\Cl35\raw\2001VO24.csv'

with open(csv_file, 'r') as f:
    lines = f.readlines()

print("=" * 100)
print("CSV ANALYSIS: 2001VO24.csv")
print("=" * 100)

# Extract Exi header (line 3, 0-indexed as line 2)
exi_line = lines[2].strip()
exi_parts = [x.strip() for x in exi_line.split(',')]
# Exi values start at column 2 (after empty cells and 'Exi' label)
exi_list = []
for x in exi_parts[2:]:
    if x and x.isdigit():
        exi_list.append(int(x))

print(f"\nLevel Energies (Exi): {exi_list}")
print(f"Total levels: {len(exi_list)}\n")

# Parse data rows
# Format: "Exf,<value>,,<int>,<int>,..." where columns after first two map to Exi values
transitions_by_exi = {exi: [] for exi in exi_list}

data_rows = []
for line_num, line in enumerate(lines[3:], start=4):
    line = line.strip()
    if not line or not line.startswith('Exf'):
        continue
    
    parts = [x.strip() for x in line.split(',')]
    
    # parts[0] = 'Exf'
    # parts[1] = Exf value
    # parts[2] onwards = intensities
    
    if len(parts) < 2:
        continue
    
    try:
        exf = int(parts[1])
    except ValueError:
        continue
    
    data_rows.append((exf, parts))

# Map intensities to Exi values
print("=" * 100)
print("PARSING TRANSITIONS")
print("=" * 100)

for exf, parts in data_rows:
    print(f"\nExf = {exf}:")
    
    # Intensities start at column index 2 in the parts array
    # They map to Exi values in order
    for exi_idx, exi in enumerate(exi_list):
        intensity_col = 2 + exi_idx
        
        if intensity_col >= len(parts):
            continue
        
        intensity_str = parts[intensity_col].strip()
        if intensity_str and intensity_str.isdigit():
            intensity = int(intensity_str)
            if intensity > 0:
                egamma = exi - exf
                if egamma > 0:
                    transitions_by_exi[exi].append((egamma, intensity, exf))
                    print(f"  Col {intensity_col}: Exi={exi}, Egamma={egamma}, RI={intensity}")

# Print final summary
print("\n" + "=" * 100)
print("FINAL TRANSITION SUMMARY BY LEVEL (Exi)")
print("=" * 100)

total_gammas = 0
for exi in exi_list:
    if transitions_by_exi[exi]:
        # Sort by gamma energy (ascending)
        trans_sorted = sorted(transitions_by_exi[exi], key=lambda x: x[0])
        print(f"\nLevel Exi = {exi} keV ({len(trans_sorted)} gammas):")
        for egamma, intensity, exf in trans_sorted:
            print(f"  G {egamma:5d}   RI={intensity:3d}")
            total_gammas += 1

print(f"\n{'=' * 100}")
print(f"TOTAL GAMMA TRANSITIONS: {total_gammas}")
print(f"{'=' * 100}")
