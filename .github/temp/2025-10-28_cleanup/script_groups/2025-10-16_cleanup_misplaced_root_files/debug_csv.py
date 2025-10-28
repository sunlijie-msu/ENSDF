#!/usr/bin/env python3
"""
Debug CSV parsing
"""

import csv

csv_file = r'd:\X\ND\ENSDF\A35\Cl35\raw\2001VO24.csv'

# Parse CSV
with open(csv_file) as f:
    reader = csv.reader(f)
    lines = list(reader)

# Find header line with Exi values
print("First 10 lines:")
for idx in range(min(10, len(lines))):
    print(f"  Line {idx}: {lines[idx][:15]}")  # Show first 15 columns
print()

# Find Exi line
exi_line_idx = None
for idx, line in enumerate(lines):
    if line and len(line) > 1 and line[1] == 'Exi':
        exi_line_idx = idx
        print(f"Found Exi header at line {idx}: {line[:5]}")
        break

if exi_line_idx is None:
    print("ERROR: No Exi header found!")
    exit(1)

exi_line = lines[exi_line_idx]
print(f"Exi line: {exi_line}")
print()

# Extract Exi values
exi_values = []
exi_cols = {}
for col_idx, val in enumerate(exi_line[2:], start=2):
    if val.strip():
        try:
            exi = int(val)
            exi_values.append(exi)
            exi_cols[exi] = col_idx
            print(f"  Found Exi={exi} at column {col_idx}")
        except:
            pass

print(f"\nTotal Exi values: {len(exi_values)}")
print(f"Exi values: {exi_values}")
print(f"Column mapping: {exi_cols}")
print()

# Show sample data rows
print("Sample data rows (first 5):")
for row_idx in range(exi_line_idx + 1, min(exi_line_idx + 6, len(lines))):
    row = lines[row_idx]
    if row and row[0]:
        print(f"  Line {row_idx} (Exf={row[0]}): {row[:5]}")
