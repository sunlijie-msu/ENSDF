"""
Process branching ratio CSV data and generate ENSDF G-records.
Author: Nuclear Data Processing Script
Date: 2025-10-03
"""

import csv
import sys

def parse_csv_data(csv_file):
    """Parse CSV file and extract branching ratio data."""
    with open(csv_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Parse header to get Exf values (final level energies) - on line 2
    exf_header = lines[1].strip().split(',')
    exf_values = []
    for val in exf_header[2:]:  # Skip first two columns
        if val.strip():
            exf_values.append(float(val.strip()))
    
    # Parse data rows (starting from line 4, index 3)
    resonance_data = []
    for line in lines[3:]:  # Skip first three header lines
        if not line.strip():
            continue
        parts = line.strip().split(',')
        if len(parts) < 2:
            continue
        
        try:
            ep = parts[0].strip()
            exi = parts[1].strip()
            if not ep or not exi:
                continue
            
            ep_val = float(ep)
            exi_val = float(exi)
            
            # Extract branching ratios - PRESERVE EXACT FORMAT
            branching_ratios = []
            for i, val in enumerate(parts[2:]):
                if i >= len(exf_values):
                    break
                val_clean = val.strip().replace('\n', '').replace('"', '')
                if val_clean:
                    try:
                        # Store as string to preserve exact format (no .0 addition)
                        br_value = val_clean
                        # Verify it's a valid number
                        float(br_value)
                        branching_ratios.append((exf_values[i], br_value))
                    except ValueError:
                        continue
            
            if branching_ratios:
                resonance_data.append({
                    'Ep': ep_val,
                    'Exi': exi_val,
                    'transitions': branching_ratios
                })
        except (ValueError, IndexError):
            continue
    
    return resonance_data

def generate_ensdf_records(resonance_data):
    """Generate ENSDF L and G records."""
    ensdf_lines = []
    
    for res in resonance_data:
        exi = res['Exi']
        
        # Add L-record for this resonance level
        ensdf_lines.append(f" 35CL  L {exi:<10}")
        
        # Calculate gamma energies and add G-records in ASCENDING energy order
        gamma_records = []
        for exf, br_str in res['transitions']:
            eg = exi - exf
            # Use br_str directly to preserve exact format
            gamma_records.append((eg, br_str))
        
        # Sort by gamma energy (ascending order)
        gamma_records.sort(key=lambda x: x[0])
        
        # Add G-records - preserve exact BR format
        for eg, br_str in gamma_records:
            # Format: columns 10-19 for energy, columns 23-29 for RI
            ensdf_lines.append(f" 35CL  G {eg:<10}{' '*3}{br_str:<7}")
    
    return ensdf_lines

def main():
    if len(sys.argv) < 2:
        print("Usage: python process_branching_ratios.py <csv_file>")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    
    # Parse CSV data
    print(f"[Processing] Reading CSV file: {csv_file}")
    resonance_data = parse_csv_data(csv_file)
    print(f"[Success] Found {len(resonance_data)} resonance levels")
    
    # Generate ENSDF records
    ensdf_lines = generate_ensdf_records(resonance_data)
    
    # Output results
    print("\n[Generated ENSDF Records]")
    print("=" * 80)
    for line in ensdf_lines:
        print(line)
    print("=" * 80)
    print(f"\n[Complete] Generated {len(ensdf_lines)} ENSDF records")
    
    # Save to output file
    output_file = csv_file.replace('.csv', '_ensdf_output.txt')
    with open(output_file, 'w') as f:
        f.write('\n'.join(ensdf_lines))
    print(f"[Saved] Output saved to: {output_file}")

if __name__ == '__main__':
    main()
