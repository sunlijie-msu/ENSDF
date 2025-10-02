#!/usr/bin/env python3
"""
CRITICAL VERIFICATION: Check all 33 reference levels against 1976ME12.ens file
User provided corrected reference data - must verify 100% matching
"""

import re
import os

def read_ensdf_file(filename):
    """Read the ENSDF file and extract L-record data with exact positioning"""
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
    # CORRECTED reference data from user - all 33 levels
    reference_data = {
        1219.3: 0.1,   1763.4: 0.7,   2644.7: 1.3,   2694.7: 1.2,   3003.7: 0.8,
        3163.9: 0.7,   3920.7: 1.3,   3944.1: 1.1,   3979.0: 1.5,   4059.4: 0.4,
        4114.0: 1.0,   4174.7: 1.0,   4180.1: 1.5,   4347.2: 1.2,   4624.2: 2.0,
        4766.9: 1.5,   4841.7: 1.9,   4855.7: 1.9,   4885.0: 2.0,   5010.4: 1.8,
        5166.7: 1.5,   5216.2: 1.5,   5403.6: 1.0,   5586.0: 2.0,   5600.1: 1.5,
        5646.0: 2.0,   5656.0: 2.0,   5683.0: 2.0,   5759.0: 3.0,   5806.0: 2.0,
        6107.2: 1.5,   6181.0: 3.0,   6493.0: 3.0
    }
    
    # Read current file
    filename = "d:/X/ND/ENSDF/A35/Cl35/temp/1976ME12.ens"
    current_data = read_ensdf_file(filename)
    
    print("CRITICAL VERIFICATION: 33 Reference Levels vs File")
    print("=" * 60)
    print("Energy   | File DE | Ref dEx | Expected DE | Status      | Line")
    print("-" * 60)
    
    missing_levels = []
    incorrect_de = []
    correct_count = 0
    
    # Create lookup for current data by energy
    current_lookup = {}
    for record in current_data:
        energy = record['energy']
        # Handle floating point precision issues
        for ref_energy in reference_data.keys():
            if abs(energy - ref_energy) < 0.1:
                current_lookup[ref_energy] = record
                break
    
    # Check each reference level
    for ref_energy in sorted(reference_data.keys()):
        ref_uncertainty = reference_data[ref_energy]
        
        if ref_energy in current_lookup:
            record = current_lookup[ref_energy]
            current_de = record['de_field']
            
            # Convert reference uncertainty to ENSDF DE field value
            # For decimal energies: multiply uncertainty by 10 for DE field
            if '.' in str(ref_energy):
                expected_de = int(ref_uncertainty * 10)
            else:
                expected_de = int(ref_uncertainty)
            
            expected_de_str = str(expected_de) if expected_de >= 10 else f"{expected_de} "
            
            # Check if current DE matches expected
            current_de_clean = current_de.strip() if current_de else ""
            expected_de_clean = str(expected_de)
            
            if current_de_clean == expected_de_clean:
                status = "CORRECT"
                correct_count += 1
            else:
                status = "WRONG DE"
                incorrect_de.append({
                    'energy': ref_energy,
                    'line': record['line'],
                    'current_de': current_de,
                    'expected_de': expected_de_clean,
                    'ref_uncertainty': ref_uncertainty
                })
            
            print(f"{ref_energy:7.1f} | {current_de:7s} | {ref_uncertainty:6.1f} | {expected_de_clean:10s} | {status:10s} | {record['line']:4d}")
        else:
            status = "MISSING"
            missing_levels.append(ref_energy)
            print(f"{ref_energy:7.1f} | {'N/A':7s} | {ref_uncertainty:6.1f} | {'N/A':10s} | {status:10s} | N/A")
    
    print("=" * 60)
    print(f"SUMMARY:")
    print(f"  Reference levels: {len(reference_data)}")
    print(f"  Found in file: {len(reference_data) - len(missing_levels)}")
    print(f"  Missing from file: {len(missing_levels)}")
    print(f"  Correct DE values: {correct_count}")
    print(f"  Wrong DE values: {len(incorrect_de)}")
    
    if missing_levels:
        print(f"\nCRITICAL: MISSING LEVELS ({len(missing_levels)}):")
        for energy in sorted(missing_levels):
            print(f"  {energy:7.1f} keV - NOT FOUND IN FILE")
    
    if incorrect_de:
        print(f"\nDE CORRECTIONS NEEDED ({len(incorrect_de)}):")
        for fix in incorrect_de:
            print(f"  Line {fix['line']:3d}: {fix['energy']:7.1f} keV - DE '{fix['current_de']}' should be '{fix['expected_de']}'")
    
    if not missing_levels and not incorrect_de:
        print("\nSUCCESS: All 33 reference levels found with correct DE values!")
    else:
        print(f"\nPROBLEMS FOUND: {len(missing_levels)} missing + {len(incorrect_de)} wrong DE values")
        print("ACTION REQUIRED: Fix missing levels and DE field corrections")

if __name__ == "__main__":
    main()