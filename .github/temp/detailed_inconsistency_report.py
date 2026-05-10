#!/usr/bin/env python3
"""
Generate detailed report of all 4 Jpi consistency inconsistencies found in markdown
"""

import re

# Read markdown
with open('XUNDL/2026BAAA_CR11022_209Po_original_Table_I.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Extract data rows
data_rows = []
for line_num, line in enumerate(lines, 1):
    if line.startswith('|') and 'keV' not in line and '---' not in line and line_num > 5:
        cells = [c.strip() for c in line.split('|')[1:-1]]
        if len(cells) >= 3 and (cells[0][0].isdigit() or cells[0].startswith('(')):
            data_rows.append({
                'line': line_num,
                'Egamma': cells[0],
                'Jpi': cells[1],
                'Ei': cells[2],
                'raw': line.rstrip()
            })

print("=" * 100)
print("DETAILED REPORT: MARKDOWN SOURCE DATA CONSISTENCY ERRORS")
print("=" * 100)

# Find the 4 specific inconsistencies
print("\n[INCONSISTENCY 1] Level E_i = 4908.7 keV")
print("-" * 100)
for row in data_rows:
    if '4908.7' in row['Ei']:
        print(f"  Line {row['line']}: Egamma={row['Egamma']:<10} Jpi_i={row['Jpi']}")

print("\nISSUE: Level appears with TWO DIFFERENT Jpi values:")
print("  - Jpi_i = 29/2+ (appears at least once)")
print("  - Jpi_i = 29/2- (appears at least once)")
print("\nThis is a PARITY MISMATCH. Either the level is positive parity or negative parity,")
print("not both. The source publication must clarify which is correct.")

print("\n" + "=" * 100)
print("[INCONSISTENCY 2] Level E_i = 5635.7 keV")
print("-" * 100)
for row in data_rows:
    if '5635.7' in row['Ei']:
        print(f"  Line {row['line']}: Egamma={row['Egamma']:<10} Jpi_i={row['Jpi']}")

print("\nISSUE: Level appears with TWO DIFFERENT Jpi notation:")
print("  - Jpi_i = (33/2) (parenthetical - uncertain)")
print("  - Jpi_i = 33/2+ (plain + sign - confirmed parity)")
print("\nThis is a NOTATION MISMATCH. The level cannot be both uncertain and confirmed,")
print("and the parity designation differs.")

print("\n" + "=" * 100)
print("[INCONSISTENCY 3] Level E_i = 6300.2 keV")
print("-" * 100)
for row in data_rows:
    if '6300.2' in row['Ei']:
        print(f"  Line {row['line']}: Egamma={row['Egamma']:<10} Jpi_i={row['Jpi']}")

print("\nISSUE: Level appears with TWO DIFFERENT Jpi notation:")
print("  - Jpi_i = (39/2+) (parenthetical - uncertain)")
print("  - Jpi_i = 39/2+ (plain - confirmed)")
print("\nThis is a CERTAINTY MISMATCH. The parentheses indicate uncertain Jpi in ENSDF,")
print("but the same numerical value appears without parentheses elsewhere in the table.")

print("\n" + "=" * 100)
print("[INCONSISTENCY 4] Level E_i = 6461.6 keV")
print("-" * 100)
for row in data_rows:
    if '6461.6' in row['Ei']:
        print(f"  Line {row['line']}: Egamma={row['Egamma']:<10} Jpi_i={row['Jpi']}")

print("\nISSUE: Level appears with TWO DIFFERENT Jpi notation:")
print("  - Jpi_i = (41/2+) (parenthetical - uncertain)")
print("  - Jpi_i = 41/2+ (plain - confirmed)")
print("\nThis is a CERTAINTY MISMATCH. Same as Inconsistency 3.")

print("\n" + "=" * 100)
print("SUMMARY: ALL 4 INCONSISTENCIES")
print("=" * 100)

print("""
Type 1 - PARITY MISMATCH (1 occurrence):
  Level 4908.7 keV: Has both 29/2+ and 29/2- assignments
  
Type 2 - NOTATION MISMATCH (3 occurrences):
  Level 5635.7 keV: Has both (33/2) and 33/2+ assignments
  Level 6300.2 keV: Has both (39/2+) and 39/2+ assignments
  Level 6461.6 keV: Has both (41/2+) and 41/2+ assignments

ROOT CAUSE: The markdown table source has internal inconsistencies that must be
resolved by consulting the original publication or author.

IMPACT ON ENSDF: These inconsistencies propagated to the ENSDF file because the
source data was ambiguous. The ENSDF file currently has both forms of each level
(uncertain and confirmed versions), which is a valid representation of measurement
uncertainty BUT reflects the source publication ambiguity.

ACTION REQUIRED: 
1. Consult the 2026BAAA publication (or contact authors) to clarify:
   - Is level 4908.7 keV: 29/2+ or 29/2-?
   - Are levels 5635.7, 6300.2, 6461.6 keV definitively assigned, or uncertain?
   
2. Once clarified, update the markdown table to reflect single, consistent values.

3. Update ENSDF file to match the clarified source data.
""")
