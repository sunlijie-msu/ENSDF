#!/usr/bin/env python3
"""
Verify that all 2025LAAA gammas from the placement table are correctly placed in the ENSDF file.
"""

def parse_placement_table(file_path):
    """Parse the placement table to extract 2025LAAA gamma energies and their expected placements."""
    gammas_2025 = []
    
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    for line in lines:
        if line.strip() and not line.startswith('=') and not line.startswith('-') and not line.startswith('FINAL') and '|' in line:
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 7:
                try:
                    eli = float(parts[0])
                    ji = parts[1] 
                    elf = float(parts[2])
                    jf = parts[3]
                    eg_2012 = parts[4]
                    ri_2012 = parts[5]
                    eg_2025 = parts[6]
                    
                    if eg_2025 and eg_2025 != 'EG_2025':
                        gammas_2025.append({
                            'eli': eli,
                            'ji': ji,
                            'elf': elf, 
                            'jf': jf,
                            'eg_2025': float(eg_2025),
                            'eg_2012': eg_2012,
                            'ri_2012': ri_2012
                        })
                except (ValueError, IndexError):
                    continue
    
    return gammas_2025

def parse_ensdf_gammas(file_path):
    """Parse ENSDF file to extract gamma rays and their level placements."""
    ensdf_gammas = []
    current_level = None
    
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    for line in lines:
        if '127I   L' in line:
            # Extract level energy
            parts = line.split()
            if len(parts) >= 3:
                try:
                    current_level = float(parts[2])
                except ValueError:
                    pass
        elif '127I   G' in line and current_level is not None:
            # Extract gamma energy
            parts = line.split()
            if len(parts) >= 3:
                try:
                    gamma_energy = float(parts[2])
                    ensdf_gammas.append({
                        'level': current_level,
                        'gamma': gamma_energy
                    })
                except ValueError:
                    pass
    
    return ensdf_gammas

def main():
    placement_file = "XUNDL/2025LAAA_vs_2012DI06.ens"
    ensdf_file = "XUNDL/2025LAAA_CH11036_127I.ens"
    
    print("Parsing placement table...")
    gammas_2025 = parse_placement_table(placement_file)
    print(f"Found {len(gammas_2025)} 2025LAAA gamma rays in placement table")
    
    print("\nParsing ENSDF file...")
    ensdf_gammas = parse_ensdf_gammas(ensdf_file)
    print(f"Found {len(ensdf_gammas)} gamma rays in ENSDF file")
    
    # Check which 2025LAAA gammas are missing from ENSDF
    print("\nChecking for missing 2025LAAA gammas:")
    missing_count = 0
    
    for gamma in gammas_2025:
        eli = gamma['eli']
        eg_2025 = gamma['eg_2025']
        
        # Look for this gamma in ENSDF under the correct level
        found = False
        for ensdf_gamma in ensdf_gammas:
            if abs(ensdf_gamma['level'] - eli) < 0.1 and abs(ensdf_gamma['gamma'] - eg_2025) < 1.0:
                found = True
                break
        
        if not found:
            print(f"MISSING: {eg_2025} keV gamma from level {eli} keV ({gamma['ji']} → {gamma['jf']})")
            missing_count += 1
    
    print(f"\nTotal missing gammas: {missing_count}")
    print(f"Total placed gammas: {len(gammas_2025) - missing_count}")
    
    # Check for extra gammas in ENSDF that don't match 2025LAAA
    print("\nChecking for potential extra gammas in ENSDF:")
    extra_count = 0
    
    for ensdf_gamma in ensdf_gammas:
        level = ensdf_gamma['level']
        gamma = ensdf_gamma['gamma']
        
        # Look for matching 2025LAAA gamma
        found = False
        for gamma_2025 in gammas_2025:
            if abs(gamma_2025['eli'] - level) < 0.1 and abs(gamma_2025['eg_2025'] - gamma) < 1.0:
                found = True
                break
        
        if not found:
            print(f"EXTRA(?): {gamma} keV gamma from level {level} keV")
            extra_count += 1
    
    print(f"\nTotal potentially extra gammas: {extra_count}")

if __name__ == "__main__":
    main()
