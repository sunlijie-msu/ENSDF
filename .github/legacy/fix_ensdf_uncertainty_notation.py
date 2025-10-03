#!/usr/bin/env python3
"""
Fix {In} notation in 1972HU10.ens wg/dwg comments - IN-PLACE CONVERSION

CRITICAL: This script converts EXISTING {I} notation from WRONG decimal format to CORRECT integer format
- Does NOT use lookup table
- Parses current wg/dwg values from file
- Converts {I0.1} → {I1}, {I1.1} → {I11}, {I2.7} → {I27}, etc.

ENSDF {In} Notation Rule:
- For values with 1 decimal place: dwg * 10 = integer uncertainty
- Example: wg=3.6, {I1.1} → {I11} (because 1.1 * 10 = 11)
"""

import re
import sys

def convert_uncertainty_notation(old_uncertainty_str):
    """
    Convert uncertainty from decimal format to integer format
    
    Args:
        old_uncertainty_str: String like "0.1", "1.1", "2.7", "3", etc.
    
    Returns:
        Integer string like "1", "11", "27", "30", etc.
    """
    try:
        # Parse the old uncertainty value
        old_unc = float(old_uncertainty_str)
        
        # Scale by 10 (since wg is always formatted with 1 decimal)
        new_unc_int = round(old_unc * 10)
        
        return str(new_unc_int)
    except:
        # If parsing fails, return original
        return old_uncertainty_str

def process_file(input_file, output_file):
    """Process file and convert all {I} notation from decimal to integer format"""
    
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    modified_lines = []
    update_count = 0
    
    # Pattern to match: |w|g=X.X eV {I...} (1972Hu10)
    # Capture groups: (wg_value) and (uncertainty_value)
    pattern = r'(\|w\|g=)([0-9.]+)(\s+eV\s+)\{I([0-9.]+)\}(\s+\(1972Hu10\))'
    
    for i, line in enumerate(lines, 1):
        # Check if this line has wg comment
        if '|w|g=' in line and '{I' in line:
            match = re.search(pattern, line)
            if match:
                prefix = match.group(1)      # "|w|g="
                wg_value = match.group(2)    # e.g., "3.6"
                middle = match.group(3)      # " eV "
                old_unc = match.group(4)     # e.g., "1.1" (WRONG - decimal)
                suffix = match.group(5)      # " (1972Hu10)"
                
                # Convert uncertainty to integer format
                new_unc = convert_uncertainty_notation(old_unc)
                
                # Only update if conversion changed the value
                if new_unc != old_unc:
                    # Build new comment
                    new_comment = f"{prefix}{wg_value}{middle}{{I{new_unc}}}{suffix}"
                    
                    # Replace in line
                    new_line = re.sub(pattern, new_comment, line)
                    
                    update_count += 1
                    print(f"[UPDATE {update_count}] Line {i}:")
                    print(f"  wg={wg_value} eV, old_unc={{I{old_unc}}} → new_unc={{I{new_unc}}}")
                    print(f"  OLD: {line.rstrip()}")
                    print(f"  NEW: {new_line.rstrip()}")
                    
                    modified_lines.append(new_line)
                else:
                    # No change needed (already integer format)
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
        print("Usage: python fix_ensdf_uncertainty_notation.py <input_file> [output_file]")
        print("Example: python fix_ensdf_uncertainty_notation.py 1972HU10.ens 1972HU10_FIXED.ens")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else input_file.replace('.ens', '_FIXED.ens')
    
    print(f"[START] Converting {{I}} notation from decimal to integer format")
    print(f"  Input:  {input_file}")
    print(f"  Output: {output_file}")
    print()
    
    count = process_file(input_file, output_file)
    
    if count > 0:
        print(f"\n[SUCCESS] Converted {count} uncertainties from {{I0.1}} to {{I1}} format")
        print(f"[CRITICAL] ALL {{In}} notation now uses INTEGERS ({{I11}}, not {{I1.1}})")
        print(f"\n[NEXT STEP] Copy {output_file} to 1972HU10.ens if verification passes")
    else:
        print(f"\n[INFO] No decimal {{I}} notation found - file may already be correct")
