#!/usr/bin/env python3
"""
ENSDF Verification Script - 2025LAAA vs 2012DI06 Placement Table Verification
==============================================================================

This script verifies that the 47 gamma transitions in the 2025LAAA placement table
are correctly placed in the ENSDF file. It does NOT assume the ENSDF file should
only contain these 47 gammas - other legitimate gammas may exist.

The script only checks:
1. Each of the 47 placement table gammas exists in the ENSDF file
2. Each gamma is placed under the correct initial level energy
3. Reports any misplacements or missing gammas

It does NOT:
- Count total gammas in ENSDF file
- Assume extra gammas are wrong
- Add or remove any gammas

Author: Nuclear Data Verification System
Date: September 2025
"""

import re
import sys

def read_placement_table(filename):
    """Read the placement table and extract valid gamma placements"""
    placements = []
    
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"ERROR: Placement table file '{filename}' not found")
        return []
    
    for line in lines:
        # Skip headers, dashes, and TBD entries
        if ('ELI' in line or '---' in line or 'TBD' in line or 
            'keV' in line or 'FINAL TABLE' in line or line.strip() == ''):
            continue
            
        # Look for data lines with energy values
        if re.match(r'^\s*\d+\.\d+', line):
            parts = line.strip().split('|')
            if len(parts) >= 7:
                try:
                    eli = float(parts[0].strip())
                    ji = parts[1].strip()
                    elf = float(parts[2].strip())
                    jf = parts[3].strip()
                    eg_2012 = float(parts[4].strip())
                    ri_2012 = parts[5].strip()
                    eg_2025 = float(parts[6].strip())
                    
                    placements.append({
                        'eli': eli,
                        'ji': ji,
                        'elf': elf,
                        'jf': jf,
                        'eg_2012': eg_2012,
                        'ri_2012': ri_2012,
                        'eg_2025': eg_2025
                    })
                except (ValueError, IndexError):
                    continue
    
    return placements

def read_ensdf_structure(filename):
    """Read ENSDF file and extract level and gamma structure"""
    levels = {}  # energy -> {jp, gammas: []}
    current_level = None
    
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"ERROR: ENSDF file '{filename}' not found")
        return {}
    
    for line in lines:
        if len(line) < 8:
            continue
            
        # Level record
        if line[7:8] == 'L':
            energy_str = line[9:19].strip()
            jp_str = line[21:39].strip()
            
            if energy_str:
                try:
                    energy = float(energy_str)
                    if energy not in levels:
                        levels[energy] = {'jp': jp_str, 'gammas': []}
                    current_level = energy
                except ValueError:
                    continue
        
        # Gamma record
        elif line[7:8] == 'G' and current_level is not None:
            energy_str = line[9:19].strip()
            if energy_str:
                try:
                    gamma_energy = float(energy_str)
                    levels[current_level]['gammas'].append(gamma_energy)
                except ValueError:
                    continue
    
    return levels

def verify_placements(placement_table_file, ensdf_file):
    """Verify that placement table gammas are correctly placed in ENSDF file"""
    
    print("ENSDF PLACEMENT VERIFICATION - 2025LAAA vs 2012DI06")
    print("=" * 60)
    
    # Read data
    placements = read_placement_table(placement_table_file)
    ensdf_levels = read_ensdf_structure(ensdf_file)
    
    if not placements:
        print("ERROR: No valid placements found in placement table")
        return False
    
    if not ensdf_levels:
        print("ERROR: No valid structure found in ENSDF file")
        return False
    
    print(f"Placement table: {len(placements)} gamma transitions")
    print(f"ENSDF file: {len(ensdf_levels)} levels")
    print()
    
    errors = 0
    
    # Check each placement
    for i, placement in enumerate(placements):
        eli = placement['eli']
        eg_2025 = placement['eg_2025']
        
        print(f"Checking {eg_2025} keV gamma:")
        print(f"  Should be under: {eli} keV ({placement['ji']})")
        
        # Find the initial level in ENSDF
        level_found = False
        gamma_found = False
        
        # Look for exact or very close level energy match
        for level_energy in ensdf_levels.keys():
            if abs(level_energy - eli) < 0.1:  # Within 0.1 keV
                level_found = True
                print(f"  Level found: {level_energy} keV")
                
                # Look for gamma in this level
                for gamma_energy in ensdf_levels[level_energy]['gammas']:
                    if abs(gamma_energy - eg_2025) < 0.1:  # Within 0.1 keV
                        gamma_found = True
                        print(f"  ✅ CORRECT: Gamma {gamma_energy} keV found under {level_energy} keV")
                        break
                
                if not gamma_found:
                    print(f"  ❌ ERROR: Gamma {eg_2025} keV NOT found under level {level_energy} keV")
                    print(f"    Available gammas: {ensdf_levels[level_energy]['gammas']}")
                    errors += 1
                break
        
        if not level_found:
            print(f"  ❌ ERROR: Initial level {eli} keV not found in ENSDF file")
            errors += 1
        
        print()
    
    print("=" * 60)
    print(f"VERIFICATION SUMMARY: {errors} ERRORS FOUND")
    
    if errors == 0:
        print("✅ ALL PLACEMENT TABLE GAMMAS ARE CORRECTLY PLACED")
    else:
        print(f"❌ {errors} PLACEMENT ERRORS NEED TO BE FIXED")
    
    return errors == 0

if __name__ == "__main__":
    placement_file = "XUNDL/2025LAAA_vs_2012DI06.ens"
    ensdf_file = "XUNDL/2025LAAA_CH11036_127I.ens"
    
    verify_placements(placement_file, ensdf_file)
