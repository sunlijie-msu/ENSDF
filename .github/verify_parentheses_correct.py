#!/usr/bin/env python3
"""
Verify J-π assignments including parentheses formatting between ENSDF and XUNDL files
with energy tolerance matching - PROPERLY HANDLES XUNDL FORMAT.
"""

import re

def extract_ensdf_levels(filename):
    """Extract level data from ENSDF file"""
    levels = []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Find L-records with energy and J-π
        lines = content.split('\n')
        for line in lines:
            if line.startswith('127I') and ' L ' in line:
                # Parse ENSDF L-record: NUCID L Energy [DE] J-π
                match = re.match(r'^127I\s+L\s+(\d+(?:\.\d+)?)\s+(\d+\s+)?([^\s].*?)(?:\s+BAND\(\w\))?(?:\s*)?$', line)
                if match:
                    energy_str = match.group(1)
                    jpi = match.group(3).strip()
                    try:
                        energy = float(energy_str)
                        levels.append((energy, jpi))
                        print(f"ENSDF: {energy:8.2f} keV -> '{jpi}'")
                    except ValueError:
                        continue
                
    except FileNotFoundError:
        print(f"File not found: {filename}")
        return []
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return []
    
    return sorted(levels)

def extract_xundl_levels(filename):
    """Extract level data from XUNDL file - handle format: 127I L Energy [DE] J-π [BAND]"""
    levels = []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            
        lines = content.split('\n')
        for line in lines:
            if line.startswith('127I') and ' L ' in line:
                # Parse XUNDL L-record: 127I L Energy [DE] J-π [BAND]
                # Example: "127I   L 57.46      8 7/2+                                                  b"
                parts = line.split()
                if len(parts) >= 4:
                    try:
                        energy = float(parts[2])
                        
                        # Find J-π: skip past uncertainty if present
                        jpi_candidates = parts[3:]
                        jpi = None
                        
                        for candidate in jpi_candidates:
                            # Look for J-π pattern (contains / or parentheses, not just digits)
                            if '/' in candidate or '(' in candidate or candidate.endswith(('+', '-')):
                                jpi = candidate
                                break
                            # Also check if it's a simple J value like "5/2+" but written as separate components
                            elif candidate in ['5/2+', '7/2+', '9/2+', '11/2+', '13/2+', '15/2+', '17/2+', '19/2+', '21/2+', '23/2+', '25/2+', '27/2+', '29/2+', '31/2+', '33/2+', '35/2+',
                                              '5/2-', '7/2-', '9/2-', '11/2-', '13/2-', '15/2-', '17/2-', '19/2-', '21/2-', '23/2-', '25/2-', '27/2-', '29/2-', '31/2-', '33/2-', '35/2-']:
                                jpi = candidate
                                break
                        
                        # If no clear J-π found, reconstruct from the line
                        if not jpi:
                            # Find everything after the uncertainty (number) but before band designation
                            line_after_energy = line[line.find(parts[2]) + len(parts[2]):].strip()
                            # Remove leading uncertainty number if present
                            if line_after_energy and line_after_energy[0].isdigit():
                                line_after_energy = line_after_energy.split(None, 1)[1] if ' ' in line_after_energy else ''
                            
                            # Extract J-π part (everything before excessive spaces that indicate band designation)
                            jpi_match = re.match(r'^([^\s]+(?:/\d+)?[+-]?(?:\([^)]*\))?[+-]?)', line_after_energy)
                            if jpi_match:
                                jpi = jpi_match.group(1)
                        
                        if jpi:
                            levels.append((energy, jpi))
                            print(f"XUNDL: {energy:8.2f} keV -> '{jpi}'")
                            
                    except (ValueError, IndexError):
                        continue
                
    except FileNotFoundError:
        print(f"File not found: {filename}")
        return []
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return []
    
    return sorted(levels)

def find_matching_level(target_energy, levels, tolerance=1.0):
    """Find matching level within tolerance"""
    for energy, jpi in levels:
        if abs(energy - target_energy) <= tolerance:
            return energy, jpi
    return None, None

def main():
    print("DETAILED J-π PARENTHESES VERIFICATION WITH TOLERANCE MATCHING")
    print("="*80)
    
    ensdf_file = "XUNDL/2025LAAA_CH11036_127I.ens"
    xundl_file = "XUNDL/2012DI06_127I_xundl-1.xundl"
    
    print(f"\nExtracting ENSDF levels from {ensdf_file}:")
    print("-" * 50)
    ensdf_levels = extract_ensdf_levels(ensdf_file)
    
    print(f"\nExtracting XUNDL levels from {xundl_file}:")
    print("-" * 50)
    xundl_levels = extract_xundl_levels(xundl_file)
    
    print(f"\nCOMPARISON RESULTS:")
    print("="*80)
    print(f"{'ENSDF Energy':>12} {'ENSDF J-π':>12} {'XUNDL Energy':>12} {'XUNDL J-π':>12} {'Status':>15}")
    print("-" * 80)
    
    consistent = 0
    inconsistent = 0
    tolerance = 1.0  # keV
    
    for ensdf_energy, ensdf_jpi in ensdf_levels:
        xundl_energy, xundl_jpi = find_matching_level(ensdf_energy, xundl_levels, tolerance)
        
        if xundl_energy is not None:
            if ensdf_jpi == xundl_jpi:
                status = "✅ CONSISTENT"
                consistent += 1
            else:
                status = "❌ MISMATCH"
                inconsistent += 1
                print(f"    MISMATCH: '{ensdf_jpi}' vs '{xundl_jpi}'")
                
            print(f"{ensdf_energy:12.2f} {ensdf_jpi:>12} {xundl_energy:12.2f} {xundl_jpi:>12} {status:>15}")
        else:
            print(f"{ensdf_energy:12.2f} {ensdf_jpi:>12} {'---':>12} {'---':>12} {'❌ NO MATCH':>15}")
            inconsistent += 1
    
    print("\n" + "="*80)
    print(f"SUMMARY:")
    print(f"  Total ENSDF levels: {len(ensdf_levels)}")
    print(f"  Total XUNDL levels: {len(xundl_levels)}")
    print(f"  Consistent matches: {consistent}")
    print(f"  Inconsistent/missing: {inconsistent}")
    print(f"  Tolerance used: ±{tolerance} keV")
    
    if inconsistent == 0:
        print(f"\n🎯 PERFECT! All J-π assignments including parentheses are consistent!")
    else:
        print(f"\n⚠️  Found {inconsistent} inconsistencies that need attention!")
        
        # Show image verification
        print(f"\nIMAGE VERIFICATION CHECK:")
        print(f"Checking levels from user's image against both files...")
        image_levels = [
            (3957.9, "(27/2-)"),  # From image 
            (2976.1, "23/2-"),    # From image
            (2545.4, "19/2-"),    # From image  
            (1893.9, "15/2-"),    # From image
            (1235.2, "11/2-"),    # From image
        ]
        
        for img_energy, img_jpi in image_levels:
            ensdf_match = find_matching_level(img_energy, ensdf_levels, 1.0)
            xundl_match = find_matching_level(img_energy, xundl_levels, 1.0)
            
            print(f"  {img_energy:8.1f} keV image: {img_jpi}")
            if ensdf_match[0]:
                print(f"    ENSDF: {ensdf_match[1]} {'✅' if ensdf_match[1] == img_jpi else '❌'}")
            if xundl_match[0]:
                print(f"    XUNDL: {xundl_match[1]} {'✅' if xundl_match[1] == img_jpi else '❌'}")

if __name__ == "__main__":
    main()
