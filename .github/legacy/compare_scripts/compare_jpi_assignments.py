#!/usr/bin/env python3
"""
Comprehensive J-π comparison between main ENSDF file and reference XUNDL file.
Systematically compare all ~30 levels between the two files.
"""

import re

def extract_jpi_from_ensdf(filename):
    """Extract energy and J-π from ENSDF L records."""
    levels = {}
    
    with open(filename, 'r') as f:
        for line in f:
            if len(line) >= 8 and line[7] == 'L':
                # Extract energy from columns 10-19
                energy_str = line[9:19].strip()
                if energy_str:
                    try:
                        energy = float(energy_str)
                        # Extract J-π from columns 23-39 (left-justified)
                        jpi_str = line[22:39].strip()
                        if jpi_str:
                            levels[energy] = jpi_str
                        else:
                            levels[energy] = "NO J-π"
                    except ValueError:
                        continue
    
    return levels

def extract_jpi_from_xundl(filename):
    """Extract energy and J-π from XUNDL file."""
    levels = {}
    
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if '|' in line and not line.startswith('ELI'):
                parts = line.split('|')
                if len(parts) >= 2:
                    # ELI column (initial level)
                    eli_str = parts[0].strip()
                    ji_str = parts[1].strip()
                    
                    # Extract energy from strings like "57.46(8)" 
                    energy_match = re.match(r'([\d.]+)', eli_str)
                    if energy_match:
                        try:
                            energy = float(energy_match.group(1))
                            levels[energy] = ji_str
                        except ValueError:
                            continue
                    
                    # Also check ELF column (final level) if different
                    if len(parts) >= 4:
                        elf_str = parts[2].strip()
                        jf_str = parts[3].strip()
                        
                        energy_match = re.match(r'([\d.]+)', elf_str)
                        if energy_match:
                            try:
                                energy = float(energy_match.group(1))
                                if energy not in levels:  # Don't overwrite if already present
                                    levels[energy] = jf_str
                            except ValueError:
                                continue
    
    return levels

def compare_jpi_assignments(ensdf_file, xundl_file):
    """Compare J-π assignments between ENSDF and XUNDL files."""
    
    print("COMPREHENSIVE J-π COMPARISON ANALYSIS")
    print("=" * 70)
    print(f"ENSDF file: {ensdf_file}")
    print(f"XUNDL file: {xundl_file}")
    print()
    
    ensdf_levels = extract_jpi_from_ensdf(ensdf_file)
    xundl_levels = extract_jpi_from_xundl(xundl_file)
    
    print(f"ENSDF levels found: {len(ensdf_levels)}")
    print(f"XUNDL levels found: {len(xundl_levels)}")
    print()
    
    # Match levels by energy (within tolerance)
    tolerance = 1.0  # keV tolerance for matching
    matches = []
    ensdf_only = []
    xundl_only = []
    
    for ensdf_energy, ensdf_jpi in sorted(ensdf_levels.items()):
        best_match = None
        best_diff = float('inf')
        
        for xundl_energy, xundl_jpi in xundl_levels.items():
            diff = abs(ensdf_energy - xundl_energy)
            if diff < tolerance and diff < best_diff:
                best_match = (xundl_energy, xundl_jpi)
                best_diff = diff
        
        if best_match:
            matches.append((ensdf_energy, ensdf_jpi, best_match[0], best_match[1], best_diff))
        else:
            ensdf_only.append((ensdf_energy, ensdf_jpi))
    
    # Find XUNDL levels without ENSDF matches
    for xundl_energy, xundl_jpi in sorted(xundl_levels.items()):
        found_match = False
        for ensdf_energy in ensdf_levels:
            if abs(xundl_energy - ensdf_energy) < tolerance:
                found_match = True
                break
        if not found_match:
            xundl_only.append((xundl_energy, xundl_jpi))
    
    # Generate detailed comparison report
    print("DETAILED LEVEL-BY-LEVEL COMPARISON:")
    print("=" * 70)
    print(f"{'#':<3} {'ENSDF E':<10} {'ENSDF J-π':<12} {'XUNDL E':<10} {'XUNDL J-π':<12} {'Status'}")
    print("-" * 70)
    
    consistent_count = 0
    inconsistent_count = 0
    
    for i, (ensdf_e, ensdf_jpi, xundl_e, xundl_jpi, diff) in enumerate(sorted(matches), 1):
        # Normalize J-π strings for comparison
        ensdf_norm = ensdf_jpi.replace(' ', '').replace('(', '').replace(')', '')
        xundl_norm = xundl_jpi.replace(' ', '').replace('(', '').replace(')', '')
        
        if ensdf_norm == xundl_norm or ensdf_jpi == xundl_jpi:
            status = "✅ CONSISTENT"
            consistent_count += 1
        else:
            status = "❌ INCONSISTENT"
            inconsistent_count += 1
        
        print(f"{i:<3} {ensdf_e:<10.2f} {ensdf_jpi:<12} {xundl_e:<10.2f} {xundl_jpi:<12} {status}")
    
    # Show levels only in ENSDF
    if ensdf_only:
        print(f"\nLEVELS ONLY IN ENSDF ({len(ensdf_only)}):")
        print("-" * 35)
        for i, (energy, jpi) in enumerate(ensdf_only, 1):
            print(f"{len(matches)+i:<3} {energy:<10.2f} {jpi:<12} {'---':<10} {'---':<12} ENSDF ONLY")
    
    # Show levels only in XUNDL
    if xundl_only:
        print(f"\nLEVELS ONLY IN XUNDL ({len(xundl_only)}):")
        print("-" * 35)
        for energy, jpi in xundl_only:
            print(f"    {'---':<10} {'---':<12} {energy:<10.2f} {jpi:<12} XUNDL ONLY")
    
    print(f"\nSUMMARY:")
    print("=" * 30)
    print(f"✅ Consistent J-π: {consistent_count}")
    print(f"❌ Inconsistent J-π: {inconsistent_count}")
    print(f"📊 Total compared: {len(matches)}")
    print(f"📝 ENSDF only: {len(ensdf_only)}")
    print(f"📄 XUNDL only: {len(xundl_only)}")
    
    if inconsistent_count == 0:
        print(f"\n🎯 PERFECT! All J-π assignments are consistent!")
    else:
        print(f"\n⚠️  {inconsistent_count} levels need J-π review/correction")
    
    return matches, ensdf_only, xundl_only, consistent_count, inconsistent_count

if __name__ == "__main__":
    ensdf_file = "XUNDL/2025LAAA_CH11036_127I.ens"
    xundl_file = "XUNDL/2012DI06_127I_all_gamma_transitions.xundl"
    
    compare_jpi_assignments(ensdf_file, xundl_file)
