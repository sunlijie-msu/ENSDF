#!/usr/bin/env python3
"""
Extract all gamma energies from 2012DI06 and identify close energies (<1.0 keV difference)
"""

def extract_2012DI06_gammas():
    # Read the 2012DI06 XUNDL file and extract all gamma energies
    gammas_2012 = []
    
    with open("XUNDL/2012DI06_127I_xundl-1.xundl", "r") as f:
        for line_num, line in enumerate(f, 1):
            if line.startswith("127I   G "):
                # Extract energy from columns 10-19
                energy_str = line[9:19].strip()
                try:
                    energy = float(energy_str)
                    gammas_2012.append((energy, line_num, line.strip()))
                except ValueError:
                    print(f"Could not parse energy on line {line_num}: '{energy_str}'")
    
    # Sort by energy
    gammas_2012.sort()
    
    print("STEP 1: ALL GAMMA ENERGIES FROM 2012DI06")
    print("=" * 60)
    print(f"Total gamma transitions found: {len(gammas_2012)}")
    print()
    
    for i, (energy, line_num, line) in enumerate(gammas_2012):
        print(f"{i+1:2d}. {energy:7.1f} keV (line {line_num:3d}): {line}")
    print()
    
    # Find close energies (<1.0 keV difference)
    close_groups = []
    i = 0
    while i < len(gammas_2012):
        group = [gammas_2012[i]]
        j = i + 1
        while j < len(gammas_2012) and gammas_2012[j][0] - gammas_2012[i][0] < 1.0:
            group.append(gammas_2012[j])
            j += 1
        
        if len(group) > 1:
            close_groups.append(group)
        
        i = j if len(group) > 1 else i + 1
    
    print("CLOSE GAMMA ENERGIES (<1.0 keV difference):")
    print("=" * 60)
    
    if not close_groups:
        print("No gamma energies within 1.0 keV of each other found.")
    else:
        for group_num, group in enumerate(close_groups, 1):
            print(f"GROUP {group_num}:")
            for energy, line_num, line in group:
                print(f"  {energy:6.1f} keV (line {line_num:3d}): {line}")
            
            # Calculate differences within group
            if len(group) > 1:
                print("  Differences:")
                for i in range(len(group)-1):
                    diff = group[i+1][0] - group[i][0]
                    print(f"    {group[i+1][0]:6.1f} - {group[i][0]:6.1f} = {diff:4.1f} keV")
            print()
    
    return gammas_2012, close_groups

if __name__ == "__main__":
    gammas_2012, close_groups = extract_2012DI06_gammas()
