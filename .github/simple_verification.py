#!/usr/bin/env python3
"""
Simple comparison between placement table and ENSDF file to find specific errors
"""

def get_placement_data():
    """Get gamma-to-level assignments from validated placement table"""
    placements = {}
    
    with open("XUNDL/2025LAAA_vs_2012DI06.ens", 'r') as f:
        lines = f.readlines()
    
    for line in lines:
        if '|' in line and 'keV' not in line and 'ELI' not in line and '---' not in line and 'FINAL' not in line:
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 7:
                try:
                    eli = float(parts[0])
                    ji = parts[1].strip()
                    elf = float(parts[2])
                    jf = parts[3].strip()
                    eg_2025 = parts[6].strip()
                    
                    if eg_2025 != 'TBD' and eg_2025:
                        energy = float(eg_2025)
                        placements[energy] = {
                            'initial_level': eli,
                            'initial_jp': ji,
                            'final_level': elf,
                            'final_jp': jf
                        }
                except (ValueError, IndexError):
                    continue
    
    return placements

def get_ensdf_structure():
    """Get current ENSDF level and gamma structure"""
    levels = {}
    gammas = {}
    current_level = None
    
    with open("XUNDL/2025LAAA_CH11036_127I.ens", 'r') as f:
        lines = f.readlines()
    
    for i, line in enumerate(lines):
        if len(line) > 8 and line[7] == 'L':  # Level record
            try:
                energy_str = line[9:19].strip()
                jp_str = line[21:39].strip()
                
                if energy_str:
                    energy = float(energy_str)
                    levels[energy] = jp_str
                    current_level = energy
            except:
                continue
                
        elif len(line) > 8 and line[7] == 'G' and current_level is not None:  # Gamma record
            try:
                gamma_energy_str = line[9:19].strip()
                if gamma_energy_str:
                    gamma_energy = float(gamma_energy_str)
                    gammas[gamma_energy] = current_level
            except:
                continue
    
    return levels, gammas

def find_errors():
    """Find specific errors by comparing placement table with ENSDF"""
    
    print("VERIFICATION OF ENSDF FILE AGAINST PLACEMENT TABLE:")
    print("=" * 70)
    
    placements = get_placement_data()
    ensdf_levels, ensdf_gammas = get_ensdf_structure()
    
    print(f"Placement table: {len(placements)} gammas")
    print(f"ENSDF file: {len(ensdf_levels)} levels, {len(ensdf_gammas)} gammas")
    print()
    
    errors = []
    
    # Check each gamma from placement table
    for gamma_energy, correct_data in placements.items():
        correct_initial = correct_data['initial_level']
        correct_initial_jp = correct_data['initial_jp']
        
        print(f"Checking {gamma_energy} keV gamma:")
        print(f"  Should be under: {correct_initial} keV ({correct_initial_jp})")
        
        if gamma_energy in ensdf_gammas:
            current_level = ensdf_gammas[gamma_energy]
            print(f"  Currently under: {current_level} keV", end="")
            
            if current_level in ensdf_levels:
                current_jp = ensdf_levels[current_level]
                print(f" ({current_jp})")
                
                # Check if placement is correct
                if abs(current_level - correct_initial) > 0.1:
                    print(f"  ❌ WRONG LEVEL: Should be {correct_initial}, not {current_level}")
                    errors.append(f"{gamma_energy} keV: wrong level ({current_level} → {correct_initial})")
                elif current_jp != correct_initial_jp:
                    print(f"  ❌ WRONG J-π: Should be {correct_initial_jp}, not {current_jp}")
                    errors.append(f"{gamma_energy} keV: wrong J-π ({current_jp} → {correct_initial_jp})")
                else:
                    print(f"  ✅ CORRECT")
            else:
                print(f" (J-π unknown)")
                errors.append(f"{gamma_energy} keV: level {current_level} missing J-π")
        else:
            print(f"  ❌ MISSING from ENSDF file!")
            errors.append(f"{gamma_energy} keV: missing entirely")
        
        print()
    
    # Check for missing levels
    print("CHECKING FOR MISSING LEVELS:")
    print("-" * 30)
    
    required_levels = set()
    for data in placements.values():
        required_levels.add((data['initial_level'], data['initial_jp']))
        required_levels.add((data['final_level'], data['final_jp']))
    
    for level_energy, level_jp in required_levels:
        if level_energy not in ensdf_levels:
            print(f"❌ Missing level: {level_energy} keV ({level_jp})")
            errors.append(f"Missing level: {level_energy} keV ({level_jp})")
        elif ensdf_levels[level_energy] != level_jp:
            print(f"❌ Wrong J-π for {level_energy} keV: {ensdf_levels[level_energy]} → {level_jp}")
            errors.append(f"Wrong J-π for {level_energy} keV: {ensdf_levels[level_energy]} → {level_jp}")
    
    print("\n" + "=" * 70)
    print(f"SUMMARY: {len(errors)} ERRORS FOUND")
    
    if errors:
        print("\nALL ERRORS:")
        for i, error in enumerate(errors, 1):
            print(f"{i:2d}. {error}")
    else:
        print("✅ No errors found!")
    
    return errors

if __name__ == "__main__":
    errors = find_errors()
