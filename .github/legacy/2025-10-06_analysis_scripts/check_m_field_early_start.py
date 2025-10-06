#!/usr/bin/env python3
"""
Check M field positioning in ENSDF file.
M field (columns 33-41) must be LEFT-JUSTIFIED at column 33.
Column 32 MUST be a space (mandatory space after DRI field).
"""

import sys


def check_m_field_positioning(filename):
    """Check G-records where M field starts at column 32 instead of 33."""
    
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    errors = 0
    error_examples = []
    
    for i, line in enumerate(lines, start=1):
        # Skip non-G-records or lines too short
        if len(line) < 41:
            continue
        
        # ONLY check G-records (not cG comment lines)
        if not (line[7] == 'G' and line[8] == ' ' and line[6] == ' '):
            continue
        
        # Pad line to 80 characters
        padded_line = line.ljust(80, ' ')
        
        # Column 32 (idx 31) MUST be space
        # M field starts at column 33 (idx 32)
        col32 = padded_line[31]
        m_field = padded_line[32:41]
        
        # Check if col 32 has non-space character (M field starting early)
        if col32 != ' ' and m_field.strip():
            errors += 1
            if len(error_examples) < 20:
                error_examples.append((i, col32, m_field.strip(), line.rstrip()))
    
    print(f"Total M field positioning errors (starting at col 32 instead of 33): {errors}\n")
    
    if error_examples:
        print("First 20 examples:")
        for line_num, col32_char, m_val, line_text in error_examples:
            print(f"  Line {line_num}: Col 32 has '{col32_char}', M field='{m_val}'")
            print(f"    {line_text}")
            print()
    else:
        print("No M field positioning errors found!")
    
    return errors


if __name__ == "__main__":
    filename = r'A35\Cl35\new\Cl35_34s_p_g.ens'
    error_count = check_m_field_positioning(filename)
    sys.exit(1 if error_count > 0 else 0)
