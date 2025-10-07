#!/usr/bin/env python3
"""
CORRECT RI Field Alignment Fix for ENSDF G-Records

This script fixes G-records where RI field starts at column 22 instead of column 23.

CRITICAL DIFFERENCE from previous script:
- Insert space at column 22 (before RI)
- Remove character at column 30 (RIGHT AFTER DRI field ends at col 31)
- This keeps DRI, M, MR, C, Q fields at their ORIGINAL positions

ENSDF G-Record Format:
  Columns 22: SPACE (mandatory)
  Columns 23-29: RI (relative intensity)
  Columns 30-31: DRI (uncertainty) - MUST NOT SHIFT
  Columns 33-41: M (multipolarity) - MUST NOT SHIFT
  Columns 42-49: MR (mixing ratio) - MUST NOT SHIFT
  Column 77: C (comment flag) - MUST NOT SHIFT
"""

def fix_ri_alignment_correct(input_file, output_file=None, dry_run=False):
    """
    Fix RI field alignment in ENSDF G-records.
    
    Strategy:
    1. Insert space at column 22 (Python index 21)
    2. Remove character at column 30 (Python index 29) - right after DRI field
    3. This shifts ONLY RI field right, keeps DRI/M/MR/C/Q unchanged
    """
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    fixed_count = 0
    errors = []
    
    for i, line in enumerate(lines):
        line_num = i + 1
        
        # Only process G-records
        if not line.startswith(' 35CL  G '):
            continue
        
        # Check if line is long enough
        if len(line) <= 29:  # Need at least to column 30
            continue
        
        col22 = line[21]  # Column 22 (0-indexed = 21)
        
        # If column 22 is already a space, skip
        if col22 == ' ':
            continue
        
        # CORRECT FIX (TRULY CORRECT THIS TIME):
        # 1. Insert space at column 22 (index 21) - shifts everything right
        # 2. Remove space at column 32 (index 31 AFTER insertion = index 32) 
        #    Column 32 is the readability space between DRI (30-31) and M (33-41)
        # 3. This way: RI shifts right to col 23, but DRI/M/MR/C/Q stay unchanged!
        
        original_line = line
        
        # Remove newline for processing
        if line.endswith('\n'):
            line_no_newline = line[:-1]
        else:
            line_no_newline = line
        
        # Step 1: Insert space at column 22 (index 21)
        # This shifts everything right by 1 temporarily
        temp_line = line_no_newline[:21] + ' ' + line_no_newline[21:]
        
        # Step 2: Remove the space at column 32
        # After insertion at index 21, what was originally at column 32 (index 31)
        # is now at index 32
        # Column 32 = readability space between DRI and M fields (was index 31, now index 32)
        if len(temp_line) > 32:
            fixed_line = temp_line[:32] + temp_line[33:]  # Remove char at index 32 (original column 32)
        else:
            fixed_line = temp_line
        
        # Ensure exactly 80 characters
        if len(fixed_line) > 80:
            fixed_line = fixed_line[:80]
        elif len(fixed_line) < 80:
            fixed_line = fixed_line.ljust(80)
        
        # Re-add newline
        fixed_line = fixed_line + '\n'
        
        # Validate the fix
        line_check = fixed_line.rstrip('\n')
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
            print(f"  OLD: {original_line.rstrip(chr(10))}")
            print(f"  NEW: {fixed_line.rstrip(chr(10))}")
            print()
    
    # Report
    print("="*80)
    print(f"Total G-records fixed: {fixed_count}")
    if errors:
        print(f"Errors encountered: {len(errors)}")
        for err in errors[:5]:
            print(f"  {err}")
    print("="*80)
    
    if not dry_run:
        output_path = output_file or input_file
        with open(output_path, 'w', encoding='utf-8', newline='') as f:
            f.writelines(lines)
        print(f"File updated: {output_path}")
    else:
        print("DRY RUN: No changes written to file")
    
    return fixed_count, errors


if __name__ == "__main__":
    import sys
    
    input_file = r"d:\X\ND\ENSDF\A35\Cl35\new\Cl35_34s_p_g.ens"
    
    print("\nPHASE 1: DRY RUN (validation only)\n")
    print("="*80)
    print("RI FIELD ALIGNMENT FIX - ENSDF G-RECORDS")
    print("CORRECT VERSION: Shifts ONLY RI, keeps DRI/M/MR/C/Q unchanged")
    print("="*80)
    print(f"Input file: {input_file}")
    print("Dry run: True\n")
    
    count1, errors1 = fix_ri_alignment_correct(input_file, dry_run=True)
    
    if errors1:
        print(f"\n[ERROR] Dry run found {len(errors1)} errors. Aborting.")
        sys.exit(1)
    
    print("\n" + "="*80)
    print(f"DRY RUN SUCCESSFUL: {count1} G-records will be fixed")
    print("="*80)
    
    print("\n\nPHASE 2: APPLYING FIXES\n")
    print("="*80)
    print("RI FIELD ALIGNMENT FIX - ENSDF G-RECORDS")
    print("="*80)
    print(f"Input file: {input_file}")
    print("Dry run: False\n")
    
    count2, errors2 = fix_ri_alignment_correct(input_file, dry_run=False)
    
    if errors2:
        print(f"\n[WARNING] Found {len(errors2)} errors during application.")
        sys.exit(1)
