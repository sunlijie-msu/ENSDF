#!/usr/bin/env python3
"""
Debug script to understand lifetime extraction
"""

import re

def debug_ensdf_extraction():
    ensdf_file = "XUNDL/2025LAAA_CH11036_127I.ens"
    
    with open(ensdf_file, 'r') as f:
        lines = f.readlines()
    
    current_level = None
    lifetimes = {}
    
    for i, line in enumerate(lines):
        # Check for level records
        if len(line) > 8 and line[7] == 'L' and line[8] == ' ':
            # Extract energy from columns 10-19
            energy_str = line[9:19].strip()
            try:
                current_level = float(energy_str)
                print(f"Found level: {current_level} keV at line {i+1}")
            except:
                current_level = None
        
        # Check for lifetime comments
        elif 'GTA' in line or 'GTB' in line or 'Ave' in line:
            print(f"Found lifetime line {i+1}: {line.strip()}")
            if current_level is not None:
                print(f"  Associated with level {current_level} keV")
                
                # Extract τ values using regex
                tau_pattern = r'\|t\{-(\w+)\}=([0-9.]+) ps \{I\+(\d+)-(\d+)\}'
                matches = re.findall(tau_pattern, line)
                print(f"  Regex matches: {matches}")
                
                if current_level not in lifetimes:
                    lifetimes[current_level] = {}
                
                for match in matches:
                    tau_type, value, plus_err, minus_err = match
                    lifetimes[current_level][tau_type] = {
                        'value': float(value),
                        'plus': int(plus_err),
                        'minus': int(minus_err)
                    }
                    print(f"    Added {tau_type}: {value} +{plus_err}-{minus_err}")
    
    print(f"\nFinal extracted lifetimes: {lifetimes}")
    return lifetimes

if __name__ == "__main__":
    debug_ensdf_extraction()
