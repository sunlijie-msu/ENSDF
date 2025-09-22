#!/usr/bin/env python3
"""
ENSDF Line Ruler - Visual Column Verification Tool
🎯 CRITICAL STRATEGY: This ruler technique is ESSENTIAL for precise ENSDF column positioning
Use this tool before and after any ENSDF column edits to avoid positioning errors!

This tool was developed after discovering systematic column positioning errors 
when moving E{-α} values from comment lines to S/DS fields. The ruler immediately
revealed that K flags were incorrectly positioned at column 80 instead of column 77.

LESSON LEARNED: Never trust column positioning without visual verification!
"""

import sys

def verify_line_positioning(line):
    """Verify ENSDF line positioning using visual ruler - THE MOST EFFECTIVE DEBUG TOOL"""
    
    print('🎯 ENSDF 80-Column Ruler - CRITICAL POSITIONING TOOL:')
    print('Ones:  12345678901234567890123456789012345678901234567890123456789012345678901234567890')
    print('Tens:  1111111111222222222233333333334444444444555555555566666666667777777777888888888999')
    print(f'Line:  {line}')
    print(f'Length: {len(line)} characters')
    print()
    
    # Critical ENSDF field boundaries for L-records
    critical_positions = {
        65: 'S field start (spectroscopic strength)',
        74: 'S field end',
        75: 'DS field start (uncertainty)',
        76: 'DS field end', 
        77: 'C field (Comment flag) ← CRITICAL: K flags belong HERE!',
        78: 'Should be blank',
        79: 'Should be blank',
        80: 'Should be blank (line end) ← NOT for flags!'
    }
    
    print('🔍 Character-by-character mapping for critical fields:')
    for i, char in enumerate(line, 1):
        if i in critical_positions:
            status = "🎯" if (i == 77 and char in ['K', 'M', 'S', 'C', ' ']) else "⚠️" if i == 77 else ""
            print(f'Col {i:2d}: "{char}" <- {critical_positions[i]} {status}')
        elif i >= 60:
            print(f'Col {i:2d}: "{char}"')
    
    print()
    
    # Check ENSDF compliance
    errors = []
    warnings = []
    
    if len(line) != 80:
        errors.append(f'Line length {len(line)} != 80 characters')
    
    if len(line) >= 77:
        char_77 = line[76] if len(line) > 76 else ' '
        if char_77 not in ['C', ' ', 'K', 'M', 'S']:  # Valid comment flags
            errors.append(f'Invalid character "{char_77}" at column 77 (Comment flag position)')
        elif char_77 == 'K':
            print('🎯 SUCCESS: K flag correctly positioned at column 77!')
    
    # Check for flags in wrong positions (common mistake)
    if len(line) >= 80:
        char_80 = line[79] if len(line) > 79 else ' '
        if char_80 in ['K', 'M', 'S', 'C']:
            errors.append(f'Flag "{char_80}" found at column 80 - should be at column 77!')
    
    if errors:
        print('❌ ERRORS FOUND:')
        for error in errors:
            print(f'  - {error}')
    elif warnings:
        print('⚠️ WARNINGS:')
        for warning in warnings:
            print(f'  - {warning}')
    else:
        print('✅ Line appears correctly formatted')
    
    return len(errors) == 0

def demonstrate_ruler_effectiveness():
    """Demonstrate how the ruler technique catches positioning errors"""
    
    print("="*70)
    print("🎯 RULER TECHNIQUE DEMONSTRATION")
    print("="*70)
    print("This tool was created after a critical positioning error was discovered.")
    print("The K flags were incorrectly placed at column 80 instead of column 77.")
    print("The ruler technique immediately revealed this systematic error!")
    print()
    
    # Example of incorrect positioning (before fix)
    wrong_line = ' 35CL  L 9127      9 5/2                                        2404      9    K'
    print("❌ BEFORE FIX (K flag at column 80 - WRONG!):")
    verify_line_positioning(wrong_line)
    
    print("\n" + "="*50)
    
    # Example of correct positioning (after fix)
    correct_line = ' 35CL  L 9127      9 5/2                                        2404      9 K   '
    print("✅ AFTER FIX (K flag at column 77 - CORRECT!):")
    verify_line_positioning(correct_line)
    
    print("\n" + "="*70)
    print("🚨 KEY LESSON: Always use this ruler BEFORE and AFTER ENSDF edits!")
    print("   - Prevents systematic column positioning errors")
    print("   - Catches mistakes that validation tools might miss")
    print("   - Essential for maintaining ENSDF format compliance")
    print("="*70)

if __name__ == '__main__':
    # Simple command-line interface:
    # - no args: run built-in demonstration
    # - --line "<line>" : verify a single provided line
    # - --file <path> : scan an ENSDF file and verify L-records and K-flag placements
    import argparse

    parser = argparse.ArgumentParser(description='ENSDF 80-column ruler and verifier')
    parser.add_argument('--line', help='Verify a single line (pass the full 80-char line in quotes)')
    parser.add_argument('--file', help='Path to an ENSDF file to scan and verify L-records')
    parser.add_argument('--show-only-wrong', action='store_true', help='When scanning a file, only print lines with errors')

    args = parser.parse_args()

    if args.line:
        verify_line_positioning(args.line)
    elif args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as fh:
                lines = fh.readlines()
        except Exception as e:
            print(f'ERROR: Could not open file {args.file}: {e}')
            sys.exit(2)

        total = 0
        errors_found = 0
        for lineno, raw in enumerate(lines, 1):
            line = raw.rstrip('\n')
            # Only check L-records (type 'L' in column 8)
            if len(line) >= 8 and line[7] == 'L':
                total += 1
                ok = verify_line_positioning(line)
                if not ok:
                    errors_found += 1
                    if args.show_only_wrong:
                        print(f'Line {lineno}:')
                        print(line)
                        print('-'*40)
        print(f'Checked {total} L-record lines: {errors_found} lines with errors')
        if errors_found:
            sys.exit(1)
    else:
        demonstrate_ruler_effectiveness()