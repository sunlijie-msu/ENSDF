#!/usr/bin/env python3
"""
Comprehensive ENSDF G-record formatting fix script
Fixes ALL field positioning errors in G-records:
1. RI values at column 22 → move to column 23
2. DRI fields not LEFT-JUSTIFIED → LEFT-JUSTIFY at column 30
3. Column 32 violations → ensure it's a SPACE
4. M field not LEFT-JUSTIFIED → LEFT-JUSTIFY at column 33
"""

import sys
import os

def fix_g_record_formatting(filename):
    """Fix all G-record formatting issues in ENSDF file"""
    
    if not os.path.exists(filename):
        print(f"ERROR: File '{filename}' not found!")
        return False
    
    # Read all lines
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    total_lines = len(lines)
    g_records_fixed = 0
    fixes_applied = []
    
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
        
        # Work with 80-character padded line
        fixed_line = original_line.ljust(80, ' ')
        line_modified = False
        errors_fixed = []
        
        # FIX 1: RI value at column 22 (should be at 23)
        if fixed_line[21] != ' ' and fixed_line[21].isdigit():
            # RI is shifted left - column 22 has digit
            # Need to insert space at col 22 and shift RI right
            errors_fixed.append('RI shifted left (col 22 had digit)')
            # This is complex - need to reconstruct the line
            # Extract fields carefully
            prefix = fixed_line[:21]  # NUCID through DE field
            ri_value = fixed_line[21]  # Character at col 22
            rest = fixed_line[22:]  # Everything else
            
            # Find where RI value ends in DRI field
            dri_start = rest[:2]  # Should be in DRI position
            
            # Reconstruct with space at col 22, RI starting at col 23
            fixed_line = prefix + ' ' + ri_value + rest[1:]
            line_modified = True
        
        # FIX 2: DRI field not LEFT-JUSTIFIED (cols 30-31)
        dri_field = fixed_line[29:31]
        if dri_field.strip() and dri_field[0] == ' ':
            # DRI has leading space - not LEFT-JUSTIFIED
            errors_fixed.append(f'DRI not LEFT-JUSTIFIED: [{dri_field}]')
            dri_value = dri_field.strip()
            
            # Check if DRI marker extends to column 32
            col32_char = fixed_line[31] if len(fixed_line) > 31 else ' '
            if col32_char != ' ' and col32_char.isalpha():
                # Might be 'LT' or 'GT' split across boundary
                dri_value = dri_value + col32_char
                # Left-justify in cols 30-31, clear col 32
                fixed_line = fixed_line[:29] + dri_value.ljust(2, ' ')[:2] + ' ' + fixed_line[32:]
            else:
                # Just left-justify DRI in cols 30-31
                fixed_line = fixed_line[:29] + dri_value.ljust(2, ' ') + fixed_line[31:]
            line_modified = True
        
        # FIX 3: Column 32 must be SPACE (readability space)
        elif fixed_line[31] != ' ':
            col32_char = fixed_line[31]
            # Check if it's part of DRI marker (LT, GT)
            if col32_char.isalpha() and dri_field.strip():
                errors_fixed.append(f'DRI marker extends to col 32: {dri_field}{col32_char}')
                # Combine with DRI and left-justify
                full_dri = dri_field.strip() + col32_char
                fixed_line = fixed_line[:29] + full_dri.ljust(2, ' ')[:2] + ' ' + fixed_line[32:]
                line_modified = True
        
        # FIX 4: M field not LEFT-JUSTIFIED (cols 33-41)
        m_field = fixed_line[32:41]
        if m_field.strip() and m_field[0] == ' ':
            # M field has leading space - not LEFT-JUSTIFIED
            errors_fixed.append(f'M field not LEFT-JUSTIFIED: [{m_field}]')
            m_value = m_field.strip()
            fixed_line = fixed_line[:32] + m_value.ljust(9, ' ') + fixed_line[41:]
            line_modified = True
        
        if line_modified:
            g_records_fixed += 1
            lines[line_num - 1] = fixed_line.rstrip() + '\n'
            fixes_applied.append({
                'line_num': line_num,
                'errors': errors_fixed,
                'original': original_line,
                'fixed': fixed_line.rstrip()
            })
            
            if g_records_fixed <= 20:  # Show first 20 fixes
                print(f"Line {line_num}: {', '.join(errors_fixed)}")
                print(f"  BEFORE: {original_line}")
                print(f"  AFTER:  {fixed_line.rstrip()}")
                print()
    
    if g_records_fixed > 20:
        print(f"... and {g_records_fixed - 20} more G-records fixed (showing first 20)")
        print()
    
    # Write fixed file
    with open(filename, 'w') as f:
        f.writelines(lines)
    
    print(f"\nSUMMARY:")
    print(f"  Total G-records fixed: {g_records_fixed}")
    print(f"  File updated: {filename}")
    
    return True

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python fix_g_record_formatting.py <ensdf_file>")
        sys.exit(1)
    
    filename = sys.argv[1]
    success = fix_g_record_formatting(filename)
    sys.exit(0 if success else 1)
