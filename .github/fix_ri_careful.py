#!/usr/bin/env python3
"""
CAREFUL ENSDF G-record RI field positioning fix
Only fixes RI values shifted LEFT by 1 column (column 22 contains digit instead of space)

CRITICAL: Preserves all other field values exactly, including multi-digit uncertainties
"""

import sys
import os

def fix_ri_positioning_careful(filename):
    """Fix RI field positioning errors where column 22 contains digit"""
    
    if not os.path.exists(filename):
        print(f"ERROR: File '{filename}' not found!")
        return False
    
    # Create backup
    backup_file = filename + '.backup_before_careful_ri_fix'
    with open(filename, 'r') as f:
        backup_content = f.read()
    with open(backup_file, 'w') as f:
        f.write(backup_content)
    print(f"Backup created: {backup_file}")
    print()
    
    # Read all lines
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    total_lines = len(lines)
    g_records_fixed = 0
    
    print(f"Processing {filename}...")
    print(f"Total lines: {total_lines}")
    print()
    
    for line_num, line in enumerate(lines, 1):
        original_line = line.rstrip('\n\r')
        
        # Only process G-records
        if len(original_line) < 32:
            continue
        if not (original_line[7] == 'G' and original_line[5] == ' ' and original_line[6] == ' '):
            continue
        
        # Check if column 22 (0-based index 21) contains a digit
        col22_char = original_line[21] if len(original_line) > 21 else ' '
        
        if col22_char.isdigit():
            # RI is shifted left - column 22 has digit instead of space
            # FIX: Insert space at column 22, which shifts everything right by 1
            
            # Split line: prefix (cols 1-21) + col22 + rest
            prefix = original_line[:21]  # Columns 1-21 (NUCID through DE)
            rest_of_line = original_line[21:]  # Column 22 onwards
            
            # Insert space at column 22
            fixed_line = prefix + ' ' + rest_of_line
            
            # Truncate to 80 characters if needed (or keep original length)
            if len(original_line) >= 80:
                fixed_line = fixed_line[:80]
            
            lines[line_num - 1] = fixed_line.rstrip() + '\n'
            g_records_fixed += 1
            
            if g_records_fixed <= 20:  # Show first 20 fixes
                print(f"Line {line_num}: RI shifted left (col 22 = '{col22_char}')")
                print(f"  BEFORE: {original_line}")
                print(f"  AFTER:  {fixed_line.rstrip()}")
                
                # Verify the fix
                new_col22 = fixed_line[21] if len(fixed_line) > 21 else '?'
                new_ri_field = fixed_line[22:29] if len(fixed_line) > 22 else '?'
                print(f"  VERIFY: Col 22 = '{new_col22}', RI field (23-29) = [{new_ri_field}]")
                print()
    
    if g_records_fixed > 20:
        print(f"... and {g_records_fixed - 20} more G-records fixed (showing first 20)")
        print()
    
    # Write fixed file
    with open(filename, 'w') as f:
        f.writelines(lines)
    
    print(f"\nSUMMARY:")
    print(f"  Total G-records with RI shifted left: {g_records_fixed}")
    print(f"  File updated: {filename}")
    print(f"  Backup saved: {backup_file}")
    
    return True

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python fix_ri_careful.py <ensdf_file>")
        sys.exit(1)
    
    filename = sys.argv[1]
    success = fix_ri_positioning_careful(filename)
    sys.exit(0 if success else 1)
