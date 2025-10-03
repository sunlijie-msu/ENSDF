"""
Add Ep and dEp values to S and DS fields, and add cL comments with wg values.
"""

import sys

# Data from 1972HU10 CSV table
# Format: Exi_rounded -> (Ep, dEp, wg, dwg)
# Manual mapping based on file Exi values and CSV Ep values
EP_DATA = {
    7063.0: ("716", "0.7", "0.2", "0.1"),
    7100.0: ("754.1", "0.7", "0.5", "0.3"),
    7175.0: ("831.5", "0.8", "0.4", "0.2"),
    7192.0: ("848.2", "0.7", "1.1", "0.3"),
    7223.0: ("880.5", "0.8", "0.4", "0.2"),
    7231.0: ("889", "0.8", "1.3", "0.4"),
    7269.0: ("928.2", "0.9", "1.4", "0.4"),
    7358.0: ("1020.4", "0.8", "3.2", "1.0"),
    7392.0: ("1054.9", "1.0", "0.4", "0.2"),
    7448.0: ("1112.2", "1.0", "0.3", "0.2"),
    7499.0: ("1165", None, "0.6", "0.3"),
    7500.0: ("1165", None, "0.6", "0.3"),  # Duplicate Ep for close energies
    7517.0: ("1183.2", "1.1", "0.2", "0.1"),
    7546.0: ("1213.7", "1.0", "21", "3"),
    7558.0: ("1225.6", "1.0", "1.5", "0.5"),
    7598.0: ("1266.5", "1.0", "3.2", "1.0"),
    7616.0: ("1285.5", "1.1", "1.2", "0.4"),
    7653.0: ("1323.7", "1.2", "0.5", "0.3"),
    7669.0: ("1339.8", "1.1", "1.5", "0.5"),
    7683.0: ("1353.7", "1.1", "2.5", "0.8"),
    7691.0: ("1362.4", "1.2", "0.4", "0.2"),
    7704.0: ("1375.7", "1.1", "3.7", "1.1"),
    7743.0: ("1415.6", "1.2", "1.3", "0.4"),
    7775.0: ("1449", "1.1", "1.5", "0.5"),
    7780.0: ("1453.6", "1.1", "0.8", "0.4"),
    7795.0: ("1469.6", "1.2", "1.5", "0.5"),
    7834.0: ("1510", None, "11", "3"),
    7866.0: ("1542.3", "1.3", "0.5", "0.3"),
    7878.0: ("1554.9", "1.2", "1.6", "0.5"),
    7897.0: ("1574.4", "1.2", "1.4", "0.4"),
    7921.0: ("1598.9", "1.3", "0.8", "0.4"),
    7968.0: ("1647.3", "1.2", "1.2", "0.4"),
    7985.0: ("1665.2", "1.2", "1.5", "0.5"),
    7993.0: ("1673.7", "1.1", "2.7", "0.8"),
    7999.0: ("1679.7", "1.1", "4.1", "1.2"),
    8004.0: ("1684.3", "1.3", "4.5", "1.4"),
    8033.0: ("1714", "1.1", "0.9", "0.5"),
    8036.0: ("1717.9", "1.1", "3.5", "1.1"),
    8073.0: ("1756", "1.0", "1.6", "0.5"),
    8093.0: ("1776.7", "1.1", "2.5", "0.8"),
    8104.0: ("1787.7", "1.1", "4.2", "1.3"),
    8111.0: ("1794.8", "1.3", "1.2", "0.4"),
    8144.0: ("1829.1", "1.3", "2.4", "0.7"),
    8154.0: ("1839", "1.2", "2.1", "0.6"),
    8177.0: ("1862.7", "1.3", "0.8", "0.4"),
    8207.0: ("1893.2", "1.1", "8.0", "2.4"),
    8215.0: ("1901.8", "1.1", "6.2", "1.9"),
    8382.0: ("2101", "1.4", "3.6", "1.1"),
    # Note: Remaining Ep values from CSV (1928.2-2096.6) don't have corresponding Exi in file
}


def format_ensdf_l_record_with_ep(line, ep_str, dep_str):
    """
    Add Ep to S field (cols 65-74) and dEp to DS field (cols 75-76).
    ENSDF L-record format:
    Cols 1-5: NUCID
    Col 6: CONT
    Col 7: BLANK
    Col 8: TYPE ("L")
    Col 9: BLANK
    Cols 10-19: E (level energy)
    Cols 20-21: DE
    Cols 22-39: J, space-separated
    Cols 40-49: T
    Cols 50-55: DT
    Cols 56-64: L
    Cols 65-74: S (LEFT-JUSTIFIED, 10 chars)
    Cols 75-76: DS (LEFT-JUSTIFIED, 2 chars)
    Col 77: C
    Cols 78-80: Rest
    """
    # Current line should be exactly 80 chars (or less if fields are empty)
    # Read existing fields
    nucid = line[0:5]  # " 35CL"
    cont = line[5:6] if len(line) > 5 else " "
    blank1 = line[6:7] if len(line) > 6 else " "
    type_field = line[7:8] if len(line) > 7 else "L"
    blank2 = line[8:9] if len(line) > 8 else " "
    e_field = line[9:19] if len(line) > 9 else ""
    de_field = line[19:21] if len(line) > 19 else ""
    space1 = line[21:22] if len(line) > 21 else " "
    j_field = line[22:39] if len(line) > 22 else ""
    t_field = line[39:49] if len(line) > 39 else ""
    dt_field = line[49:55] if len(line) > 49 else ""
    l_field = line[55:64] if len(line) > 55 else ""
    
    # S field: Ep value, left-justified in 10-char field
    s_field = f"{ep_str:<10}"
    
    # DS field: dEp value, left-justified in 2-char field
    if dep_str is None:
        ds_field = "  "
    elif len(dep_str) == 1:
        ds_field = f"{dep_str} "  # Single digit + space
    else:
        ds_field = dep_str[:2]  # Take first 2 chars
    
    # C field (col 77) - empty for now
    c_field = " "
    
    # Cols 78-80 - empty
    rest = "   "
    
    # Assemble the line
    ensdf_line = (nucid + cont + blank1 + type_field + blank2 + 
                  e_field + de_field + space1 + j_field + 
                  t_field + dt_field + l_field + s_field + ds_field + 
                  c_field + rest)
    
    # Ensure exactly 80 characters
    ensdf_line = ensdf_line.ljust(80)[:80]
    
    return ensdf_line


def format_cl_comment(wg_str, dwg_str):
    """
    Format cL comment line with wg value.
    Format: ' 35CL cL $|w|g=X.X eV {I} (1972Hu10)'
    """
    # Build the comment string
    comment_text = f"|w|g={wg_str} eV {{I{dwg_str}}} (1972Hu10)"
    
    # ENSDF cL record format:
    # Cols 1-5: NUCID
    # Col 6: CONT (space)
    # Col 7: BLANK
    # Col 8: "c"
    # Col 9: "L"
    # Cols 10-80: Comment text starting with "$"
    
    nucid = " 35CL"
    cont = " "
    blank = " "
    c_char = "c"
    l_char = "L"
    
    # Comment starts at col 10, max 71 chars
    comment_field = f" ${comment_text}"
    
    ensdf_line = nucid + cont + blank + c_char + l_char + comment_field
    
    # Pad to 80 characters
    ensdf_line = ensdf_line.ljust(80)[:80]
    
    return ensdf_line


def main(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    output_lines = []
    i = 0
    modifications = 0
    comments_added = 0
    
    while i < len(lines):
        line = lines[i].rstrip('\n')
        
        # Check if this is an L-record in the resonance section
        if len(line) >= 8 and line[7:8] == 'L' and line[0:5] == ' 35CL':
            # Extract energy from E field (cols 10-19)
            e_str = line[9:19].strip()
            if e_str:
                try:
                    exi = float(e_str)
                    
                    # Look up in EP_DATA
                    if exi in EP_DATA:
                        ep, dep, wg, dwg = EP_DATA[exi]
                        
                        # Format new L-record with S and DS fields
                        new_line = format_ensdf_l_record_with_ep(line, ep, dep)
                        output_lines.append(new_line + '\n')
                        modifications += 1
                        
                        # Add cL comment line after this L-record
                        cl_line = format_cl_comment(wg, dwg)
                        output_lines.append(cl_line + '\n')
                        comments_added += 1
                        
                        i += 1
                        continue
                except ValueError:
                    pass
        
        # Keep line as-is
        output_lines.append(line + '\n')
        i += 1
    
    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(output_lines)
    
    print(f"Modified {modifications} L-records")
    print(f"Added {comments_added} cL comment lines")
    print(f"Output written to: {output_file}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python add_ep_data.py <input.ens> <output.ens>")
        sys.exit(1)
    
    main(sys.argv[1], sys.argv[2])
