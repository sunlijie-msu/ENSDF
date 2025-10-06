#!/usr/bin/env python3
"""
Analyze M and MR field positioning errors in specific lines.
Shows exact character-by-character positions for debugging.
"""

import sys

def analyze_line(line_num, line):
    """Analyze a single line showing all relevant field positions."""
    
    # Ensure line is padded to 80 characters
    padded = line.ljust(80, ' ')
    
    print(f"\nLine {line_num}: {line.rstrip()}")
    print("Column ruler:")
    print("         1         2         3         4         5         6         7         8")
    print("12345678901234567890123456789012345678901234567890123456789012345678901234567890")
    print(padded)
    print()
    
    # Check if it's a G-record
    if len(line) >= 8 and line[7] == 'G':
        # Extract key fields
        ri_field = padded[22:29]  # cols 23-29
        dri_field = padded[29:31]  # cols 30-31
        col32 = padded[31] if len(line) > 31 else '?'
        m_field = padded[32:41]  # cols 33-41
        mr_field = padded[41:49]  # cols 42-49
        dmr_field = padded[49:55]  # cols 50-55
        
        print(f"  RI (cols 23-29):   [{ri_field}]")
        print(f"  DRI (cols 30-31):  [{dri_field}]")
        print(f"  Col 32 (SPACE):    [{col32}] = {repr(col32)}")
        print(f"  M (cols 33-41):    [{m_field}]")
        print(f"  MR (cols 42-49):   [{mr_field}]")
        print(f"  DMR (cols 50-55):  [{dmr_field}]")
        
        # Check for errors
        errors = []
        
        # Check M field (should start at col 33, not have leading space)
        if m_field and m_field[0] == ' ' and m_field.strip():
            errors.append("M field has leading space - should start at col 33")
        
        # Check MR field (should start at col 42, not have leading space)
        if mr_field and mr_field[0] == ' ' and mr_field.strip():
            errors.append("MR field has leading space - should start at col 42")
        
        if errors:
            print("  ERRORS:")
            for err in errors:
                print(f"    - {err}")
        else:
            print("  OK!")


def main():
    filename = "A35/Cl35/new/Cl35_34s_p_g.ens"
    
    # Lines with M field errors: 474, 873, 926, 1010, 1089, 1699, 1799, 2006, 2010, 2014, 2022, 2361, 2367, 2370
    # Lines with MR field errors: 288, 305, 308, 367, 371, 396, 398, 408, 474, 479
    
    error_lines = [288, 305, 474, 873, 926, 1010]
    
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print("ANALYZING M AND MR FIELD ERRORS:")
    print("=" * 80)
    
    for line_num in error_lines:
        if line_num <= len(lines):
            analyze_line(line_num, lines[line_num - 1])
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
