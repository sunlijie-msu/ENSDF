#!/usr/bin/env python3
"""Data consistency check for 125I gamma transitions markdown table."""

import re
from collections import defaultdict

file_path = r'd:\X\ND\ENSDF\XUNDL\2026XUAA_CQ11029_125I.md'

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Parse all data rows
data_rows = []
level_jpi = {}  # level_E -> {ji: set(), jf: set(), rows_as_ji: [], rows_as_jf: []}

row_idx = 0
for line_num, line in enumerate(lines, 1):
    # Skip headers
    if '---' in line or 'Eγ' in line or 'Gamma' in line:
        continue
    
    # Match data rows
    if line.strip().startswith('|') and '---' not in line:
        parts = [p.strip() for p in line.split('|')]
        parts = [p for p in parts if p]
        
        if len(parts) >= 7:
            try:
                egamma = float(parts[0])
                einit = float(parts[1])
                jijf_str = parts[3]
                
                # Parse Ji → Jf (use both ASCII and Unicode arrows)
                jijf_split = re.split(r'→|→', jijf_str)
                if len(jijf_split) >= 2:
                    ji = jijf_split[0].strip()
                    jf = jijf_split[1].strip()
                    
                    # Calculate expected final level energy
                    efinal_expected = round(einit - egamma, 1)
                    
                    data_rows.append({
                        'line': line_num,
                        'egamma': egamma,
                        'einit': einit,
                        'efinal_exp': efinal_expected,
                        'ji': ji,
                        'jf': jf
                    })
                    
                    # Track level Jπ
                    if einit not in level_jpi:
                        level_jpi[einit] = {'ji': set(), 'jf': set(), 'ji_rows': [], 'jf_rows': []}
                    level_jpi[einit]['ji'].add(ji)
                    level_jpi[einit]['ji_rows'].append(line_num)
                    
                    if efinal_expected not in level_jpi:
                        level_jpi[efinal_expected] = {'ji': set(), 'jf': set(), 'ji_rows': [], 'jf_rows': []}
                    level_jpi[efinal_expected]['jf'].add(jf)
                    level_jpi[efinal_expected]['jf_rows'].append(line_num)
                    
                    row_idx += 1
            except (ValueError, IndexError):
                pass

print(f"Total rows parsed: {len(data_rows)}")
print(f"Total levels found: {len(level_jpi)}\n")

# === CHECK 1: Jπ CONSISTENCY ===
print("=" * 80)
print("CHECK 1: JPπ CONSISTENCY")
print("=" * 80)

jpi_mismatches = []
for level_e in sorted(level_jpi.keys()):
    level_info = level_jpi[level_e]
    ji_vals = level_info['ji']
    jf_vals = level_info['jf']
    
    # If level appears as both initial and final
    if ji_vals and jf_vals:
        all_vals = ji_vals | jf_vals
        if len(all_vals) > 1:
            jpi_mismatches.append((level_e, ji_vals, jf_vals))

if jpi_mismatches:
    print(f"\n⚠️  FOUND {len(jpi_mismatches)} LEVELS WITH INCONSISTENT Jπ:\n")
    for level_e, ji_set, jf_set in sorted(jpi_mismatches):
        print(f"  ❌ E = {level_e:.1f} keV:")
        print(f"     As Ji (initial):     {', '.join(sorted(ji_set))}")
        print(f"     As Jf (final):       {', '.join(sorted(jf_set))}")
        print()
else:
    print("\n✓ PASS: All levels have consistent Jπ values.\n")

# === CHECK 2: ENERGY CONSERVATION ===
print("=" * 80)
print("CHECK 2: ENERGY CONSERVATION (Efinal ≈ Einitial - Egamma)")
print("=" * 80)

tolerance = 1.0
energy_mismatches = []

for row in data_rows:
    eg = row['egamma']
    ei = row['einit']
    jf_expected = row['jf']
    ef_calc = row['efinal_exp']
    
    # Find actual final level in table with matching Jf and closest energy
    best_match = None
    best_dev = float('inf')
    
    for level_e, level_info in level_jpi.items():
        if jf_expected in level_info['jf']:
            dev = abs(level_e - ef_calc)
            if dev < best_dev:
                best_dev = dev
                best_match = level_e
    
    if best_match is not None and best_dev > tolerance:
        energy_mismatches.append({
            'line': row['line'],
            'egamma': eg,
            'einit': ei,
            'efinal_calc': ef_calc,
            'efinal_actual': best_match,
            'deviation': best_dev,
            'jf': jf_expected
        })

if energy_mismatches:
    print(f"\n⚠️  FOUND {len(energy_mismatches)} TRANSITIONS WITH ENERGY MISMATCH > {tolerance} keV:\n")
    for m in sorted(energy_mismatches, key=lambda x: x['deviation'], reverse=True)[:15]:
        print(f"  ❌ Line {m['line']}: Eγ = {m['egamma']:.1f} keV")
        print(f"     Einit = {m['einit']:.1f} keV  →  Efinal_calc = {m['efinal_calc']:.1f} keV")
        print(f"     BUT level with Jf={m['jf']} found at E = {m['efinal_actual']:.1f} keV")
        print(f"     Δ = {m['deviation']:.2f} keV (exceeds tolerance)")
        print()
else:
    print(f"\n✓ PASS: All transitions satisfy energy conservation (tolerance: ±{tolerance} keV).\n")

# === FINAL SUMMARY ===
print("=" * 80)
print("COMPLIANCE CHECKLIST")
print("=" * 80)
print(f"Total rows analyzed:           {len(data_rows)}")
print(f"Unique levels:                 {len(level_jpi)}")
print(f"Jπ consistency violations:     {len(jpi_mismatches)}")
print(f"Energy conservation violations: {len(energy_mismatches)}")
print("\nStatus:")
if len(jpi_mismatches) == 0 and len(energy_mismatches) == 0:
    print("  ✓ ALL CHECKS PASSED")
else:
    print("  ⚠️  ERRORS DETECTED - SEE ABOVE FOR DETAILS")
print("=" * 80)
