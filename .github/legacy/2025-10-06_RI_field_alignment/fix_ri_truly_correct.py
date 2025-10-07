#!/usr/bin/env python3
"""
ACTUALLY CORRECT RI Field Alignment Fix for ENSDF G-Records

The problem: RI field content starts at column 22 instead of column 23
The solution: RECONSTRUCT the line with correct field positioning

CRITICAL INSIGHT:
- Original: RI value starts at column 22, everything after is at correct positions
- Desired: RI value starts at column 23, everything after stays at correct positions
- Method: Extract RI value, reposition it, preserve all other fields

ENSDF G-Record Format:
  Column 22: SPACE (mandatory)
  Columns 23-29: RI (relative intensity) ← Must be LEFT-JUSTIFIED here
  Columns 30-31: DRI (uncertainty) ← Must stay here!
  Column 32: SPACE
  Columns 33-41: M (multipolarity) ← Must stay here!
  Columns 42-49: MR (mixing ratio) ← Must stay here!
  Column 77: C (comment flag) ← Must stay here!
"""

def fix_ri_alignment_actually_correct(input_file, output_file=None, dry_run=False):
    """
    Fix RI field alignment by reconstructing lines with correct field positions.
    
    Strategy:
    1. Identify where RI content currently is (starts at col 22)
    2. Extract the RI value
    3. Reconstruct line: keep cols 1-21, add space at col 22, add RI at col 23, keep rest from col 30 onward
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
        if len(line) < 30:
            continue
        
        # Remove newline for processing
        if line.endswith('\n'):
            line_no_newline = line[:-1]
        else:
            line_no_newline = line
        
        col22 = line_no_newline[21] if len(line_no_newline) > 21 else ' '
        
        # If column 22 is already a space, skip
        if col22 == ' ':
            continue
        
        original_line = line
        
        # CORRECT RECONSTRUCTION:
        # Part 1: Columns 1-21 (indices 0-20) - everything before col 22 - keep as-is
        part1 = line_no_newline[:21]
        
        # Part 2: Column 22 (index 21) - insert mandatory space
        part2 = ' '
        
        # Part 3: Columns 23-29 (indices 22-28, that's 7 chars) - RI field
        # Current RI content starts at col 22 (index 21) and is 7 chars long
        ri_content = line_no_newline[21:28]  # Extract indices 21-27 (7 chars)
        part3 = ri_content
        
        # Part 4: Columns 30 onward (indices 29 onward) - DRI, M, MR, C, Q all unchanged
        # Original column 30 is at index 29 (NOT 28!)
        part4 = line_no_newline[29:] if len(line_no_newline) > 29 else ''
        
        # Reconstruct the line
        fixed_line = part1 + part2 + part3 + part4
        
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
    print("ACTUALLY CORRECT VERSION: Reconstruct lines with proper field positions")
    print("="*80)
    print(f"Input file: {input_file}")
    print("Dry run: True\n")
    
    count1, errors1 = fix_ri_alignment_actually_correct(input_file, dry_run=True)
    
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
    
    count2, errors2 = fix_ri_alignment_actually_correct(input_file, dry_run=False)
    
    if errors2:
        print(f"\n[WARNING] Found {len(errors2)} errors during application.")
        sys.exit(1)
