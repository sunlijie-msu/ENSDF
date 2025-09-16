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
- Columns 23-39: J-pi field (starts at col 23)
- Columns 40-49: Half-life (T) field
- Columns 56-64: Angular momentum transfer (L)
- Columns 65-74: Spectroscopic factor (S)

Usage: 
  python column_calibrate.py "filename.ens"                  # Validate only
  python column_calibrate.py "filename.ens" --fix            # Validate and fix line lengths  
  python column_calibrate.py "filename.ens" --detailed       # Detailed character mapping
  python column_calibrate.py "filename.ens" --header         # Header format check only
  python column_calibrate.py "filename.ens" --comment-flags   # Comment flags (P, D, T, C, etc.)
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
        print(f"\nSUCCESS: File updated: {filename}")
        print("SUCCESS: All data record lines now exactly 80 characters")
    elif dry_run and lines_modified > 0:
        print(f"\nDRY RUN: Would modify {lines_modified} data record lines")
    elif lines_modified == 0:
        print("\nSUCCESS: All data record lines already exactly 80 characters - no changes needed")
    
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

def validate_comment_flags(filename):
    """
    Validate ALL comment flags are positioned in column 77.
    
    ENSDF Format Rule: Comment flags (C field) must be in column 77 exactly.
    Common comment flags include:
    - P = Possible level (uncertain assignment)
    - D = Doublet (two unresolved peaks) 
    - T = Triplet (three unresolved peaks)
    - C = Coincidence information
    - Other alphabetic characters for various comments
    """
    print(f"\nCOMMENT FLAG VALIDATION: {filename}")
    print("=" * 60)
    print("Checking comment flags in column 77 (C field)...")
    print("Common flags: P=possible, D=doublet, T=triplet, C=coincidence")
    print()
    print('ENSDF 80-Column Ruler:')
    print('         1         2         3         4         5         6         7         8')
    print('12345678901234567890123456789012345678901234567890123456789012345678901234567890')
    print(' ' * 76 + '^-- Column 77 (C field - comment flags)')
    print()
    
    errors_found = False
    flags_analyzed = 0
    flag_summary = {}
    misplaced_flags = []
    
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    for line_num, line in enumerate(lines, 1):
        line_content = line.rstrip('\n\r')
        
        # Check if this is a data record line (L, G, E, B, DP records)
        if not is_data_record_line(line_content):
            continue
        
        # Check columns 75-80 for ANY alphabetic characters (potential comment flags)
        for col in range(75, min(len(line_content), 81)):  # Check columns 75-80
            char = line_content[col - 1]  # Convert to 0-based index
            
            # ANY alphabetic character could be a comment flag
            if char.isalpha():
                flags_analyzed += 1
                
                # Track flag types for summary
                if char not in flag_summary:
                    flag_summary[char] = {'correct': 0, 'incorrect': []}
                
                if col == 77:
                    # Interpret common flags
                    flag_meaning = {
                        'P': 'possible level', 'D': 'doublet', 'T': 'triplet', 
                        'C': 'coincidence', 'S': 'predicted', '?': 'uncertain'
                    }.get(char, 'comment')
                    
                    print(f"✓ Line {line_num}: Comment flag '{char}' ({flag_meaning}) correctly in column 77")
                    flag_summary[char]['correct'] += 1
                else:
                    print(f"✗ Line {line_num}: Comment flag '{char}' INCORRECTLY positioned in column {col}")
                    print(f"   Expected: column 77 (C field), Actual: column {col}")
                    print(f"   Line content: {line_content}")
                    print(f"   {' ' * (col - 1)}^(actual: {col})")
                    print(f"   {' ' * 76}^(required: 77)")
                    flag_summary[char]['incorrect'].append((line_num, col))
                    misplaced_flags.append((line_num, char, col))
                    errors_found = True
                print()
    
    # Enhanced summary with flag type breakdown
    print(f"COMMENT FLAG SUMMARY:")
    print(f"  Total comment flags analyzed: {flags_analyzed}")
    print(f"  Flag types found: {', '.join(sorted(flag_summary.keys())) if flag_summary else 'None'}")
    print()
    
    if flag_summary:
        for flag_type in sorted(flag_summary.keys()):
            correct_count = flag_summary[flag_type]['correct']
            incorrect_list = flag_summary[flag_type]['incorrect']
            total_count = correct_count + len(incorrect_list)
            
            # Add meaning for common flags
            flag_meaning = {
                'P': '(possible level)', 'D': '(doublet)', 'T': '(triplet)', 
                'C': '(coincidence)', 'S': '(predicted)', '?': '(uncertain)'
            }.get(flag_type, '(comment)')
            
            print(f"  Flag '{flag_type}' {flag_meaning}: {total_count} total")
            print(f"    ✓ Correct (column 77): {correct_count}")
            if incorrect_list:
                print(f"    ✗ Incorrect positions: {len(incorrect_list)}")
                for line_num, pos in incorrect_list:
                    print(f"      Line {line_num}: column {pos}")
            print()
    
    if errors_found:
        print(f"  🚨 ERROR: {len(misplaced_flags)} comment flags incorrectly positioned")
        print(f"  📏 CRITICAL: ALL comment flags must be in column 77 (C field)")
        return False
    else:
        print(f"  ✅ SUCCESS: All comment flags correctly positioned in column 77")
        return True

def validate_band_flags(filename):
    """
    DEPRECATED: Use validate_comment_flags() instead.
    This function only checked limited band flags and missed P, D, and other comment flags.
    """
    print(f"\n⚠️  WARNING: validate_band_flags() is deprecated")
    print(f"   Use validate_comment_flags() for comprehensive comment flag validation")
    print(f"   The old function only checked A,B,b,C,c and missed P,D,T comment flags!")
    print()
    
    # Call the enhanced function instead
    return validate_comment_flags(filename)

def validate_ensdf_file(filename, detailed=False, header_only=False):
    """Validate ENSDF file field positions focusing on data record lines."""
    
    if not os.path.exists(filename):
        print(f"ERROR: File {filename} not found!")
        return False
        
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
        print("\nUSE --fix flag to automatically correct data record line lengths")
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
            # Examples: L=1 -> 1 at col 56
            #          L=1+2 -> 1 at col 56, +2 at col 57-58  
            #          L=1,2 -> 1 at col 56, ,2 at col 57-58
            #          L=1,2,3 -> 1 at col 56, ,2 at col 57-58, ,3 at col 59-60
            
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
    
    # Always validate comment flags unless header-only mode
    if not header_only:
        comment_flag_success = validate_comment_flags(filename)
        return (not errors_found) and comment_flag_success
        
    return not errors_found

def main():
    parser = argparse.ArgumentParser(
        description='ENSDF Column Calibration and Line Length Fixing',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python column_calibrate.py "file.ens"                  # Validate only
  python column_calibrate.py "file.ens" --fix            # Fix line lengths
  python column_calibrate.py "file.ens" --detailed       # Detailed analysis
  python column_calibrate.py "file.ens" --header         # Header check only
  python column_calibrate.py "file.ens" --comment-flags      # Comment flags (P, D, T, C, etc.)
  python column_calibrate.py "file.ens" --band-only        # Band flags only (DEPRECATED)
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
                       help='Check band flag positioning only (DEPRECATED - use --comment-flags)')
    parser.add_argument('--comment-flags', action='store_true',
                       help='Check comment flag positioning (P=possible, D=doublet, T=triplet, etc.)')
    
    args = parser.parse_args()
    
    filename = args.filename
    fix_mode = args.fix
    dry_run = args.dry_run
    detailed = args.detailed
    header_only = args.header
    band_only = args.band_only
    terminal_only = args.comment_flags
    
    if not os.path.exists(filename):
        print(f"ERROR: File '{filename}' not found!")
        sys.exit(1)
    
    success = True
    
    # Handle comment-flags-only mode
    if terminal_only:
        comment_success = validate_comment_flags(filename)
        sys.exit(0 if comment_success else 1)
    
    # Handle deprecated band-only mode with warning
    if band_only:
        print("⚠️  WARNING: --band-only is deprecated. Use --comment-flags for comprehensive comment flag validation")
        band_success = validate_band_flags(filename)  # This now calls validate_comment_flags internally
        sys.exit(0 if band_success else 1)
    
    # Fix line lengths if requested
    if fix_mode:
        lines_fixed, errors = fix_line_lengths(filename, dry_run=dry_run)
        if errors > 0:
            success = False
        print()
    
    # Always validate after fixing (or just validate if no fix)
    if not dry_run:  # Skip validation during dry run to avoid redundant output
        validation_success = validate_ensdf_file(filename, detailed=detailed, header_only=header_only, band_only=False)
        success = success and validation_success
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
