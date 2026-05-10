#!/usr/bin/env python3
"""
Value Occurrence Check for markdown table - CHECK FOR INTERNAL CONSISTENCY
Verifies that every level energy appearing multiple times in the markdown table
has consistent energy, uncertainty, and J-pi across all occurrences.
"""

import re
from collections import defaultdict

# Read markdown
with open('XUNDL/2026BAAA_CR11022_209Po_original_Table_I.md', 'r', encoding='utf-8') as f:
    md_lines = f.readlines()

print("=" * 100)
print("MARKDOWN VALUE OCCURRENCE CHECK - INTERNAL DATA CONSISTENCY")
print("=" * 100)

# Step 1: Column Mapping
print("\nSTEP 1: COLUMN MAPPING")
print("-" * 100)

headers = []
data_rows = []

for line_num, line in enumerate(md_lines, 1):
    if '###' in line:
        continue
    if '| :---' in line:
        print(f"Line {line_num}: [SEPARATOR - skip]")
        continue
    if not line.startswith('|'):
        continue
    
    cells = [c.strip() for c in line.split('|')[1:-1]]
    
    if 'keV' in line and 'Egamma' in line or 'Eg' in line:
        print(f"Line {line_num}: [HEADER]")
        for i, cell in enumerate(cells, 1):
            print(f"    Col {i}: {cell[:50]}")
        headers = cells
        continue
    
    if any(x.isdigit() for x in cells[0]) or cells[0].startswith('('):
        data_rows.append({
            'line': line_num,
            'cells': cells,
            'raw': line.rstrip()
        })

print(f"\nTotal data rows: {len(data_rows)}")

# Step 2: Extract canonical level registry
print("\n" + "=" * 100)
print("STEP 2: CANONICAL LEVEL REGISTRY (from Ei column)")
print("-" * 100)

level_registry = {}

for row in data_rows:
    cells = row['cells']
    if len(cells) < 3:
        continue
    
    ei_raw = cells[2].strip()
    if not ei_raw or '---' in ei_raw or ei_raw == '-':
        continue
    
    match = re.match(r'([\d.]+)\((\d+)\)', ei_raw)
    if match:
        ei_numeric = float(match.group(1))
        ei_uncertainty = match.group(2)
        jpi_i_raw = cells[1].strip()
        
        if ei_numeric not in level_registry:
            level_registry[ei_numeric] = {
                'ei_str': match.group(1),
                'ei_uncertainty': ei_uncertainty,
                'ei_raw': ei_raw,
                'jpi_i': jpi_i_raw,
                'occurrences': []
            }
        
        level_registry[ei_numeric]['occurrences'].append({
            'line': row['line'],
            'eg_raw': cells[0].strip(),
            'jpi_transition': jpi_i_raw
        })

print(f"Unique level energies in Ei: {len(level_registry)}")

# Step 3: Occurrence Scan
print("\n" + "=" * 100)
print("STEP 3: OCCURRENCE SCAN - CONSISTENCY CHECK")
print("-" * 100)

inconsistencies = []

for ei_numeric in sorted(level_registry.keys()):
    level_data = level_registry[ei_numeric]
    occurrences = level_data['occurrences']
    
    if len(occurrences) <= 1:
        continue
    
    print(f"\n[MULTI-OCCURRENCE] Level: E_i = {level_data['ei_raw']} keV")
    print(f"  Jpi_i = {level_data['jpi_i']}")
    print(f"  Found {len(occurrences)} occurrence(s):")
    
    first_ei_raw = level_data['ei_raw']
    first_jpi_i = level_data['jpi_i']
    
    for occ in occurrences:
        print(f"    Line {occ['line']}: Egamma={occ['eg_raw']:<10}")
        
        for row in data_rows:
            if row['line'] != occ['line']:
                continue
            
            cells = row['cells']
            ei_from_row = cells[2].strip()
            jpi_from_row = cells[1].strip()
            
            if ei_from_row != first_ei_raw:
                print(f"      [ERROR] ENERGY MISMATCH: '{ei_from_row}' vs '{first_ei_raw}'")
                inconsistencies.append({
                    'level': ei_numeric,
                    'type': 'energy',
                    'line': occ['line'],
                    'value': ei_from_row,
                    'expected': first_ei_raw
                })
            
            jpi_i_only = jpi_from_row.split('\\to')[0].strip() if '\\to' in jpi_from_row else jpi_from_row.strip()
            first_jpi_i_only = first_jpi_i.split('\\to')[0].strip() if '\\to' in first_jpi_i else first_jpi_i.strip()
            
            jpi_i_clean = jpi_i_only.replace('$', '').strip()
            first_jpi_i_clean = first_jpi_i_only.replace('$', '').strip()
            
            if jpi_i_clean != first_jpi_i_clean:
                print(f"      [ERROR] Jpi MISMATCH: '{jpi_i_clean}' vs '{first_jpi_i_clean}'")
                print(f"              Full transition: {jpi_from_row}")
                inconsistencies.append({
                    'level': ei_numeric,
                    'type': 'jpi',
                    'line': occ['line'],
                    'value': jpi_i_clean,
                    'expected': first_jpi_i_clean,
                    'full_jpi': jpi_from_row
                })
            break

# Step 4: Report
print("\n" + "=" * 100)
print("STEP 4: INCONSISTENCY REPORT")
print("=" * 100)

if not inconsistencies:
    print("\n[PASS] NO INCONSISTENCIES FOUND")
else:
    print(f"\n[FAIL] FOUND {len(inconsistencies)} INCONSISTENCIES:\n")
    
    by_level = defaultdict(list)
    for inc in inconsistencies:
        by_level[inc['level']].append(inc)
    
    for level_ei in sorted(by_level.keys()):
        print(f"\nLEVEL: E_i = {level_ei} keV")
        print("-" * 80)
        
        for inc in by_level[level_ei]:
            print(f"  Line {inc['line']}: {inc['type'].upper()} MISMATCH")
            print(f"    Found:    {inc['value']}")
            print(f"    Expected: {inc['expected']}")
            if 'full_jpi' in inc:
                print(f"    Full: {inc['full_jpi']}")

# Step 5: Summary
print("\n" + "=" * 100)
print("STEP 5: COMPLETENESS AND SUMMARY")
print("=" * 100)

print(f"\nData rows checked: {len(data_rows)}")
print(f"Unique level energies: {len(level_registry)}")
print(f"Levels with multiple occurrences: {sum(1 for v in level_registry.values() if len(v['occurrences']) > 1)}")

if inconsistencies:
    print(f"\n[FAIL] INTERNAL DATA CONSISTENCY: FAILED")
    print(f"  {len(inconsistencies)} inconsistencies detected in markdown source table")
    print(f"\n  Analysis: The markdown table has level energies appearing multiple times")
    print(f"  with DIFFERENT Jpi notation (parenthetical vs plain form).")
    print(f"\n  This indicates a source data error in the published table that must be")
    print(f"  resolved before proceeding with ENSDF data entry.")
else:
    print(f"\n[PASS] INTERNAL DATA CONSISTENCY: PASSED")
