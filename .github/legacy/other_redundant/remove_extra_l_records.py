#!/usr/bin/env python3
"""
Systematically remove extra L records and their associated G records from ENSDF file.
Only keep L records that correspond to ELI energies in the comparison file.
"""

import re

def remove_extra_l_records(filename):
    """Remove L records that don't correspond to required ELI energies."""
    
    # Energies to remove (identified from comparison)
    energies_to_remove = [
        1918.60, 1923.90, 2024.10, 2068.40, 2157.90, 2178.40, 
        2264.60, 2315.60, 2343.10, 2477.70, 2511.50, 2901.23, 3692.70
    ]
    
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    new_lines = []
    skip_until_next_l = False
    current_l_energy = None
    
    for i, line in enumerate(lines):
        # Check if this is an L record
        if len(line) >= 8 and line[7] == 'L':
            # Extract energy from columns 10-19
            energy_str = line[9:19].strip()
            if energy_str:
                try:
                    energy = float(energy_str)
                    current_l_energy = energy
                    
                    # Check if this energy should be removed
                    should_remove = any(abs(energy - rem_energy) < 0.01 for rem_energy in energies_to_remove)
                    
                    if should_remove:
                        print(f"Removing L record: {energy:8.2f} keV")
                        skip_until_next_l = True
                        continue  # Skip this L record
                    else:
                        skip_until_next_l = False
                        
                except ValueError:
                    pass
        
        # If we're skipping records for a removed L level
        if skip_until_next_l:
            # Check if this is another L record (end of skipping)
            if len(line) >= 8 and line[7] == 'L':
                # This is a new L record, process it normally
                energy_str = line[9:19].strip()
                if energy_str:
                    try:
                        energy = float(energy_str)
                        current_l_energy = energy
                        
                        should_remove = any(abs(energy - rem_energy) < 0.01 for rem_energy in energies_to_remove)
                        
                        if should_remove:
                            print(f"Removing L record: {energy:8.2f} keV")
                            skip_until_next_l = True
                            continue
                        else:
                            skip_until_next_l = False
                            new_lines.append(line)
                    except ValueError:
                        new_lines.append(line)
                else:
                    new_lines.append(line)
            else:
                # Skip this line (G record, comment, etc. for removed L level)
                continue
        else:
            # Keep this line
            new_lines.append(line)
    
    # Write the cleaned file
    backup_filename = filename + '.backup'
    with open(backup_filename, 'w') as f:
        with open(filename, 'r') as orig:
            f.write(orig.read())
    print(f"Backup created: {backup_filename}")
    
    with open(filename, 'w') as f:
        f.writelines(new_lines)
    
    print(f"Removed {len(energies_to_remove)} L records and their associated lines")
    print("Updated file written successfully")

if __name__ == "__main__":
    remove_extra_l_records("XUNDL/2025LAAA_CH11036_127I.ens")
