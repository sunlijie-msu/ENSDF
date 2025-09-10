#!/usr/bin/env python3
"""
Add missing 2025LAAA gamma transitions to ENSDF file using placement data from 2025LAAA_vs_2012DI06.ens
"""

import re

def parse_placement_table():
    """Parse the placement table to get gamma placement information"""
    placements = {}
    
    with open('XUNDL/2025LAAA_vs_2012DI06.ens', 'r') as f:
        lines = f.readlines()
    
    for line in lines:
        # Skip header lines
        if 'ELI' in line or '---' in line or '===' in line or not line.strip():
            continue
            
        # Parse data lines with format: ELI | JI | ELF | JF | EG_2012 | RI_2012 | EG_2025
        parts = [p.strip() for p in line.split('|')]
        if len(parts) >= 7:
            try:
                eli = float(parts[0])
                ji = parts[1]
                elf = float(parts[2]) 
                jf = parts[3]
                eg_2025 = float(parts[6])
                
                placements[eg_2025] = {
                    'initial_level': eli,
                    'initial_jp': ji,
                    'final_level': elf,
                    'final_jp': jf
                }
            except (ValueError, IndexError):
                continue
    
    return placements

def get_current_ensdf_gammas():
    """Get current gamma energies in ENSDF file"""
    current_gammas = set()
    
    with open('XUNDL/2025LAAA_CH11036_127I.ens', 'r') as f:
        lines = f.readlines()
    
    for line in lines:
        if len(line) >= 8 and line[7:8] == 'G' and line[8:9] == ' ':
            energy_str = line[9:19].strip()
            if energy_str:
                try:
                    gamma_energy = float(energy_str)
                    current_gammas.add(gamma_energy)
                except ValueError:
                    pass
    
    return current_gammas

def get_ensdf_levels():
    """Get current levels in ENSDF file with their line positions"""
    levels = {}
    
    with open('XUNDL/2025LAAA_CH11036_127I.ens', 'r') as f:
        lines = f.readlines()
    
    for i, line in enumerate(lines):
        if len(line) >= 8 and line[7:8] == 'L' and line[8:9] == ' ':
            energy_str = line[9:19].strip()
            if energy_str:
                try:
                    energy = float(energy_str)
                    jp = line[22:39].strip()
                    levels[energy] = {
                        'jp': jp,
                        'line_index': i,
                        'gammas': []
                    }
                except ValueError:
                    pass
    
    # Now find all gammas for each level
    current_level = None
    for i, line in enumerate(lines):
        if len(line) >= 8 and line[7:8] == 'L' and line[8:9] == ' ':
            energy_str = line[9:19].strip()
            if energy_str:
                try:
                    current_level = float(energy_str)
                except ValueError:
                    pass
        elif len(line) >= 8 and line[7:8] == 'G' and line[8:9] == ' ' and current_level is not None:
            energy_str = line[9:19].strip()
            if energy_str:
                try:
                    gamma_energy = float(energy_str)
                    levels[current_level]['gammas'].append({
                        'energy': gamma_energy,
                        'line_index': i
                    })
                except ValueError:
                    pass
    
    return levels

def find_missing_levels_needed():
    """Identify any levels that need to be added"""
    placements = parse_placement_table()
    current_levels = get_ensdf_levels()
    
    missing_levels = set()
    
    for gamma_energy, placement in placements.items():
        initial_level = placement['initial_level']
        if initial_level not in current_levels:
            missing_levels.add((initial_level, placement['initial_jp']))
    
    return sorted(missing_levels)

def add_missing_levels():
    """Add any missing levels that are needed for gamma placements"""
    missing_levels = find_missing_levels_needed()
    
    if not missing_levels:
        return
    
    print(f"Adding {len(missing_levels)} missing levels:")
    for energy, jp in missing_levels:
        print(f"  Level {energy:8.1f} keV ({jp})")
    
    # Read current file
    with open('XUNDL/2025LAAA_CH11036_127I.ens', 'r') as f:
        lines = f.readlines()
    
    # Find where to insert each level (maintain energy order)
    current_levels = get_ensdf_levels()
    level_energies = sorted(current_levels.keys())
    
    for level_energy, jp in missing_levels:
        # Find insertion point
        insert_after_index = -1
        for i, existing_energy in enumerate(level_energies):
            if level_energy > existing_energy:
                insert_after_index = current_levels[existing_energy]['line_index']
            else:
                break
        
        # Create level record
        level_line = f"127I   L {level_energy:<10.1f} {jp:<17}\n"
        
        # Insert after the determined position
        lines.insert(insert_after_index + 1, level_line)
        
        # Update line indices for subsequent levels
        for energy in current_levels:
            if current_levels[energy]['line_index'] > insert_after_index:
                current_levels[energy]['line_index'] += 1
        
        # Add to current_levels tracking
        current_levels[level_energy] = {
            'jp': jp,
            'line_index': insert_after_index + 1,
            'gammas': []
        }
        level_energies = sorted(current_levels.keys())
    
    # Write back to file
    with open('XUNDL/2025LAAA_CH11036_127I.ens', 'w') as f:
        f.writelines(lines)

def add_missing_gammas():
    """Add missing gamma transitions using placement data"""
    placements = parse_placement_table()
    current_gammas = get_current_ensdf_gammas()
    
    # Find missing gammas
    missing_gammas = []
    for gamma_energy in placements:
        # Check if gamma is already present (within 0.5 keV tolerance)
        found = False
        for current_gamma in current_gammas:
            if abs(gamma_energy - current_gamma) <= 0.5:
                found = True
                break
        if not found:
            missing_gammas.append(gamma_energy)
    
    if not missing_gammas:
        print("No missing gammas to add!")
        return
    
    print(f"Adding {len(missing_gammas)} missing gamma transitions:")
    for gamma_energy in sorted(missing_gammas):
        placement = placements[gamma_energy]
        print(f"  {gamma_energy:6.1f} keV -> Level {placement['initial_level']:8.1f} keV")
    
    # Read current file
    with open('XUNDL/2025LAAA_CH11036_127I.ens', 'r') as f:
        lines = f.readlines()
    
    # Process each missing gamma
    for gamma_energy in sorted(missing_gammas):
        placement = placements[gamma_energy]
        initial_level = placement['initial_level']
        
        # Find the level this gamma belongs to
        level_found = False
        level_line_index = -1
        
        for i, line in enumerate(lines):
            if len(line) >= 8 and line[7:8] == 'L' and line[8:9] == ' ':
                energy_str = line[9:19].strip()
                if energy_str:
                    try:
                        level_energy = float(energy_str)
                        if abs(level_energy - initial_level) <= 0.1:
                            level_found = True
                            level_line_index = i
                            break
                    except ValueError:
                        pass
        
        if not level_found:
            print(f"WARNING: Could not find level {initial_level} for gamma {gamma_energy}")
            continue
        
        # Find existing gammas for this level and determine insertion point
        gamma_insertion_index = level_line_index
        existing_gammas = []
        
        # Scan forward from level to find all gammas for this level
        j = level_line_index + 1
        while j < len(lines):
            line = lines[j]
            if len(line) >= 8 and line[7:8] == 'L' and line[8:9] == ' ':
                # Hit next level, stop
                break
            elif len(line) >= 8 and line[7:8] == 'G' and line[8:9] == ' ':
                energy_str = line[9:19].strip()
                if energy_str:
                    try:
                        existing_gamma_energy = float(energy_str)
                        existing_gammas.append((existing_gamma_energy, j))
                    except ValueError:
                        pass
            j += 1
        
        # Find where to insert new gamma (maintain energy order)
        insert_index = level_line_index + 1  # Default: right after level
        for existing_energy, existing_index in existing_gammas:
            if gamma_energy > existing_energy:
                insert_index = existing_index + 1
            else:
                break
        
        # Create gamma record
        gamma_line = f"127I   G {gamma_energy:<10.1f}                                                  \n"
        
        # Insert the gamma line
        lines.insert(insert_index, gamma_line)
    
    # Write back to file
    with open('XUNDL/2025LAAA_CH11036_127I.ens', 'w') as f:
        f.writelines(lines)

def main():
    print("ADDING MISSING 2025LAAA GAMMA TRANSITIONS TO ENSDF")
    print("=" * 60)
    
    # First add any missing levels
    add_missing_levels()
    
    # Then add missing gammas
    add_missing_gammas()
    
    print("\nCompleted adding missing gamma transitions!")

if __name__ == "__main__":
    main()
