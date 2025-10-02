#!/usr/bin/env python3
"""
Check for missing levels in 1976ME12.ens file compared to reference data
"""

def read_ensdf_energies(filename):
    """Read energies from ENSDF file L-records"""
    energies = set()
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                if len(line) >= 8 and line[7] == 'L' and line[8] == ' ':
                    energy_str = line[9:19].strip()
                    if energy_str:
                        try:
                            energy = float(energy_str)
                            energies.add(energy)
                        except ValueError:
                            continue
    except FileNotFoundError:
        print(f"ERROR: File {filename} not found")
        return set()
    
    return energies

def main():
    # Reference data energies (all 33 levels)
    reference_energies = {
        744.8, 1219.3, 1763.4, 2644.7, 2694.7, 3003.7, 3058.9, 3164.3, 3348.7, 3400.7,
        3558.1, 3589.8, 3622.7, 3734.7, 3784.1, 3806.1, 3874.1, 3899.1, 3928.1, 3966.1,
        4114.0, 4174.7, 4180.1, 4347.2, 4624.2, 4766.9, 4880.2, 4928.2, 5184.2, 5251.2,
        5380.2, 5522.2, 5557.2
    }
    
    # Read current file energies
    filename = "d:/X/ND/ENSDF/A35/Cl35/temp/1976ME12.ens"
    current_energies = read_ensdf_energies(filename)
    
    print("Level Energy Comparison")
    print("=" * 40)
    print(f"Reference levels: {len(reference_energies)}")
    print(f"Current file levels: {len(current_energies)}")
    
    # Find missing levels
    missing = reference_energies - current_energies
    extra = current_energies - reference_energies
    
    if missing:
        print(f"\nMissing levels ({len(missing)}):")
        for energy in sorted(missing):
            print(f"  {energy:7.1f} keV")
    
    if extra:
        print(f"\nExtra levels in file ({len(extra)}):")
        for energy in sorted(extra):
            print(f"  {energy:7.1f} keV")
    
    if not missing and not extra:
        print("\nSUCCESS: All reference levels are present in the file!")
    
    print(f"\nLevels correctly present: {len(reference_energies & current_energies)}")

if __name__ == "__main__":
    main()