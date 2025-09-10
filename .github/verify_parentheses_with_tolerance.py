#!/usr/bin/env python3
"""
Verify J-π assignments between ENSDF and XUNDL files with energy tolerance matching.
Accounts for sub-keV differences in energy measurements.
"""

import re

def extract_ensdf_levels(filename):
    """Extract energy levels and J-π from ENSDF file."""
    levels = []
    try:
        with open(filename, 'r') as f:
            for line in f:
                if line.startswith('127I   L '):
                    # Extract energy (columns 10-19) and J-π (columns 23-39)
                    energy_str = line[9:19].strip()
                    jpi_str = line[22:39].strip()
                    
                    if energy_str and jpi_str:
                        try:
                            energy = float(energy_str)
                            levels.append((energy, jpi_str))
                        except ValueError:
                            continue
    except FileNotFoundError:
        print(f"Error: File {filename} not found")
        return []
    
    return sorted(levels)

def extract_xundl_levels(filename):
    """Extract energy levels and J-π from XUNDL comparison file."""
    levels = []
    try:
        with open(filename, 'r') as f:
            content = f.read()
            
            # Look for sections with level data
            # Pattern: energy value followed by J-π assignment
            # Example: 0.00     5/2+     0.0      5/2+
            lines = content.split('\n')
            
            for line in lines:
                # Skip header lines and comments
                if line.strip().startswith('#') or 'Initial' in line or 'Final' in line:
                    continue
                
                # Look for lines with energy and J-π data
                # Split by whitespace and look for energy + J-π patterns
                parts = line.split()
                if len(parts) >= 4:
                    try:
                        # Try to parse first value as energy
                        energy = float(parts[0])
                        # Look for J-π pattern in subsequent parts
                        for i in range(1, len(parts)):
                            if re.match(r'^\(?[0-9]+/2[+-]\)?$', parts[i]):
                                jpi = parts[i]
                                levels.append((energy, jpi))
                                break
                    except (ValueError, IndexError):
                        continue
    except FileNotFoundError:
        print(f"Error: File {filename} not found")
        return []
    
    return sorted(list(set(levels)))  # Remove duplicates and sort

def find_matching_level(target_energy, levels, tolerance=1.0):
    """Find level within tolerance of target energy."""
    for energy, jpi in levels:
        if abs(energy - target_energy) <= tolerance:
            return energy, jpi
    return None, None

def main():
    ensdf_file = "XUNDL/2025LAAA_CH11036_127I.ens"
    xundl_file = "XUNDL/2025LAAA_vs_2012DI06.ens"
    
    print("DETAILED PARENTHESES VERIFICATION WITH ENERGY TOLERANCE")
    print("=" * 80)
    print(f"Comparing {ensdf_file} vs {xundl_file}")
    print(f"Using energy tolerance: ±1.0 keV")
    print()
    
    # Extract levels from both files
    ensdf_levels = extract_ensdf_levels(ensdf_file)
    xundl_levels = extract_xundl_levels(xundl_file)
    
    print(f"Found {len(ensdf_levels)} levels in ENSDF file")
    print(f"Found {len(xundl_levels)} levels in XUNDL file")
    print()
    
    # Compare each ENSDF level with XUNDL levels
    print("LEVEL-BY-LEVEL COMPARISON WITH TOLERANCE MATCHING:")
    print("-" * 80)
    print(f"{'#':<3} {'ENSDF Energy':<12} {'ENSDF J-π':<12} {'XUNDL Energy':<12} {'XUNDL J-π':<12} {'Status':<15}")
    print("-" * 80)
    
    consistent_count = 0
    inconsistent_count = 0
    not_found_count = 0
    
    for i, (ensdf_energy, ensdf_jpi) in enumerate(ensdf_levels, 1):
        # Find matching level in XUNDL data
        xundl_energy, xundl_jpi = find_matching_level(ensdf_energy, xundl_levels, tolerance=1.0)
        
        if xundl_jpi is None:
            status = "❌ NOT FOUND"
            not_found_count += 1
            xundl_energy_str = "---"
            xundl_jpi_str = "---"
        elif ensdf_jpi == xundl_jpi:
            status = "✅ CONSISTENT"
            consistent_count += 1
            xundl_energy_str = f"{xundl_energy:.2f}"
            xundl_jpi_str = xundl_jpi
        else:
            status = "⚠️ DIFFERENT"
            inconsistent_count += 1
            xundl_energy_str = f"{xundl_energy:.2f}"
            xundl_jpi_str = xundl_jpi
        
        print(f"{i:<3} {ensdf_energy:<12.2f} {ensdf_jpi:<12} {xundl_energy_str:<12} {xundl_jpi_str:<12} {status:<15}")
    
    print("-" * 80)
    print()
    
    # Summary statistics
    total_levels = len(ensdf_levels)
    print("SUMMARY STATISTICS:")
    print("=" * 40)
    print(f"Total ENSDF levels: {total_levels}")
    print(f"Consistent J-π assignments: {consistent_count}")
    print(f"Inconsistent J-π assignments: {inconsistent_count}")
    print(f"Not found in XUNDL: {not_found_count}")
    print(f"Consistency rate: {(consistent_count/total_levels)*100:.1f}%")
    print()
    
    # Check for parentheses issues specifically
    print("PARENTHESES ANALYSIS:")
    print("=" * 40)
    parentheses_issues = []
    
    for ensdf_energy, ensdf_jpi in ensdf_levels:
        xundl_energy, xundl_jpi = find_matching_level(ensdf_energy, xundl_levels, tolerance=1.0)
        
        if xundl_jpi and ensdf_jpi != xundl_jpi:
            # Check if the difference is only parentheses
            ensdf_core = ensdf_jpi.strip('()')
            xundl_core = xundl_jpi.strip('()')
            
            if ensdf_core == xundl_core:
                parentheses_issues.append((ensdf_energy, ensdf_jpi, xundl_jpi))
    
    if parentheses_issues:
        print("PARENTHESES FORMATTING ISSUES FOUND:")
        print(f"{'Energy':<10} {'ENSDF J-π':<12} {'XUNDL J-π':<12}")
        print("-" * 35)
        for energy, ensdf_jpi, xundl_jpi in parentheses_issues:
            print(f"{energy:<10.2f} {ensdf_jpi:<12} {xundl_jpi:<12}")
    else:
        print("✅ No parentheses formatting issues detected")
    
    print()
    
    # Final verdict
    if inconsistent_count == 0:
        print("🎯 PERFECT! All J-π assignments are consistent with tolerance matching!")
    else:
        print(f"⚠️ Found {inconsistent_count} inconsistent J-π assignments")
        print("❗ Manual review required for inconsistent assignments")

if __name__ == "__main__":
    main()
