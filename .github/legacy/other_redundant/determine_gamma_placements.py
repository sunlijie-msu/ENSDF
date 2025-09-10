#!/usr/bin/env python3
"""
Determine proper level placements for missing 2025LAAA gamma transitions
using the final matching table and nuclear structure logic
"""

import json

def load_final_table_data():
    """Load the matching data from our final table analysis"""
    # From the final table analysis, here are the placements for missing gammas
    placement_data = {
        # Energy: (initial_level, final_level, reference_info)
        187.5: (2976.1, 2788.42, "23/2- -> 21/2+"),
        188.0: (2545.13, 2357.1, "19/2- -> 17/2+"), 
        409.9: (4367.4, 3957.9, "(29/2-) -> (27/2-)"),
        419.0: (3207.3, 2788.42, "(23/2+) -> 21/2+"),
        431.2: (2976.1, 2545.13, "23/2- -> 19/2-"),
        431.5: (2788.42, 2356.75, "21/2+ -> 19/2+"),
        472.5: (2829.6, 2357.1, "(19/2+) -> 17/2+"),
        480.5: (2356.75, 1876.02, "19/2+ -> 17/2+"),
        601.3: (5242.6, 4641.6, "(35/2-) -> (31/2-)"),
        653.1: (4641.6, 3988.5, "(31/2-) -> (27/2-)"),
        806.5: (2357.1, 1550.68, "17/2+ -> 13/2+"),
        812.3: (3600.8, 2788.42, "(25/2+) -> 21/2+"),
        850.5: (3207.3, 2356.75, "(23/2+) -> 19/2+"),
        855.8: (2829.6, 1973.8, "(19/2+) -> 15/2+"),
        877.0: (2356.75, 1479.75, "19/2+ -> 15/2+"),
        912.0: (2788.42, 1876.02, "21/2+ -> 17/2+"),
        982.1: (3957.9, 2976.1, "(27/2-) -> 23/2-"),
        1012.5: (3988.5, 2976.1, "(27/2-) -> 23/2-"),
        1085.5: (3442.6, 2357.1, "(21/2+) -> 17/2+"),
        380.0: None,  # Need to determine placement
    }
    return placement_data

def parse_ensdf_levels():
    """Parse ENSDF file to get current level structure"""
    levels = {}
    
    with open('XUNDL/2025LAAA_CH11036_127I.ens', 'r') as f:
        lines = f.readlines()
    
    for line in lines:
        if len(line) >= 8 and line[7:8] == 'L' and line[8:9] == ' ':
            energy_str = line[9:19].strip()
            if energy_str:
                try:
                    energy = float(energy_str)
                    jp = line[22:39].strip()
                    levels[energy] = {
                        'jp': jp,
                        'line_number': lines.index(line) + 1
                    }
                except ValueError:
                    pass
    
    return levels

def find_gamma_insertions():
    """Determine where to insert each missing gamma"""
    placement_data = load_final_table_data()
    levels = parse_ensdf_levels()
    
    insertions = []
    
    for gamma_energy, placement_info in placement_data.items():
        if placement_info is None:
            print(f"WARNING: No placement determined for {gamma_energy} keV")
            continue
            
        initial_level, final_level, transition_info = placement_info
        
        # Check if initial level exists in current ENSDF
        if initial_level not in levels:
            print(f"WARNING: Initial level {initial_level} not found for gamma {gamma_energy}")
            # Need to add this level first
            insertions.append({
                'type': 'level',
                'energy': initial_level,
                'gamma_energy': gamma_energy,
                'transition_info': transition_info
            })
        else:
            # Level exists, just need to add gamma
            insertions.append({
                'type': 'gamma',
                'level_energy': initial_level,
                'gamma_energy': gamma_energy,
                'final_level': final_level,
                'transition_info': transition_info
            })
    
    return insertions

def main():
    print("DETERMINING GAMMA PLACEMENT FOR MISSING TRANSITIONS")
    print("=" * 60)
    
    levels = parse_ensdf_levels()
    insertions = find_gamma_insertions()
    
    print(f"Current levels in ENSDF: {len(levels)}")
    print("\nLevels found:")
    for energy in sorted(levels.keys()):
        print(f"  {energy:8.1f} keV - {levels[energy]['jp']}")
    
    print(f"\nMissing gamma insertions needed: {len(insertions)}")
    
    gamma_insertions = [x for x in insertions if x['type'] == 'gamma']
    level_insertions = [x for x in insertions if x['type'] == 'level']
    
    print(f"\nGamma insertions: {len(gamma_insertions)}")
    for insertion in sorted(gamma_insertions, key=lambda x: x['level_energy']):
        print(f"  {insertion['gamma_energy']:6.1f} keV -> Level {insertion['level_energy']:8.1f} keV ({insertion['transition_info']})")
    
    if level_insertions:
        print(f"\nLevel insertions needed: {len(level_insertions)}")
        for insertion in level_insertions:
            print(f"  Level {insertion['energy']:8.1f} keV for gamma {insertion['gamma_energy']:6.1f} keV")

if __name__ == "__main__":
    main()
