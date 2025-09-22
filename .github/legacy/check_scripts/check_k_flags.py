#!/usr/bin/env python3
"""
Quick check for K flag positioning at column 80 in ENSDF files
"""

import sys

def check_k_flags(filename):
    """Check K flag positioning at column 80"""
    
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    print('ENSDF 80-Column Ruler:')
    print('Ones:  12345678901234567890123456789012345678901234567890123456789012345678901234567890')
    print('Tens:  1111111111222222222233333333334444444444555555555566666666667777777777888888888999')
    print()
    
    # Find K-flagged L-records
    k_flagged_lines = []
    for i, line in enumerate(lines, 1):
        if line.strip() and len(line) > 7 and line[7:8] == 'L' and 'K' in line:
            k_flagged_lines.append((i, line.rstrip()))
    
    print(f'Found {len(k_flagged_lines)} K-flagged L-records:')
    print()
    
    all_correct = True
    for line_num, line in k_flagged_lines:
        print(f'Line {line_num}:')
        print(f'Ruler: 12345678901234567890123456789012345678901234567890123456789012345678901234567890')
        print(f'Line:  {line}')
        print(f'Length: {len(line)} characters')
        
        # Check if K flag is at position 80 (index 79)
        if len(line) == 80 and line[79] == 'K':
            print('✅ K flag correctly positioned at column 80')
        else:
            if len(line) != 80:
                print(f'❌ Line length incorrect: {len(line)} chars (should be 80)')
            if len(line) > 79 and line[79] != 'K':
                print(f'❌ Character at position 80: "{line[79]}" (should be "K")')
            elif len(line) <= 79:
                print('❌ Line too short - K flag missing')
            all_correct = False
        print()
    
    if all_correct:
        print('🎯 SUCCESS: All K flags correctly positioned at column 80!')
    else:
        print('❌ ERRORS: Some K flags are NOT correctly positioned!')
    
    return all_correct

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python check_k_flags.py <filename>")
        sys.exit(1)
    
    filename = sys.argv[1]
    success = check_k_flags(filename)
    sys.exit(0 if success else 1)