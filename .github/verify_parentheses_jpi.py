#!/usr/bin/env python3
"""
Comprehensive J-π comparison with parentheses verification
Compares ENSDF file with XUNDL comparison table, focusing on parentheses formatting
"""

import re

def parse_comparison_table(filepath):
    """Parse the comparison table to extract J-π values with parentheses"""
    jpi_data = {}
    
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Find all lines with energy and J-π data
    pattern = r'(\d+\.?\d*)\s+\|\s+([^|]+?)\s+\|'
    
    lines = content.split('\n')
    for line in lines:
        if '|' in line and 'keV' not in line and '----' not in line and 'ELI' not in line:
            # Extract initial level energy and J-π
            parts = line.split('|')
            if len(parts) >= 2:
                try:
                    energy_str = parts[0].strip()
                    jpi_str = parts[1].strip()
                    
                    if energy_str and jpi_str and energy_str.replace('.', '').isdigit():
                        energy = float(energy_str)
                        jpi_data[energy] = jpi_str
                        print(f"Comparison table: {energy} keV → {jpi_str}")
                except (ValueError, IndexError):
                    continue
    
    return jpi_data

def parse_ensdf_levels(filepath):
    """Parse ENSDF file to extract L-record J-π values with parentheses"""
    jpi_data = {}
    
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    
    for line in lines:
        if len(line) >= 39 and line[7:9].strip() == 'L':
            try:
                # Extract energy (columns 10-19)
                energy_str = line[9:19].strip()
                if energy_str:
                    energy = float(energy_str)
                    
                    # Extract J-π (columns 23-39)
                    jpi = line[22:39].strip()
                    if jpi:
                        jpi_data[energy] = jpi
                        print(f"ENSDF: {energy} keV → {jpi}")
            except (ValueError, IndexError):
                continue
    
    return jpi_data

def compare_jpi_with_parentheses(ensdf_data, comparison_data):
    """Compare J-π assignments with special attention to parentheses"""
    print("\n" + "="*80)
    print("DETAILED J-π COMPARISON WITH PARENTHESES VERIFICATION")
    print("="*80)
    
    matches = 0
    mismatches = 0
    
    print(f"\n{'Energy':<12} {'ENSDF J-π':<15} {'Table J-π':<15} {'Status':<20}")
    print("-" * 65)
    
    for energy in sorted(ensdf_data.keys()):
        ensdf_jpi = ensdf_data[energy]
        
        # Find matching energy in comparison data (with tolerance)
        table_jpi = None
        for comp_energy, comp_jpi in comparison_data.items():
            if abs(energy - comp_energy) < 0.1:  # 0.1 keV tolerance
                table_jpi = comp_jpi
                break
        
        if table_jpi:
            # Check exact match including parentheses
            if ensdf_jpi == table_jpi:
                status = "✅ EXACT MATCH"
                matches += 1
            else:
                status = "❌ MISMATCH"
                mismatches += 1
                print(f"MISMATCH DETAILS:")
                print(f"  ENSDF: '{ensdf_jpi}'")
                print(f"  Table: '{table_jpi}'")
                print(f"  Parentheses difference: {has_parentheses(ensdf_jpi)} vs {has_parentheses(table_jpi)}")
        else:
            status = "⚠️ NO TABLE MATCH"
            mismatches += 1
        
        print(f"{energy:<12.2f} {ensdf_jpi:<15} {table_jpi or 'N/A':<15} {status}")
    
    print("\n" + "="*80)
    print("PARENTHESES VERIFICATION SUMMARY:")
    print("="*80)
    print(f"Total levels compared: {len(ensdf_data)}")
    print(f"Exact matches (including parentheses): {matches}")
    print(f"Mismatches: {mismatches}")
    print(f"Success rate: {matches / len(ensdf_data) * 100:.1f}%")
    
    if mismatches == 0:
        print("\n🎯 PERFECT! All J-π assignments including parentheses are identical!")
    else:
        print(f"\n⚠️ Found {mismatches} mismatches that need attention!")
    
    return matches, mismatches

def has_parentheses(jpi_str):
    """Check if J-π has parentheses (indicating tentative assignment)"""
    return '(' in jpi_str and ')' in jpi_str

def main():
    ensdf_file = "XUNDL/2025LAAA_CH11036_127I.ens"
    comparison_file = "XUNDL/2025LAAA_vs_2012DI06.ens"
    
    print("Parsing ENSDF file...")
    ensdf_data = parse_ensdf_levels(ensdf_file)
    print(f"\nFound {len(ensdf_data)} levels in ENSDF file")
    
    print("\nParsing comparison table...")
    comparison_data = parse_comparison_table(comparison_file)
    print(f"\nFound {len(comparison_data)} levels in comparison table")
    
    print("\nComparing J-π assignments...")
    matches, mismatches = compare_jpi_with_parentheses(ensdf_data, comparison_data)

if __name__ == "__main__":
    main()
