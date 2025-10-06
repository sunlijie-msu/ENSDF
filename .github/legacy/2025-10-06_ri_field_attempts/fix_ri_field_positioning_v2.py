"""
Fix RI field positioning in ENSDF G-records (CORRECTED VERSION).

PROBLEM: RI values starting at column 22 instead of column 23 (missing mandatory space at col 22)
When RI is shifted left by 1 column, ALL subsequent fields are also shifted left by 1.

SOLUTION: Insert space at column 22, shift all fields after DE to the right by 1 position

CRITICAL SAFETY RULES:
1. ONLY fix G-records (column 8 = 'G')
2. EXCLUDE comment lines (column 7 = 'c')
3. Insert space at column 22
4. Shift columns 22-79 to the right by 1 position (becoming cols 23-80)
5. This preserves ALL field values exactly as they were
"""

import sys

def fix_ri_positioning(filepath):
    """Fix RI field positioning in G-records by inserting space at col 22."""
    
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
        # Check: column 7 (index 6) must NOT be 'c', column 8 must be 'G', column 9 must be space
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
            # SIMPLE AND SAFE APPROACH:
            # Take cols 1-21 (NUCID through DE field)
            # Insert a space at col 22
            # Take cols 22-79 and shift them to cols 23-80
            
            prefix = line_content[0:21]     # Cols 1-21 (everything before the error)
            shifted_content = line_content[21:79]  # Cols 22-79 (to be shifted right)
            
            # Build corrected line:
            # Cols 1-21: unchanged (NUCID, CONT, TYPE, E, DE)
            # Col 22: SPACE (inserted - this is the fix!)
            # Cols 23-80: shifted_content (RI, DRI, M, MR, DMR, CC, DCC, TI, DTI, C, Q)
            fixed_line = prefix + ' ' + shifted_content
            
            # Ensure exactly 80 characters
            fixed_line = fixed_line[:80].ljust(80)
            
            # Show fix details for first 5 fixes
            if fixed_count < 5:
                print(f"\n[FIX {fixed_count + 1}] Line {line_num}:")
                print(f"  BEFORE: {line_content[:70]}")
                print(f"  AFTER:  {fixed_line[:70]}")
                print(f"  Col 22 BEFORE: '{line_content[21]}' -> AFTER: '{fixed_line[21]}' (SPACE)")
                print(f"  Cols 22-30 BEFORE: [{line_content[21:30]}]")
                print(f"  Cols 22-30 AFTER:  [{fixed_line[21:30]}]")
            
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
        print(f"[OK] {fixed_count} G-records fixed (space inserted at col 22)")
        print(f"[OK] All fields after col 21 shifted right by 1 position")
        return True
    else:
        print("\n[OK] No RI field positioning errors found")
        return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fix_ri_field_positioning_v2.py <ensdf_file>")
        sys.exit(1)
    
    filepath = sys.argv[1]
    success = fix_ri_positioning(filepath)
    sys.exit(0 if success else 1)
