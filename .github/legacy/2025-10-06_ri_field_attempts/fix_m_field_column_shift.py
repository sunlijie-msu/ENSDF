#!/usr/bin/env python3
"""
Fix M field positioning in ENSDF file.
M field must start at column 33, not column 32.
Column 32 MUST be a space (mandatory space after DRI field).

This script fixes G-records where M field incorrectly starts at column 32.
"""

import sys


def fix_m_field_positioning(filename):
    """Fix G-records where M field starts at column 32 instead of 33."""
    
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    fixed_count = 0
    fixed_lines = []
    
    for line in lines:
        # Preserve newline
        original_line = line
        line_content = line.rstrip('\n')
        
        # Skip non-G-records or lines too short
        if len(line_content) < 41:
            fixed_lines.append(original_line)
            continue
        
        # ONLY fix G-records (not cG comment lines or other records)
        if not (len(line_content) >= 9 and line_content[7] == 'G' and 
                line_content[8] == ' ' and line_content[6] == ' '):
            fixed_lines.append(original_line)
            continue
        
        # Pad to exactly 80 characters for analysis
        padded_line = line_content.ljust(80, ' ')
        
        # Check column 32 (idx 31) - should be space
        # Check if M field (cols 33-41) has content
        col32 = padded_line[31]
        m_field = padded_line[32:41]
        
        # If col 32 is NOT space AND M field has content, this is an error
        if col32 != ' ' and m_field.strip():
            # FIX: Insert space at column 32, shift everything after right by 1
            # But we must preserve 80-character line length!
            # So we need to: insert space at col 32, drop last character
            
            # Build corrected line:
            # Cols 1-31 stay same
            # Col 32 becomes space
            # Cols 33-79 become old cols 32-78
            # Col 80 becomes space (we lose old col 79, but it's usually space)
            
            fixed_line = padded_line[:31] + ' ' + padded_line[31:79]
            
            # Ensure exactly 80 characters
            if len(fixed_line) != 80:
                print(f"WARNING: Fixed line length is {len(fixed_line)}, expected 80")
                print(f"  Original: {repr(padded_line)}")
                print(f"  Fixed:    {repr(fixed_line)}")
            
            fixed_lines.append(fixed_line + '\n')
            fixed_count += 1
        else:
            fixed_lines.append(original_line)
    
    # Write fixed file
    with open(filename, 'w', encoding='utf-8', newline='\n') as f:
        f.writelines(fixed_lines)
    
    print(f"Fixed {fixed_count} M field positioning errors")
    return fixed_count


if __name__ == "__main__":
    filename = r'A35\Cl35\new\Cl35_34s_p_g.ens'
    
    print("Fixing M field positioning errors...")
    fixed_count = fix_m_field_positioning(filename)
    
    if fixed_count > 0:
        print(f"\n✓ Successfully fixed {fixed_count} lines")
        print("  M field now starts at column 33 (with space at column 32)")
        print("  This also corrects MR, DMR, CC, DCC, TI, DTI, C, Q field positions")
    else:
        print("\nNo M field positioning errors found")
    
    sys.exit(0)
