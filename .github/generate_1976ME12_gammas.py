#!/usr/bin/env python3
"""
Generate G-records for 1976ME12 resonance levels with branching ratios.

For each resonance level:
1. Match Ep_keV (from CSV) to S field value in L-record
2. Use Ex_keV to calculate Eg = Ex_keV - Efinal_keV
3. Add G-record with Eg (no DE) and RI (no DRI)
4. Sort G-records by ascending Eg within each level
"""

def format_g_record(eg_kev, ri_value):
    """
    Format a G-record with exact 80-character ENSDF format.
    
    G-record format:
    Columns 1-5: NUCID (" 35CL")
    Columns 6-9: "  G " (continuation, blank, type, blank)
    Columns 10-19: Eg (gamma energy, LEFT-JUSTIFIED, no DE)
    Columns 20-21: DE field (BLANK - no uncertainty)
    Column 22: space separator
    Columns 23-29: RI (relative intensity, LEFT-JUSTIFIED, no DRI)
    Columns 30-80: All blank (no DRI, no multipolarity, etc.)
    """
    nucid = " 35CL"
    cont = " "
    blank1 = " "
    rec_type = "G"
    blank2 = " "
    
    # Format Eg field (10-19): LEFT-JUSTIFIED, one decimal place if integer
    if eg_kev == int(eg_kev):
        eg_str = f"{int(eg_kev)}"
    else:
        eg_str = f"{eg_kev:.1f}"
    eg_field = f"{eg_str:<10}"
    
    # DE field (20-21): BLANK (no uncertainty)
    de_field = "  "
    
    # Space separator (22)
    space_sep = " "
    
    # RI field (23-29): LEFT-JUSTIFIED, format depends on value
    if ri_value == int(ri_value):
        ri_str = f"{int(ri_value)}"
    else:
        ri_str = f"{ri_value}"
    ri_field = f"{ri_str:<7}"
    
    # Remaining fields (30-80): All blank (51 characters)
    remaining = " " * 51
    
    # Construct full line
    line = (nucid + cont + blank1 + rec_type + blank2 + 
            eg_field + de_field + space_sep + ri_field + remaining)
    
    # Verify exactly 80 characters
    if len(line) != 80:
        raise ValueError(f"Line length {len(line)} != 80: {line}")
    
    return line


# Branching ratio data from CSV (47 resonances with gamma data)
# Format: (Ep_keV, Ex_keV, {final_level_MeV: RI_value})
branching_data = [
    (716, 7069, {0: 49, 1.22: 18, 1.76: 14, 2.65: 1.6, 2.69: 5, 3.00: 3, 3.16: 6, 4.06: 1.4, 4.11: 0.6, 4.18: 0.5}),
    (755, 7106, {0: 15, 1.22: 64, 1.76: 4, 2.69: 11, 3.00: 3, 3.92: 1.5, 4.18: 1.5}),
    (832, 7181, {0: 38, 1.22: 17, 2.69: 4, 3.92: 3, 3.98: 9, 4.06: 22, 4.175: 0.8}),
    (848, 7197, {0: 2, 1.22: 67, 1.76: 0.5, 2.69: 1.1, 3.92: 4, 3.98: 1.8, 4.06: 3, 4.18: 16}),
    (879, 7227, {0: 59, 1.76: 7, 2.69: 10, 3.92: 1.5, 4.06: 2, 4.18: 8}),
    (889, 7236, {0: 93, 1.22: 1.8, 1.76: 0.2, 2.65: 3, 2.69: 1.8}),
    (929, 7275, {0: 69, 1.22: 24, 2.69: 1.1, 3.98: 0.8, 4.06: 0.9, 4.175: 0.4}),
    (1021, 7365, {0: 10, 1.22: 73, 1.76: 8, 2.69: 0.5, 3.00: 0.3, 3.92: 0.8, 3.98: 3, 4.06: 2, 4.18: 0.5}),
    (1057, 7400, {1.76: 2, 2.65: 13, 3.00: 14, 3.16: 47, 3.92: 5, 4.06: 8}),
    (1165, 7505, {0: 0.3, 1.22: 18, 1.76: 0.7, 2.65: 7, 3.00: 4, 3.16: 4, 3.92: 2, 4.06: 50, 4.18: 3}),
    (1212, 7551, {0: 0.2, 1.76: 0.3, 2.65: 0.5, 3.00: 2, 3.16: 95}),
    (1225, 7563, {0: 34, 1.22: 35, 2.69: 22, 3.92: 1.6, 3.98: 0.5, 4.06: 6, 4.18: 0.9}),
    (1266, 7602, {0: 33, 1.22: 1.1, 1.76: 19, 2.65: 1.9, 2.69: 18, 3.00: 8, 3.16: 5, 4.06: 2, 4.18: 3}),
    (1285, 7621, {0: 78, 1.76: 10, 3.16: 3, 4.06: 2, 4.18: 3}),
    (1340, 7674, {0: 0.8, 1.76: 57, 2.65: 13, 3.00: 9, 3.16: 1.8, 4.175: 5}),
    (1354, 7688, {0: 70, 1.22: 1, 1.76: 0.7, 3.00: 10, 4.06: 6, 4.175: 4, 4.18: 3}),
    (1375, 7709, {0: 83, 1.22: 0.5, 1.76: 0.4, 2.65: 4, 3.00: 1, 3.92: 0.6, 4.06: 2, 4.18: 2}),
    (1415, 7747, {1.22: 0.6, 1.76: 2.4, 2.65: 43, 3.16: 16, 3.92: 10, 4.06: 6}),
    (1448, 7779, {0: 18, 1.22: 11, 1.76: 40, 2.65: 1.3, 2.69: 9, 3.00: 4, 3.16: 2, 4.06: 1.1, 4.18: 7}),
    (1452, 7784, {0: 1.7, 1.22: 1.2, 1.76: 18, 2.65: 8, 3.16: 5, 3.92: 11, 4.06: 1.2, 4.11: 6, 4.175: 36}),
    (1468, 7799, {0: 83, 1.22: 9, 4.06: 0.3}),
    (1511, 7841, {0: 21, 1.22: 37, 1.76: 1.9, 3.00: 4, 3.92: 0.2, 3.94: 0.5, 4.06: 2, 4.175: 3, 4.18: 28}),
    (1542, 7871, {0: 61, 1.22: 13, 1.76: 17, 4.175: 5}),
    (1555, 7883, {0: 10, 1.76: 30, 2.69: 25, 3.00: 11, 3.92: 2, 4.06: 2, 4.11: 1.3, 4.18: 3}),
    (1574, 7901, {0: 4, 1.76: 68, 2.69: 1.3, 3.16: 4, 4.06: 3, 4.175: 8, 4.18: 8}),
    (1598, 7925, {0: 41, 1.22: 27, 1.76: 1.5, 2.65: 0.9, 2.69: 11, 3.00: 0.9, 3.92: 1.2, 3.98: 1.5, 4.06: 1.7, 4.175: 5, 4.18: 3}),
    (1647, 7973, {1.22: 1, 1.76: 20, 2.65: 20, 3.00: 5, 3.16: 10, 4.06: 6, 4.18: 6}),
    (1666, 7991, {0: 36, 1.22: 60, 4.06: 1}),
    (1673, 7998, {0: 78, 1.76: 0.9, 2.65: 0.6, 2.69: 0.2, 3.00: 2, 3.16: 7, 4.06: 1.1, 4.18: 4}),
    (1678, 8003, {0: 1.4, 1.76: 70, 2.65: 1.6, 3.16: 0.8, 3.92: 3, 4.175: 10}),
    (1683, 8007, {0: 55, 1.22: 0.6, 1.76: 15, 2.65: 4, 2.69: 1.7, 3.00: 2, 3.16: 15}),
    (1717, 8041, {0: 8, 1.22: 4, 1.76: 15, 2.69: 57, 3.00: 4, 3.92: 1.4, 3.98: 0.8, 4.06: 3, 4.18: 1.6}),
    (1756, 8077, {1.76: 56, 3.00: 2, 4.18: 8}),
    (1776, 8098, {0: 39, 1.76: 8, 2.65: 17, 2.69: 5, 3.16: 5, 3.92: 1.8, 4.06: 2, 4.18: 1.9}),
    (1787, 8109, {0: 37, 1.22: 35, 1.76: 3, 2.69: 9, 3.00: 9, 3.98: 3, 4.06: 1.3, 4.18: 1.6}),
    (1794, 8116, {0: 25, 1.22: 32, 1.76: 5, 2.69: 13, 3.00: 1.9, 3.98: 5, 4.06: 1.3, 4.175: 7}),
    (1830, 8150, {0: 62, 1.22: 15, 2.69: 3, 3.92: 3, 3.98: 2, 4.06: 3, 4.18: 8}),
    (1839, 8159, {0: 3, 1.76: 1, 2.65: 51, 3.00: 6, 3.16: 5, 3.98: 2, 4.06: 1, 4.11: 7, 4.18: 5}),
    (1891, 8210, {0: 78, 1.22: 3, 1.76: 14, 2.69: 0.5, 3.00: 1.1, 4.06: 1.5}),
    (1900, 8218, {0: 45, 1.76: 1.4, 2.69: 3, 3.00: 5, 3.16: 41}),
    (1927, 8244, {1.22: 91, 3.00: 2, 4.175: 7}),
    (1954, 8271, {0: 45, 1.76: 8, 2.65: 4, 2.69: 6, 3.00: 13, 3.16: 7, 3.92: 3, 4.18: 12}),
    (1963, 8279, {0: 29, 1.76: 23, 2.65: 3, 2.69: 3, 3.00: 10, 3.92: 5, 4.06: 1.5, 4.175: 2}),
    (1968, 8284, {0: 28, 1.76: 7, 3.16: 26, 4.06: 6, 4.18: 14}),
    (1974, 8290, {0: 13, 1.22: 44, 2.69: 23, 3.98: 1, 4.06: 3, 4.06: 2, 4.18: 9}),
    (1985, 8300, {0: 13, 1.22: 24, 1.76: 8, 2.65: 6, 2.69: 10, 3.00: 1, 3.16: 1, 4.06: 10, 4.175: 6}),
    (2006, 8321, {0: 78, 1.22: 2, 1.76: 1.8, 2.65: 0.9, 2.69: 1.6, 3.00: 3, 3.16: 0.5, 3.98: 3, 4.06: 1.2}),
]

# Final level energies (keV) - convert from MeV
final_levels = {
    0: 0,
    1.22: 1220,
    1.76: 1760,
    2.65: 2650,
    2.69: 2690,
    3.00: 3000,
    3.16: 3160,
    3.92: 3920,
    3.94: 3940,
    3.98: 3980,
    4.06: 4060,
    4.11: 4110,
    4.175: 4175,
    4.18: 4180,
}

def main():
    print("[*] Generating G-records for 1976ME12 resonances with branching ratios...")
    
    output_lines = []
    output_lines.append("# Generated G-records for 1976ME12 resonances")
    output_lines.append("# Format: Ep_keV | Ex_keV | Gamma transitions")
    output_lines.append("#")
    
    total_gammas = 0
    
    for ep_kev, ex_kev, branching_dict in branching_data:
        # Calculate gamma energies and create G-records
        gamma_records = []
        
        for efinal_mev, ri_value in branching_dict.items():
            efinal_kev = final_levels[efinal_mev]
            eg_kev = ex_kev - efinal_kev
            
            # Format G-record
            g_line = format_g_record(eg_kev, ri_value)
            gamma_records.append((eg_kev, g_line))
        
        # Sort by ascending gamma energy (ENSDF requirement)
        gamma_records.sort(key=lambda x: x[0])
        
        # Add section header
        output_lines.append(f"# Ep={ep_kev} keV, Ex={ex_kev} keV ({len(gamma_records)} gammas)")
        
        # Add G-records
        for eg_kev, g_line in gamma_records:
            output_lines.append(g_line)
            total_gammas += 1
        
        # Add blank separator
        output_lines.append("")
    
    # Write to output file
    output_file = "A35/Cl35/temp/1976ME12_gammas_generated.txt"
    with open(output_file, 'w') as f:
        f.write('\n'.join(output_lines))
    
    print(f"[OK] Generated {total_gammas} G-records for {len(branching_data)} resonances")
    print(f"[OK] Output file: {output_file}")
    print(f"[OK] Total lines: {len(output_lines)}")

if __name__ == "__main__":
    main()
