#!/usr/bin/env python3
"""
Corrected extraction that properly associates lifetime comments with levels
"""

import re

def corrected_extraction():
    ensdf_file = "XUNDL/2025LAAA_CH11036_127I.ens"
    
    with open(ensdf_file, 'r') as f:
        lines = f.readlines()
    
    levels = []  # Keep track of all levels in order
    lifetimes = {}
    
    tau_pattern = r'\|t\{-(\w+)\}=([0-9.]+) ps \{I\+(\d+)-(\d+)\}'
    
    for i, line in enumerate(lines):
        # Check for level records
        if len(line) > 8 and line[7] == 'L' and line[8] == ' ':
            energy_str = line[9:19].strip()
            try:
                level_energy = float(energy_str)
                levels.append((level_energy, i+1))  # Store energy and line number
            except:
                pass
        
        # Check for lifetime comments
        elif '|t{-' in line:
            matches = re.findall(tau_pattern, line)
            if matches:
                # Find the most recent level before this comment
                current_level = None
                for level_energy, level_line in reversed(levels):
                    if level_line < i+1:  # Level must be before this comment
                        current_level = level_energy
                        break
                
                if current_level is not None:
                    if current_level not in lifetimes:
                        lifetimes[current_level] = {}
                    
                    print(f"Line {i+1}: Associating lifetime data with level {current_level} keV")
                    print(f"  Line content: {line.strip()}")
                    
                    for match in matches:
                        tau_type, value, plus_err, minus_err = match
                        lifetimes[current_level][tau_type] = {
                            'value': float(value),
                            'plus': int(plus_err) / 100.0,
                            'minus': int(minus_err) / 100.0
                        }
                        print(f"    {tau_type}: {value} +{plus_err/100:.2f}-{minus_err/100:.2f} ps")
                    print()
    
    print("Final extracted lifetimes:")
    for level in sorted(lifetimes.keys()):
        print(f"  {level} keV: {lifetimes[level]}")
    
    return lifetimes

if __name__ == "__main__":
    corrected_extraction()
