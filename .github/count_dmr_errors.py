#!/usr/bin/env python3
"""
Count DMR field positioning errors in ENSDF file.
DMR field (columns 50-55) must be LEFT-JUSTIFIED at column 50.
"""

import sys


def count_dmr_errors(filename):
    """Count G-records with DMR field not LEFT-JUSTIFIED at column 50."""
    
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    dmr_errors = 0
    error_examples = []
    
    for i, line in enumerate(lines, start=1):
        # Skip non-G-records or lines too short
        if len(line) < 50:  # Need at least up to DMR field
            continue
        
        if not (line[7] == 'G' and line[8] == ' '):
            continue
        
        # Pad line to 80 characters
        padded_line = line.ljust(80, ' ')
        
        # Extract DMR field (columns 50-55, 0-indexed: 49-55)
        dmr_field = padded_line[49:55]
        
        # Check if DMR field has content and leading space
        if dmr_field.strip() and dmr_field[0] == ' ':
            dmr_errors += 1
            if len(error_examples) < 20:
                dmr_value = dmr_field.strip()
                # Find where it actually starts
                actual_start_col = 50
                for j, char in enumerate(dmr_field):
                    if char != ' ':
                        actual_start_col = 50 + j
                        break
                error_examples.append((i, dmr_value, actual_start_col, line.rstrip()))
    
    print(f"Total DMR field errors: {dmr_errors}\n")
    
    if error_examples:
        print("First 20 examples:")
        for line_num, dmr_val, start_col, line_text in error_examples:
            print(f"  Line {line_num}: DMR=[{dmr_val}] starts at col {start_col} (should be 50)")
            print(f"    {line_text}")
    
    return dmr_errors


if __name__ == "__main__":
    filename = "A35/Cl35/new/Cl35_34s_p_g.ens"
    count_dmr_errors(filename)
