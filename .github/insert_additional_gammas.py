#!/usr/bin/env python3
"""
Insert additional gamma transitions from "Other final levels" into ENSDF file.

This script reads the processed additional gammas and inserts them into 1972HU10.ens
while maintaining ascending energy order for G-records within each level.
"""

import sys

# Additional gamma data (from process_other_final_levels.py output)
# Format: {exi_keV: [(eg_keV, br_value), ...], ...}
ADDITIONAL_GAMMAS = {
    '7175': [('1075.0', '4')],
    '7192': [('2182.0', '1'), ('2342.0', '2')],
    '7223': [('1123.0', '3'), ('1373.0', '1'), ('1543.0', '2'), ('1823.0', '1'), ('2013.0', '6')],
    '7269': [('1519.0', '1.5'), ('1869.0', '0.5'), ('2259.0', '1.5'), ('2429.0', '1')],
    '7358': [('1708.0', '0.5'), ('2348.0', '0.5'), ('2518.0', '1')],
    '7392': [('3042.0', '10')],
    '7500': [('1400.0', '10')],
    '7517': [('1917.0', '2'), ('1927.0', '3'), ('3167.0', '2')],
    '7546': [('1906.0', '0.5'), ('1956.0', '0.2'), ('2776.0', '1.5')],
    '7616': [('2406.0', '3')],
    '7653': [('1553.0', '3'), ('1973.0', '1'), ('2003.0', '1'), ('2813.0', '3')],
    '7669': [('2509.0', '4'), ('2789.0', '1'), ('3319.0', '6')],
    '7683': [('1933.0', '0.5'), ('2083.0', '2'), ('2283.0', '2'), ('2473.0', '0.5')],
    '7691': [('2091.0', '1')],
    '7704': [('2054.0', '4'), ('2864.0', '1')],
    '7743': [('2863.0', '19'), ('2973.0', '1')],
    '7775': [('2935.0', '2'), ('3005.0', '2')],
    '7780': [('2190.0', '1'), ('2380.0', '1'), ('2570.0', '1'), ('3010.0', '7'), ('3430.0', '2')],
    '7795': [('2045.0', '0.5'), ('2145.0', '1'), ('2395.0', '2'), ('2785.0', '2'), ('2945.0', '0.5')],
    '7834': [('1734.0', '1'), ('2624.0', '1')],
    '7866': [('2856.0', '4')],
    '7878': [('2228.0', '9'), ('3038.0', '3'), ('3248.0', '1')],
    '7968': [('2328.0', '3'), ('2378.0', '2'), ('2758.0', '3'), ('3088.0', '9'), ('3198.0', '6'), ('3618.0', '8')],
    '7985': [('1885.0', '1'), ('2335.0', '1')],
    '7993': [('2593.0', '3')],
    '7999': [('2359.0', '3'), ('3229.0', '8')],
    '8033': [('2233.0', '6')],
    '8073': [('2433.0', '10'), ('2483.0', '11'), ('2863.0', '7'), ('2913.0', '1'), ('3193.0', '2'), ('3303.0', '4')],
    '8093': [('2293.0', '1'), ('2453.0', '5'), ('2493.0', '6'), ('2883.0', '1'), ('2933.0', '2'), ('3253.0', '3'), ('3323.0', '1')],
    '8104': [('2504.0', '0.5'), ('3254.0', '0.5'), ('3264.0', '0.5')],
    '8111': [('1621.0', '6'), ('2511.0', '3')],
    '8144': [('2464.0', '1'), ('3134.0', '2')],
    '8154': [('2514.0', '3'), ('2564.0', '7'), ('2944.0', '8')],
    '8177': [('3547.0', '9')],
}

def format_ensdf_g_record(eg, br):
    """Format a G-record in ENSDF 80-column format."""
    # ENSDF G-record format with correct column positioning:
    # Cols 1-5: NUCID (" 35CL")
    # Col 6: CONT (" ")
    # Col 7: BLANK (" ")
    # Col 8: TYPE ("G")
    # Col 9: BLANK (" ")
    # Cols 10-19: E (energy, left-justified)
    # Cols 20-21: DE (energy uncertainty, EMPTY for BR-only data)
    # Col 22: SPACE (" ")
    # Cols 23-29: RI (relative intensity / BR, left-justified)
    # Remaining cols: spaces to pad to 80 chars
    
    # Build the record field by field
    nucid = " 35CL"  # cols 1-5
    cont = " "  # col 6
    blank1 = " "  # col 7
    type_field = "G"  # col 8
    blank2 = " "  # col 9
    e_field = f"{eg:<10}"  # cols 10-19 (left-justified, 10 chars)
    de_field = "  "  # cols 20-21 (empty - no energy uncertainty for BR data)
    space = " "  # col 22
    ri_field = f"{br:<7}"  # cols 23-29 (left-justified, 7 chars)
    
    # Assemble the line up to column 29
    ensdf_line = nucid + cont + blank1 + type_field + blank2 + e_field + de_field + space + ri_field
    
    # Pad to exactly 80 characters
    if len(ensdf_line) < 80:
        ensdf_line = ensdf_line + ' ' * (80 - len(ensdf_line))
    elif len(ensdf_line) > 80:
        # Truncate if too long (should not happen)
        ensdf_line = ensdf_line[:80]
    
    return ensdf_line + '\n'

def extract_energy_from_g_record(line):
    """Extract energy value from G-record for sorting."""
    if len(line) < 19 or line[7:8].strip() != 'G':
        return None
    energy_str = line[9:19].strip()
    try:
        return float(energy_str)
    except ValueError:
        return None

def extract_level_energy(line):
    """Extract level energy from L-record."""
    if len(line) < 19 or line[7:8].strip() != 'L':
        return None
    energy_str = line[9:19].strip()
    try:
        energy_float = float(energy_str)
        # Return as integer string if it's a whole number
        if energy_float == int(energy_float):
            return str(int(energy_float))
        else:
            return str(energy_float)
    except ValueError:
        return None

def process_ensdf_file(input_file, output_file):
    """Read ENSDF file, insert additional G-records, maintain ascending order."""
    
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    current_level = None
    level_g_records = []
    total_added = 0
    levels_modified = 0
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Check if this is an L-record
        if line[7:8] == 'L':
            # Process previous level's G-records if any
            if current_level and level_g_records:
                # Add collected G-records (already sorted)
                new_lines.extend(level_g_records)
                level_g_records = []
            
            # Add the L-record
            new_lines.append(line)
            
            # Extract level energy
            level_energy_str = extract_level_energy(line)
            current_level = level_energy_str
            
            i += 1
            
        # Check if this is a G-record
        elif line[7:8] == 'G' and current_level:
            # Collect all G-records for this level
            level_g_records.append(line)
            i += 1
            
            # Continue collecting G-records for this level
            while i < len(lines) and lines[i][7:8] == 'G':
                level_g_records.append(lines[i])
                i += 1
            
            # Check if we have additional gammas for this level
            if current_level in ADDITIONAL_GAMMAS:
                # Add additional G-records
                for eg, br in ADDITIONAL_GAMMAS[current_level]:
                    new_g_record = format_ensdf_g_record(eg, br)
                    level_g_records.append(new_g_record)
                    total_added += 1
                
                levels_modified += 1
            
            # Sort all G-records by ascending energy
            level_g_records_with_energy = []
            for g_line in level_g_records:
                eg = extract_energy_from_g_record(g_line)
                if eg is not None:
                    level_g_records_with_energy.append((eg, g_line))
            
            level_g_records_with_energy.sort(key=lambda x: x[0])
            level_g_records = [g_line for eg, g_line in level_g_records_with_energy]
            
            # Add sorted G-records
            new_lines.extend(level_g_records)
            level_g_records = []
            
        else:
            # Not L or G record, just add it
            new_lines.append(line)
            i += 1
    
    # Write updated file
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        for line in new_lines:
            f.write(line)
    
    return total_added, levels_modified

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python insert_additional_gammas.py <input_ensdf> <output_ensdf>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    print(f"\n[Inserting Additional Gamma Transitions]")
    print("=" * 80)
    print(f"Input file:  {input_file}")
    print(f"Output file: {output_file}")
    print()
    
    total_added, levels_modified = process_ensdf_file(input_file, output_file)
    
    print(f"\n[Summary]")
    print(f"  - Added {total_added} additional G-records")
    print(f"  - Modified {levels_modified} levels")
    print(f"  - Output written to: {output_file}")
    print()
    print("[Next Steps]")
    print("  1. Validate 80-column format:")
    print(f"     python .github/column_calibrate.py \"{output_file}\"")
    print("  2. Validate energy ordering:")
    print(f"     python .github/check_gamma_ordering.py \"{output_file}\"")
    print("=" * 80)
