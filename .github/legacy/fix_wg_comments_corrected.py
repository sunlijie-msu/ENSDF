#!/usr/bin/env python3
"""
Fix wg/dwg comments in 1972HU10.ens with CORRECT {In} notation

CRITICAL CORRECTION:
- Previous version WRONGLY used {I0.1}, {I1.1}, {I2.7} format (decimals)
- CORRECT ENSDF format: {I1}, {I11}, {I27} (integers only!)

ENSDF {In} Notation Rules (from copilot-instructions.md lines 1629+):
- For 1 decimal place: value(n) means value ± n*0.1
  - 3.6(11) → 3.6 ± 1.1 eV → {I11}
  - 1.0(2) → 1.0 ± 0.2 eV → {I2}
  - 0.5(3) → 0.5 ± 0.3 eV → {I3}
- For 0 decimals: value(n) means value ± n
  - 11(3) → 11 ± 3 eV → {I3}
  - 5(30) → 5 ± 30 eV → {I30}

Conversion Algorithm:
1. Count decimal places in wg value
2. Scale dwg by 10^(decimal_places) to get last-digit representation
3. Round to nearest integer
4. Format as {I<integer>} with NO decimals
"""

import re
import sys
from decimal import Decimal, ROUND_HALF_UP

# Data table from user (58 entries)
DATA_TABLE = [
    (7066.3, 716.0, 7.0, 0.2, 0.1),
    (7087.1, 737.0, 7.0, 0.5, 0.3),
    (7147.3, 797.0, 7.0, 0.5, 0.2),
    (7159.3, 809.0, 7.0, 0.3, 0.1),
    (7172.6, 822.0, 6.0, 0.4, 0.1),
    (7185.3, 835.0, 7.0, 0.1, 0.1),
    (7232.9, 882.0, 7.0, 0.3, 0.1),
    (7234.3, 883.0, 6.0, 3.2, 2.0),
    (7261.3, 910.0, 6.0, 0.1, 0.1),
    (7279.3, 928.0, 7.0, 0.3, 0.1),
    (7313.3, 962.0, 7.0, 1.0, 0.2),
    (7355.3, 1005.0, 7.0, 1.0, 0.6),
    (7414.9, 1064.0, 7.0, 0.1, 0.1),
    (7420.3, 1069.0, 7.0, 0.3, 0.1),
    (7421.3, 1070.0, 7.0, 0.8, 0.2),
    (7440.3, 1089.0, 7.0, 0.2, 0.1),
    (7445.7, 1095.0, 7.0, 0.2, 0.1),
    (7502.5, 1165.0, 15.0, 1.0, 0.2),
    (7518.9, 1168.0, 7.0, 0.2, 0.1),
    (7551.9, 1201.0, 7.0, 0.4, 0.1),
    (7553.3, 1202.0, 7.0, 0.5, 0.1),
    (7581.3, 1230.0, 7.0, 3.0, 1.8),
    (7588.3, 1237.0, 7.0, 0.2, 0.1),
    (7611.3, 1260.0, 7.0, 0.3, 0.1),
    (7641.3, 1290.0, 7.0, 0.2, 0.1),
    (7663.3, 1312.0, 7.0, 0.3, 0.1),
    (7669.8, 1319.0, 7.0, 0.2, 0.1),
    (7683.8, 1333.0, 7.0, 0.2, 0.1),
    (7699.8, 1349.0, 7.0, 0.3, 0.1),
    (7724.3, 1373.0, 7.0, 0.9, 0.2),
    (7731.3, 1380.0, 7.0, 0.5, 0.1),
    (7747.3, 1396.0, 7.0, 1.0, 0.3),
    (7764.3, 1413.0, 7.0, 0.9, 0.3),
    (7769.3, 1418.0, 7.0, 0.7, 0.2),
    (7773.3, 1422.0, 7.0, 0.2, 0.1),
    (7776.3, 1425.0, 7.0, 3.0, 0.6),
    (7779.3, 1428.0, 7.0, 1.0, 0.3),
    (7799.3, 1448.0, 7.0, 0.9, 0.3),
    (7803.3, 1452.0, 7.0, 0.6, 0.2),
    (7808.3, 1457.0, 7.0, 0.1, 0.1),
    (7824.3, 1473.0, 7.0, 0.1, 0.1),
    (7826.3, 1475.0, 7.0, 1.0, 0.3),
    (7831.3, 1480.0, 7.0, 0.6, 0.2),
    (7833.3, 1482.0, 7.0, 1.0, 0.3),
    (7836.3, 1485.0, 7.0, 0.7, 0.2),
    (7837.7, 1510.0, 24.0, 1.0, 0.6),
    (7845.8, 1495.0, 7.0, 0.3, 0.1),
    (7875.3, 1524.0, 7.0, 0.4, 0.1),
    (7895.3, 1544.0, 7.0, 0.5, 0.2),
    (7909.3, 1558.0, 7.0, 0.7, 0.2),
    (7933.3, 1582.0, 7.0, 0.8, 0.2),
    (7936.3, 1585.0, 7.0, 0.5, 0.2),
    (7949.3, 1598.0, 7.0, 3.0, 0.6),
    (7955.9, 1605.0, 7.0, 0.5, 0.2),
    (7963.3, 1612.0, 7.0, 0.8, 0.2),
    (7979.3, 1628.0, 7.0, 5.0, 3.0),
    (7994.3, 1643.0, 7.0, 0.7, 0.3),
    (8000.9, 1650.0, 7.0, 3.6, 1.1),
]

def format_wg_comment(wg, dwg):
    """
    Format wg/dwg comment with CORRECT ENSDF {In} notation
    
    CRITICAL ALGORITHM:
    wg is ALWAYS formatted with 1 decimal place (e.g., "5.0", "3.6", "0.2")
    Therefore, dwg must ALWAYS be scaled by 10 to get {In} integer
    
    Examples:
    - wg=3.6, dwg=1.1 → "3.6 eV {I11}" (1.1*10=11)
    - wg=1.0, dwg=0.2 → "1.0 eV {I2}" (0.2*10=2)
    - wg=0.5, dwg=0.3 → "0.5 eV {I3}" (0.3*10=3)
    - wg=5.0, dwg=3.0 → "5.0 eV {I30}" (3.0*10=30)
    - wg=11.0, dwg=3.0 → "11.0 eV {I30}" (3.0*10=30)
    """
    # Format wg value (ALWAYS 1 decimal place)
    if wg == int(wg):
        wg_str = f"{int(wg)}.0"
    else:
        wg_str = f"{wg:.1f}".rstrip('0').rstrip('.')
        if '.' not in wg_str:
            wg_str += ".0"
    
    # Calculate {In} integer representation
    # Since wg is ALWAYS formatted with 1 decimal, scale factor is ALWAYS 10
    uncertainty_int = round(dwg * 10)
    
    return f"|w|g={wg_str} eV {{I{uncertainty_int}}} (1972Hu10)"

def process_file(input_file, output_file):
    """Process ENSDF file and update wg/dwg comments"""
    
    # Create lookup dictionary: (Exi, Ep) -> (wg, dwg)
    wg_lookup = {}
    for exi, ep, _, wg, dwg in DATA_TABLE:
        # Round Exi to 1 decimal for matching
        exi_key = round(exi, 1)
        # Ep can be integer or float
        ep_key = ep if ep == int(ep) else ep
        wg_lookup[(exi_key, ep_key)] = (wg, dwg)
    
    print(f"[INFO] Created lookup table with {len(wg_lookup)} entries")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    modified_lines = []
    update_count = 0
    current_exi = None
    current_ep = None
    
    for i, line in enumerate(lines, 1):
        # Check if this is an L-record (level)
        if len(line) >= 8 and line[7] == 'L':
            # Extract Exi (energy) from columns 10-19
            exi_str = line[9:19].strip()
            if exi_str:
                try:
                    current_exi = round(float(exi_str), 1)
                except ValueError:
                    current_exi = None
        
        # Check if this is an L-record with S field (Ep in columns 65-74)
        if len(line) >= 74 and line[7] == 'L':
            ep_str = line[64:74].strip()
            if ep_str:
                try:
                    ep_float = float(ep_str)
                    current_ep = ep_float if ep_float != int(ep_float) else int(ep_float)
                except ValueError:
                    current_ep = None
        
        # Check if this is a cL comment with wg value (columns 7-9 contain "cL ")
        if len(line) >= 10 and line[7:10] == 'cL ' and '|w|g=' in line:
            # Try to update this comment
            if current_exi is not None and current_ep is not None:
                key = (current_exi, current_ep)
                
                # Debug output for first 5 matches
                if update_count < 5:
                    print(f"[DEBUG] Line {i}: key={key}, in_lookup={key in wg_lookup}")
                
                if key in wg_lookup:
                    wg, dwg = wg_lookup[key]
                    new_comment = format_wg_comment(wg, dwg)
                    
                    # Replace the wg/dwg portion of the comment
                    # Pattern: "|w|g=X.X eV {I...} (1972Hu10)" - note decimals in {I} are WRONG!
                    old_pattern = r'\|w\|g=[0-9.]+\s+eV\s+\{I[0-9.]+\}\s+\(1972Hu10\)'
                    if re.search(old_pattern, line):
                        new_line = re.sub(old_pattern, new_comment, line)
                        if new_line != line:
                            update_count += 1
                            print(f"[UPDATE {update_count}] Line {i}: Exi={current_exi}, Ep={current_ep}")
                            print(f"  OLD: {line.rstrip()}")
                            print(f"  NEW: {new_line.rstrip()}")
                            modified_lines.append(new_line)
                        else:
                            modified_lines.append(line)
                    else:
                        modified_lines.append(line)
                else:
                    modified_lines.append(line)
            else:
                modified_lines.append(line)
        else:
            modified_lines.append(line)
    
    # Write updated file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(modified_lines)
    
    print(f"\n[SUMMARY]")
    print(f"  Total updates: {update_count}")
    print(f"  Output written to: {output_file}")
    
    return update_count

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python fix_wg_comments_corrected.py <input_file> [output_file]")
        print("Example: python fix_wg_comments_corrected.py 1972HU10.ens 1972HU10_fixed.ens")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else input_file.replace('.ens', '_fixed.ens')
    
    print(f"[START] Fixing wg/dwg comments with CORRECT {{In}} notation")
    print(f"  Input:  {input_file}")
    print(f"  Output: {output_file}")
    print()
    
    count = process_file(input_file, output_file)
    
    if count > 0:
        print(f"\n[SUCCESS] Updated {count} wg/dwg comments with correct {{In}} notation")
        print(f"[CRITICAL] All uncertainties now use INTEGER format ({{I11}}, not {{I1.1}})")
    else:
        print(f"\n[WARNING] No updates made - please check input file")
