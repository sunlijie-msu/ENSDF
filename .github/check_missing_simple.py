#!/usr/bin/env python3
"""
Simple script to add missing 2025LAAA gammas to ENSDF based on placement table
"""

# Missing gammas from analysis with their placements (level energy from table)
missing_gammas = [
    # gamma_energy: (level_energy_in_table, level_energy_in_ensdf)
    (187.5, 2976.1, None),  # Need new level
    (188.0, 2545.1, None),  # Need new level  
    (409.9, 4367.4, None), # Need new level
    (419.0, 3207.3, None), # Need new level
    (431.2, 2976.1, None), # Need new level
    (431.5, 2788.4, None), # Need new level
    (472.5, 2829.6, None), # Need new level
    (480.5, 2356.8, None), # Need new level
    (601.3, 5242.6, None), # Need new level
    (653.1, 4641.6, None), # Need new level
    (806.5, 2357.1, None), # Need new level
    (812.3, 3600.8, None), # Need new level
    (850.5, 3207.3, None), # Need new level
    (855.8, 2829.6, None), # Need new level
    (877.0, 2356.8, None), # Need new level
    (912.0, 2788.4, None), # Need new level
    (982.1, 3957.9, None), # Need new level
    (1012.5, 3988.5, None), # Need new level
    (1085.5, 3442.6, None), # Need new level
]

# Read current ENSDF file
with open('XUNDL/2025LAAA_CH11036_127I.ens', 'r') as f:
    lines = f.readlines()

print("Current ENSDF structure:")
current_levels = []
for line in lines:
    if len(line) >= 8 and line[7:8] == 'L' and line[8:9] == ' ':
        energy_str = line[9:19].strip()
        if energy_str:
            try:
                energy = float(energy_str)
                jp = line[22:39].strip()
                current_levels.append((energy, jp))
                print(f"  Level {energy:8.1f} keV ({jp})")
            except ValueError:
                pass

print(f"\nCurrent levels: {len(current_levels)}")
print(f"Missing gammas that need levels: {len(missing_gammas)}")

# Determine which levels need to be added
levels_to_add = set()
for gamma_energy, table_level, ensdf_level in missing_gammas:
    # Check if this level already exists
    found = False
    for curr_energy, curr_jp in current_levels:
        if abs(curr_energy - table_level) <= 5.0:  # 5 keV tolerance
            found = True
            print(f"Gamma {gamma_energy:6.1f} -> Existing level {curr_energy:8.1f}")
            break
    if not found:
        levels_to_add.add(table_level)
        print(f"Gamma {gamma_energy:6.1f} -> NEW level {table_level:8.1f} needed")

print(f"\nNew levels needed: {len(levels_to_add)}")
for level in sorted(levels_to_add):
    print(f"  {level:8.1f} keV")
