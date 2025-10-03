"""
Fix Ep, dEp, and ωγ data in 1972HU10.ens using CORRECT precise Ep values.

This script uses ALL 58 Ep values from the revised data.
Sp = 6368 keV (proton separation energy for 34S(p,γ)35Cl)
Exi = Ep + Sp

Some L-records will have Ep but no G-records (resonances without gamma decay).
"""

# REVISED Ep data with ALL decimal places (58 total entries)
# Calculated Exi = Ep + 6368 keV
EP_PRECISE_DATA = {
    # Exi (rounded) -> (Ep_str, dEp_str, wg_str, dwg_str)
    7084: ("716.0", "0.7", "0.2", "0.1"),      # 716.0 + 6368 = 7084.0
    7122: ("754.1", "0.7", "0.5", "0.3"),      # 754.1 + 6368 = 7122.1
    7200: ("831.5", "0.8", "0.4", "0.2"),      # 831.5 + 6368 = 7199.5
    7216: ("848.2", "0.7", "1.1", "0.3"),      # 848.2 + 6368 = 7216.2
    7249: ("880.5", "0.8", "0.4", "0.2"),      # 880.5 + 6368 = 7248.5
    7257: ("889.0", "0.8", "1.3", "0.4"),      # 889.0 + 6368 = 7257.0
    7296: ("928.2", "0.9", "1.4", "0.4"),      # 928.2 + 6368 = 7296.2
    7388: ("1020.4", "0.8", "3.2", "1.0"),     # 1020.4 + 6368 = 7388.4
    7423: ("1054.9", "1.0", "0.4", "0.2"),     # 1054.9 + 6368 = 7422.9
    7480: ("1112.2", "1.0", "0.3", "0.2"),     # 1112.2 + 6368 = 7480.2
    7533: ("1165", None, "0.6", "0.3"),        # 1165 + 6368 = 7533 (no dEp, matches Exi 7533 from CSV)
    7551: ("1183.2", "1.1", "0.2", "0.1"),     # 1183.2 + 6368 = 7551.2
    7582: ("1213.7", "1.0", "21", "3"),        # 1213.7 + 6368 = 7581.7
    7594: ("1225.6", "1.0", "1.5", "0.5"),     # 1225.6 + 6368 = 7593.6
    7635: ("1266.5", "1.0", "3.2", "1.0"),     # 1266.5 + 6368 = 7634.5
    7654: ("1285.5", "1.1", "1.2", "0.4"),     # 1285.5 + 6368 = 7653.5
    7692: ("1323.7", "1.2", "0.5", "0.3"),     # 1323.7 + 6368 = 7691.7
    7708: ("1339.8", "1.1", "1.5", "0.5"),     # 1339.8 + 6368 = 7707.8
    7722: ("1353.7", "1.1", "2.5", "0.8"),     # 1353.7 + 6368 = 7721.7
    7730: ("1362.4", "1.2", "0.4", "0.2"),     # 1362.4 + 6368 = 7730.4
    7744: ("1375.7", "1.1", "3.7", "1.1"),     # 1375.7 + 6368 = 7743.7
    7784: ("1415.6", "1.2", "1.3", "0.4"),     # 1415.6 + 6368 = 7783.6
    7817: ("1449.0", "1.1", "1.5", "0.5"),     # 1449.0 + 6368 = 7817.0
    7822: ("1453.6", "1.1", "0.8", "0.4"),     # 1453.6 + 6368 = 7821.6
    7838: ("1469.6", "1.2", "1.5", "0.5"),     # 1469.6 + 6368 = 7837.6
    7878: ("1510", None, "11", "3"),           # 1510 + 6368 = 7878 (no dEp, might match Exi 7878 from CSV)
    7910: ("1542.3", "1.3", "0.5", "0.3"),     # 1542.3 + 6368 = 7910.3
    7923: ("1554.9", "1.2", "1.6", "0.5"),     # 1554.9 + 6368 = 7922.9
    7942: ("1574.4", "1.2", "1.4", "0.4"),     # 1574.4 + 6368 = 7942.4
    7967: ("1598.9", "1.3", "0.8", "0.4"),     # 1598.9 + 6368 = 7966.9
    8015: ("1647.3", "1.2", "1.2", "0.4"),     # 1647.3 + 6368 = 8015.3
    8033: ("1665.2", "1.2", "1.5", "0.5"),     # 1665.2 + 6368 = 8033.2
    8042: ("1673.7", "1.1", "2.7", "0.8"),     # 1673.7 + 6368 = 8041.7
    8048: ("1679.7", "1.1", "4.1", "1.2"),     # 1679.7 + 6368 = 8047.7
    8052: ("1684.3", "1.3", "4.5", "1.4"),     # 1684.3 + 6368 = 8052.3
    8082: ("1714.0", "1.1", "0.9", "0.5"),     # 1714.0 + 6368 = 8082.0
    8086: ("1717.9", "1.1", "3.5", "1.1"),     # 1717.9 + 6368 = 8085.9
    8124: ("1756.0", "1.0", "1.6", "0.5"),     # 1756.0 + 6368 = 8124.0
    8145: ("1776.7", "1.1", "2.5", "0.8"),     # 1776.7 + 6368 = 8144.7
    8156: ("1787.7", "1.1", "4.2", "1.3"),     # 1787.7 + 6368 = 8155.7
    8163: ("1794.8", "1.3", "1.2", "0.4"),     # 1794.8 + 6368 = 8162.8
    8197: ("1829.1", "1.3", "2.4", "0.7"),     # 1829.1 + 6368 = 8197.1
    8207: ("1839.0", "1.2", "2.1", "0.6"),     # 1839.0 + 6368 = 8207.0
    8231: ("1862.7", "1.3", "0.8", "0.4"),     # 1862.7 + 6368 = 8230.7
    8261: ("1893.2", "1.1", "8.0", "2.4"),     # 1893.2 + 6368 = 8261.2
    8270: ("1901.8", "1.1", "6.2", "1.9"),     # 1901.8 + 6368 = 8269.8
    8296: ("1928.2", "1.3", "1.9", "0.6"),     # 1928.2 + 6368 = 8296.2 (NEW - not in original CSV)
    8324: ("1955.9", "1.3", "1.8", "0.5"),     # 1955.9 + 6368 = 8323.9 (NEW)
    8332: ("1964.1", "1.4", "1.6", "0.5"),     # 1964.1 + 6368 = 8332.1 (NEW)
    8338: ("1970.0", "1.3", "2.4", "0.7"),     # 1970.0 + 6368 = 8338.0 (NEW)
    8344: ("1975.6", "1.3", "2.9", "0.9"),     # 1975.6 + 6368 = 8343.6 (NEW)
    8354: ("1986.0", "1.3", "4.0", "1.2"),     # 1986.0 + 6368 = 8354.0 (NEW)
    8375: ("2006.7", "1.2", "4.2", "1.3"),     # 2006.7 + 6368 = 8374.7 (NEW)
    8379: ("2010.5", "1.3", "1.0", "0.3"),     # 2010.5 + 6368 = 8378.5 (NEW)
    8442: ("2073.5", "1.2", "14.1", "4.2"),    # 2073.5 + 6368 = 8441.5 (NEW)
    8448: ("2080.0", "1.4", "0.6", "0.3"),     # 2080.0 + 6368 = 8448.0 (NEW)
    8465: ("2096.6", "1.2", "6.4", "1.9"),     # 2096.6 + 6368 = 8464.6 (NEW)
    8469: ("2101.0", "1.4", "3.6", "1.1"),     # 2101.0 + 6368 = 8469.0 (NEW)
}

def format_ensdf_l_record_with_ep(line, ep_str, dep_str):
    """
    Format L-record with S field (Ep) and DS field (dEp).
    
    S field: columns 65-74 (10 chars, left-justified)
    DS field: columns 75-76 (2 chars, left-justified)
    Total line: exactly 80 characters
    
    CRITICAL: All Ep values now have decimals, so uncertainty conversion is straightforward:
    E.g., Ep=716.0±0.7 -> S="716.0", DS="7" (uncertainty 0.7×10^1 = 7 in last digit)
    E.g., Ep=2073.5±1.2 -> S="2073.5", DS="12" (uncertainty 1.2×10^1 = 12 in last digit)
    """
    # Extract existing L-record content (cols 1-64)
    base_record = line[:64] if len(line) >= 64 else line.ljust(64)
    
    # Format S field (10 chars, left-justified)
    s_field = f"{ep_str:<10}"
    
    # Format DS field (2 chars, left-justified)
    if dep_str is None:
        ds_field = "  "
    else:
        # Convert uncertainty to integer representation
        # All Ep values have 1 decimal place, so multiply dEp by 10
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
    uncertainty_notation = f"{{I{dwg_str}}}"
    
    comment = f" 35CL  cL $|w|g={wg_str} eV {uncertainty_notation} (1972Hu10)"
    
    # Pad to exactly 80 characters
    return comment.ljust(80)

def create_new_l_record(exi, ep_str, dep_str):
    """
    Create a new L-record for resonances that don't exist in the file yet.
    
    Format: ' 35CL  L EEEE.E                                                 EP        DE'
    """
    # Format Exi value (no uncertainty needed as per user)
    exi_str = f"{exi:.1f}"
    
    # Build L-record parts
    nucid = " 35CL"
    cont = " "
    blank1 = " "
    rec_type = "L"
    blank2 = " "
    e_field = f"{exi_str:<10}"  # Left-justified, 10 chars
    de_field = "  "  # No uncertainty for E(level)
    space = " "
    jp_field = " " * 17  # J-π field empty
    t_field = " " * 10   # Half-life field empty
    dt_field = " " * 6   # T uncertainty empty
    l_field = " " * 9    # L-transfer empty
    
    # S and DS fields
    s_field = f"{ep_str:<10}"
    if dep_str is None:
        ds_field = "  "
    else:
        dep_float = float(dep_str)
        if '.' in ep_str:
            decimals = len(ep_str.split('.')[1])
        else:
            decimals = 0
        dep_int = int(round(dep_float * (10 ** decimals)))
        dep_ensdf = str(dep_int)
        if len(dep_ensdf) == 1:
            ds_field = f"{dep_ensdf} "
        else:
            ds_field = dep_ensdf[:2]
    
    c_flag = " "
    ending = "   "
    
    line = nucid + cont + blank1 + rec_type + blank2 + e_field + de_field + space + jp_field + t_field + dt_field + l_field + s_field + ds_field + c_flag + ending
    
    return line[:80].ljust(80)

def main():
    input_file = r"A35\Cl35\temp\1972HU10.ens"
    output_file = r"A35\Cl35\temp\1972HU10_corrected.ens"
    
    with open(input_file, 'r') as f:
        lines = f.readlines()
    
    # Track which Exi values we find in the file
    found_exi = set()
    
    new_lines = []
    i = 0
    levels_processed = 0
    
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
                    
                    # Mark this Exi as found
                    found_exi.add(exi_rounded)
                    
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
                    print(f"[OK] Level {exi:.1f}: Ep={ep_str}, dEp={dep_str}, wg={wg_str}, dwg={dwg_str}")
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
    
    # Find missing Exi values and create new L-records
    missing_exi = set(EP_PRECISE_DATA.keys()) - found_exi
    if missing_exi:
        print(f"\n[INFO] Creating {len(missing_exi)} new L-records for resonances not in original file:")
        # Insert new L-records in ascending energy order at the end
        new_l_records = []
        for exi in sorted(missing_exi):
            ep_str, dep_str, wg_str, dwg_str = EP_PRECISE_DATA[exi]
            new_l_line = create_new_l_record(exi, ep_str, dep_str)
            cl_comment = format_cl_comment(wg_str, dwg_str)
            new_l_records.append(new_l_line + '\n')
            new_l_records.append(cl_comment + '\n')
            print(f"[NEW] Level {exi:.1f}: Ep={ep_str}, dEp={dep_str}, wg={wg_str}, dwg={dwg_str}")
        
        # Append new L-records at the end
        new_lines.extend(new_l_records)
        levels_processed += len(missing_exi)
    
    # Write corrected file
    with open(output_file, 'w') as f:
        f.writelines(new_lines)
    
    print(f"\n[SUMMARY] Processed {levels_processed} resonance levels")
    print(f"[SUCCESS] Corrected file written to: {output_file}")

if __name__ == "__main__":
    main()
