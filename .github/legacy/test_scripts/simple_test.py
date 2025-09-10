#!/usr/bin/env python3
"""
Simple direct test of the ENSDF file reading
"""

import re

def simple_extraction_test():
    ensdf_file = "XUNDL/2025LAAA_CH11036_127I.ens"
    
    with open(ensdf_file, 'r') as f:
        lines = f.readlines()
    
    current_level = None
    lifetimes = {}
    
    tau_pattern = r'\|t\{-(\w+)\}=([0-9.]+) ps \{I\+(\d+)-(\d+)\}'
    
    for i, line in enumerate(lines):
        # Check for level records
        if len(line) > 8 and line[7] == 'L' and line[8] == ' ':
            energy_str = line[9:19].strip()
            try:
                current_level = float(energy_str)
                print(f"Level found: {current_level} keV at line {i+1}")
            except:
                current_level = None
        
        # Check for any line with τ values
        if '|t{-' in line:
            print(f"Lifetime line {i+1}: {line.strip()}")
            print(f"  Current level: {current_level}")
            
            matches = re.findall(tau_pattern, line)
            print(f"  Matches: {matches}")
            
            if current_level is not None and matches:
                if current_level not in lifetimes:
                    lifetimes[current_level] = {}
                
                for match in matches:
                    tau_type, value, plus_err, minus_err = match
                    lifetimes[current_level][tau_type] = {
                        'value': float(value),
                        'plus': int(plus_err) / 100.0,
                        'minus': int(minus_err) / 100.0
                    }
                    print(f"    Added {tau_type}: {value} +{plus_err}-{minus_err}")
            print()
    
    print(f"Final extracted lifetimes:")
    for level, data in lifetimes.items():
        print(f"  {level} keV: {data}")

if __name__ == "__main__":
    simple_extraction_test()
