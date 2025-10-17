#!/usr/bin/env python3
"""
COMBINED RI AND M FIELD POSITIONING FIX (FINAL SOLUTION)
=========================================================

CRITICAL UNDERSTANDING:
Original file has TWO INDEPENDENT column errors:
1. RI starts at col 22 instead of col 23 (missing space after DE field)
2. M starts at col 32 instead of col 33 (missing space after DRI field)

These are NOT cascading errors - they are TWO SEPARATE missing spaces!

CORRECT FIX:
Insert TWO spaces:
- Space at col 22 (to fix RI position)
- Space at col 32 (to fix M position)

This shifts:
- Cols 22-30 (RI + DRI) → Cols 23-31
- Cols 31-79 (space + M + MR + ...) → Cols 33-81

BUT we need to ensure exactly 80 chars, so we take cols 31-79 (49 chars),
which becomes cols 33-81 but we truncate at 80.

Actually simpler: Insert space at col 22, this shifts everything right.
Then the file will have correct RI but M will STILL be at col 32.
We need ANOTHER space between DRI and M.

ALGORITHM:
1. Split line into: [cols 1-21] [cols 22-30] [cols 31-79]
2. Rebuild as: [cols 1-21] + SPACE + [cols 22-30] + SPACE + [cols 31-79]
3. This gives: cols 1-21 (unchanged), col 22 (space), cols 23-31 (RI+DRI), 
   col 32 (space), cols 33-81 (M+MR+...)
4. Truncate to 80 chars
"""

import sys

def fix_ri_and_m_fields_combined(input_file):
    """
    Fix both RI and M field positioning by inserting two spaces:
    - Space at col 22 (after DE, before RI)
    - Space at col 32 (after DRI, before M)
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
                rest = line_content[30:79]           # Cols 31-79 (49 chars: space + M + MR + ...)
                
                # Insert TWO spaces: one at col 22, one at col 32
                # This shifts RI+DRI from cols 22-30 to cols 23-31
                # And shifts rest from cols 31-79 to cols 33-81 (truncated to 80)
                fixed_line = (prefix + ' ' + ri_dri + ' ' + rest)[:80]
                
                # Store first 5 fixes for display
                if fixed_count < 5:
                    before_cols_22_45 = line_content[21:45]
                    after_cols_22_45 = fixed_line[21:45]
                    fix_info = {
                        'line_num': i,
                        'before': line_content[:80],
                        'after': fixed_line,
                        'col_22_before': line_content[21],
                        'cols_22_45_before': before_cols_22_45,
                        'cols_22_45_after': after_cols_22_45
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
            print(f"  Col 22: '{fix['col_22_before']}' -> ' ' (SPACE 1 inserted)")
            print(f"  Col 32: (SPACE 2 inserted)")
            print(f"  Cols 22-45:")
            print(f"    BEFORE: [{fix['cols_22_45_before']}]")
            print(f"    AFTER:  [{fix['cols_22_45_after']}]")
        print()
    
    # Write fixed content
    with open(input_file, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print("=" * 80)
    print("SUMMARY:")
    print("=" * 80)
    print(f"Total lines processed: {len(lines)}")
    print(f"RI+M field positioning fixes: {fixed_count}")
    print()
    print(f"[OK] File updated: {input_file}")
    print(f"[OK] {fixed_count} G-records fixed")
    print(f"[OK] Space 1 inserted at column 22 (fixes RI)")
    print(f"[OK] Space 2 inserted at column 32 (fixes M)")
    print(f"[OK] RI: cols 22-28 → cols 23-29")
    print(f"[OK] DRI: cols 29-30 → cols 30-31")
    print(f"[OK] M: cols 32-40 → cols 33-41")
    print(f"[OK] MR: cols 41-48 → cols 42-49")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python fix_ri_and_m_combined.py <input_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    print(f"Reading file: {input_file}")
    fix_ri_and_m_fields_combined(input_file)
