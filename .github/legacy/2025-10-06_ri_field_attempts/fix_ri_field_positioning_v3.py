"""
Fix RI field positioning in ENSDF G-records (FINAL CORRECT VERSION).

PROBLEM: RI values starting at column 22 instead of column 23
CAUSE: Missing mandatory space at column 22
EFFECT: Fields shifted left: RI, DRI, and the space before M field
SOLUTION: Insert space at column 22, shift ONLY columns 22-31 to the right

This preserves M, MR, DMR, CC, DCC, TI, DTI, C, Q fields at their correct positions.
"""

import sys

def fix_ri_positioning(filepath):
    """Fix RI field positioning by inserting space at col 22 and shifting cols 22-31 right."""
    
    print(f"Reading file: {filepath}")
    print("=" * 80)
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"[ERROR] File not found: {filepath}")
        return False
    
    fixed_count = 0
    fixed_lines = []
    
    for line_num, line in enumerate(lines, start=1):
        original_line = line
        line_content = line.rstrip('\n')
        
        # Skip lines too short to be G-records
        if len(line_content) < 32:
            fixed_lines.append(original_line)
            continue
        
        # CRITICAL: ONLY fix G-records (NOT cG comment lines)
        # Column 7 (index 6) must NOT be 'c' (excludes cG, cL, cE, cB)
        # Column 8 (index 7) must be 'G'
        # Column 9 (index 8) must be ' '
        if not (len(line_content) >= 9 and 
                line_content[7] == 'G' and 
                line_content[8] == ' ' and 
                line_content[6] != 'c'):
            fixed_lines.append(original_line)
            continue
        
        # Pad to exactly 80 characters if needed
        line_content = line_content.ljust(80)
        
        # Check if column 22 is NOT a space (this is the error we're fixing)
        if line_content[21] != ' ':
            # CORRECT APPROACH:
            # Columns 1-21: unchanged (NUCID, CONT, TYPE, E, DE)
            # Column 22: INSERT SPACE (the fix!)
            # Columns 22-31: shift RIGHT by 1 (becomes columns 23-32)
            #   This includes: RI (22-28 -> 23-29), DRI (29-30 -> 30-31), SPACE (31 -> 32)
            # Columns 32-79: unchanged (M, MR, DMR, CC, DCC, TI, DTI, C, Q)
            
            prefix = line_content[0:21]          # Cols 1-21 (unchanged)
            ri_dri_space = line_content[21:31]   # Cols 22-31 (to be shifted right)
            rest = line_content[31:80]           # Cols 32-80 (unchanged)
            
            # Build corrected line
            fixed_line = prefix + ' ' + ri_dri_space + rest
            
            # Ensure exactly 80 characters
            fixed_line = fixed_line[:80].ljust(80)
            
            # Show fix details for first 5 fixes
            if fixed_count < 5:
                print(f"\n[FIX {fixed_count + 1}] Line {line_num}:")
                print(f"  BEFORE: {line_content[:50]}")
                print(f"  AFTER:  {fixed_line[:50]}")
                print(f"  Col 22: '{line_content[21]}' -> ' ' (SPACE inserted)")
                print(f"  Cols 22-35:")
                print(f"    BEFORE: [{line_content[21:35]}]")
                print(f"    AFTER:  [{fixed_line[21:35]}]")
            
            fixed_lines.append(fixed_line + '\n')
            fixed_count += 1
        else:
            # Column 22 is already a space - no fix needed
            fixed_lines.append(original_line)
    
    print(f"\n{'=' * 80}")
    print(f"SUMMARY:")
    print(f"{'=' * 80}")
    print(f"Total lines processed: {len(lines)}")
    print(f"RI field positioning fixes: {fixed_count}")
    
    if fixed_count > 0:
        # Write fixed content back to file
        with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
            f.writelines(fixed_lines)
        print(f"\n[OK] File updated: {filepath}")
        print(f"[OK] {fixed_count} G-records fixed")
        print(f"[OK] Space inserted at column 22")
        print(f"[OK] Columns 22-31 (RI, DRI, space) shifted right by 1")
        print(f"[OK] Columns 32-80 (M, MR, etc.) remain unchanged")
        return True
    else:
        print("\n[OK] No RI field positioning errors found")
        return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fix_ri_field_positioning_v3.py <ensdf_file>")
        sys.exit(1)
    
    filepath = sys.argv[1]
    success = fix_ri_positioning(filepath)
    sys.exit(0 if success else 1)
