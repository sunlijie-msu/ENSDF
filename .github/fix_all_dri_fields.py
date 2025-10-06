#!/usr/bin/env python3
"""
CAREFUL DRI field fix - handles three cases:
1. Single-digit uncertainties with leading space → LEFT-JUSTIFY
2. Two-character markers split (LT, GT, LE, GE, etc.) → combine and LEFT-JUSTIFY
3. Two-digit uncertainties split (" 1" + "0" = "10") → combine properly

CRITICAL: Must preserve data integrity!
"""

import sys
import os

def fix_dri_fields_careful(filename):
    """Fix ALL DRI field positioning errors carefully"""
    
    if not os.path.exists(filename):
        print(f"ERROR: File '{filename}' not found!")
        return False
    
    # Create backup
    backup_file = filename + '.backup_before_complete_dri_fix'
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
        
        # Only process G-records (need at least 31 chars to have DRI field)
        if len(original_line) < 31:
            continue
        if not (len(original_line) >= 8 and original_line[7] == 'G' and original_line[5] == ' ' and original_line[6] == ' '):
            continue
        
        # Work with padded line
        fixed_line = original_line.ljust(80, ' ')
        
        # Extract DRI field (cols 30-31, 0-based 29:31)
        dri_field = fixed_line[29:31]
        
        # Skip if DRI is empty or already left-justified
        if not dri_field.strip() or dri_field[0] != ' ':
            continue
        
        # DRI has content and starts with space - need to fix
        dri_value = dri_field[1]  # Character at position 30 (second char of DRI field)
        col32_char = fixed_line[31]  # Character at column 32
        
        # Determine what we have:
        # Case 1: DRI " L" + col32 "T" → combine to "LT"
        # Case 2: DRI " 1" + col32 "0" → combine to "10" (two-digit uncertainty)
        # Case 3: DRI " 1" + col32 " " → single digit "1", left-justify to "1 "
        
        if col32_char.isalpha() and dri_value.isalpha():
            # Two-character marker split across boundary (LT, GT, LE, GE, etc.)
            full_dri = dri_value + col32_char
            fixed_line = fixed_line[:29] + full_dri + ' ' + fixed_line[32:]
            g_records_fixed += 1
            
            if g_records_fixed <= 30:
                print(f"Line {line_num}: DRI marker '{full_dri}' split → combined in cols 30-31")
                print(f"  BEFORE: {original_line[:50]}")
                print(f"  AFTER:  {fixed_line[:50].rstrip()}")
                print()
        
        elif col32_char.isdigit() and dri_value.isdigit():
            # Two-digit uncertainty split (10, 15, 20, etc.)
            full_dri = dri_value + col32_char
            fixed_line = fixed_line[:29] + full_dri + ' ' + fixed_line[32:]
            g_records_fixed += 1
            
            if g_records_fixed <= 30:
                print(f"Line {line_num}: DRI uncertainty '{full_dri}' split → combined in cols 30-31")
                print(f"  BEFORE: {original_line[:50]}")
                print(f"  AFTER:  {fixed_line[:50].rstrip()}")
                print()
        
        else:
            # Single-digit or single-character value - just left-justify
            fixed_line = fixed_line[:29] + dri_value + ' ' + fixed_line[31:]
            g_records_fixed += 1
            
            if g_records_fixed <= 30:
                print(f"Line {line_num}: DRI '{dri_value}' left-justified to col 30")
                print(f"  BEFORE: {original_line[:50]}")
                print(f"  AFTER:  {fixed_line[:50].rstrip()}")
                print()
        
        lines[line_num - 1] = fixed_line.rstrip() + '\n'
    
    if g_records_fixed > 30:
        print(f"... and {g_records_fixed - 30} more DRI fields fixed (showing first 30)")
        print()
    
    # Write fixed file
    with open(filename, 'w') as f:
        f.writelines(lines)
    
    print(f"\nSUMMARY:")
    print(f"  Total DRI fields fixed: {g_records_fixed}")
    print(f"  File updated: {filename}")
    print(f"  Backup saved: {backup_file}")
    
    return True

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python fix_all_dri_fields.py <ensdf_file>")
        sys.exit(1)
    
    filename = sys.argv[1]
    success = fix_dri_fields_careful(filename)
    sys.exit(0 if success else 1)
