#!/usr/bin/env python3
"""
Check the specific 10 levels from the user's image for parentheses consistency.
Image shows ALL levels WITHOUT parentheses, but let's verify what's actually in the files.
"""

import re

def check_specific_levels():
    """Check the specific levels from the image"""
    
    # Image levels (ALL WITHOUT parentheses according to user)
    image_levels = [
        (3958.7, "27/2-"),   # Image shows NO parentheses
        (2976.6, "23/2-"),   # Image shows NO parentheses  
        (2545.4, "19/2-"),   # Image shows NO parentheses
        (1893.9, "15/2-"),   # Image shows NO parentheses
        (1235.2, "11/2-"),   # Image shows NO parentheses
        (2356.7, "19/2+"),   # Image shows NO parentheses
        (1876.2, "17/2+"),   # Image shows NO parentheses
        (1479.7, "15/2+"),   # Image shows NO parentheses
        (716.4, "11/2+"),    # Image shows NO parentheses
        (744.9, "9/2+"),     # Image shows NO parentheses
    ]
    
    ensdf_file = "XUNDL/2025LAAA_CH11036_127I.ens"
    xundl_file = "XUNDL/2012DI06_127I_xundl-1.xundl"
    
    print("CHECKING 10 SPECIFIC LEVELS FROM IMAGE")
    print("="*60)
    print("Image shows ALL levels WITHOUT parentheses")
    print("Let's verify what's actually in the ENSDF and XUNDL files...")
    print()
    
    # Read ENSDF file
    ensdf_levels = {}
    try:
        with open(ensdf_file, 'r', encoding='utf-8') as f:
            content = f.read()
        lines = content.split('\n')
        for line in lines:
            if line.startswith('127I') and ' L ' in line:
                match = re.match(r'^127I\s+L\s+(\d+(?:\.\d+)?)\s+(\d+\s+)?([^\s].*?)(?:\s*)?$', line)
                if match:
                    energy_str = match.group(1)
                    jpi = match.group(3).strip()
                    try:
                        energy = float(energy_str)
                        ensdf_levels[energy] = jpi
                    except ValueError:
                        continue
    except Exception as e:
        print(f"Error reading ENSDF file: {e}")
        return
    
    # Read XUNDL file
    xundl_levels = {}
    try:
        with open(xundl_file, 'r', encoding='utf-8') as f:
            content = f.read()
        lines = content.split('\n')
        for line in lines:
            if line.startswith('127I') and ' L ' in line:
                parts = line.split()
                if len(parts) >= 4:
                    try:
                        energy = float(parts[2])
                        # Find J-π: skip past uncertainty if present
                        jpi_candidates = parts[3:]
                        jpi = None
                        for candidate in jpi_candidates:
                            if '/' in candidate or '(' in candidate or candidate.endswith(('+', '-')):
                                jpi = candidate
                                break
                        if jpi:
                            xundl_levels[energy] = jpi
                    except (ValueError, IndexError):
                        continue
    except Exception as e:
        print(f"Error reading XUNDL file: {e}")
        return
    
    def find_closest_level(target_energy, levels_dict, tolerance=2.0):
        """Find closest level within tolerance"""
        best_match = None
        best_diff = float('inf')
        for energy, jpi in levels_dict.items():
            diff = abs(energy - target_energy)
            if diff <= tolerance and diff < best_diff:
                best_match = (energy, jpi)
                best_diff = diff
        return best_match
    
    print(f"{'Image Energy':>12} {'Image J-π':>10} {'ENSDF Energy':>12} {'ENSDF J-π':>12} {'XUNDL Energy':>12} {'XUNDL J-π':>12} {'Status':>15}")
    print("-" * 95)
    
    issues_found = 0
    
    for img_energy, img_jpi in image_levels:
        ensdf_match = find_closest_level(img_energy, ensdf_levels)
        xundl_match = find_closest_level(img_energy, xundl_levels)
        
        ensdf_energy, ensdf_jpi = ensdf_match if ensdf_match else (0, "NOT FOUND")
        xundl_energy, xundl_jpi = xundl_match if xundl_match else (0, "NOT FOUND")
        
        # Check for parentheses issues
        status = "✅ CONSISTENT"
        if ensdf_jpi != "NOT FOUND" and ensdf_jpi != img_jpi:
            if ensdf_jpi.startswith('(') and ensdf_jpi.endswith(')'):
                status = "❌ ENSDF HAS ()"
                issues_found += 1
            else:
                status = "❌ J-π MISMATCH"
                issues_found += 1
        
        if xundl_jpi != "NOT FOUND" and xundl_jpi != img_jpi:
            if xundl_jpi.startswith('(') and xundl_jpi.endswith(')'):
                if status == "✅ CONSISTENT":
                    status = "❌ XUNDL HAS ()"
                else:
                    status = "❌ BOTH HAVE ()"
                issues_found += 1
        
        print(f"{img_energy:12.1f} {img_jpi:>10} {ensdf_energy:12.1f} {ensdf_jpi:>12} {xundl_energy:12.1f} {xundl_jpi:>12} {status:>15}")
        
        # Detailed analysis for mismatches
        if status != "✅ CONSISTENT":
            print(f"  → IMAGE: '{img_jpi}' (NO parentheses)")
            if ensdf_jpi != "NOT FOUND":
                print(f"  → ENSDF: '{ensdf_jpi}' {'(HAS parentheses)' if ensdf_jpi.startswith('(') else '(NO parentheses)'}")
            if xundl_jpi != "NOT FOUND":
                print(f"  → XUNDL: '{xundl_jpi}' {'(HAS parentheses)' if xundl_jpi.startswith('(') else '(NO parentheses)'}")
            print()
    
    print("\n" + "="*60)
    print(f"SUMMARY:")
    print(f"Issues found: {issues_found}")
    
    if issues_found > 0:
        print(f"\n⚠️ USER IS CORRECT! There are parentheses inconsistencies!")
        print(f"The image shows levels WITHOUT parentheses, but files may have parentheses.")
    else:
        print(f"\n✅ All levels match the image formatting")

if __name__ == "__main__":
    check_specific_levels()
