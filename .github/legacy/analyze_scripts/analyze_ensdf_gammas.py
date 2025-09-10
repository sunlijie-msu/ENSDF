#!/usr/bin/env python3
"""
Analyze current ENSDF file to extract all gamma energies and level placements
"""

import json
import re

def parse_ensdf_file(filename):
    """Parse ENSDF file to extract levels and gammas"""
    levels = []
    gammas = []
    current_level_energy = None
    
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    for line in lines:
        if len(line) < 80:
            line = line.ljust(80)
        
        # L-record (level)
        if line[7:8] == 'L' and line[8:9] == ' ':
            energy_str = line[9:19].strip()
            if energy_str:
                try:
                    current_level_energy = float(energy_str)
                    jp = line[22:39].strip()
                    levels.append({
                        'energy': current_level_energy,
                        'jp': jp,
                        'line': line.rstrip()
                    })
                except ValueError:
                    pass
        
        # G-record (gamma)
        elif line[7:8] == 'G' and line[8:9] == ' ':
            energy_str = line[9:19].strip()
            if energy_str:
                try:
                    gamma_energy = float(energy_str)
                    ri_str = line[22:29].strip()
                    multipolarity = line[31:41].strip()
                    gammas.append({
                        'energy': gamma_energy,
                        'ri': ri_str,
                        'multipolarity': multipolarity,
                        'level_energy': current_level_energy,
                        'line': line.rstrip()
                    })
                except ValueError:
                    pass
    
    return levels, gammas

def load_2025_gammas():
    """Load gamma energies from JSON file"""
    with open('XUNDL/2025LAAA_CH11036_127I_gamma_energies.json', 'r') as f:
        data = json.load(f)
    
    gamma_energies = []
    for transition in data['gamma_transitions']:
        gamma_energies.append(transition['energy']['value'])
    
    return sorted(gamma_energies)

def find_missing_gammas(ensdf_gammas, target_gammas, tolerance=0.5):
    """Find gamma energies from target list not present in ENSDF"""
    missing = []
    ensdf_energies = [g['energy'] for g in ensdf_gammas]
    
    for target_energy in target_gammas:
        found = False
        for ensdf_energy in ensdf_energies:
            if abs(target_energy - ensdf_energy) <= tolerance:
                found = True
                break
        if not found:
            missing.append(target_energy)
    
    return missing

def main():
    print("ANALYZING CURRENT ENSDF FILE FOR GAMMA PLACEMENTS")
    print("=" * 60)
    
    # Parse current ENSDF file
    levels, gammas = parse_ensdf_file('XUNDL/2025LAAA_CH11036_127I.ens')
    
    print(f"Current ENSDF contains:")
    print(f"  Levels: {len(levels)}")
    print(f"  Gamma transitions: {len(gammas)}")
    print()
    
    # Load target gamma energies
    target_gammas = load_2025_gammas()
    print(f"Target 2025LAAA gammas: {len(target_gammas)}")
    
    # Find missing gammas
    missing = find_missing_gammas(gammas, target_gammas)
    
    print(f"\nMISSING GAMMA TRANSITIONS: {len(missing)}")
    if missing:
        print("Missing energies (keV):")
        for energy in sorted(missing):
            print(f"  {energy:8.1f}")
    
    print(f"\nCURRENT GAMMA ENERGIES IN ENSDF:")
    for gamma in sorted(gammas, key=lambda x: x['energy']):
        print(f"  {gamma['energy']:8.1f} keV (level {gamma['level_energy']:8.1f})")
    
    print(f"\nTARGET 2025LAAA GAMMA ENERGIES:")
    for energy in target_gammas:
        print(f"  {energy:8.1f} keV")
    
    # Check for misplacements
    print(f"\nGAMMA PLACEMENT VERIFICATION:")
    for gamma in gammas:
        # Find corresponding target gamma
        matched = False
        for target in target_gammas:
            if abs(gamma['energy'] - target) <= 0.5:
                matched = True
                break
        if matched:
            print(f"  {gamma['energy']:8.1f} keV: PRESENT")
        else:
            print(f"  {gamma['energy']:8.1f} keV: NOT IN TARGET LIST")

if __name__ == "__main__":
    main()
