#!/usr/bin/env python3
"""
Quick RI Field Position Checker for ENSDF Files
Checks if RI values in G-records start at column 23 (LEFT-JUSTIFIED)
"""

import sys

if len(sys.argv) < 2:
    print("Usage: python check_ri_positioning.py filename.ens")
    sys.exit(1)

filename = sys.argv[1]

print(f"Checking RI field positioning in: {filename}")
print("=" * 80)
print("ENSDF Rule: RI field (columns 23-29) must be LEFT-JUSTIFIED at column 23")
print()

with open(filename, 'r') as f:
    lines = f.readlines()

errors = []
total_g_records = 0

for line_num, line in enumerate(lines, 1):
    # Check for G-record: column 8='G', column 6 and 7 are blank spaces
    if len(line) >= 32:
        if line[7] == 'G' and line[5] == ' ' and line[6] == ' ':
            total_g_records += 1
            
            # Extract RI field (columns 23-29, 0-based index 22:29)
            ri_field = line[22:29]
            
            # Skip if RI field is completely empty
            if not ri_field.strip():
                continue
            
            # CRITICAL CHECK: Column 22 must be a SPACE (readability space between DE and RI)
            # If column 22 has a digit/character, RI is shifted left (WRONG!)
            if line[21] != ' ':  # Column 22 is at index 21
                errors.append({
                    'line_num': line_num,
                    'line': line.rstrip(),
                    'ri_field': ri_field,
                    'col22_char': line[21],
                    'error_type': 'RI starts at column 22 (should be 23)'
                })
                continue
            
            # Check if RI starts at column 23 (index 22)
            # If column 23 is a space but there's content later, it's shifted right (WRONG!)
            if line[22] == ' ' and ri_field[1:].strip():
                errors.append({
                    'line_num': line_num,
                    'line': line.rstrip(),
                    'ri_field': ri_field,
                    'error_type': 'RI starts after column 23 (should be 23)'
                })

print(f"Total G-records analyzed: {total_g_records}")
print(f"G-records with RI not starting at column 23: {len(errors)}")
print()

if errors:
    print("ERRORS FOUND:")
    print("=" * 80)
    print("Column ruler for reference:")
    print("         1111111111222222222233333333334444444444555555555566666666667777777777")
    print("12345678901234567890123456789012345678901234567890123456789012345678901234567890")
    print()
    
    for i, err in enumerate(errors[:20], 1):
        print(f"{i}. Line {err['line_num']}: {err['error_type']}")
        print(f"   RI field (cols 23-29): [{err['ri_field']}]")
        if 'col22_char' in err:
            print(f"   Column 22 contains: '{err['col22_char']}' (should be SPACE)")
        print(f"   {err['line']}")
        print()
    
    if len(errors) > 20:
        print(f"... and {len(errors) - 20} more errors")
    
    sys.exit(1)
else:
    print("[OK] All RI fields correctly positioned at column 23")
    sys.exit(0)
