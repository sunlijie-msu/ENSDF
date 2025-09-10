#!/usr/bin/env python3
"""
ENSDF Column Calibration Script - Enhanced with Line Length Fixing
=================================================================

Advanced ENSDF field validation and 80-character line length fixing.
Validates ENSDF field positions and can automatically fix line length issues.

ENSDF L-Record Field Positions (Mandatory):
- Columns 1-5:   NUCID
- Column 8:      Record type "L" 
- Columns 10-19: Energy field (E)
- Columns 23-39: J-π field (starts at col 23)
- Columns 40-49: Half-life (T) field
- Columns 56-64: Angular momentum transfer (L)
- Columns 65-74: Spectroscopic factor (S)

Usage: 
  python column_calibrate.py "filename.ens"              # Validate only
  python column_calibrate.py "filename.ens" --fix        # Validate and fix line lengths
  python column_calibrate.py "filename.ens" --detailed   # Detailed character mapping
  python column_calibrate.py "filename.ens" --header     # Header format check only
"""

import sys
import os
import argparse

def is_data_record_line(line):
    """
    Check if a line is a data record line (L, G, E, B, DP records).
    These are the lines that must be exactly 80 characters.
    Comment lines are handled by separate tools.
    """
    if len(line) < 8:
        return False
    
    # Check for data record types in column 8 (0-based index 7)
    record_type = line[7] if len(line) > 7 else ' '
    data_record_types = ['L', 'G', 'E', 'B']  # Main data record types
    
    # Also check for DP records (delayed proton)
    if len(line) > 8 and line[7:9] == 'DP':
        return True
        
    return record_type in data_record_types

def fix_line_lengths(filename, dry_run=False):
    """
    Fix ENSDF file line lengths to be exactly 80 characters.
    Only processes data record lines (L, G, E, B, DP records).
    Comment lines are handled by separate tools.
    
    Args:
        filename: Path to ENSDF file
        dry_run: If True, only report what would be changed without modifying file
        
    Returns:
        tuple: (lines_fixed, errors_found)
    """
    
    if not os.path.exists(filename):
        print(f"ERROR: File {filename} not found!")
        return 0, 1
        
    print(f"{'DRY RUN - ' if dry_run else ''}Fixing data record line lengths in: {filename}")
    print("=" * 70)
    print("Note: Only checking L, G, E, B, and DP record lines (data records)")
    print("      Comment lines are handled by separate tools")
    print()
    
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    fixed_lines = []
    lines_modified = 0
    issues_found = []
    
    for line_num, line in enumerate(lines, 1):
        original_line = line
        line_content = line.rstrip('\n\r')  # Remove only line endings
        current_length = len(line_content)
        
        # Only process data record lines
        if not is_data_record_line(line_content):
            # Keep non-data lines as-is (comment lines, headers, etc.)
            fixed_lines.append(line)
            continue
        
        if current_length == 80:
            # Perfect length - keep as is
            fixed_lines.append(line_content + '\n')
        elif current_length < 80:
            # Too short - pad with spaces to 80 characters
            padded_line = line_content.ljust(80)
            fixed_lines.append(padded_line + '\n')
            lines_modified += 1
            issues_found.append((line_num, 'SHORT', current_length, 80 - current_length))
            if not dry_run:
                print(f"Line {line_num}: {line_content[7]} record - Padded {80 - current_length} spaces (was {current_length} chars)")
        elif current_length > 80:
            # Too long - trim to exactly 80 characters
            trimmed_line = line_content[:80]
            fixed_lines.append(trimmed_line + '\n')
            lines_modified += 1
            issues_found.append((line_num, 'LONG', current_length, current_length - 80))
            if not dry_run:
                print(f"Line {line_num}: {line_content[7]} record - Trimmed {current_length - 80} characters (was {current_length} chars)")
    
    # Remove any trailing empty lines
    while fixed_lines and fixed_lines[-1].strip() == '':
        removed_line = fixed_lines.pop()
        lines_modified += 1
        if not dry_run:
            print(f"Removed trailing empty line")
    
    # Summary
    print(f"\nSummary:")
    print(f"  Total lines processed: {len(lines)}")
    print(f"  Data record lines modified: {lines_modified}")
    
    if issues_found:
        print(f"\nData record issues fixed:")
        short_lines = [x for x in issues_found if x[1] == 'SHORT']
        long_lines = [x for x in issues_found if x[1] == 'LONG']
        
        if short_lines:
            print(f"  Short data records padded: {len(short_lines)}")
        if long_lines:
            print(f"  Long data records trimmed: {len(long_lines)}")
    
    # Write fixed file if not dry run
    if not dry_run and lines_modified > 0:
        with open(filename, 'w') as f:
            f.writelines(fixed_lines)
        print(f"\n✅ File updated: {filename}")
        print("✅ All data record lines now exactly 80 characters")
    elif dry_run and lines_modified > 0:
        print(f"\n📋 DRY RUN: Would modify {lines_modified} data record lines")
    elif lines_modified == 0:
        print("\n✅ All data record lines already exactly 80 characters - no changes needed")
    
    return lines_modified, 0

def print_ruler():
    """Print the 80-column ruler for visual reference."""
    print('ENSDF 80-Column Ruler:')
    print('Ones:  12345678901234567890123456789012345678901234567890123456789012345678901234567890')
    print('Tens:  1111111111222222222233333333334444444444555555555566666666667777777777888888888999')

def find_field_positions(line, field_chars):
    """Find positions of specific characters that represent field values."""
    positions = []
    for i, char in enumerate(line, 1):
        if char in field_chars and i > 50:  # Look for L-transfer fields after col 50
            positions.append(i)
    return positions

def validate_band_flags(filename):
    """Validate band assignment flags are positioned in column 77"""
    print(f"\nBAND FLAG VALIDATION: {filename}")
    print("=" * 60)
    print("Checking band assignment flags (A, B, b, C, c) in column 77...")
    print()
    print('ENSDF 80-Column Ruler:')
    print('         1         2         3         4         5         6         7         8')
    print('12345678901234567890123456789012345678901234567890123456789012345678901234567890')
    print(' ' * 76 + '^-- Column 77 (required position)')
    print()
    
    band_flags = ['A', 'B', 'b', 'C', 'c']
    errors_found = False
    flags_analyzed = 0
    
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    for line_num, line in enumerate(lines, 1):
        line_content = line.rstrip('\n\r')
        
        # Check if this is an L-record with potential band flags
        if len(line_content) < 10 or ' L ' not in line_content[6:10]:
            continue
        
        # Look for band flags anywhere in the line after column 70
        flag_found = None
        flag_position = None
        
        for i, char in enumerate(line_content[70:], 71):
            if char in band_flags:
                flag_found = char
                flag_position = i
                break
        
        if flag_found:
            flags_analyzed += 1
            if flag_position == 77:
                print(f"OK Line {line_num}: Band flag '{flag_found}' correctly positioned in column 77")
            else:
                print(f"ERROR Line {line_num}: Band flag '{flag_found}' INCORRECTLY positioned in column {flag_position}")
                print(f"   Expected: column 77, Actual: column {flag_position}")
                print(f"   Line content: {line_content}")
                print(f"   {' ' * (flag_position - 1)}^(actual: {flag_position})")
                print(f"   {' ' * 76}^(required: 77)")
                errors_found = True
            print()
    
    print(f"BAND FLAG SUMMARY:")
    print(f"  Total L-records with band flags analyzed: {flags_analyzed}")
    
    if errors_found:
        print(f"  ERROR: Some band flags incorrectly positioned")
        print(f"  All band flags must be in column 77 exactly")
        return False
    else:
        print(f"  SUCCESS: All band flags correctly positioned in column 77")
        return True

def validate_ensdf_file(filename, detailed=False, header_only=False, band_only=False):
    """Validate ENSDF file field positions focusing on data record lines."""
    
    if not os.path.exists(filename):
        print(f"ERROR: File {filename} not found!")
        return False
    
    if band_only:
        return validate_band_flags(filename)
        
    print(f"Validating ENSDF file: {filename}")
    print("=" * 60)
    print_ruler()
    print()
    
    errors_found = False
    
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    # Check for line length issues in data record lines only
    length_issues = []
    for line_num, line in enumerate(lines, 1):
        line_content = line.rstrip('\n\r')
        length = len(line_content)
        
        # Only check data record lines for 80-character compliance
        if is_data_record_line(line_content) and length != 80:
            length_issues.append((line_num, length, line_content[7] if len(line_content) > 7 else '?'))
    
    if length_issues:
        print("DATA RECORD LINE LENGTH ISSUES DETECTED:")
        for line_num, length, record_type in length_issues:
            if length < 80:
                print(f"  Line {line_num}: {record_type} record - {length} chars (short by {80 - length})")
            else:
                print(f"  Line {line_num}: {record_type} record - {length} chars (long by {length - 80})")
        print("\n💡 Use --fix flag to automatically correct data record line lengths")
        print("   Example: python column_calibrate.py \"filename.ens\" --fix")
        print("   Note: Comment lines are handled by separate tools")
        print()
        errors_found = True
    
    if header_only:
        return not errors_found
    
    for line_num, line in enumerate(lines, 1):
        # Skip short lines and non-L records for L-field validation
        if len(line) < 10 or ' L ' not in line[6:10]:
            continue
            
        # Look for L-transfer field (typically around column 56)
        l_field_text = ""
        if len(line) > 60:
            # Extract potential L-field content (columns 56-64)
            l_field_content = line[55:64].strip()  # 0-based indexing: col 56-64 = index 55-63
            
            # Check if this contains L-transfer values (digits, commas, parentheses)
            if l_field_content and any(c.isdigit() for c in l_field_content):
                # Check if it's really L-transfer (not energy, uncertainty, etc.)
                if not any(x in l_field_content for x in ['keV', 'eV', 'MeV', '.']):
                    l_field_text = l_field_content
        
        # Report L-field positioning
        if l_field_text:
            print(f"LINE {line_num}: L-transfer field analysis")
            print(f"Line:  {line.rstrip()}")
            if detailed:
                print_ruler()
            
            # CORRECT L-field validation logic based on user specification:
            # Rule: L always starts from col 56
            # Examples: L=1 → 1 at col 56
            #          L=1+2 → 1 at col 56, +2 at col 57-58  
            #          L=1,2 → 1 at col 56, ,2 at col 57-58
            #          L=1,2,3 → 1 at col 56, ,2 at col 57-58, ,3 at col 59-60
            
            # Check if the first character of L-field is at column 56
            first_char_at_56 = line[55] if len(line) > 55 else ' '  # Column 56 (0-based index 55)
            
            if first_char_at_56.isdigit():
                # Good: First L-value starts at column 56
                print(f"OK L={l_field_text} correctly positioned at column 56")
            elif l_field_text and l_field_text[0].isdigit():
                # L-field has content but doesn't start at column 56
                # Find where it actually starts
                actual_start_pos = None
                for i, char in enumerate(line[55:64], 56):  # Search columns 56-64
                    if char.isdigit():
                        actual_start_pos = i
                        break
                if actual_start_pos:
                    print(f"ERROR L={l_field_text} incorrectly positioned at column {actual_start_pos} (should be 56)")
                    errors_found = True
                else:
                    print(f"WARNING: Could not determine L-field position for '{l_field_text}'")
            else:
                print(f"WARNING: L-field content '{l_field_text}' doesn't start with digit")
            print()
    
    if not errors_found:
        print("SUCCESS: All ENSDF field positions appear correct!")
        if length_issues == []:  # No length issues either
            print("SUCCESS: All data record lines are exactly 80 characters!")
    else:
        print("ERROR: Field positioning errors found - see details above")
    
    # Always validate band flags unless header-only mode
    if not header_only:
        band_success = validate_band_flags(filename)
        return (not errors_found) and band_success
        
    return not errors_found

def main():
    parser = argparse.ArgumentParser(
        description='ENSDF Column Calibration and Line Length Fixing',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python column_calibrate.py "file.ens"              # Validate only
  python column_calibrate.py "file.ens" --fix        # Fix line lengths
  python column_calibrate.py "file.ens" --detailed   # Detailed analysis
  python column_calibrate.py "file.ens" --header     # Header check only
  python column_calibrate.py "file.ens" --band-only  # Band flags only
  python column_calibrate.py "file.ens" --fix --dry-run  # Preview changes
        """
    )
    
    parser.add_argument('filename', help='ENSDF file to process')
    parser.add_argument('--fix', action='store_true', 
                       help='Fix line lengths to exactly 80 characters')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be changed without modifying file')
    parser.add_argument('--detailed', action='store_true',
                       help='Show detailed character mapping with ruler')
    parser.add_argument('--header', action='store_true',
                       help='Check header format only')
    parser.add_argument('--band-only', action='store_true',
                       help='Check band flag positioning only')
    
    args = parser.parse_args()
    
    filename = args.filename
    fix_mode = args.fix
    dry_run = args.dry_run
    detailed = args.detailed
    header_only = args.header
    band_only = args.band_only
    
    if not os.path.exists(filename):
        print(f"ERROR: File '{filename}' not found!")
        sys.exit(1)
    
    success = True
    
    # Fix line lengths if requested
    if fix_mode:
        lines_fixed, errors = fix_line_lengths(filename, dry_run=dry_run)
        if errors > 0:
            success = False
        print()
    
    # Always validate after fixing (or just validate if no fix)
    if not dry_run:  # Skip validation during dry run to avoid redundant output
        validation_success = validate_ensdf_file(filename, detailed=detailed, header_only=header_only, band_only=band_only)
        success = success and validation_success
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
