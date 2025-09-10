#!/usr/bin/env python3
"""
Verify J-π assignments including parentheses formatting between ENSDF and XUNDL files
with energy tolerance matching - FIXED to handle XUNDL band designations.
"""

import re

def extract_ensdf_levels(filename):
    """Extract level data from ENSDF file"""
    levels = []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Find L-records with energy and J-π
        l_records = re.findall(r'^127I\s+L\s+(\d+(?:\.\d+)?)\s+\d*\s+([^\s]+.*?)(?:\s+BAND\(\w\))?(?:\s+[A-Z])?$', content, re.MULTILINE)
        
        for energy_str, jpi in l_records:
            try:
                energy = float(energy_str)
                jpi_clean = jpi.strip()
                levels.append((energy, jpi_clean))
                print(f"ENSDF: {energy:8.2f} keV -> '{jpi_clean}'")
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
    """Extract level data from XUNDL file - handle band designations properly"""
    levels = []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Find L-records and extract J-π carefully
        lines = content.split('\n')
        for line in lines:
            if line.startswith('127I') and ' L ' in line:
                # Parse the L-record line manually
                parts = line.split()
                if len(parts) >= 4:
                    try:
                        energy = float(parts[2])
                        # The J-π is in the 4th position, but may have trailing band info
                        jpi_raw = parts[3]
                        
                        # Remove common band designations and trailing spaces
                        jpi_clean = jpi_raw.strip()
                        
                        levels.append((energy, jpi_clean))
                        print(f"XUNDL: {energy:8.2f} keV -> '{jpi_clean}'")
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

if __name__ == "__main__":
    main()
