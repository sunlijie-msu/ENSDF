#!/usr/bin/env python3
"""
Verify DE uncertainty corrections for 1976ME12.ens file
Compare current DE values with reference data to determine what corrections are still needed
"""

import re
import os

def read_ensdf_file(filename):
    """Read the ENSDF file and extract L-record data"""
    l_records = []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                if len(line) >= 8 and line[7] == 'L' and line[8] == ' ':
                    # Extract energy (cols 10-19) and DE (cols 20-21)
                    energy_str = line[9:19].strip()
                    de_str = line[19:21].strip()
                    
                    if energy_str:
                        try:
                            energy = float(energy_str)
                            de_val = de_str if de_str else "NONE"
                            l_records.append({
                                'line': line_num,
                                'energy': energy,
                                'de_field': de_str,
                                'de_display': de_val,
                                'full_line': line.rstrip()
                            })
                        except ValueError:
                            continue
    except FileNotFoundError:
        print(f"ERROR: File {filename} not found")
        return []
    
    return l_records

def main():
    # Reference data from user - correct uncertainties in keV
    reference_data = {
        744.8: 0.1,    1219.3: 0.1,   1763.4: 0.7,   2644.7: 1.3,   2694.7: 1.2,
        3003.7: 0.8,   3058.9: 0.8,   3164.3: 0.8,   3348.7: 0.9,   3400.7: 0.9,
        3558.1: 1.4,   3589.8: 1.4,   3622.7: 1.2,   3734.7: 1.2,   3784.1: 0.9,
        3806.1: 2.0,   3874.1: 1.0,   3899.1: 1.0,   3928.1: 1.0,   3966.1: 1.0,
        4114.0: 1.0,   4174.7: 1.0,   4180.1: 1.5,   4347.2: 1.2,   4624.2: 2.0,
        4766.9: 1.5,   4880.2: 1.5,   4928.2: 1.5,   5184.2: 2.0,   5251.2: 3.0,
        5380.2: 3.0,   5522.2: 3.0,   5557.2: 3.0
    }
    
    # Read current file
    filename = "d:/X/ND/ENSDF/A35/Cl35/temp/1976ME12.ens"
    current_data = read_ensdf_file(filename)
    
    print("DE Field Correction Analysis")
    print("=" * 50)
    print("Energy   | Current DE | Reference | Expected DE | Status")
    print("-" * 50)
    
    corrections_needed = []
    correct_count = 0
    
    for record in current_data:
        energy = record['energy']
        current_de = record['de_field']
        
        if energy in reference_data:
            ref_uncertainty = reference_data[energy]
            
            # Convert reference uncertainty to ENSDF DE field value
            # For 1 decimal place energies: uncertainty * 10 = DE field value
            if '.' in str(energy) and len(str(energy).split('.')[1]) == 1:
                expected_de = int(ref_uncertainty * 10)
            else:
                expected_de = int(ref_uncertainty)
            
            expected_de_str = str(expected_de) if expected_de >= 10 else f"{expected_de} "
            
            if current_de == str(expected_de) or current_de == expected_de_str.strip():
                status = "CORRECT"
                correct_count += 1
            else:
                status = "NEEDS FIX"
                corrections_needed.append({
                    'energy': energy,
                    'line': record['line'],
                    'current_de': current_de,
                    'expected_de': expected_de_str,
                    'ref_uncertainty': ref_uncertainty
                })
            
            print(f"{energy:7.1f} | {current_de:10s} | {ref_uncertainty:8.1f} | {expected_de_str:10s} | {status}")
    
    print("=" * 50)
    print(f"Summary: {correct_count} correct, {len(corrections_needed)} need correction")
    
    if corrections_needed:
        print("\nCorrections still needed:")
        print("-" * 30)
        for fix in corrections_needed:
            print(f"Line {fix['line']:3d}: {fix['energy']:7.1f} keV - DE '{fix['current_de']}' → '{fix['expected_de'].strip()}'")
    else:
        print("\nSUCCESS: All DE fields are correctly formatted!")

if __name__ == "__main__":
    main()