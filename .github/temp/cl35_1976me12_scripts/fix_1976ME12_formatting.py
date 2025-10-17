#!/usr/bin/env python3
"""
Fix 1976ME12.ens file formatting issues:
1. Remove ALL gamma energy uncertainties (DE field columns 20-21) from G-records
2. Fix T field LEFT-JUSTIFICATION in L-records (must start at column 40)

Author: Nuclear Data Expert AI
Date: 2025-10-02
"""

import sys
import re

def fix_g_record_remove_de(line):
    """
    Remove DE field (columns 20-21) from G-record.
    
    G-record format:
    Columns 1-9: NUCID + CONT + BLANK + "G" + BLANK
    Columns 10-19: Gamma energy (LEFT-JUSTIFIED)
    Columns 20-21: DE uncertainty (TO BE REMOVED - REPLACED WITH SPACES)
    Column 22: SPACE (readability space)
    Columns 23-29: RI relative intensity (LEFT-JUSTIFIED)
    Columns 30-31: DRI uncertainty (LEFT-JUSTIFIED, includes LT/GT markers)
    Columns 32-80: Rest of G-record fields
    
    CRITICAL: DO NOT SHIFT columns after 22! RI and DRI must stay in same positions (23-29, 30-31).
    
    Strategy: Replace columns 20-21 with TWO SPACES, keep everything else unchanged.
    """
    if len(line) != 80:
        print(f"[WARNING] G-record not 80 chars (len={len(line)}): {repr(line)}")
        return line
    
    # Extract parts
    prefix = line[0:19]     # Columns 1-19 (NUCID through E field)
    # DE field at columns 20-21 will be REPLACED with spaces
    rest = line[21:80]      # Columns 22-80 (everything after DE - UNCHANGED)
    
    # Construct new line: prefix + two spaces + rest
    new_line = prefix + "  " + rest
    
    if len(new_line) != 80:
        print(f"[ERROR] Fixed G-record not 80 chars (len={len(new_line)}): {repr(new_line)}")
        return line
    
    return new_line

def fix_l_record_t_field_justification(line):
    """
    Fix T field LEFT-JUSTIFICATION in L-record.
    
    L-record format:
    Columns 1-39: NUCID through J field
    Columns 40-49: T field (half-life with units) - MUST BE LEFT-JUSTIFIED
    Columns 50-55: DT field (half-life uncertainty)
    Columns 56-80: L, S, DS, C fields
    
    Current problem: T field has leading spaces like "                   145 FS    30"
    Should be: "145 FS    30" starting at column 40
    
    SPECIAL CASE: "GT 1000 FS" is 11 characters - must compress to fit in 10-char T field
    Solution: Remove space between value and unit: "GT 1000FS" (10 chars exactly)
    
    Strategy: Extract T+DT fields (columns 40-55), strip leading spaces from T field,
    handle unit spacing, reformat with proper spacing, reconstruct line.
    """
    if len(line) != 80:
        print(f"[WARNING] L-record not 80 chars (len={len(line)}): {repr(line)}")
        return line
    
    # Extract parts
    prefix = line[0:39]       # Columns 1-39
    t_dt_fields = line[39:55] # Columns 40-55 (T + DT fields)
    suffix = line[55:80]      # Columns 56-80
    
    # Parse T and DT fields
    # T field is columns 40-49 (10 chars), DT field is columns 50-55 (6 chars)
    t_field_raw = t_dt_fields[0:10]  # Columns 40-49
    dt_field_raw = t_dt_fields[10:16]    # Columns 50-55
    
    # Combine T and DT to get full lifetime string
    combined = (t_field_raw + dt_field_raw).strip()
    
    # Check if lifetime data exists
    if combined == "":
        # No lifetime data, leave as-is
        return line
    
    # Fix specific known cases
    # Case 1: "GT 1000 FS" - compress to "GT 1000FS" (remove space before FS)
    if "GT 1000 F" in t_field_raw and dt_field_raw.strip().startswith("S"):
        t_value = "GT 1000FS"
        dt_value = dt_field_raw.strip()[1:].strip()  # Remove leading 'S'
        t_field_fixed = t_value.ljust(10)
        dt_field_fixed = dt_value.ljust(6)
    # Case 2: "LT X FS" - compress if needed
    elif combined.startswith("LT") and " FS" in combined:
        # Remove extra spaces to fit in T field
        parts = combined.split()
        if len(parts) >= 3:  # LT, value, FS, [uncertainty]
            t_value = f"LT {parts[1]}FS"  # e.g., "LT 6FS" or "LT 7FS"
            dt_value = " ".join(parts[3:]) if len(parts) > 3 else ""
            t_field_fixed = t_value.ljust(10)
            dt_field_fixed = dt_value.ljust(6)
        else:
            # Fallback
            t_field_fixed = combined[0:10].ljust(10)
            dt_field_fixed = combined[10:16].ljust(6) if len(combined) > 10 else " ".ljust(6)
    # Case 3: Normal "VALUE UNIT UNCERTAINTY" format
    else:
        # Split into parts
        parts = combined.split()
        if len(parts) >= 3:
            # Format: VALUE UNIT UNCERTAINTY
            # e.g., "145 FS 30" or "530 FS 90"
            value_unit = f"{parts[0]} {parts[1]}"  # e.g., "145 FS"
            uncertainty = parts[2]
            t_field_fixed = value_unit.ljust(10)
            dt_field_fixed = uncertainty.ljust(6)
        elif len(parts) == 2:
            # Format: VALUE UNIT (no uncertainty)
            value_unit = f"{parts[0]} {parts[1]}"
            t_field_fixed = value_unit.ljust(10)
            dt_field_fixed = "      "
        else:
            # Single value or unknown format - use as-is
            t_field_fixed = combined[0:10].ljust(10)
            dt_field_fixed = combined[10:16].ljust(6) if len(combined) > 10 else "      "
    
    # Reconstruct line
    new_line = prefix + t_field_fixed + dt_field_fixed + suffix
    
    if len(new_line) != 80:
        print(f"[ERROR] Fixed L-record not 80 chars (len={len(new_line)}): {repr(new_line)}")
        return line
    
    return new_line

def main():
    input_file = "A35/Cl35/temp/1976ME12.ens"
    output_file = "A35/Cl35/temp/1976ME12_FIXED.ens"
    
    print(f"Reading: {input_file}")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    fixed_lines = []
    g_count = 0
    l_count = 0
    
    for i, line in enumerate(lines, 1):
        # Remove newline for processing
        line = line.rstrip('\n\r')
        
        # Detect record type
        if len(line) >= 9:
            record_type = line[7:8]
            
            if record_type == 'G':
                # Fix G-record: remove DE field
                fixed_line = fix_g_record_remove_de(line)
                g_count += 1
            elif record_type == 'L':
                # Fix L-record: LEFT-JUSTIFY T field
                fixed_line = fix_l_record_t_field_justification(line)
                l_count += 1
            else:
                # Other records: leave as-is
                fixed_line = line
        else:
            # Short lines: leave as-is
            fixed_line = line
        
        # Add back newline
        fixed_lines.append(fixed_line + '\n')
    
    print(f"Fixed {g_count} G-records (removed DE field)")
    print(f"Fixed {l_count} L-records (LEFT-JUSTIFIED T field)")
    
    print(f"Writing: {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(fixed_lines)
    
    print("[OK] File processing complete!")
    print(f"[INFO] Please review {output_file} before replacing original")

if __name__ == "__main__":
    main()
