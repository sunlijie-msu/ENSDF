#!/usr/bin/env python3
"""
Comprehensive validation of |w|γ values in ENSDF against original 1976SP08.txt data.
This script performs systematic comparison of every gamma width value and uncertainty
to ensure absolute accuracy between evaluated and original experimental data.
"""

import re
import sys

def load_original_data(filename):
    """Load original 1976SP08.txt data into dictionary keyed by Ex energy."""
    
    original_data = {}
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Error reading original data file: {e}")
        return {}
    
    # Skip header line, process data
    for line in lines[1:]:
        line = line.strip()
        if line:
            try:
                parts = line.split('\t')
                if len(parts) >= 5:
                    ex = float(parts[0])  # Excitation energy
                    ep = float(parts[1])  # Proton energy
                    dep = float(parts[2]) # Proton energy uncertainty
                    wg = float(parts[3])  # Gamma width
                    dwg = float(parts[4]) # Gamma width uncertainty
                    
                    original_data[ex] = {
                        'Ex': ex,
                        'Ep': ep,
                        'DEp': dep,
                        'wg': wg,
                        'Dwg': dwg
                    }
            except (ValueError, IndexError) as e:
                print(f"Warning: Could not parse line: {line} ({e})")
    
    return original_data

def extract_ensdf_data(filename):
    """Extract all |w|γ entries from ENSDF with corresponding level energies."""
    
    results = []
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Error reading ENSDF file: {e}")
        return []
    
    # Find all |w|γ entries from 1976Sp08
    wgamma_pattern = r'\$\|w\|g=([\d\.]+)\s*eV\s*\{I(\d+)\}\s*\(1976Sp08\)'
    
    for i, line in enumerate(lines):
        match = re.search(wgamma_pattern, line)
        if match:
            wg_value = float(match.group(1))
            uncertainty_digits = int(match.group(2))
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
                    'uncertainty_digits': uncertainty_digits,
                    'full_line': line.strip()
                })
    
    return results

def calculate_uncertainty_value(wg_value, uncertainty_digits):
    """Calculate actual uncertainty value from ENSDF {In} notation."""
    
    # Count decimal places in wg_value
    wg_str = str(wg_value)
    if '.' in wg_str:
        decimal_places = len(wg_str.split('.')[1])
    else:
        decimal_places = 0
    
    # Uncertainty affects the rightmost digits
    uncertainty_value = uncertainty_digits * (10 ** (-decimal_places))
    
    return uncertainty_value

def find_closest_match(ensdf_energy, original_data, tolerance=5.0):
    """Find the closest matching original data entry by excitation energy."""
    
    best_match = None
    min_diff = float('inf')
    
    for ex, data in original_data.items():
        diff = abs(ensdf_energy - ex)
        if diff < min_diff and diff <= tolerance:
            min_diff = diff
            best_match = data
    
    return best_match, min_diff

def compare_data(ensdf_file, original_file):
    """Perform comprehensive comparison of ENSDF vs original data."""
    
    print("Loading original 1976SP08.txt data...")
    original_data = load_original_data(original_file)
    print(f"Loaded {len(original_data)} original data entries")
    
    print("\nExtracting ENSDF |w|γ entries...")
    ensdf_data = extract_ensdf_data(ensdf_file)
    print(f"Found {len(ensdf_data)} ENSDF entries from 1976Sp08")
    
    print("\n" + "="*100)
    print("SYSTEMATIC VALIDATION OF ALL |w|γ VALUES vs 1976SP08.txt ORIGINAL DATA")
    print("="*100)
    
    matches = 0
    discrepancies = 0
    no_match_found = 0
    
    for i, entry in enumerate(ensdf_data, 1):
        print(f"\n[{i:2d}/85] Validating Line {entry['line']:4d}: Level {entry['level_energy']:7.1f} keV")
        print(f"      ENSDF: |w|γ = {entry['wg_value']} eV {{I{entry['uncertainty_digits']}}}")
        
        # Find corresponding original data
        original_match, energy_diff = find_closest_match(entry['level_energy'], original_data)
        
        if original_match:
            print(f"      Original Ex = {original_match['Ex']:7.1f} keV (ΔE = {energy_diff:4.1f} keV)")
            print(f"      Original: wg = {original_match['wg']} eV, Dwg = {original_match['Dwg']} eV")
            
            # Calculate ENSDF uncertainty value
            ensdf_uncertainty = calculate_uncertainty_value(entry['wg_value'], entry['uncertainty_digits'])
            
            # Compare values
            wg_match = abs(entry['wg_value'] - original_match['wg']) < 0.001
            uncert_match = abs(ensdf_uncertainty - original_match['Dwg']) < 0.001
            
            print(f"      ENSDF uncertainty: {ensdf_uncertainty} eV")
            
            if wg_match and uncert_match:
                print(f"      ✅ PERFECT MATCH: Both wγ and uncertainty agree")
                matches += 1
            else:
                print(f"      ❌ DISCREPANCY FOUND:")
                if not wg_match:
                    diff = entry['wg_value'] - original_match['wg']
                    print(f"         • wγ mismatch: ENSDF={entry['wg_value']} vs Original={original_match['wg']} (Δ={diff:+.3f})")
                if not uncert_match:
                    diff_uncert = ensdf_uncertainty - original_match['Dwg']
                    print(f"         • Uncertainty mismatch: ENSDF={ensdf_uncertainty} vs Original={original_match['Dwg']} (Δ={diff_uncert:+.3f})")
                discrepancies += 1
        else:
            print(f"      ⚠️  NO MATCH FOUND in original data (closest was {energy_diff:.1f} keV away)")
            no_match_found += 1
    
    # Final summary
    print("\n" + "="*100)
    print("VALIDATION SUMMARY")
    print("="*100)
    print(f"Total ENSDF entries validated: {len(ensdf_data)}")
    print(f"Perfect matches found:         {matches}")
    print(f"Discrepancies detected:        {discrepancies}")
    print(f"No original match found:       {no_match_found}")
    print(f"Validation accuracy:           {matches/len(ensdf_data)*100:.1f}%")
    
    if discrepancies > 0:
        print(f"\n❌ CRITICAL: {discrepancies} discrepancies found requiring correction!")
    else:
        print(f"\n✅ SUCCESS: All {matches} |w|γ values match original 1976SP08.txt data perfectly!")

def main():
    if len(sys.argv) != 3:
        print("Usage: python validate_wgamma_data.py <ensdf_file> <1976SP08.txt>")
        sys.exit(1)
    
    ensdf_file = sys.argv[1]
    original_file = sys.argv[2]
    
    compare_data(ensdf_file, original_file)

if __name__ == "__main__":
    main()