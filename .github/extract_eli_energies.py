#!/usr/bin/env python3
"""
Extract ELI (initial level) energies from 2025LAAA_vs_2012DI06.ens comparison file
to determine which L records should exist in the main ENSDF file.
"""

import re
import sys

def extract_eli_energies(filename):
    """Extract all unique ELI energies from the comparison file."""
    eli_energies = set()
    
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    # Find the data section (after the header lines)
    data_started = False
    for line in lines:
        line = line.strip()
        
        # Skip header lines
        if 'ELI' in line and 'JI' in line and 'ELF' in line:
            data_started = True
            continue
        if not data_started:
            continue
        if line.startswith('---'):
            continue
        if not line or line.startswith('FINAL') or line.startswith('='):
            continue
            
        # Parse data lines - ELI is the first column
        parts = line.split('|')
        if len(parts) >= 2:
            eli_str = parts[0].strip()
            # Remove 'TBD' entries
            if eli_str != 'TBD' and eli_str:
                try:
                    eli_energy = float(eli_str)
                    eli_energies.add(eli_energy)
                except ValueError:
                    continue
    
    return sorted(eli_energies)

def main():
    comparison_file = "XUNDL/2025LAAA_vs_2012DI06.ens"
    
    try:
        eli_energies = extract_eli_energies(comparison_file)
        
        print(f"Found {len(eli_energies)} unique ELI (initial level) energies:")
        print("=" * 50)
        for i, energy in enumerate(eli_energies, 1):
            print(f"{i:2d}. {energy:8.2f} keV")
        
        print("\n" + "=" * 50)
        print("These are the ONLY level energies that should have L records in 2025LAAA_CH11036_127I.ens")
        
        return eli_energies
        
    except Exception as e:
        print(f"Error: {e}")
        return []

if __name__ == "__main__":
    main()
