"""
Fix RI field positioning in ENSDF G-records.

PROBLEM: RI values starting at column 22 instead of column 23 (missing mandatory space at col 22)
SOLUTION: Insert space at column 22, LEFT-JUSTIFY RI at column 23, preserve all other fields

CRITICAL SAFETY RULES:
1. ONLY fix G-records (column 8 = 'G')
2. EXCLUDE comment lines (column 6 = 'c')
3. Insert space at column 22
4. LEFT-JUSTIFY RI at column 23
5. Preserve all other fields at correct positions
"""

import sys

def fix_ri_positioning(filepath):
    """Fix RI field positioning in G-records."""
    
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
    errors_found = []
    
    for line_num, line in enumerate(lines, start=1):
        original_line = line
        line_content = line.rstrip('\n')
        
        # Skip lines too short to be G-records
        if len(line_content) < 32:
            fixed_lines.append(original_line)
            continue
        
        # CRITICAL: ONLY fix G-records (NOT cG comment lines)
        # Check: column 7 must be space (not 'c'), column 8 must be 'G', column 9 must be space
        # Column 7 (index 6) has 'c' for comment lines (cG, cL, cE, cB)
        # Column 7 (index 6) has ' ' for data records (G, L, E, B)
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
            # Extract all fields from their CURRENT (wrong) positions
            nucid = line_content[0:5]      # Cols 1-5
            cont = line_content[5]          # Col 6
            blank1 = ' '                    # Col 7 (must be space)
            record_type = 'G'               # Col 8
            blank2 = ' '                    # Col 9 (must be space)
            e_field = line_content[9:19]   # Cols 10-19 (energy)
            de_field = line_content[19:21] # Cols 20-21 (energy uncertainty)
            
            # RI field is currently starting at col 22 (wrong) - extract it
            # We need to find where RI ends and DRI begins
            # RI should be in cols 23-29 (7 chars), DRI in cols 30-31 (2 chars)
            # Currently RI is at cols 22-28, DRI at cols 29-30
            
            # Extract RI from wrong position (cols 22-28, 7 chars)
            ri_wrong_pos = line_content[21:28].rstrip()  # Get RI, remove trailing spaces
            
            # Extract DRI from wrong position (cols 29-30, 2 chars)
            dri_wrong_pos = line_content[28:30]
            
            # Extract all remaining fields from their current positions
            # After RI/DRI, the rest should be at correct positions
            # M field at cols 33-41, MR at cols 42-49, etc.
            remaining_after_dri = line_content[31:]  # Everything after col 31
            
            # Build corrected line with RI at correct position
            # Col 22 = SPACE (mandatory separator)
            # Cols 23-29 = RI LEFT-JUSTIFIED
            # Cols 30-31 = DRI LEFT-JUSTIFIED
            
            fixed_line = (
                nucid +                        # Cols 1-5
                cont +                         # Col 6
                blank1 +                       # Col 7
                record_type +                  # Col 8
                blank2 +                       # Col 9
                e_field +                      # Cols 10-19
                de_field +                     # Cols 20-21
                ' ' +                          # Col 22 (MANDATORY SPACE - this is the fix!)
                ri_wrong_pos.ljust(7) +        # Cols 23-29 (RI LEFT-JUSTIFIED)
                dri_wrong_pos +                # Cols 30-31 (DRI)
                remaining_after_dri            # Cols 32-80
            )
            
            # Ensure exactly 80 characters
            fixed_line = fixed_line[:80].ljust(80)
            
            # Show fix details for first 5 fixes
            if fixed_count < 5:
                print(f"\n[FIX {fixed_count + 1}] Line {line_num}:")
                print(f"  BEFORE: {line_content[:60]}")
                print(f"  AFTER:  {fixed_line[:60]}")
                print(f"  RI='{ri_wrong_pos}' DRI='{dri_wrong_pos}'")
                print(f"  Col 22: '{line_content[21]}' -> ' ' (SPACE inserted)")
            
            fixed_lines.append(fixed_line + '\n')
            fixed_count += 1
            
            if fixed_count <= 10:
                errors_found.append({
                    'line_num': line_num,
                    'before': line_content[:50],
                    'after': fixed_line[:50]
                })
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
        print(f"[OK] {fixed_count} G-records fixed (RI field now at column 23)")
        return True
    else:
        print("\n[OK] No RI field positioning errors found")
        return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fix_ri_field_positioning.py <ensdf_file>")
        sys.exit(1)
    
    filepath = sys.argv[1]
    success = fix_ri_positioning(filepath)
    sys.exit(0 if success else 1)
