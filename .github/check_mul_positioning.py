#!/usr/bin/env python3
"""Check MUL field positioning in ENSDF G-records."""

import sys

def check_mul_positioning(filename):
    """Check if MUL fields start at column 33."""
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print('CHECKING ALL G-RECORDS FOR MUL POSITIONING ERRORS:')
    print('=' * 85)
    print('         1         2         3         4         5         6         7         8')
    print('12345678901234567890123456789012345678901234567890123456789012345678901234567890')
    print('                                ^--------^ MUL field (columns 33-41)')
    print()
    
    errors = []
    for i, line in enumerate(lines, 1):
        # TRUE G-record check
        if len(line) >= 9 and line[6] == ' ' and line[7] == 'G' and line[0:5].strip() and 'c' not in line[0:7]:
            mul_region = line[31:41] if len(line) >= 41 else line[31:]
            mul_content = mul_region.strip()
            
            if mul_content:
                # Find first non-space character in columns 32-41
                first_char_idx = None
                for j in range(31, min(41, len(line))):
                    if line[j] != ' ':
                        first_char_idx = j
                        break
                
                if first_char_idx is not None:
                    actual_col = first_char_idx + 1
                    if actual_col != 33:
                        errors.append((i, mul_content, actual_col, line.rstrip()))
                        print(f'❌ Line {i:3d}: MUL="{mul_content}" starts at column {actual_col} (should be 33)')
                        print(f'   {line.rstrip()}')
                        print()
    
    print()
    if errors:
        print(f'❌ CRITICAL: {len(errors)} MUL positioning errors found!')
        print()
        for line_num, mul, col, _ in errors:
            print(f'  Line {line_num}: "{mul}" at column {col} (shift RIGHT by {33-col})')
        return 1
    else:
        print('✅ SUCCESS: All MUL fields correctly positioned at column 33')
        return 0

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python check_mul_positioning.py <filename>')
        sys.exit(1)
    
    sys.exit(check_mul_positioning(sys.argv[1]))
