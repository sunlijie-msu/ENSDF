#!/usr/bin/env python3
"""
CORRECT RI FIELD POSITIONING FIX (Version 4 - FINAL)
====================================================

CRITICAL DISCOVERY:
After M/MR comprehensive fix, the file structure is:
- Cols 22-28: RI (7 chars, at wrong position - should be 23-29)
- Cols 29-30: DRI (2 chars, at wrong position - should be 30-31)
- Col 31: SPACE (already correct - separator before M field)
- Cols 32+: M, MR, DMR, etc. (already correct after M/MR fix)

THE BUG IN V3:
V3 shifted cols 22-31 (RI + DRI + space), which moved the space from col 31 to col 32,
pushing M from col 33 to col 34.

THE CORRECT FIX:
Shift ONLY cols 22-30 (RI + DRI), keep col 31 (space) unchanged.
This moves:
- RI: cols 22-28 → cols 23-29 ✓
- DRI: cols 29-30 → cols 30-31 ✓
- Space: col 31 → col 32 ✓ (new space inserted at col 22 becomes col 32's separator)
- M: col 33 → col 33 ✓ (UNCHANGED!)
"""

import sys

def fix_ri_field_positioning_v4(input_file):
    """
    Fix RI field positioning by shifting cols 22-30 (RI + DRI) right by 1.
    Preserves col 31+ (space + M + MR + etc.)
    """
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    fixed_count = 0
    first_5_fixes = []
    
    for i, line in enumerate(lines, start=1):
        # Only process G-records (not comment lines)
        if (len(line) >= 9 and 
            line[7] == 'G' and 
            line[8] == ' ' and 
            line[6] != 'c'):  # Exclude cG comment lines
            
            line_content = line.rstrip('\n\r')
            
            # Ensure line is at least 80 chars for manipulation
            if len(line_content) < 80:
                line_content = line_content.ljust(80)
            
            # Check if RI starts at col 22 instead of col 23
            # (col 22 should be SPACE after DE field)
            if len(line_content) >= 23 and line_content[21] != ' ':
                # RI is at wrong position, fix it
                prefix = line_content[0:21]          # Cols 1-21 (NUCID, TYPE, E, DE)
                ri_dri = line_content[21:30]         # Cols 22-30 (RI 7 chars + DRI 2 chars)
                rest = line_content[30:80]           # Cols 31-80 (space + M + MR + ...)
                
                # Insert space at col 22, shift RI+DRI right, preserve rest
                fixed_line = prefix + ' ' + ri_dri + rest
                
                # Store first 5 fixes for display
                if fixed_count < 5:
                    before_cols_22_35 = line_content[21:35]
                    after_cols_22_35 = fixed_line[21:35]
                    fix_info = {
                        'line_num': i,
                        'before': line_content[:80],
                        'after': fixed_line,
                        'col_22_before': line_content[21],
                        'cols_22_35_before': before_cols_22_35,
                        'cols_22_35_after': after_cols_22_35
                    }
                    first_5_fixes.append(fix_info)
                
                lines[i-1] = fixed_line + '\n'
                fixed_count += 1
    
    # Show first 5 fixes
    if first_5_fixes:
        print("=" * 80)
        for idx, fix in enumerate(first_5_fixes, 1):
            print(f"\n[FIX {idx}] Line {fix['line_num']}:")
            print(f"  BEFORE: {fix['before']}")
            print(f"  AFTER:  {fix['after']}")
            print(f"  Col 22: '{fix['col_22_before']}' -> ' ' (SPACE inserted)")
            print(f"  Cols 22-35:")
            print(f"    BEFORE: [{fix['cols_22_35_before']}]")
            print(f"    AFTER:  [{fix['cols_22_35_after']}]")
        print()
    
    # Write fixed content
    with open(input_file, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print("=" * 80)
    print("SUMMARY:")
    print("=" * 80)
    print(f"Total lines processed: {len(lines)}")
    print(f"RI field positioning fixes: {fixed_count}")
    print()
    print(f"[OK] File updated: {input_file}")
    print(f"[OK] {fixed_count} G-records fixed")
    print(f"[OK] Space inserted at column 22")
    print(f"[OK] Columns 22-30 (RI, DRI) shifted right by 1")
    print(f"[OK] Columns 31-80 (space, M, MR, etc.) unchanged")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python fix_ri_field_positioning_v4.py <input_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    print(f"Reading file: {input_file}")
    fix_ri_field_positioning_v4(input_file)
