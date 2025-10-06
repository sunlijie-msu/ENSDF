"""
Map ENSDF resonance section against CSV extraction to identify ALL duplicate G-records,
wrong L-energies, and create systematic correction plan.
"""

import re
import sys
from pathlib import Path

def parse_ensdf_resonances(ensdf_file):
    """Parse resonance section of ENSDF file (lines 157-853)"""
    with open(ensdf_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Start from line 157 (index 156) - resonance section
    resonance_lines = lines[156:]
    
    levels = []
    current_level = None
    
    for idx, line in enumerate(resonance_lines, start=157):
        if len(line) < 10:
            continue
        
        record_type = line[7] if len(line) > 7 else ' '
        
        if record_type == 'L':
            # Save previous level if exists
            if current_level is not None:
                levels.append(current_level)
            
            # Parse new L-record
            try:
                # Energy at columns 10-19
                e_str = line[9:19].strip()
                e_val = float(e_str) if e_str else None
                
                # Ep at columns 65-74 (S-field for resonances)
                ep_str = line[64:74].strip()
                ep_val = float(ep_str) if ep_str else None
                
                current_level = {
                    'line_number': idx,
                    'energy': e_val,
                    'ep': ep_val,
                    'gammas': [],
                    'l_record': line.rstrip()
                }
            except (ValueError, IndexError):
                print(f"WARNING: Cannot parse L-record at line {idx}")
                continue
        
        elif record_type == 'G' and current_level is not None:
            # Parse G-record
            try:
                # Gamma energy at columns 10-19
                eg_str = line[9:19].strip()
                eg_val = float(eg_str) if eg_str else None
                
                # RI at columns 23-29
                ri_str = line[22:29].strip()
                ri_val = float(ri_str) if ri_str else None
                
                current_level['gammas'].append({
                    'line_number': idx,
                    'energy': eg_val,
                    'ri': ri_val,
                    'g_record': line.rstrip()
                })
            except (ValueError, IndexError):
                print(f"WARNING: Cannot parse G-record at line {idx}")
                continue
    
    # Don't forget last level
    if current_level is not None:
        levels.append(current_level)
    
    return levels

def load_csv_extraction():
    """Load CSV extraction data from previous script output"""
    # This data is from extract_resonances_1976me12.py output
    # Hardcoded for speed - would parse output file in production
    
    csv_data = {}
    
    # Map Ep -> expected Exi and gammas
    # From extraction output, we know:
    # Level 10: Ep=1165, Exi=7505, 10 gammas
    
    csv_data[1165.0] = {
        'exi': 7505.0,
        'gammas': [2495.0, 3324.9, 3445.6, 3560.9, 4341.1, 4501.3, 4860.3, 5741.6, 6285.7, 7505.0]
    }
    
    csv_data[1112.2] = {
        'exi': 7452.4,  # Need to verify from CSV
        'gammas': []  # Unknown - need to extract
    }
    
    csv_data[1181.4] = {
        'exi': 7519.6,  # Need to verify from CSV
        'gammas': []  # Unknown - need to extract
    }
    
    # NOTE: This is incomplete - full implementation would parse all 48 CSV rows
    # For now, focus on the three problematic levels
    
    return csv_data

def find_duplicates(ensdf_levels):
    """Find duplicate G-record sets"""
    
    # Create signature for each level's gamma set
    gamma_signatures = {}
    
    for level in ensdf_levels:
        # Create signature from gamma energies + RIs
        sig_parts = []
        for gamma in level['gammas']:
            sig_parts.append(f"{gamma['energy']:.1f}_{gamma['ri']}")
        
        signature = "|".join(sorted(sig_parts))
        
        if signature not in gamma_signatures:
            gamma_signatures[signature] = []
        
        gamma_signatures[signature].append(level)
    
    # Find duplicates (signatures with multiple levels)
    duplicates = {}
    for sig, levels_list in gamma_signatures.items():
        if len(levels_list) > 1:
            duplicates[sig] = levels_list
    
    return duplicates

def main():
    ensdf_file = Path(r"d:\X\ND\ENSDF\A35\Cl35\temp\1976ME12.ens")
    
    print("=" * 80)
    print("MAPPING ENSDF RESONANCES AGAINST CSV EXTRACTION")
    print("=" * 80)
    print()
    
    # Parse ENSDF
    print("Parsing ENSDF resonance section...")
    ensdf_levels = parse_ensdf_resonances(ensdf_file)
    print(f"Found {len(ensdf_levels)} levels in ENSDF resonance section")
    print()
    
    # Find duplicates
    print("Searching for duplicate G-record patterns...")
    duplicates = find_duplicates(ensdf_levels)
    
    if not duplicates:
        print("No duplicate G-record patterns found (UNEXPECTED!)")
        return 0
    
    print(f"Found {len(duplicates)} duplicate G-record patterns")
    print()
    
    # Analyze each duplicate pattern
    for dup_idx, (sig, levels_list) in enumerate(duplicates.items(), start=1):
        print(f"\n--- DUPLICATE PATTERN #{dup_idx} ---")
        print(f"Number of levels with identical gamma set: {len(levels_list)}")
        print(f"Gamma signature: {sig[:80]}...")
        print()
        
        for level in levels_list:
            print(f"  Level at line {level['line_number']}:")
            print(f"    L-energy: {level['energy']} keV")
            print(f"    Ep: {level['ep']} keV")
            print(f"    Gammas: {len(level['gammas'])} transitions")
            
            # Show first 3 gammas
            for gamma in level['gammas'][:3]:
                print(f"      Line {gamma['line_number']}: E={gamma['energy']} keV, RI={gamma['ri']}")
            
            if len(level['gammas']) > 3:
                print(f"      ... ({len(level['gammas']) - 3} more gammas)")
            print()
    
    # Detailed analysis of the known problematic case (Ep=1165)
    print("\n" + "=" * 80)
    print("DETAILED ANALYSIS: Ep=1165 keV case")
    print("=" * 80)
    print()
    
    # Find levels with Ep ~1165
    ep_target = 1165.0
    matching_levels = [lvl for lvl in ensdf_levels if lvl['ep'] and abs(lvl['ep'] - ep_target) < 1.0]
    
    if matching_levels:
        for level in matching_levels:
            print(f"ENSDF Level at line {level['line_number']}:")
            print(f"  L-energy: {level['energy']} keV (CSV expects 7505.0 keV)")
            print(f"  Ep: {level['ep']} keV")
            print(f"  Gammas: {len(level['gammas'])}")
            
            # Expected gammas from CSV
            expected = [2495.0, 3324.9, 3445.6, 3560.9, 4341.1, 4501.3, 4860.3, 5741.6, 6285.7, 7505.0]
            actual = [g['energy'] for g in level['gammas']]
            
            if actual == expected:
                print(f"  GAMMA MATCH: Gammas match CSV extraction perfectly!")
            else:
                print(f"  GAMMA MISMATCH!")
                print(f"    Expected: {expected}")
                print(f"    Actual: {actual}")
            
            # Energy error
            if level['energy']:
                error = level['energy'] - 7505.0
                print(f"  L-ENERGY ERROR: {error:+.1f} keV (ENSDF - CSV)")
            print()
    
    print("=" * 80)
    print("CORRECTION PLAN:")
    print("=" * 80)
    print()
    print("1. For each duplicate pattern:")
    print("   - Identify which level should have which gamma set (using Ep matching)")
    print("   - Delete duplicate G-record blocks")
    print("   - Correct L-record energies to match CSV Exi values")
    print()
    print("2. Systematic approach:")
    print("   - Match ENSDF Ep to CSV Ep (unique identifier)")
    print("   - Use CSV Exi as correct L-energy value")
    print("   - Use CSV gamma energies as correct G-record values")
    print("   - Delete any G-records that don't match CSV for that Ep")
    print()
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
