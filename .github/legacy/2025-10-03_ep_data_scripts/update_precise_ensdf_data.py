"""
Update ENSDF file with precise Exi, Ep, dEp, and wg values from user table.

CRITICAL ENSDF Uncertainty Notation Rules:
- S field: Value with decimal (e.g., 716.0)
- DS field: Uncertainty without decimal (e.g., 7 means 0.7)
- {I} notation: Uncertainty in last digit (e.g., {I1} for 0.2 eV means 0.1 uncertainty)
"""

import re
import sys

# Precise data from user table (58 entries)
PRECISE_DATA = [
    (7066.3, 716.0, 0.7, 0.2, 0.1),
    (7103.4, 754.1, 0.7, 0.5, 0.3),
    (7178.5, 831.5, 0.8, 0.4, 0.2),
    (7194.8, 848.2, 0.7, 1.1, 0.3),
    (7226.1, 880.5, 0.8, 0.4, 0.2),
    (7234.4, 889.0, 0.8, 1.3, 0.4),
    (7272.5, 928.2, 0.9, 1.4, 0.4),
    (7362.0, 1020.4, 0.8, 3.2, 1.0),
    (7395.6, 1054.9, 1.0, 0.4, 0.2),
    (7451.2, 1112.2, 1.0, 0.3, 0.2),
    (7502.5, 1165, None, 0.6, 0.3),  # No dEp
    (7520.2, 1183.2, 1.1, 0.2, 0.1),
    (7549.8, 1213.7, 1.0, 21, 3),
    (7561.4, 1225.6, 1.0, 1.5, 0.5),
    (7601.1, 1266.5, 1.0, 3.2, 1.0),
    (7619.6, 1285.5, 1.1, 1.2, 0.4),
    (7656.7, 1323.7, 1.2, 0.5, 0.3),
    (7672.3, 1339.8, 1.1, 1.5, 0.5),
    (7685.8, 1353.7, 1.1, 2.5, 0.8),
    (7694.3, 1362.4, 1.2, 0.4, 0.2),
    (7707.2, 1375.7, 1.1, 3.7, 1.1),
    (7746.0, 1415.6, 1.2, 1.3, 0.4),
    (7778.4, 1449.0, 1.1, 1.5, 0.5),
    (7782.9, 1453.6, 1.1, 0.8, 0.4),
    (7798.4, 1469.6, 1.2, 1.5, 0.5),
    (7837.7, 1510, None, 11, 3),  # No dEp
    (7869.0, 1542.3, 1.3, 0.5, 0.3),
    (7881.3, 1554.9, 1.2, 1.6, 0.5),
    (7900.2, 1574.4, 1.2, 1.4, 0.4),
    (7924.0, 1598.9, 1.3, 0.8, 0.4),
    (7971.0, 1647.3, 1.2, 1.2, 0.4),
    (7988.4, 1665.2, 1.2, 1.5, 0.5),
    (7996.7, 1673.7, 1.1, 2.7, 0.8),
    (8002.5, 1679.7, 1.1, 4.1, 1.2),
    (8007.0, 1684.3, 1.3, 4.5, 1.4),
    (8035.8, 1714.0, 1.1, 0.9, 0.5),
    (8039.6, 1717.9, 1.1, 3.5, 1.1),
    (8076.6, 1756.0, 1.0, 1.6, 0.5),
    (8096.7, 1776.7, 1.1, 2.5, 0.8),
    (8107.4, 1787.7, 1.1, 4.2, 1.3),
    (8114.3, 1794.8, 1.3, 1.2, 0.4),
    (8147.6, 1829.1, 1.3, 2.4, 0.7),
    (8157.3, 1839.0, 1.2, 2.1, 0.6),
    (8180.3, 1862.7, 1.3, 0.8, 0.4),
    (8209.9, 1893.2, 1.1, 8.0, 2.4),
    (8218.3, 1901.8, 1.1, 6.2, 1.9),
    (8243.9, 1928.2, 1.3, 1.9, 0.6),
    (8270.8, 1955.9, 1.3, 1.8, 0.5),
    (8278.8, 1964.1, 1.4, 1.6, 0.5),
    (8284.5, 1970.0, 1.3, 2.4, 0.7),
    (8290.0, 1975.6, 1.3, 2.9, 0.9),
    (8300.1, 1986.0, 1.3, 4.0, 1.2),
    (8320.2, 2006.7, 1.2, 4.2, 1.3),
    (8323.9, 2010.5, 1.3, 1.0, 0.3),
    (8385.1, 2073.5, 1.2, 14.1, 4.2),
    (8391.4, 2080.0, 1.4, 0.6, 0.3),
    (8407.5, 2096.6, 1.2, 6.4, 1.9),
    (8411.8, 2101.0, 1.4, 3.6, 1.1),
]

# Create mapping by Ep (rounded to match existing data)
ep_to_data = {}
for exi, ep, dep, wg, dwg in PRECISE_DATA:
    # Use Ep as key (will match S field in file)
    ep_key = ep
    ep_to_data[ep_key] = (exi, ep, dep, wg, dwg)

print(f"[INFO] Loaded {len(ep_to_data)} precise data entries")
print(f"[INFO] Sample entries:")
for i, (ep_key, (exi, ep, dep, wg, dwg)) in enumerate(list(ep_to_data.items())[:3]):
    print(f"  Ep={ep_key} -> Exi={exi}, dEp={dep}, wg={wg}, dwg={dwg}")

def extract_energy_from_l_record(line):
    """Extract energy from L-record (cols 10-19)."""
    if len(line) >= 19 and line[7:9].strip() == 'L':
        e_str = line[9:19].strip()
        if e_str:
            try:
                return float(e_str)
            except:
                return None
    return None

def extract_s_field(line):
    """Extract S field value (cols 65-74) from L-record."""
    if len(line) >= 74:
        s_str = line[64:74].strip()
        if s_str:
            try:
                return float(s_str)
            except:
                return None
    return None

def format_s_field(ep, dep):
    """
    Format S and DS fields according to ENSDF rules.
    S field (cols 65-74): Value with decimal, LEFT-JUSTIFIED (e.g., "716.0     ")
    DS field (cols 75-76): Uncertainty without decimal (e.g., "7 " for 0.7)
    
    CRITICAL: User clarified - S field must always have decimal point!
    """
    # Format Ep value - ALWAYS include decimal point
    # 716.0 -> "716.0", 1165 -> "1165", 754.1 -> "754.1"
    if isinstance(ep, int):
        ep_str = f"{ep}"  # Keep integer format for values like 1165
    elif ep == int(ep):
        ep_str = f"{int(ep)}.0"  # Add .0 for values like 716.0
    else:
        ep_str = f"{ep:.1f}"  # Keep decimal for values like 754.1
    
    # Format dEp uncertainty (convert 0.7 -> 7, 1.0 -> 10, etc.)
    if dep is None:
        dep_str = ""
    else:
        # Convert decimal to integer representation
        # 0.7 -> 7, 1.0 -> 10, 1.1 -> 11, etc.
        dep_int = int(round(dep * 10))
        dep_str = str(dep_int)
        if len(dep_str) > 2:
            dep_str = dep_str[:2]  # Truncate to 2 chars max
    
    # Construct fields
    s_field = ep_str.ljust(10)  # Left-justified, 10 chars
    ds_field = dep_str.ljust(2)  # Left-justified, 2 chars
    
    return s_field, ds_field

def format_wg_comment(wg, dwg):
    """
    Format |w|g comment with correct {I} notation.
    Example: 0.2 eV {I0.1} means 0.2 ± 0.1
    {I} represents uncertainty in the value itself (not last digit)
    """
    # Format wg value (remove unnecessary decimals)
    if isinstance(wg, int) or wg == int(wg):
        wg_str = str(int(wg))
    else:
        wg_str = f"{wg:.1f}".rstrip('0').rstrip('.')
        if '.' not in wg_str:
            wg_str = str(int(float(wg_str)))
    
    # Format dwg uncertainty
    if isinstance(dwg, int) or dwg == int(dwg):
        dwg_str = str(int(dwg))
    else:
        dwg_str = f"{dwg:.1f}".rstrip('0').rstrip('.')
        if '.' not in dwg_str:
            dwg_str = str(int(float(dwg_str)))
    
    return f"|w|g={wg_str} eV {{I{dwg_str}}} (1972Hu10)"

def update_l_record_energy(line, new_exi):
    """Update L-record energy field (cols 10-19) with new precise Exi."""
    if len(line) < 80:
        return line
    
    # Format new Exi
    if isinstance(new_exi, int) or new_exi == int(new_exi):
        exi_str = f"{int(new_exi)}.0"
    else:
        exi_str = f"{new_exi:.1f}"
    
    # Update energy field (cols 10-19, left-justified)
    new_line = line[:9] + exi_str.ljust(10) + line[19:]
    return new_line

def update_l_record_s_ds(line, ep, dep):
    """Update S and DS fields in L-record."""
    if len(line) < 80:
        return line
    
    s_field, ds_field = format_s_field(ep, dep)
    
    # Replace S field (cols 65-74) and DS field (cols 75-76)
    new_line = line[:64] + s_field + ds_field + line[76:]
    return new_line

def update_cl_comment(line, wg, dwg):
    """Update cL comment line with new |w|g value."""
    wg_comment = format_wg_comment(wg, dwg)
    new_line = f" 35CL  cL ${wg_comment}".ljust(80)
    return new_line

def process_file(input_file, output_file):
    """Process ENSDF file and update with precise data."""
    with open(input_file, 'r') as f:
        lines = f.readlines()
    
    updated_lines = []
    updates_count = 0
    i = 0
    
    while i < len(lines):
        line = lines[i].rstrip('\n')
        
        # Check if this is an L-record with S field data
        if len(line) >= 74 and line[7:9].strip() == 'L':
            ep_val = extract_s_field(line)
            
            if ep_val is not None and ep_val in ep_to_data:
                # Found a match - update this L-record and its cL comment
                exi, ep, dep, wg, dwg = ep_to_data[ep_val]
                
                # Update L-record Exi
                line = update_l_record_energy(line, exi)
                
                # Update S and DS fields
                line = update_l_record_s_ds(line, ep, dep)
                
                # Add updated L-record
                updated_lines.append(line + '\n')
                
                # Check if next line is cL comment
                if i + 1 < len(lines):
                    next_line = lines[i + 1]
                    if 'cL $|w|g=' in next_line:
                        # Update cL comment
                        new_cl = update_cl_comment(next_line, wg, dwg)
                        updated_lines.append(new_cl + '\n')
                        i += 2  # Skip both L and cL lines
                        updates_count += 1
                        print(f"[UPDATE] Exi={exi:.1f}, Ep={ep}, dEp={dep}, wg={wg}, dwg={dwg}")
                        continue
                
                # No cL comment found - still count as update
                updates_count += 1
                print(f"[UPDATE] Exi={exi:.1f}, Ep={ep}, dEp={dep} (no cL comment)")
                i += 1
                continue
        
        # Not a match - keep line as-is
        updated_lines.append(line + '\n')
        i += 1
    
    # Write output
    with open(output_file, 'w') as f:
        f.writelines(updated_lines)
    
    print(f"\n[SUMMARY] Updated {updates_count} L-records with precise data")
    print(f"[SUCCESS] Output written to: {output_file}")

if __name__ == "__main__":
    input_file = "A35/Cl35/temp/1972HU10.ens"
    output_file = "A35/Cl35/temp/1972HU10_precise.ens"
    
    process_file(input_file, output_file)
