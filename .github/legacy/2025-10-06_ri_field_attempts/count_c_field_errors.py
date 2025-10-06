#!/usr/bin/env python3
"""
Count column 77 (C field) positioning errors in ENSDF G-records.
Comment flags must be in column 77, NOT column 78.
"""

import sys


def count_c_field_errors(filename):
    """Count G-records with comment flag in wrong column."""
    
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    c_field_errors = 0
    error_examples = []
    
    for i, line in enumerate(lines, start=1):
        # Skip non-G-records
        if len(line) < 8:
            continue
        
        if not (line[7] == 'G' and line[8] == ' '):
            continue
        
        # Pad line to 80 characters
        padded_line = line.ljust(80, ' ')
        
        # Check column 77 (index 76) and column 78 (index 77)
        col_77 = padded_line[76]
        col_78 = padded_line[77] if len(line) > 77 else ' '
        
        # Valid comment flags: A-Z, a-z, *, &, @
        valid_flags = set('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz*&@')
        
        # Error if column 77 is space but column 78 has a flag
        if col_77 == ' ' and col_78 in valid_flags:
            c_field_errors += 1
            if len(error_examples) < 20:
                error_examples.append((i, col_78, line.rstrip()))
    
    print(f"Total C field (column 77) positioning errors: {c_field_errors}\n")
    
    if error_examples:
        print("First 20 examples:")
        for line_num, flag, line_text in error_examples:
            print(f"  Line {line_num}: Flag '{flag}' at col 78 (should be col 77)")
            print(f"    {line_text}")
    
    return c_field_errors


if __name__ == "__main__":
    filename = "A35/Cl35/new/Cl35_34s_p_g.ens"
    count_c_field_errors(filename)
