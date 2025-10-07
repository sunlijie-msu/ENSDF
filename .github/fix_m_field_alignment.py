#!/usr/bin/env python3
"""
Fix Multipolarity (M field) Alignment for ENSDF G-Records

Problem: M field content starts at column 32 instead of column 33
Solution: Reconstruct lines with correct field positioning

ENSDF G-Record Format:
  Columns 30-31: DRI (uncertainty)
  Column 32: SPACE (mandatory separator)
  Columns 33-41: M (multipolarity) - must be LEFT-JUSTIFIED at column 33
  Columns 42-49: MR (mixing ratio)
  
Strategy (same as RI fix):
1. Extract M field content from where it currently is (starting at col 32)
2. Reconstruct line: keep cols 1-31, add space at col 32, add M at col 33, keep rest from col 42 onward
3. Ensure 80-character line length
"""

def fix_m_alignment(input_file, output_file=None, dry_run=False):
    """
    Fix M field alignment by reconstructing lines with correct field positions.
    
    Strategy:
    1. Identify where M content currently is (starts at col 32)
    2. Extract the M field value (9 characters for columns 33-41)
    3. Reconstruct: keep cols 1-31, add space at col 32, add M at col 33, keep rest from col 42+
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
        if len(line) < 42:
            continue
        
        # Remove newline for processing
        if line.endswith('\n'):
            line_no_newline = line[:-1]
        else:
            line_no_newline = line
        
        col32 = line_no_newline[31] if len(line_no_newline) > 31 else ' '
        
        # If column 32 is already a space, skip (already correct)
        if col32 == ' ':
            continue
        
        # Check if there's actually M field content
        m_field_check = line_no_newline[32:41] if len(line_no_newline) > 41 else ''
        if not m_field_check.strip():
            continue  # No M field content, skip
        
        original_line = line
        
        # RECONSTRUCTION STRATEGY:
        # Part 1: Columns 1-31 (indices 0-30) - everything up to and including DRI field
        part1 = line_no_newline[:31]
        
        # Part 2: Column 32 (index 31) - insert mandatory space
        part2 = ' '
        
        # Part 3: Columns 33-41 (indices 32-40, that's 9 chars) - M field
        # Current M content starts at col 32 (index 31) and is 9 chars long
        m_content = line_no_newline[31:40]  # Extract indices 31-39 (9 chars)
        part3 = m_content
        
        # Part 4: Columns 42 onward (indices 41 onward) - MR, DMR, CC, etc. all unchanged
        # Original column 42 is at index 41 (NOT 40!)
        part4 = line_no_newline[41:] if len(line_no_newline) > 41 else ''
        
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
        
        if fixed_line[31] != ' ':
            errors.append(f"Line {line_num}: Column 32 still not space after fix!")
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
    print("M FIELD (MULTIPOLARITY) ALIGNMENT FIX - ENSDF G-RECORDS")
    print("Strategy: Reconstruct lines with proper field positions")
    print("="*80)
    print(f"Input file: {input_file}")
    print("Dry run: True\n")
    
    count1, errors1 = fix_m_alignment(input_file, dry_run=True)
    
    if errors1:
        print(f"\n[ERROR] Dry run found {len(errors1)} errors. Aborting.")
        sys.exit(1)
    
    print("\n" + "="*80)
    print(f"DRY RUN SUCCESSFUL: {count1} G-records will be fixed")
    print("="*80)
    
    print("\n\nPHASE 2: APPLYING FIXES\n")
    print("="*80)
    print("M FIELD (MULTIPOLARITY) ALIGNMENT FIX - ENSDF G-RECORDS")
    print("="*80)
    print(f"Input file: {input_file}")
    print("Dry run: False\n")
    
    count2, errors2 = fix_m_alignment(input_file, dry_run=False)
    
    if errors2:
        print(f"\n[WARNING] Found {len(errors2)} errors during application.")
        sys.exit(1)
