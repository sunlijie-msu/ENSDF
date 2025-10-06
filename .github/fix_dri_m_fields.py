#!/usr/bin/env python3
"""
Fix remaining G-record formatting issues:
1. DRI fields not LEFT-JUSTIFIED (leading spaces)
2. Column 32 violations (must be SPACE)
3. M fields not LEFT-JUSTIFIED (leading spaces)

CRITICAL: Preserve all other field values exactly!
"""

import sys
import os

def fix_remaining_g_record_issues(filename):
    """Fix DRI, column 32, and M field formatting issues"""
    
    if not os.path.exists(filename):
        print(f"ERROR: File '{filename}' not found!")
        return False
    
    # Create backup
    backup_file = filename + '.backup_before_dri_m_fix'
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
        if len(original_line) < 42:
            continue
        if not (original_line[7] == 'G' and original_line[5] == ' ' and original_line[6] == ' '):
            continue
        
        # Work with padded line to ensure we can access all columns
        fixed_line = original_line.ljust(80, ' ')
        line_modified = False
        errors_fixed = []
        
        # FIX 1: DRI field not LEFT-JUSTIFIED (cols 30-31, 0-based 29:31)
        dri_field = fixed_line[29:31]
        if dri_field.strip() and dri_field[0] == ' ':
            # DRI has leading space - need to LEFT-JUSTIFY
            dri_value = dri_field.strip()
            
            # Check if DRI value extends to column 32 (like "LT" split as " L" + "T")
            col32_char = fixed_line[31]
            if col32_char != ' ' and col32_char.isalpha() and len(dri_value) == 1:
                # DRI marker split across boundary (e.g., " L" in cols 30-31, "T" in col 32)
                full_dri = dri_value + col32_char
                if full_dri in ['LT', 'GT', 'LE', 'GE', 'AP', 'CA', 'SY']:
                    # Valid 2-character marker split across cols 30-31 and 32
                    # Left-justify full marker in cols 30-31, clear col 32
                    fixed_line = fixed_line[:29] + full_dri.ljust(2)[:2] + ' ' + fixed_line[32:]
                    errors_fixed.append(f'DRI "{full_dri}" split across cols 30-32, now in cols 30-31')
                    line_modified = True
                else:
                    # Not a valid marker - just left-justify DRI, clear col 32
                    fixed_line = fixed_line[:29] + dri_value.ljust(2) + ' ' + fixed_line[32:]
                    errors_fixed.append(f'DRI "{dri_value}" left-justified, col 32 cleared')
                    line_modified = True
            else:
                # Normal case - just left-justify DRI in cols 30-31
                fixed_line = fixed_line[:29] + dri_value.ljust(2) + fixed_line[31:]
                errors_fixed.append(f'DRI "{dri_value}" left-justified')
                line_modified = True
        
        # FIX 2: Column 32 must be SPACE (if not already fixed above)
        elif fixed_line[31] != ' ' and not line_modified:
            col32_char = fixed_line[31]
            # Check if it's orphaned character from DRI marker
            dri_field_check = fixed_line[29:31]
            if col32_char.isalpha() and dri_field_check.strip():
                # Might be DRI marker continuation
                full_dri = dri_field_check.strip() + col32_char
                if full_dri in ['LT', 'GT', 'LE', 'GE', 'AP', 'CA', 'SY']:
                    # Move to proper DRI position
                    fixed_line = fixed_line[:29] + full_dri.ljust(2)[:2] + ' ' + fixed_line[32:]
                    errors_fixed.append(f'Col 32 "{col32_char}" merged with DRI to form "{full_dri}"')
                    line_modified = True
            
            if not line_modified:
                # Just clear column 32
                fixed_line = fixed_line[:31] + ' ' + fixed_line[32:]
                errors_fixed.append(f'Col 32 cleared (was "{col32_char}")')
                line_modified = True
        
        # FIX 3: M field not LEFT-JUSTIFIED (cols 33-41, 0-based 32:41)
        m_field = fixed_line[32:41]
        if m_field.strip() and m_field[0] == ' ':
            # M field has leading space - LEFT-JUSTIFY
            m_value = m_field.strip()
            fixed_line = fixed_line[:32] + m_value.ljust(9) + fixed_line[41:]
            errors_fixed.append(f'M field "{m_value}" left-justified')
            line_modified = True
        
        if line_modified:
            g_records_fixed += 1
            lines[line_num - 1] = fixed_line.rstrip() + '\n'
            
            if g_records_fixed <= 25:  # Show first 25 fixes
                print(f"Line {line_num}: {'; '.join(errors_fixed)}")
                print(f"  BEFORE: {original_line}")
                print(f"  AFTER:  {fixed_line.rstrip()}")
                print()
    
    if g_records_fixed > 25:
        print(f"... and {g_records_fixed - 25} more G-records fixed (showing first 25)")
        print()
    
    # Write fixed file
    with open(filename, 'w') as f:
        f.writelines(lines)
    
    print(f"\nSUMMARY:")
    print(f"  Total G-records fixed: {g_records_fixed}")
    print(f"  File updated: {filename}")
    print(f"  Backup saved: {backup_file}")
    
    return True

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python fix_dri_m_fields.py <ensdf_file>")
        sys.exit(1)
    
    filename = sys.argv[1]
    success = fix_remaining_g_record_issues(filename)
    sys.exit(0 if success else 1)
