#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Value Occurrence Check for markdown table - CHECK FOR INTERNAL CONSISTENCY
Verifies that every level energy appearing multiple times in the markdown table
has consistent energy, uncertainty, and J-π across all occurrences.
"""

import re
from collections import defaultdict
import sys
sys.stdout.reconfigure(encoding='utf-8')

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
    if '###' in line:  # Title line
        continue
    if '| :---' in line:  # Separator line
        print(f"Line {line_num}: [SEPARATOR - skip]")
        continue
    if not line.startswith('|'):
        continue
    
    # Parse header or data row
    cells = [c.strip() for c in line.split('|')[1:-1]]
    
    if 'keV' in line and '→' not in line and 'Eγ' in line:
        # Header row
        print(f"Line {line_num}: [HEADER]")
        print(f"  Columns: {len(cells)}")
        for i, cell in enumerate(cells, 1):
            print(f"    Col {i}: {cell[:50]}")
        headers = cells
        continue
    
    if any(x.isdigit() for x in cells[0]) or cells[0].startswith('('):
        # Data row
        data_rows.append({
            'line': line_num,
            'cells': cells,
            'raw': line.rstrip()
        })

print(f"\nTotal header rows: 1")
print(f"Total data rows: {len(data_rows)}")

# Step 2: Extract canonical level registry from Ei column (explicit initial state energies)
print("\n" + "=" * 100)
print("STEP 2: CANONICAL LEVEL REGISTRY (from Ei column)")
print("-" * 100)

level_registry = {}  # ei_numeric -> {energy_str, uncertainty, jpi_i}

for row in data_rows:
    cells = row['cells']
    if len(cells) < 3:
        continue
    
    ei_raw = cells[2].strip()  # Ei column
    if not ei_raw or '–' in ei_raw:
        continue
    
    # Parse Ei: format like "6461.6(4)", "1472.6(2)", etc.
    match = re.match(r'([\d.]+)\((\d+)\)', ei_raw)
    if match:
        ei_numeric = float(match.group(1))
        ei_uncertainty = match.group(2)
        
        jpi_i_raw = cells[1].strip()  # Jπi column
        
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

print(f"Unique level energies in Ei: {len(level_registry)}\n")

# Step 3: Occurrence Scan - check consistency
print("=" * 100)
print("STEP 3: OCCURRENCE SCAN - CONSISTENCY CHECK")
print("-" * 100)

inconsistencies = []

for ei_numeric in sorted(level_registry.keys()):
    level_data = level_registry[ei_numeric]
    occurrences = level_data['occurrences']
    
    if len(occurrences) <= 1:
        continue  # No multi-occurrence
    
    print(f"\n[OK] LEVEL: E_i = {level_data['ei_raw']} keV (Jpi_i = {level_data['jpi_i']})")
    print(f"  Found {len(occurrences)} occurrence(s):")
    
    # Check if all occurrences have identical energy and uncertainty
    first_ei_raw = level_data['ei_raw']
    first_jpi_i = level_data['jpi_i']
    
    for occ in occurrences:
        print(f"    Line {occ['line']}: Eγ={occ['eg_raw']:<10} Jπ_i→f={occ['jpi_transition']}")
        
        # Extract from table row for this occurrence
        for row in data_rows:
            if row['line'] != occ['line']:
                continue
            
            cells = row['cells']
            ei_from_row = cells[2].strip()
            jpi_from_row = cells[1].strip()
            
            # Check energy consistency
            if ei_from_row != first_ei_raw:
                print(f"      [ERROR] ENERGY MISMATCH: '{ei_from_row}' vs. '{first_ei_raw}'")
                inconsistencies.append({
                    'level': ei_numeric,
                    'type': 'energy',
                    'line': occ['line'],
                    'value': ei_from_row,
                    'expected': first_ei_raw
                })
            
            # Check Jπ consistency (character-for-character)
            # Extract just the Jπ_i part (before the arrow)
            jpi_i_only = jpi_from_row.split('\\to')[0].strip() if '\\to' in jpi_from_row else jpi_from_row.strip()
            first_jpi_i_only = first_jpi_i.split('\\to')[0].strip() if '\\to' in first_jpi_i else first_jpi_i.strip()
            
            # Remove LaTeX dollar signs for comparison
            jpi_i_clean = jpi_i_only.replace('$', '').strip()
            first_jpi_i_clean = first_jpi_i_only.replace('$', '').strip()
            
            if jpi_i_clean != first_jpi_i_clean:
                print(f"      [ERROR] Jpi MISMATCH: '{jpi_i_clean}' vs. '{first_jpi_i_clean}'")
                inconsistencies.append({
                    'level': ei_numeric,
                    'type': 'jpi',
                    'line': occ['line'],
                    'value': jpi_i_clean,
                    'expected': first_jpi_i_clean,
                    'full_jpi': jpi_from_row
                })
            break

# Step 4: Final Consistency Report
print("\n" + "=" * 100)
print("STEP 4: INCONSISTENCY REPORT")
print("=" * 100)

if not inconsistencies:
    print("\n[OK] NO INCONSISTENCIES FOUND")
else:
    print(f"\n[ERROR] FOUND {len(inconsistencies)} INCONSISTENCIES:\n")
    
    # Group by level energy
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
                print(f"    Full Jπ transition: {inc['full_jpi']}")

# Step 5: Completeness Check
print("\n" + "=" * 100)
print("STEP 5: COMPLETENESS CHECK")
print("=" * 100)

print(f"\n[OK] Data rows checked: {len(data_rows)}")
print(f"[OK] Unique level energies: {len(level_registry)}")
print(f"[OK] Levels with multiple occurrences: {sum(1 for v in level_registry.values() if len(v['occurrences']) > 1)}")
print(f"[OK] Total occurrences checked: {sum(len(v['occurrences']) for v in level_registry.values())}")

# Summary
print("\n" + "=" * 100)
print("SUMMARY")
print("=" * 100)

if inconsistencies:
    print(f"\n[FAIL] INTERNAL DATA CONSISTENCY: FAILED")
    print(f"  {len(inconsistencies)} inconsistencies found in markdown source table")
    print(f"\n  Root cause: The markdown table has the same level energy appearing multiple")
    print(f"  times with DIFFERENT Jpi notation (parenthetical vs. plain).")
    print(f"\n  Action required: Verify which Jpi is correct for each occurrence and")
    print(f"  resolve the inconsistency in the source publication/table.")
else:
    print("\n[PASS] INTERNAL DATA CONSISTENCY: PASSED")
    print(f"  All level energies appearing multiple times have consistent values.")
