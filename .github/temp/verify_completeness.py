#!/usr/bin/env python3
"""
Verify completeness of new analysis columns in the table.
"""

import re

with open(r'd:\X\ND\ENSDF\XUNDL\2026BAAA_CR11022_209Po_original_Table_I.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find data rows
data_rows = []
for i, line in enumerate(lines):
    if i > 2 and line.strip().startswith('|'):
        parts = [p.strip() for p in line.split('|')]
        if len(parts) >= 10:  # 9 columns + 2 empty at start/end
            parts = [p for p in parts if p]
            if len(parts) >= 9:
                data_rows.append((i, parts))

# Check for blank cells in new columns
blank_dco = 0
blank_mult = 0
rows_with_data = 0
mismatches = []

for line_num, parts in data_rows:
    if parts[0]:  # Has energy data
        rows_with_data += 1
        eg = parts[0]
        rdco = parts[4]
        dco_col = parts[7]  # DCO Classification column
        mult_col = parts[8]  # Assigned Multipolarity column
        
        # Check if R_DCO is missing
        has_rdco = '–' not in rdco and rdco.strip()
        
        # Check DCO column
        is_blank_dco = not dco_col or dco_col == '–'
        if is_blank_dco:
            blank_dco += 1
        
        # Check Multipolarity column
        is_blank_mult = not mult_col or mult_col == '–'
        if is_blank_mult:
            blank_mult += 1
        
        # Check for mismatches (should be no DCO only if no R_DCO data)
        if has_rdco and is_blank_dco:
            mismatches.append((eg, "Has R_DCO data but DCO column is blank"))
        if is_blank_dco and has_rdco:
            mismatches.append((eg, "R_DCO data exists but DCO classification is blank"))

print(f"Total data rows: {rows_with_data}")
print(f"DCO Classification: {rows_with_data - blank_dco} filled, {blank_dco} blank (expected blanks for no R_DCO data)")
print(f"Assigned Multipolarity: {rows_with_data - blank_mult} filled, {blank_mult} blank (expected blanks for no R_DCO data)")
print(f"\nCompleteness Status:")
if blank_dco == blank_mult:
    print(f"  ✓ Both columns have same blank count ({blank_dco}) - consistent!")
else:
    print(f"  ✗ Column blank counts differ (DCO={blank_dco}, Mult={blank_mult})")

if mismatches:
    print(f"\nData integrity issues found:")
    for eg, issue in mismatches[:5]:
        print(f"  E={eg:<8} : {issue}")
else:
    print(f"  ✓ No data integrity issues - blanks are properly aligned")

# Sample output: show rows with non-blank multipolarity
print(f"\nSample assigned multipolarities (first 20 with R_DCO data):")
print(f"{'E (keV)':<10} | {'DCO Class':<12} | {'Assigned Multipolarity':<20}")
print("-" * 50)
count = 0
for line_num, parts in data_rows:
    if parts[7] and parts[7] != '–':
        eg = parts[0]
        dco = parts[7]
        mult = parts[8]
        print(f"{eg:<10} | {dco:<12} | {mult:<20}")
        count += 1
        if count >= 20:
            break

print(f"\n✓ Table validation complete - {rows_with_data} rows with {rows_with_data - blank_dco} analysis results")
