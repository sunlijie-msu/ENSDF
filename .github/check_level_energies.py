#!/usr/bin/env python3
"""
Check level energies and uncertainties against reference data.
Compare L-record energies and DE fields with provided reference values.
"""

import re

def main():
    # Reference data: energy -> uncertainty
    reference = {
        1219.3: 0.1,
        1763.4: 0.7,
        2644.7: 1.3,
        2694.7: 1.2,
        3003.7: 0.8,
        3163.9: 0.7,
        3920.7: 1.3,
        3944.1: 1.1,
        3979.0: 1.5,
        4059.4: 0.4,
        4114.0: 1.0,  # Note: reference shows 4114, not 4141
        4174.7: 1.0,
        4180.1: 1.5,
        4347.2: 1.2,
        4624.2: 2.0,
        4766.9: 1.5,
        4841.7: 1.9,
        4855.7: 1.9,
        4885.0: 2.0,
        5010.4: 1.8,
        5166.7: 1.5,
        5216.2: 1.5,
        5403.6: 1.0,
        5586.0: 2.0,
        5600.1: 1.5,
        5646.0: 2.0,
        5656.0: 2.0,
        5683.0: 2.0,
        5759.0: 3.0,
        5806.0: 2.0,
        6107.2: 1.5,
        6181.0: 3.0,
        6493.0: 3.0
    }
    
    # Read the ENSDF file
    with open('A35/Cl35/temp/1976ME12.ens', 'r') as f:
        content = f.read()
    
    print("LEVEL ENERGY AND UNCERTAINTY CHECK")
    print("="*70)
    print(f"{'Energy':<10} | {'File DE':<8} | {'Ref DE':<8} | {'Status':<12} | {'Issue'}")
    print("-"*70)
    
    discrepancies = []
    
    # Extract L-records
    for line_num, line in enumerate(content.split('\n'), 1):
        if re.match(r' 35CL  L \d+', line):
            parts = line.split()
            if len(parts) >= 3:
                energy_str = parts[2]
                try:
                    energy = float(energy_str)
                except ValueError:
                    continue
                
                # Get uncertainty from file
                file_de = None
                if len(parts) >= 4 and re.match(r'\d+', parts[3]):
                    try:
                        file_de = float(parts[3])
                    except ValueError:
                        file_de = None
                
                # Check against reference
                if energy in reference:
                    ref_de = reference[energy]
                    
                    if file_de is None:
                        status = "MISSING DE"
                        issue = f"No uncertainty in file"
                        discrepancies.append((energy, "missing", ref_de))
                    elif abs(file_de - ref_de) < 0.1:  # Allow small rounding differences
                        status = "OK"
                        issue = ""
                    else:
                        status = "MISMATCH"
                        issue = f"Expected {ref_de}, found {file_de}"
                        discrepancies.append((energy, file_de, ref_de))
                    
                    print(f"{energy:<10} | {file_de if file_de else 'None':<8} | {ref_de:<8} | {status:<12} | {issue}")
                
                else:
                    # Check if this might be a close match (energy might have different precision)
                    close_matches = []
                    for ref_energy in reference.keys():
                        if abs(energy - ref_energy) < 0.5:
                            close_matches.append(ref_energy)
                    
                    if close_matches:
                        closest = min(close_matches, key=lambda x: abs(energy - x))
                        ref_de = reference[closest]
                        status = "ENERGY DIFF"
                        issue = f"File: {energy}, Ref: {closest} (diff: {energy-closest:.1f})"
                        print(f"{energy:<10} | {file_de if file_de else 'None':<8} | {ref_de:<8} | {status:<12} | {issue}")
                        discrepancies.append((energy, file_de, f"close to {closest}"))
    
    # Check for missing levels in file
    print("\nMISSING LEVELS CHECK:")
    print("-" * 40)
    file_energies = set()
    for line in content.split('\n'):
        if re.match(r' 35CL  L \d+', line):
            parts = line.split()
            if len(parts) >= 3:
                try:
                    energy = float(parts[2])
                    file_energies.add(energy)
                except ValueError:
                    continue
    
    for ref_energy in reference.keys():
        if ref_energy not in file_energies:
            # Check for close matches
            close_matches = [e for e in file_energies if abs(e - ref_energy) < 0.5]
            if not close_matches:
                print(f"MISSING: {ref_energy} keV (uncertainty {reference[ref_energy]})")
    
    print(f"\nSUMMARY:")
    print(f"Reference levels: {len(reference)}")
    print(f"Discrepancies found: {len(discrepancies)}")
    
    if discrepancies:
        print("\nDETAILED DISCREPANCIES:")
        for energy, file_val, ref_val in discrepancies:
            print(f"  {energy} keV: File={file_val}, Reference={ref_val}")

if __name__ == "__main__":
    main()