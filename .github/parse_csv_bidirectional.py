#!/usr/bin/env python3
"""
Parse 2001VO24.csv with bidirectional position verification.
L-records and G-records in keV units (integers).
"""

import csv

# Read CSV file
csv_file = r"d:\X\ND\ENSDF\A35\Cl35\raw\2001VO24.csv"
with open(csv_file, 'r') as f:
    rows = list(csv.reader(f))

print("=" * 80)
print("CSV STRUCTURE ANALYSIS")
print("=" * 80)

# Analyze structure
print("\nRow 1 (Ep row):", rows[0])
print("Row 3 (Exi row):", rows[2])

# Extract Exi values from row 3 (header row)
exi_row = rows[2]
exi_values = []
exi_col_indices = []
for col_idx in range(len(exi_row)):
    val = exi_row[col_idx].strip()
    if val and val != "Exi":
        try:
            exi_val = int(val)
            exi_values.append(exi_val)
            exi_col_indices.append(col_idx)
        except ValueError:
            pass

print(f"\nExtracted Exi values (keV): {exi_values}")
print(f"Exi column indices: {exi_col_indices}")
print(f"Total Exi levels: {len(exi_values)}")

# Extract Exf values from rows 4-end (data rows)
print("\n" + "=" * 80)
print("TRANSITIONS WITH POSITION TRACING")
print("=" * 80)

transitions = []  # List of (Exi_keV, Exf_keV, BR, source_row_idx, source_col_idx)

for row_idx in range(3, len(rows)):
    row = rows[row_idx]
    if not row or not row[0].strip():
        continue
    
    exf_label = row[0].strip()
    if exf_label != "Exf":
        continue
    
    # Column 1 has the Exf value
    exf_str = row[1].strip() if len(row) > 1 else ""
    if not exf_str:
        continue
    
    try:
        exf_keV = int(exf_str)
    except ValueError:
        continue
    
    # For each Exi column, check if there's a BR value
    for col_idx, exi_keV in zip(exi_col_indices, exi_values):
        if col_idx < len(row):
            br_str = row[col_idx].strip()
            if br_str:
                try:
                    br = int(br_str)
                    egamma = exi_keV - exf_keV
                    transitions.append((exi_keV, exf_keV, br, egamma, row_idx, col_idx))
                except ValueError:
                    pass

print(f"\nTotal transitions found: {len(transitions)}\n")

# Display all transitions with position info
print(f"{'Exi':>5} {'Exf':>5} {'BR':>3} {'Egamma':>6} {'RowIdx':>6} {'ColIdx':>6}")
print("-" * 40)
for exi, exf, br, egamma, row_idx, col_idx in sorted(transitions):
    print(f"{exi:5d} {exf:5d} {br:3d} {egamma:6d} {row_idx:6d} {col_idx:6d}")

# Organize by Exi (level)
print("\n" + "=" * 80)
print("ORGANIZED BY LEVEL (Exi)")
print("=" * 80)

levels = {}
for exi, exf, br, egamma, row_idx, col_idx in transitions:
    if exi not in levels:
        levels[exi] = []
    levels[exi].append((exf, br, egamma, row_idx, col_idx))

# Sort transitions within each level by Egamma (ascending)
for exi in sorted(levels.keys()):
    gammas = sorted(levels[exi], key=lambda x: x[2])
    levels[exi] = gammas

# Generate ENSDF records
print("\nENSDF L and G RECORDS (keV units, integer energies):\n")

ensdf_records = []

for exi in sorted(levels.keys()):
    # L-record
    l_energy_str = str(exi).ljust(10)
    l_record = f" 35CL  L {l_energy_str}"
    ensdf_records.append(l_record)
    print(l_record)
    
    # G-records (sorted by energy)
    for exf, br, egamma, row_idx, col_idx in levels[exi]:
        g_energy_str = str(egamma).ljust(10)
        ri_str = str(br).ljust(7)
        g_record = f" 35CL  G {g_energy_str}{ri_str}"
        ensdf_records.append(g_record)
        print(g_record)

print("\n" + "=" * 80)
print("VALIDATION SUMMARY")
print("=" * 80)
print(f"Total L-records: {len(levels)}")
print(f"Total G-records: {len(transitions)}")
print(f"L-record energies (keV) in ascending order: {sorted(levels.keys())}")

# Save to file
output_file = r"d:\X\ND\ENSDF\.github\ensdf_records_keV.txt"
with open(output_file, 'w') as f:
    for record in ensdf_records:
        f.write(record + "\n")

print(f"\nRecords saved to: {output_file}")
