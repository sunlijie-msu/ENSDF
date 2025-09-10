#!/usr/bin/env python3
"""
Very simple debug test
"""

def basic_debug():
    ensdf_file = "XUNDL/2025LAAA_CH11036_127I.ens"
    
    try:
        with open(ensdf_file, 'r') as f:
            lines = f.readlines()
        
        print(f"File has {len(lines)} lines")
        
        # Find lines with lifetime data
        lifetime_lines = []
        for i, line in enumerate(lines):
            if '|t{-' in line:
                lifetime_lines.append((i+1, line.strip()))
        
        print(f"Found {len(lifetime_lines)} lifetime lines:")
        for line_num, content in lifetime_lines:
            print(f"  Line {line_num}: {content}")
        
        # Find level lines
        level_lines = []
        for i, line in enumerate(lines):
            if len(line) > 8 and line[7] == 'L' and line[8] == ' ':
                energy_str = line[9:19].strip()
                level_lines.append((i+1, energy_str, line.strip()))
        
        print(f"\nFound {len(level_lines)} level lines:")
        for line_num, energy, content in level_lines[:10]:  # Show first 10
            print(f"  Line {line_num}: {energy} keV -> {content}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    basic_debug()
