#!/usr/bin/env python3
"""
Extract energy levels for all |w|γ entries from 1976Sp08 in ENSDF file.
This script finds all |w|γ=value (1976Sp08) entries and identifies 
the corresponding L-record energy by searching backwards from each match.
"""

import re
import sys

def extract_wgamma_with_levels(filename):
    """Extract all |w|γ entries with their corresponding level energies."""
    
    results = []
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Error reading file: {e}")
        return []
    
    # Find all |w|γ entries from 1976Sp08
    wgamma_pattern = r'\$\|w\|g=([\d\.]+)\s*eV\s*\{I(\d+)\}\s*\(1976Sp08\)'
    
    for i, line in enumerate(lines):
        match = re.search(wgamma_pattern, line)
        if match:
            wg_value = match.group(1)
            uncertainty = match.group(2)
            line_num = i + 1
            
            # Search backwards for the corresponding L-record
            level_energy = None
            for j in range(i - 1, -1, -1):
                if ' L ' in lines[j] and lines[j].strip().startswith('35CL'):
                    # Extract energy from L-record (columns 10-19, left-justified)
                    l_line = lines[j]
                    if len(l_line) >= 19:
                        energy_field = l_line[9:19].strip()
                        if energy_field and energy_field.replace('.', '').replace('-', '').isdigit():
                            level_energy = float(energy_field)
                            break
                # Stop if we hit another dataset or major structure change
                elif 'Dataset:' in lines[j] or lines[j].startswith('35CL  H '):
                    break
            
            if level_energy is not None:
                results.append({
                    'line': line_num,
                    'level_energy': level_energy,
                    'wg_value': wg_value,
                    'uncertainty': uncertainty,
                    'full_line': line.strip()
                })
            else:
                print(f"WARNING: Could not find level energy for line {line_num}: {line.strip()}")
    
    return results

def main():
    if len(sys.argv) != 2:
        print("Usage: python extract_wgamma_levels.py <ensdf_file>")
        sys.exit(1)
    
    filename = sys.argv[1]
    results = extract_wgamma_with_levels(filename)
    
    print(f"Found {len(results)} |w|γ entries from 1976Sp08:")
    print("=" * 80)
    print(f"{'Line':<6} {'Level Energy':<12} {'wγ Value':<10} {'Uncert':<6} {'Full Entry'}")
    print("-" * 80)
    
    for entry in results:
        uncert_str = f"{{I{entry['uncertainty']}}}"
        print(f"{entry['line']:<6} {entry['level_energy']:<12.1f} {entry['wg_value']:<10} {uncert_str:<8} {entry['full_line']}")
    
    return results

if __name__ == "__main__":
    main()