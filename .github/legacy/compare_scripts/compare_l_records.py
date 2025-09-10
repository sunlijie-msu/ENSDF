#!/usr/bin/env python3
"""
Extract all current L record energies from 2025LAAA_CH11036_127I.ens
and compare with the required ELI energies.
"""

import re

def extract_current_l_records(filename):
    """Extract all L record energies from ENSDF file."""
    l_energies = []
    
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    for line in lines:
        # Look for L records (column 8 = 'L')
        if len(line) >= 8 and line[7] == 'L':
            # Energy is in columns 10-19
            energy_str = line[9:19].strip()
            if energy_str:
                try:
                    energy = float(energy_str)
                    l_energies.append(energy)
                except ValueError:
                    continue
    
    return sorted(l_energies)

def main():
    ensdf_file = "XUNDL/2025LAAA_CH11036_127I.ens"
    
    # Required energies from comparison file (plus ground state)
    required_energies = [
        0.0,   # Ground state (always needed)
        57.46, 628.51, 650.79, 716.48, 744.76, 1235.13, 1266.29, 1306.54, 
        1479.75, 1550.68, 1876.02, 1893.64, 1973.80, 2356.75, 2357.10, 
        2545.13, 2788.42, 2829.60, 2976.10, 3207.30, 3442.60, 3557.20, 
        3600.80, 3957.90, 3988.50, 4367.40, 4641.60, 5242.60
    ]
    
    current_energies = extract_current_l_records(ensdf_file)
    
    print("CURRENT L RECORD ENERGIES:")
    print("=" * 40)
    for i, energy in enumerate(current_energies, 1):
        print(f"{i:2d}. {energy:8.2f} keV")
    
    print(f"\nFound {len(current_energies)} current L records")
    print(f"Should have {len(required_energies)} L records")
    
    # Find extra energies (in current but not required)
    extra_energies = []
    for energy in current_energies:
        if not any(abs(energy - req) < 0.01 for req in required_energies):
            extra_energies.append(energy)
    
    # Find missing energies (required but not in current)
    missing_energies = []
    for req_energy in required_energies:
        if not any(abs(req_energy - curr) < 0.01 for curr in current_energies):
            missing_energies.append(req_energy)
    
    if extra_energies:
        print(f"\nEXTRA L RECORDS TO REMOVE ({len(extra_energies)}):")
        print("-" * 40)
        for energy in extra_energies:
            print(f"  {energy:8.2f} keV")
    
    if missing_energies:
        print(f"\nMISSING L RECORDS TO ADD ({len(missing_energies)}):")
        print("-" * 40)
        for energy in missing_energies:
            print(f"  {energy:8.2f} keV")
    
    if not extra_energies and not missing_energies:
        print("\n✅ L records match perfectly!")
    else:
        print(f"\n⚠️  Need to remove {len(extra_energies)} and add {len(missing_energies)} L records")

if __name__ == "__main__":
    main()
