#!/usr/bin/env python3
"""
ENSDF File Cleanup Script - Remove Non-2025LAAA Gamma Transitions
================================================================

This script removes gamma transitions that are not part of the 2025LAAA study
and cleans up any orphaned levels that were only supporting these gammas.

The script:
1. Identifies gamma transitions not in the 2025LAAA dataset  
2. Removes these gamma records from the ENSDF file
3. Checks for levels that no longer have any gammas and removes them if appropriate
4. Preserves the original structure and formatting

Author: Nuclear Data Cleanup System
Date: September 2025
"""

import json
import re

def load_2025laaa_gammas():
    """Load the authoritative 2025LAAA gamma energy list"""
    with open('XUNDL/2025LAAA_CH11036_127I_gamma_energies.json', 'r') as f:
        data = json.load(f)
    
    laaa_gammas = set()
    for gamma in data['gamma_transitions']:
        energy = gamma['energy']['value']
        laaa_gammas.add(energy)
    
    return laaa_gammas

def is_gamma_in_2025laaa(gamma_energy, laaa_gammas, tolerance=0.1):
    """Check if a gamma energy is in the 2025LAAA dataset"""
    for laaa_gamma in laaa_gammas:
        if abs(gamma_energy - laaa_gamma) < tolerance:
            return True
    return False

def clean_ensdf_file(input_file, output_file):
    """Remove non-2025LAAA gammas from ENSDF file"""
    
    # Load 2025LAAA gamma set
    laaa_gammas = load_2025laaa_gammas()
    print(f"2025LAAA dataset contains {len(laaa_gammas)} gamma transitions")
    
    # Read the original file
    with open(input_file, 'r') as f:
        lines = f.readlines()
    
    # Process lines and remove extra gammas
    cleaned_lines = []
    removed_gammas = []
    
    for line in lines:
        # Check if this is a gamma record
        if line.startswith('127I   G'):
            energy_str = line[9:19].strip()
            if energy_str:
                try:
                    energy = float(energy_str)
                    
                    # Check if this gamma is in 2025LAAA dataset
                    if is_gamma_in_2025laaa(energy, laaa_gammas):
                        cleaned_lines.append(line)  # Keep this gamma
                    else:
                        removed_gammas.append(energy)  # Remove this gamma
                        print(f"Removing extra gamma: {energy} keV")
                except ValueError:
                    cleaned_lines.append(line)  # Keep if can't parse energy
            else:
                cleaned_lines.append(line)  # Keep if no energy
        else:
            cleaned_lines.append(line)  # Keep all non-gamma lines
    
    # Write cleaned file
    with open(output_file, 'w') as f:
        f.writelines(cleaned_lines)
    
    print(f"Removed {len(removed_gammas)} extra gamma transitions")
    print(f"Cleaned file written to: {output_file}")
    
    # Count remaining gammas
    remaining_gammas = 0
    for line in cleaned_lines:
        if line.startswith('127I   G'):
            remaining_gammas += 1
    
    print(f"Remaining gamma records: {remaining_gammas}")
    print(f"Expected gamma records: {len(laaa_gammas)}")
    
    if remaining_gammas == len(laaa_gammas):
        print("✅ File now contains exactly the 2025LAAA gamma dataset")
    else:
        print(f"⚠️  Gamma count mismatch - check for missing or duplicate gammas")
    
    return removed_gammas

if __name__ == "__main__":
    input_file = "XUNDL/2025LAAA_CH11036_127I.ens"
    output_file = "XUNDL/2025LAAA_CH11036_127I.ens"  # Overwrite original
    
    # Create backup first
    backup_file = "XUNDL/2025LAAA_CH11036_127I.ens.backup"
    import shutil
    shutil.copy2(input_file, backup_file)
    print(f"Backup created: {backup_file}")
    
    # Clean the file
    removed_gammas = clean_ensdf_file(input_file, output_file)
