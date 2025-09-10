#!/usr/bin/env python3
"""
Debug just the lifetime association
"""

import re

def debug_lifetime_association():
    ensdf_file = "XUNDL/2025LAAA_CH11036_127I.ens"
    
    with open(ensdf_file, 'r') as f:
        lines = f.readlines()
    
    levels = []
    tau_pattern = r'\|t\{-(\w+)\}=([0-9.]+) ps \{I\+(\d+)-(\d+)\}'
    
    # First pass: find all levels
    for i, line in enumerate(lines):
        if len(line) > 9 and line[7] == 'L' and line[8] == ' ':
            energy_str = line[9:19].strip()
            try:
                level_energy = float(energy_str)
                levels.append((level_energy, i+1))
            except:
                pass
    
    print(f"Found {len(levels)} levels")
    
    # Second pass: find lifetime comments and associate
    for i, line in enumerate(lines):
        if '|t{-' in line:
            print(f"\nLifetime line {i+1}: {line.strip()}")
            
            matches = re.findall(tau_pattern, line)
            print(f"Regex matches: {matches}")
            
            # Find most recent level
            recent_level = None
            for level_energy, level_line in reversed(levels):
                if level_line < i+1:
                    recent_level = level_energy
                    print(f"Most recent level: {recent_level} keV at line {level_line}")
                    break
            
            if recent_level is None:
                print("No recent level found!")
            else:
                print(f"Would associate with level {recent_level} keV")

if __name__ == "__main__":
    debug_lifetime_association()
