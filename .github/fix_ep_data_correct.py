"""
Fix Ep, dEp, and ωγ data in 1972HU10.ens using CORRECT precise Ep values.

This script uses the precise Ep values from the original chatbox data,
mapping them to the rounded Exi values in the CSV Branching_Ratios table.
"""

# Precise Ep data from revised user data (58 total resonances)
# Format: Exi (rounded from Ep + 6347) -> (Ep_str, dEp_str, wg_str, dwg_str)
EP_PRECISE_DATA = {
    # Existing L-records in file (48 resonances from CSV)
    7063: ("716.0", "0.7", "0.2", "0.1"),
    7100: ("754.1", "0.7", "0.5", "0.3"),
    7175: ("831.5", "0.8", "0.4", "0.2"),
    7192: ("848.2", "0.7", "1.1", "0.3"),
    7223: ("880.5", "0.8", "0.4", "0.2"),
    7231: ("889.0", "0.8", "1.3", "0.4"),
    7269: ("928.2", "0.9", "1.4", "0.4"),
    7358: ("1020.4", "0.8", "3.2", "1.0"),
    7392: ("1054.9", "1.0", "0.4", "0.2"),
    7448: ("1112.2", "1.0", "0.3", "0.2"),
    7499: ("1165", None, "0.6", "0.3"),           # No dEp - match Ep=1165 from CSV
    # 7500: User says match 1165 to 7499, so skip 7500
    7517: ("1183.2", "1.1", "0.2", "0.1"),
    7546: ("1213.7", "1.0", "21", "3"),
    7558: ("1225.6", "1.0", "1.5", "0.5"),
    7598: ("1266.5", "1.0", "3.2", "1.0"),
    7616: ("1285.5", "1.1", "1.2", "0.4"),
    7653: ("1323.7", "1.2", "0.5", "0.3"),
    7669: ("1339.8", "1.1", "1.5", "0.5"),
    7683: ("1353.7", "1.1", "2.5", "0.8"),
    7691: ("1362.4", "1.2", "0.4", "0.2"),
    7704: ("1375.7", "1.1", "3.7", "1.1"),
    7743: ("1415.6", "1.2", "1.3", "0.4"),
    7775: ("1449.0", "1.1", "1.5", "0.5"),
    7780: ("1453.6", "1.1", "0.8", "0.4"),
    7795: ("1469.6", "1.2", "1.5", "0.5"),
    7834: ("1510", None, "11", "3"),              # No dEp - match Ep=1513 from CSV
    7866: ("1542.3", "1.3", "0.5", "0.3"),
    7878: ("1554.9", "1.2", "1.6", "0.5"),
    7897: ("1574.4", "1.2", "1.4", "0.4"),
    7921: ("1598.9", "1.3", "0.8", "0.4"),
    7968: ("1647.3", "1.2", "1.2", "0.4"),
    7985: ("1665.2", "1.2", "1.5", "0.5"),
    7993: ("1673.7", "1.1", "2.7", "0.8"),
    7999: ("1679.7", "1.1", "4.1", "1.2"),
    8004: ("1684.3", "1.3", "4.5", "1.4"),
    8033: ("1714.0", "1.1", "0.9", "0.5"),
    8036: ("1717.9", "1.1", "3.5", "1.1"),
    8073: ("1756.0", "1.0", "1.6", "0.5"),
    8093: ("1776.7", "1.1", "2.5", "0.8"),
    8104: ("1787.7", "1.1", "4.2", "1.3"),
    8111: ("1794.8", "1.3", "1.2", "0.4"),
    8144: ("1829.1", "1.3", "2.4", "0.7"),
    8154: ("1839.0", "1.2", "2.1", "0.6"),
    8177: ("1862.7", "1.3", "0.8", "0.4"),
    8207: ("1893.2", "1.1", "8.0", "2.4"),
    8215: ("1901.8", "1.1", "6.2", "1.9"),
    8382: ("2073.5", "1.2", "14.1", "4.2"),       # From CSV Ep=2073 -> Exi=8382
    
    # NEW resonances NOT in CSV (10 additional - need to create L-records)
    8275: ("1928.2", "1.3", "1.9", "0.6"),        # Exi = 1928.2 + 6347 ≈ 8275
    8303: ("1955.9", "1.3", "1.8", "0.5"),        # Exi = 1955.9 + 6347 ≈ 8303
    8311: ("1964.1", "1.4", "1.6", "0.5"),        # Exi = 1964.1 + 6347 ≈ 8311
    8317: ("1970.0", "1.3", "2.4", "0.7"),        # Exi = 1970.0 + 6347 = 8317
    8323: ("1975.6", "1.3", "2.9", "0.9"),        # Exi = 1975.6 + 6347 ≈ 8323
    8333: ("1986.0", "1.3", "4.0", "1.2"),        # Exi = 1986.0 + 6347 = 8333
    8354: ("2006.7", "1.2", "4.2", "1.3"),        # Exi = 2006.7 + 6347 ≈ 8354
    8358: ("2010.5", "1.3", "1.0", "0.3"),        # Exi = 2010.5 + 6347 ≈ 8358
    8427: ("2080.0", "1.4", "0.6", "0.3"),        # Exi = 2080.0 + 6347 = 8427
    8444: ("2096.6", "1.2", "6.4", "1.9"),        # Exi = 2096.6 + 6347 ≈ 8444
    8448: ("2101.0", "1.4", "3.6", "1.1"),        # Exi = 2101.0 + 6347 = 8448
}

def format_ensdf_l_record_with_ep(line, ep_str, dep_str):
    """
    Format L-record with S field (Ep) and DS field (dEp).
    
    S field: columns 65-74 (10 chars, left-justified)
    DS field: columns 75-76 (2 chars, left-justified)
    Total line: exactly 80 characters
    """
    # Extract existing L-record content (cols 1-64)
    base_record = line[:64] if len(line) >= 64 else line.ljust(64)
    
    # Format S field (10 chars, left-justified)
    s_field = f"{ep_str:<10}"
    
    # Format DS field (2 chars, left-justified)
    # CRITICAL: Convert decimal uncertainty to ENSDF notation
    # E.g., Ep=2073.5±1.2 -> S="2073.5", DS="12" (uncertainty in last digit)
    if dep_str is None:
        ds_field = "  "
    else:
        # Convert uncertainty to integer representation
        # E.g., "1.2" -> "12", "0.7" -> "7", "1.0" -> "10"
        try:
            dep_float = float(dep_str)
            # Determine decimal places in Ep value
            if '.' in ep_str:
                decimals = len(ep_str.split('.')[1])
            else:
                decimals = 0
            
            # Convert uncertainty to integer in last digit position
            dep_int = int(round(dep_float * (10 ** decimals)))
            dep_ensdf = str(dep_int)
            
            # Format as 2-char field, left-justified
            if len(dep_ensdf) == 1:
                ds_field = f"{dep_ensdf} "
            else:
                ds_field = dep_ensdf[:2]
        except ValueError:
            # Fallback for non-numeric uncertainties
            if len(dep_str) == 1:
                ds_field = f"{dep_str} "
            else:
                ds_field = dep_str[:2]
    
    # Column 77 - preserve existing comment flag if any
    c_flag = line[76] if len(line) > 76 else " "
    
    # Columns 78-80 - blank
    ending = "   "
    
    # Construct final 80-char line
    result = base_record + s_field + ds_field + c_flag + ending
    
    # Ensure exactly 80 characters
    if len(result) > 80:
        result = result[:80]
    elif len(result) < 80:
        result = result.ljust(80)
    
    return result

def format_cl_comment(wg_str, dwg_str):
    """
    Format cL comment line with ωγ value.
    
    Format: ' 35CL  cL $|w|g=X.X eV {IX.X} (1972Hu10)'
    Total: exactly 80 characters
    """
    # Convert dwg_str to uncertainty notation
    # If dwg has decimal (e.g., "4.2"), use as-is: {I4.2}
    # If dwg is integer (e.g., "3"), use as-is: {I3}
    uncertainty_notation = f"{{I{dwg_str}}}"
    
    comment = f" 35CL  cL $|w|g={wg_str} eV {uncertainty_notation} (1972Hu10)"
    
    # Pad to exactly 80 characters
    return comment.ljust(80)

def main():
    input_file = r"A35\Cl35\temp\1972HU10.ens"
    output_file = r"A35\Cl35\temp\1972HU10_corrected.ens"
    
    with open(input_file, 'r') as f:
        lines = f.readlines()
    
    # Track which Exi values are already in the file
    existing_exi = set()
    for line in lines:
        if len(line) >= 8 and line[7] == 'L':
            e_field = line[9:19].strip()
            try:
                exi = float(e_field)
                exi_rounded = int(round(exi))
                existing_exi.add(exi_rounded)
            except ValueError:
                pass
    
    # Find NEW Exi values that need L-records created
    all_exi = set(EP_PRECISE_DATA.keys())
    new_exi = sorted(all_exi - existing_exi)
    
    print(f"[INFO] Existing L-records: {len(existing_exi)}")
    print(f"[INFO] New L-records to create: {len(new_exi)}")
    if new_exi:
        print(f"[INFO] New Exi values: {new_exi}")
    
    new_lines = []
    i = 0
    levels_processed = 0
    levels_created = 0
    
    while i < len(lines):
        line = lines[i].rstrip('\n')
        
        # Check if this is an L-record
        if len(line) >= 8 and line[7] == 'L':
            # Extract energy value from columns 10-19
            e_field = line[9:19].strip()
            try:
                exi = float(e_field)
                exi_rounded = int(round(exi))
                
                # Check if this Exi has Ep data
                if exi_rounded in EP_PRECISE_DATA:
                    ep_str, dep_str, wg_str, dwg_str = EP_PRECISE_DATA[exi_rounded]
                    
                    # Format L-record with S and DS fields
                    modified_line = format_ensdf_l_record_with_ep(line, ep_str, dep_str)
                    new_lines.append(modified_line + '\n')
                    
                    # Check if next line is already a cL comment
                    if i + 1 < len(lines):
                        next_line = lines[i + 1].rstrip('\n')
                        if len(next_line) >= 8 and next_line[7:9] == 'cL':
                            # Skip existing cL comment
                            i += 1
                    
                    # Add new cL comment with ωγ value
                    cl_comment = format_cl_comment(wg_str, dwg_str)
                    new_lines.append(cl_comment + '\n')
                    
                    levels_processed += 1
                    print(f"[OK] Updated Level {exi:.1f}: Ep={ep_str}, dEp={dep_str}, wg={wg_str}, dwg={dwg_str}")
                else:
                    # L-record without Ep data - keep as-is
                    new_lines.append(line + '\n')
            except ValueError:
                # Not a valid energy value
                new_lines.append(line + '\n')
        else:
            # Not an L-record - keep as-is
            new_lines.append(line + '\n')
        
        i += 1
    
    # CREATE new L-records for missing Exi values
    # Insert them at the end before the last line (file ending marker)
    if new_exi:
        print("\n[INFO] Creating new L-records for additional resonances...")
        insert_position = len(new_lines) - 1  # Before last line
        
        for exi_new in new_exi:
            ep_str, dep_str, wg_str, dwg_str = EP_PRECISE_DATA[exi_new]
            
            # Create new L-record
            # Format: " 35CL  L EEEE.E    "
            exi_str = f"{exi_new}.0"
            new_l_record = f" 35CL  L {exi_str:<10}"
            new_l_record = new_l_record.ljust(64)  # Pad to column 64
            
            # Add S and DS fields
            new_l_with_ep = format_ensdf_l_record_with_ep(new_l_record, ep_str, dep_str)
            new_lines.insert(insert_position, new_l_with_ep + '\n')
            insert_position += 1
            
            # Add cL comment
            cl_comment = format_cl_comment(wg_str, dwg_str)
            new_lines.insert(insert_position, cl_comment + '\n')
            insert_position += 1
            
            levels_created += 1
            print(f"[NEW] Created Level {exi_new}.0: Ep={ep_str}, dEp={dep_str}, wg={wg_str}, dwg={dwg_str}")
    
    # Write corrected file
    with open(output_file, 'w') as f:
        f.writelines(new_lines)
    
    print(f"\n[SUMMARY] Updated {levels_processed} existing resonance levels")
    print(f"[SUMMARY] Created {levels_created} new resonance levels")
    print(f"[SUMMARY] Total resonances: {levels_processed + levels_created}")
    print(f"[SUCCESS] Corrected file written to: {output_file}")

if __name__ == "__main__":
    main()
