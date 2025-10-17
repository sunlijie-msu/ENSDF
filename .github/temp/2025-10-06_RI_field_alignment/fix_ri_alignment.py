#!/usr/bin/env python3
"""
Automated RI field alignment script for ENSDF G-records.
Fixes G-records where RI starts at column 22 instead of column 23.

SOLUTION: Insert space at column 22, remove trailing space (maintains 80 chars).
CRITICAL: Preserves DRI, M, MR, C, Q field positions.
"""

import sys

def fix_ri_alignment(input_file, output_file=None, dry_run=False):
    """
    Fix RI field alignment in G-records.
    
    Args:
        input_file: Path to ENSDF file
        output_file: Path for output (if None, overwrites input_file)
        dry_run: If True, only report changes without modifying file
    """
    if output_file is None:
        output_file = input_file
    
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    fixed_count = 0
    errors = []
    
    print("=" * 80)
    print("RI FIELD ALIGNMENT FIX - ENSDF G-RECORDS")
    print("=" * 80)
    print(f"Input file: {input_file}")
    print(f"Dry run: {dry_run}")
    print()
    
    for i, line in enumerate(lines):
        line_num = i + 1
        
        # Only process G-records (data records, not comments)
        if not line.startswith(' 35CL  G '):
            continue
        
        # Check if line is long enough
        if len(line) <= 22:
            continue
        
        col22 = line[21]  # Column 22 (0-indexed = 21)
        
        # If column 22 is already a space, skip
        if col22 == ' ':
            continue
        
        # Fix: Insert space at column 22, remove trailing space
        # Original: " 35CL  G EEEE.E    DE100    ..."
        # Fixed:    " 35CL  G EEEE.E    DE 100   ..."
        #                              ^  ^      ^ trailing space removed
        
        original_line = line
        
        # Insert space at position 21 (column 22)
        fixed_line = line[:21] + ' ' + line[21:]
        
        # Remove one character from the end to maintain 80-char length
        # First remove newline if present
        if fixed_line.endswith('\n'):
            fixed_line = fixed_line[:-1]  # Remove newline
        
        # Now ensure exactly 80 characters
        if len(fixed_line) > 80:
            fixed_line = fixed_line[:80]  # Trim to 80
        elif len(fixed_line) < 80:
            fixed_line = fixed_line.ljust(80)  # Pad to 80
        
        # Add newline back
        fixed_line = fixed_line + '\n'
        
        # Verify fix
        line_check = fixed_line.rstrip('\n')  # Remove ONLY newline, keep trailing spaces
        if len(line_check) != 80:
            errors.append(f"Line {line_num}: Fixed line length = {len(line_check)} (expected 80)")
            continue
        
        if fixed_line[21] != ' ':
            errors.append(f"Line {line_num}: Column 22 still not space after fix!")
            continue
        
        # Apply fix
        lines[i] = fixed_line
        fixed_count += 1
        
        # Show first 10 fixes
        if fixed_count <= 10:
            print(f"Line {line_num:4d}:")
            print(f"  OLD: {original_line.rstrip(chr(10))}")  # Remove only newline
            print(f"  NEW: {fixed_line.rstrip(chr(10))}")     # Remove only newline
            print()
    
    print("=" * 80)
    print(f"Total G-records fixed: {fixed_count}")
    if errors:
        print(f"Errors encountered: {len(errors)}")
        for err in errors[:5]:
            print(f"  {err}")
    print("=" * 80)
    
    if not dry_run and fixed_count > 0:
        with open(output_file, 'w', encoding='utf-8', newline='') as f:
            f.writelines(lines)
        print(f"File updated: {output_file}")
    elif dry_run:
        print("DRY RUN: No changes written to file")
    
    return fixed_count, errors

if __name__ == '__main__':
    file = r'd:\X\ND\ENSDF\A35\Cl35\new\Cl35_34s_p_g.ens'
    
    # First do a dry run
    print("PHASE 1: DRY RUN (validation only)")
    print()
    count, errs = fix_ri_alignment(file, dry_run=True)
    
    if errs:
        print("\nERROR: Issues detected during dry run. Aborting.")
        sys.exit(1)
    
    print("\n" + "=" * 80)
    print(f"DRY RUN SUCCESSFUL: {count} G-records will be fixed")
    print("=" * 80)
    print("\nPHASE 2: APPLYING FIXES")
    print()
    
    # Now apply fixes
    count, errs = fix_ri_alignment(file, dry_run=False)
    
    if errs:
        print("\nWARNING: Errors encountered during fix!")
        sys.exit(1)
    
    print("\nFix completed successfully!")
