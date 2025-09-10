#!/usr/bin/env python3
"""
Detailed verification of J-π parentheses formatting between ENSDF and XUNDL files.
This script specifically checks that tentative assignments (with parentheses) match exactly.
"""

import re

def extract_levels_with_parentheses(file_path):
    """Extract levels with exact J-π formatting including parentheses."""
    levels = []
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Pattern for L-records: capture energy and J-π with exact formatting
    l_pattern = r'127I\s+L\s+(\d+(?:\.\d+)?)\s+([^\s]+(?:\s+[^\s]+)*?)\s*(?:\n|$)'
    
    for match in re.finditer(l_pattern, content, re.MULTILINE):
        energy_str = match.group(1)
        jpi_field = match.group(2).strip()
        
        # Clean up the J-π field - remove extra spaces but preserve parentheses
        jpi_clean = re.sub(r'\s+', ' ', jpi_field).strip()
        
        # Split on whitespace and take the first part as J-π
        jpi_parts = jpi_clean.split()
        if jpi_parts:
            jpi = jpi_parts[0]
            energy = float(energy_str)
            levels.append((energy, jpi))
    
    return sorted(levels, key=lambda x: x[0])

def main():
    print("DETAILED PARENTHESES FORMATTING VERIFICATION")
    print("=" * 80)
    print("Checking exact J-π formatting including parentheses between files\n")
    
    # Extract levels from both files
    ensdf_file = "XUNDL/2025LAAA_CH11036_127I.ens"
    xundl_file = "XUNDL/2025LAAA_vs_2012DI06.ens"
    
    print(f"Reading ENSDF file: {ensdf_file}")
    ensdf_levels = extract_levels_with_parentheses(ensdf_file)
    print(f"Found {len(ensdf_levels)} levels in ENSDF file")
    
    print(f"Reading XUNDL file: {xundl_file}")
    xundl_levels = extract_levels_with_parentheses(xundl_file)
    print(f"Found {len(xundl_levels)} levels in XUNDL file\n")
    
    # Create lookup for XUNDL levels
    xundl_dict = {energy: jpi for energy, jpi in xundl_levels}
    
    print("DETAILED PARENTHESES COMPARISON:")
    print("-" * 80)
    print(f"{'Level':<5} {'Energy':<10} {'ENSDF J-π':<12} {'XUNDL J-π':<12} {'Parentheses':<12} {'Status'}")
    print("-" * 80)
    
    inconsistencies = 0
    parentheses_issues = 0
    
    for i, (energy, ensdf_jpi) in enumerate(ensdf_levels, 1):
        if energy in xundl_dict:
            xundl_jpi = xundl_dict[energy]
            
            # Check exact formatting including parentheses
            exact_match = ensdf_jpi == xundl_jpi
            
            # Check parentheses specifically
            ensdf_has_parens = '(' in ensdf_jpi and ')' in ensdf_jpi
            xundl_has_parens = '(' in xundl_jpi and ')' in xundl_jpi
            parens_match = ensdf_has_parens == xundl_has_parens
            
            # Status determination
            if exact_match:
                status = "✅ EXACT MATCH"
            elif not parens_match:
                status = "❌ PARENTHESES MISMATCH"
                parentheses_issues += 1
                inconsistencies += 1
            else:
                status = "⚠️ VALUE MISMATCH"
                inconsistencies += 1
            
            parens_status = "MATCH" if parens_match else "DIFFER"
            
            print(f"{i:<5} {energy:<10.2f} {ensdf_jpi:<12} {xundl_jpi:<12} {parens_status:<12} {status}")
        else:
            print(f"{i:<5} {energy:<10.2f} {ensdf_jpi:<12} {'NOT FOUND':<12} {'N/A':<12} ❌ MISSING")
            inconsistencies += 1
    
    print("-" * 80)
    print(f"SUMMARY:")
    print(f"Total levels compared: {len(ensdf_levels)}")
    print(f"Exact matches (including parentheses): {len(ensdf_levels) - inconsistencies}")
    print(f"Total inconsistencies: {inconsistencies}")
    print(f"Parentheses formatting issues: {parentheses_issues}")
    
    if inconsistencies == 0:
        print("\n🎯 PERFECT! All J-π assignments including parentheses are identical!")
    else:
        print(f"\n⚠️ WARNING: {inconsistencies} inconsistencies found!")
        if parentheses_issues > 0:
            print(f"⚠️ CRITICAL: {parentheses_issues} parentheses formatting issues detected!")
    
    print("\nSPECIFIC IMAGE LEVELS CHECK:")
    print("-" * 40)
    image_energies = [3958.7, 2976.6, 2545.4, 1893.9, 1235.2, 2356.7, 1876.2, 1479.7, 716.4, 744.9]
    image_jpis = ["27/2-", "23/2-", "19/2-", "15/2-", "11/2-", "19/2+", "17/2+", "15/2+", "11/2+", "9/2+"]
    
    for img_energy, img_jpi in zip(image_energies, image_jpis):
        # Find closest energy match (within 0.5 keV)
        closest_level = None
        min_diff = float('inf')
        
        for energy, ensdf_jpi in ensdf_levels:
            diff = abs(energy - img_energy)
            if diff < min_diff and diff < 0.5:
                min_diff = diff
                closest_level = (energy, ensdf_jpi)
        
        if closest_level:
            energy, ensdf_jpi = closest_level
            xundl_jpi = xundl_dict.get(energy, "NOT FOUND")
            
            # Check if image J-π matches files (no parentheses in image)
            ensdf_core = ensdf_jpi.strip('()')
            xundl_core = xundl_jpi.strip('()')
            
            img_match_ensdf = img_jpi == ensdf_core
            img_match_xundl = img_jpi == xundl_core
            
            status = "✅" if (img_match_ensdf and img_match_xundl) else "❌"
            
            print(f"{img_energy:>6.1f} keV: Image={img_jpi:<8} ENSDF={ensdf_jpi:<12} XUNDL={xundl_jpi:<12} {status}")
        else:
            print(f"{img_energy:>6.1f} keV: Image={img_jpi:<8} NOT FOUND IN FILES                   ❌")

if __name__ == "__main__":
    main()
