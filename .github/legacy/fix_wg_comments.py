#!/usr/bin/env python3
"""
Fix wg/dwg comment values in 1972HU10_precise_sorted.ens
Problem: Some wg/dwg values in cL comments are from original file, not user's precise table
Solution: Re-process ALL cL comments based on Ep values, replace with correct wg/dwg from user table
"""

import re

# User's 58 precise data entries: (exi, ep, dep, wg, dwg)
PRECISE_DATA = [
    (7066.3, 716.0, 0.7, 0.2, 0.1),
    (7103.4, 754.1, 0.7, 0.5, 0.3),
    (7178.5, 831.5, 0.8, 1.0, 0.6),
    (7194.8, 848.2, 0.7, 0.1, 0.1),
    (7226.1, 880.5, 0.8, 0.1, 0.1),
    (7234.4, 889.0, 0.8, 1.0, 0.6),
    (7272.5, 928.2, 0.9, 0.1, 0.1),
    (7362.0, 1020.4, 0.8, 1.2, 0.8),
    (7395.6, 1054.9, 1.0, 2.5, 1.2),
    (7451.2, 1112.2, 1.0, 1.5, 0.9),
    (7502.5, 1165, None, 1.0, 0.2),
    (7520.2, 1183.2, 1.1, 2.0, 1.2),
    (7549.8, 1213.7, 1.0, 0.7, 0.4),
    (7561.4, 1225.6, 1.0, 1.0, 0.6),
    (7601.1, 1266.5, 1.0, 0.8, 0.5),
    (7619.6, 1285.5, 1.1, 0.4, 0.2),
    (7656.7, 1323.7, 1.2, 0.3, 0.2),
    (7672.3, 1339.8, 1.1, 0.8, 0.5),
    (7685.8, 1353.7, 1.1, 2.1, 1.3),
    (7694.3, 1362.4, 1.2, 0.8, 0.5),
    (7707.2, 1375.7, 1.1, 0.3, 0.2),
    (7746.0, 1415.6, 1.2, 3.0, 1.8),
    (7778.4, 1449.0, 1.1, 1.5, 0.9),
    (7782.9, 1453.6, 1.1, 2.5, 1.5),
    (7798.4, 1469.6, 1.2, 0.5, 0.3),
    (7837.7, 1510, None, 1.0, 0.6),
    (7869.0, 1542.3, 1.3, 2.5, 1.5),
    (7881.3, 1554.9, 1.2, 1.5, 0.9),
    (7900.2, 1574.4, 1.2, 4.5, 2.7),
    (7924.0, 1598.9, 1.3, 1.0, 0.6),
    (7971.0, 1647.3, 1.2, 2.0, 1.2),
    (7988.4, 1665.2, 1.2, 1.0, 0.6),
    (7996.7, 1673.7, 1.1, 1.0, 0.6),
    (8002.5, 1679.7, 1.1, 1.2, 0.7),
    (8007.0, 1684.3, 1.3, 1.5, 0.9),
    (8035.8, 1714.0, 1.1, 3.0, 1.8),
    (8039.6, 1717.9, 1.1, 5.5, 3.3),
    (8076.6, 1756.0, 1.0, 5.0, 3.0),
    (8096.7, 1776.7, 1.1, 3.0, 1.8),
    (8107.4, 1787.7, 1.1, 4.5, 2.7),
    (8114.3, 1794.8, 1.3, 1.5, 0.9),
    (8147.6, 1829.1, 1.3, 1.2, 0.7),
    (8157.3, 1839.0, 1.2, 3.5, 2.1),
    (8180.3, 1862.7, 1.3, 2.5, 1.5),
    (8209.9, 1893.2, 1.1, 6.0, 3.0),
    (8218.3, 1901.8, 1.1, 6.0, 3.0),
    (8243.9, 1928.2, 1.3, 9.0, 3.0),
    (8270.8, 1955.9, 1.3, 9.0, 3.0),
    (8278.8, 1964.1, 1.4, 2.0, 1.2),
    (8284.5, 1970.0, 1.3, 11.0, 3.0),
    (8290.0, 1975.6, 1.3, 7.0, 3.0),
    (8300.1, 1986.0, 1.3, 3.0, 1.8),
    (8320.2, 2006.7, 1.2, 5.0, 3.0),
    (8323.9, 2010.5, 1.3, 11.0, 3.0),
    (8385.1, 2073.5, 1.2, 0.6, 0.2),
    (8391.4, 2080.0, 1.4, 2.0, 1.2),
    (8407.5, 2096.6, 1.2, 3.0, 1.8),
    (8411.8, 2101.0, 1.4, 3.6, 1.1),
]

# Create Ep -> (wg, dwg) mapping
ep_to_wg = {}
for exi, ep, dep, wg, dwg in PRECISE_DATA:
    # Handle both integer and float Ep values
    if isinstance(ep, int):
        ep_key = float(ep)
    else:
        ep_key = ep
    ep_to_wg[ep_key] = (wg, dwg)

def extract_ep_from_l_record(line):
    """Extract Ep value from L-record S field (columns 65-74)"""
    if len(line) < 74:
        return None
    if not line[7:9].strip() == 'L':
        return None
    
    s_field = line[64:74].strip()
    if not s_field:
        return None
    
    try:
        ep_val = float(s_field)
        return ep_val
    except ValueError:
        return None

def format_wg_comment(wg, dwg):
    """Format wg/dwg into ENSDF {I} notation comment"""
    # Format wg value - remove trailing zeros but keep significant figures
    if wg == int(wg):
        wg_str = f"{int(wg)}.0"
    else:
        wg_str = f"{wg:.1f}".rstrip('0').rstrip('.')
        if '.' not in wg_str:
            wg_str += ".0"
    
    # Format dwg using {I} notation
    # User clarified: {I0.1} means uncertainty is 0.1, not uncertainty in last digit
    if dwg == int(dwg):
        dwg_str = f"{int(dwg)}"
    else:
        dwg_str = f"{dwg:.1f}".rstrip('0').rstrip('.')
    
    return f"|w|g={wg_str} eV {{I{dwg_str}}} (1972Hu10)"

def fix_wg_comments(input_file, output_file):
    """Fix all wg/dwg comments in ENSDF file"""
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    i = 0
    output_lines = []
    updates_count = 0
    unchanged_count = 0
    
    while i < len(lines):
        line = lines[i]
        output_lines.append(line)
        
        # Check if this is an L-record with Ep data
        ep_val = extract_ep_from_l_record(line)
        
        if ep_val is not None and ep_val in ep_to_wg:
            # Check next line for cL comment
            if i + 1 < len(lines):
                next_line = lines[i + 1]
                
                # Check if next line is cL comment with wg data
                if next_line[7:9].strip() == 'cL' and '|w|g=' in next_line:
                    # Get correct wg, dwg from table
                    wg, dwg = ep_to_wg[ep_val]
                    correct_comment = format_wg_comment(wg, dwg)
                    
                    # Extract current comment value
                    current_wg_match = re.search(r'\|w\|g=([\d.]+)\s+eV\s+\{I([\d.]+)\}', next_line)
                    if current_wg_match:
                        current_wg = current_wg_match.group(1)
                        current_dwg = current_wg_match.group(2)
                        
                        # Build new cL line with correct values
                        new_cl_line = f" 35CL  cL ${correct_comment}".ljust(80)
                        
                        if new_cl_line.strip() != next_line.strip():
                            print(f"Line {i+2}: Updating wg/dwg comment")
                            print(f"  Ep: {ep_val}")
                            print(f"  OLD: |w|g={current_wg} eV {{I{current_dwg}}}")
                            print(f"  NEW: |w|g={wg} eV {{I{dwg}}}")
                            output_lines.append(new_cl_line + '\n')
                            updates_count += 1
                        else:
                            output_lines.append(next_line)
                            unchanged_count += 1
                        
                        i += 2  # Skip the cL line we just processed
                        continue
        
        i += 1
    
    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(output_lines)
    
    print(f"\n[SUCCESS] Fixed wg/dwg comments")
    print(f"  Updates: {updates_count} comments fixed")
    print(f"  Unchanged: {unchanged_count} comments already correct")
    print(f"  Output: {output_file}")

if __name__ == "__main__":
    input_file = "A35/Cl35/temp/1972HU10_precise_sorted.ens"
    output_file = "A35/Cl35/temp/1972HU10_precise_sorted_fixed.ens"
    
    fix_wg_comments(input_file, output_file)
