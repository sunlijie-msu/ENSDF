#!/usr/bin/env python3
"""
ENSDF 80-Column Ruler - Simple Visual Verification Tool

🎯 PURPOSE: Quick visual verification of ENSDF 80-column positioning
🎯 USE FREQUENTLY: Before edit, during edit, after edit for AI self-diagnostics
🎯 CRITICAL: Prevents column positioning errors that break ENSDF format

USAGE:
  python ensdf_1line_ruler.py --line "your 80-char line"
  python ensdf_1line_ruler.py --file "filename.ens"
"""

import sys

def print_ruler(line):
    """Print simple 80-column ruler with line for quick visual verification"""
    print('🎯 ENSDF 80-Column Ruler:')
    print('Ones: 12345678901234567890123456789012345678901234567890123456789012345678901234567890')
    print('Tens: 1111111111222222222233333333334444444444555555555566666666667777777777888888888999')
    print(f'Line: {line}')
    print(f'Len:  {len(line)} chars')
    
    # Quick validation
    errors = []
    if len(line) != 80:
        errors.append(f'Length {len(line)} ≠ 80')
    
    # Check ENSDF field positions for data records
    if len(line) >= 8 and line[7] in ['L', 'G', 'E', 'B']:
        record_type = line[7]
        
        # Column 77 validation (different rules for different record types)
        if len(line) > 76:
            col_77 = line[76]
            if record_type == 'G':
                # G-record: A-Z, a-z, *, &, @, space allowed - NO ? at col 77
                if col_77 != ' ' and not (col_77.isalpha() or col_77 in ['*', '&', '@']):
                    errors.append(f'Col 77: "{col_77}" invalid G-record flag (use A-Z,a-z,*,&,@)')
                if col_77 == '?':
                    errors.append(f'Col 77: "?" forbidden in G-record (use col 80 for ?)')
            else:
                # L, E, B records: C, K, M, S, space allowed
                if col_77 not in [' ', 'C', 'K', 'M', 'S']:
                    errors.append(f'Col 77: "{col_77}" invalid {record_type}-record flag')
        
        # Column 80 validation 
        if len(line) > 79:
            col_80 = line[79]
            if record_type == 'G':
                # G-record col 80: space, ?, S allowed
                if col_80 not in [' ', '?', 'S']:
                    errors.append(f'Col 80: "{col_80}" invalid G-record additional indicator (use space,?,S)')
            else:
                # Other records: should be blank
                if col_80 in ['K', 'M', 'S', 'C']:
                    errors.append(f'Col 80: "{col_80}" flag should be at col 77')
                elif col_80 != ' ':
                    errors.append(f'Col 80: "{col_80}" should be blank for {record_type}-record')
    
    if errors:
        print(f'❌ ERRORS: {" | ".join(errors)}')
        return False
    else:
        print('✅ OK')
        return True
def scan_file(filename, show_only_wrong=False):
    """Scan ENSDF file and check all data record lines"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f'❌ ERROR: Cannot open {filename}: {e}')
        return False
    
    total_checked = 0
    error_count = 0
    
    for lineno, raw_line in enumerate(lines, 1):
        line = raw_line.rstrip('\n')
        # Check data records (L, G, E, B, DP records)
        if len(line) >= 8 and line[7] in ['L', 'G', 'E', 'B', 'D']:
            total_checked += 1
            if show_only_wrong:
                if not print_ruler(line):
                    error_count += 1
                    print(f'Line {lineno}: {line}')
                    print('-' * 40)
            else:
                print(f'\nLine {lineno}:')
                if not print_ruler(line):
                    error_count += 1
    
    print(f'\n� Summary: {total_checked} data records checked, {error_count} errors found')
    return error_count == 0

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='ENSDF 80-column ruler - simple visual verification')
    parser.add_argument('--line', help='Verify single line (in quotes)')
    parser.add_argument('--file', help='Scan ENSDF file for data record errors')
    parser.add_argument('--show-only-wrong', action='store_true', help='Show only error lines')
    
    args = parser.parse_args()
    
    if args.line:
        success = print_ruler(args.line)
        sys.exit(0 if success else 1)
    elif args.file:
        success = scan_file(args.file, args.show_only_wrong)
        sys.exit(0 if success else 1)
    else:
        print('🎯 ENSDF 80-Column Ruler Tool')
        print('Usage:')
        print('  --line "your line"     Check single line')
        print('  --file filename.ens    Check all data records in file')
        print('  --show-only-wrong      Show only error lines when scanning')
        print()
        print('💡 Use this tool FREQUENTLY during ENSDF editing:')
        print('   • BEFORE making edits (verify current state)')
        print('   • DURING editing (check each changed line)')
        print('   • AFTER editing (final validation)')
        sys.exit(0)