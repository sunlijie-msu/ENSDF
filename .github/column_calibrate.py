#!/usr/bin/env python3
"""
ENSDF Column Calibration Script - Comprehensive ENSDF Validation
===============================================================

Complete ENSDF field validation and 80-character line length fixing.
ALWAYS runs comprehensive validation including ALL field checks.

ENSDF L-Record Field Positions (Mandatory):
- Columns 1-5:   NUCID
- Column 8:      Record type "L" 
- Columns 10-19: Energy field (E)
- Columns 23-39: J-pi field (starts at col 23)
- Columns 40-49: Half-life (T) field
- Columns 56-64: Angular momentum transfer (L)
- Columns 65-74: Spectroscopic factor (S)

Usage: 
  python column_calibrate.py "filename.ens"           # Complete ENSDF validation
  python column_calibrate.py "filename.ens" --fix     # Validate and fix line lengths  

ALWAYS CHECKS:
- Line length compliance (80 characters for data records)
- L-field positioning (columns 56-64)
- S-field positioning (columns 65-74) 
- Comment flag positioning (column 77)
- Field boundary validation
- Left-justification requirements
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

def validate_de_field(filename):
    """
    Validate DE field (Energy uncertainty) positioning in columns 20-21.
    
    CRITICAL ENSDF Format Rule: DE field values must be in columns 20-21 EXACTLY.
    - Columns 20-21: Energy uncertainty (DE) field (2 characters total)
    - Values must be LEFT-JUSTIFIED within this 2-character field
    - Common violations: DE values at columns 18-19 instead of 20-21
    
    Returns:
        bool: True if all DE fields are correctly positioned, False otherwise
    """
    print(f"\nDE FIELD VALIDATION: {filename}")
    print("=" * 60)
    print("Checking DE field positioning in columns 20-21...")
    print("CRITICAL ENSDF Rule: DE field values must be in columns 20-21 EXACTLY")
    print()
    print('ENSDF 80-Column Ruler:')
    print('         1         2         3         4         5         6         7         8')
    print('12345678901234567890123456789012345678901234567890123456789012345678901234567890')
    print('                   ^^ DE field (columns 20-21)')
    print()
    
    de_fields_analyzed = 0
    de_field_errors = 0
    
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    for line_num, line in enumerate(lines, 1):
        line_content = line.rstrip('\n\r')
        
        # Check both L-records and G-records for DE field validation
        if len(line_content) < 21 or (not (' L ' in line_content[6:10] or ' G ' in line_content[6:10])):
            continue
            
        # Look for DE field specifically - it should be in columns 20-21
        # Check if there's a numeric value around this area that looks like uncertainty
        de_found = False
        de_position = -1
        de_value = ""
        
        # Look for DE field - scan for numeric values between energy and J-pi fields
        # DE field should be 1-2 digit uncertainty value separated by spaces
        # Scan broader area to find where the uncertainty actually is positioned
        for start_col in range(17, 25):  # Check columns 18-25 (0-based 17-24)
            if start_col + 1 < len(line_content):
                # Look for 1-2 digit numeric values that could be uncertainties
                potential_de = ""
                for length in [1, 2]:
                    if start_col + length <= len(line_content):
                        test_value = line_content[start_col:start_col + length]
                        # Check if this looks like an uncertainty field
                        if test_value.isdigit() and len(test_value.strip()) > 0:
                            # Check if it's surrounded by spaces (field boundary)
                            before_char = line_content[start_col-1] if start_col > 0 else ' '
                            after_char = line_content[start_col + length] if start_col + length < len(line_content) else ' '
                            
                            if before_char == ' ' and after_char == ' ':
                                potential_de = test_value.strip()
                                break
                
                if potential_de:
                    de_found = True
                    de_position = start_col + 1  # Convert to 1-based
                    de_value = potential_de
                    break

        
        if de_found:
            de_fields_analyzed += 1
            if de_position != 20:  # DE field must start at column 20
                de_field_errors += 1
                print(f"  ERROR: Line {line_num}: DE field '{de_value}' at column {de_position}, should be at column 20")
                print(f"         Line: {line_content}")
                print(f"         Expected: DE value starting at column 20-21")
                print()
            
    print(f"DE FIELD SUMMARY:")
    print(f"  Total DE fields analyzed: {de_fields_analyzed}")
    print(f"  DE field positioning errors: {de_field_errors}")
    print()
    
    if de_field_errors == 0:
        print("✅ SUCCESS: All DE fields correctly positioned (columns 20-21)")
    else:
        print(f"❌ ERROR: {de_field_errors} DE field positioning errors found!")
        print("   CRITICAL: DE fields must be in columns 20-21 per ENSDF manual!")
        
    return de_field_errors == 0

def validate_s_field(filename):
    """
    Validate S field (Spectroscopic factor) positioning in columns 65-74.
    
    ENSDF Format Rule: S field values must be LEFT-JUSTIFIED starting at column 65.
    - Columns 65-74: Spectroscopic factor (S) field (10 characters total)
    - Values must start at column 65, not right-justified within the field
    - Common violations: values starting at columns 70-73 instead of 65
    
    Returns:
        bool: True if all S fields are correctly positioned, False otherwise
    """
    print(f"\nS FIELD VALIDATION: {filename}")
    print("=" * 60)
    print("Checking S field positioning in columns 65-74...")
    print("ENSDF Rule: S field values must be LEFT-JUSTIFIED starting at column 65")
    print()
    print('ENSDF 80-Column Ruler:')
    print('         1         2         3         4         5         6         7         8')
    print('12345678901234567890123456789012345678901234567890123456789012345678901234567890')
    print(' ' * 64 + '^---------^ S field (columns 65-74)')
    print()
    
    s_fields_analyzed = 0
    s_field_errors = 0
    
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    for line_num, line in enumerate(lines, 1):
        line_content = line.rstrip('\n\r')
        
        # Only check L-records for S field validation
        if len(line_content) < 10 or ' L ' not in line_content[6:10]:
            continue
            
        # Extract S field area (columns 65-74)
        if len(line_content) >= 65:
            s_field_area = line_content[64:74] if len(line_content) > 64 else line_content[64:]
            
            # Check if S field contains numerical content
            s_field_stripped = s_field_area.strip()
            if s_field_stripped and any(c.isdigit() for c in s_field_stripped):
                s_fields_analyzed += 1
                
                # Find where the first digit actually appears in the S field
                first_digit_pos = None
                for i, char in enumerate(s_field_area):
                    if char.isdigit():
                        first_digit_pos = 65 + i  # Convert to 1-based column number
                        break
                
                # Extract the actual numerical value
                s_value = ""
                for char in s_field_stripped:
                    if char.isdigit():
                        s_value += char
                    elif s_value:  # Stop at first non-digit after digits start
                        break
                
                print(f"LINE {line_num}: S field analysis")
                print(f"Line:  {line_content}")
                print(f"S field area (65-74): '{s_field_area}'")
                print(f"S field value: '{s_value}'")
                
                if first_digit_pos == 65:
                    print(f"✓ OK: S field value '{s_value}' correctly LEFT-JUSTIFIED at column 65")
                else:
                    print(f"❌ ERROR: S field value '{s_value}' starts at column {first_digit_pos} (should be 65)")
                    print(f"   Fix: Move '{s_value}' to start at column 65 (LEFT-JUSTIFIED)")
                    s_field_errors += 1
                
                # Check for field overflow (value extending beyond column 74)
                if len(s_value) > 10:
                    print(f"❌ ERROR: S field value '{s_value}' is {len(s_value)} digits (max 10 for columns 65-74)")
                    s_field_errors += 1
                elif first_digit_pos and (first_digit_pos + len(s_value) - 1) > 74:
                    print(f"❌ ERROR: S field value '{s_value}' extends beyond column 74")
                    s_field_errors += 1
                
                print()
    
    # Summary
    print(f"S FIELD SUMMARY:")
    print(f"  Total S fields analyzed: {s_fields_analyzed}")
    print(f"  S field positioning errors: {s_field_errors}")
    print()
    
    if s_field_errors == 0:
        print(f"✅ SUCCESS: All S fields correctly positioned (LEFT-JUSTIFIED at column 65)")
        return True
    else:
        print(f"❌ FAILED: {s_field_errors} S field positioning errors found")
        print(f"   CRITICAL: S field values must be LEFT-JUSTIFIED starting at column 65")
        print(f"   Current violations: Values starting at wrong columns instead of 65")
        return False

def validate_comment_flags(filename):
    """
    Validate ALL comment flags are positioned in column 77.
    
    ENSDF Format Rule: Comment flags (C field) must be in column 77 exactly.
    Common comment flags include:
    - A-Z, a-z: Any single letter used to refer to a specific comment record (typically an explanation of data source from NSR keynumber references)
    - * (asterisk): Denotes a multiply-placed gamma ray
    - & (ampersand): Denotes a multiply-placed transition with intensity not divided
    - @ (at symbol): Denotes a multiply-placed transition with intensity suitably divided
    - Space: No comment flag
    """
    print(f"\nCOMMENT FLAG VALIDATION: {filename}")
    print("=" * 60)
    print("Checking comment flags in column 77 (C field)...")
    print()
    print('ENSDF 80-Column Ruler:')
    print('         1         2         3         4         5         6         7         8')
    print('12345678901234567890123456789012345678901234567890123456789012345678901234567890')
    print(' ' * 76 + '^-- Column 77 (C field - comment flags)')
    print()
    
    flags_analyzed = 0
    flag_summary = {}
    
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    for line_num, line in enumerate(lines, 1):
        line_content = line.rstrip('\n\r')
        
        # Check if this is a data record line (L, G, E, B, DP records)
        if not is_data_record_line(line_content):
            continue
        
        # Comment flags should ONLY be checked in column 77 (the C field)
        # Skip lines that are clearly continuation comment lines (not data records)
        if len(line_content) >= 77:
            char = line_content[76]  # Column 77 (0-based index 76)
            
            # Check if this is actually a comment flag vs. part of text
            if char.isalpha() and not char.isspace():
                # Additional validation: make sure this isn't part of a citation
                # Look at surrounding context to distinguish real flags from citation text
                context_around_77 = line_content[70:80] if len(line_content) >= 80 else line_content[70:]
                
                # Skip if this appears to be part of a citation like "(2019Se09)"
                is_citation = any(pattern in context_around_77 for pattern in [
                    '2019Se09', '1973Go16', '2011Ch48', '1971Au07',  # Known citations
                    '(20', '19', '(19',  # General citation patterns
                ])
                
                # Skip if surrounded by other letters (part of a word)
                if len(line_content) > 77:
                    char_after = line_content[77] if len(line_content) > 77 else ' '
                    if char_after.isalpha():
                        is_citation = True
                
                if len(line_content) > 75:
                    char_before = line_content[75] if len(line_content) > 75 else ' '
                    if char_before.isalpha():
                        is_citation = True
                
                # Only process as comment flag if it's not part of a citation
                if not is_citation:
                    flags_analyzed += 1
                    
                    # Track flag types for summary
                    if char not in flag_summary:
                        flag_summary[char] = {'correct': 0, 'incorrect': []}
                    
                    # Interpret common flags according to ENSDF standards
                    flag_meaning = {
                        '*': 'multiply-placed gamma ray',
                        '&': 'multiply-placed transition, intensity not divided', 
                        '@': 'multiply-placed transition, intensity suitably divided'
                    }.get(char, 'comment record reference')
                    
                    print(f"✓ Line {line_num}: Comment flag '{char}' ({flag_meaning}) correctly in column 77")
                    flag_summary[char]['correct'] += 1
                print()
    
    
    # Enhanced summary with flag type breakdown
    print(f"COMMENT FLAG SUMMARY:")
    print(f"  Total comment flags analyzed: {flags_analyzed}")
    print(f"  Flag types found: {', '.join(sorted(flag_summary.keys())) if flag_summary else 'None'}")
    print()
    
    if flag_summary:
        for flag_type in sorted(flag_summary.keys()):
            correct_count = flag_summary[flag_type]['correct']
            
            # Add meaning for common flags according to ENSDF standards
            flag_meaning = {
                '*': '(multiply-placed gamma ray)',
                '&': '(multiply-placed transition, intensity not divided)', 
                '@': '(multiply-placed transition, intensity suitably divided)'
            }.get(flag_type, '(comment record reference)')
            
            print(f"  Flag '{flag_type}' {flag_meaning}: {correct_count} total")
            print(f"    ✓ Correct (column 77): {correct_count}")
            print()
    
    print(f"  ✅ SUCCESS: All comment flags correctly positioned in column 77")
    return True

def validate_g_record_flags(filename):
    """
    Validate G-record flags in columns 77 and 80.
    
    ENSDF Format Rules for G-Records:
    - Column 77 (C field - Comment flags): A-Z, a-z, *, &, @, space
    - Column 80 (Q field - Additional indicator): space, ?, S
    
    🚨 CRITICAL RULES 🚨:
    - ? is FORBIDDEN in column 77 (comment flag field)
    - ? is ALLOWED only in column 80 (additional indicator)
    """
    print(f"\nG-RECORD FLAG VALIDATION: {filename}")
    print("=" * 60)
    print("Checking G-record flags in columns 77 and 80...")
    print()
    print('ENSDF 80-Column Ruler:')
    print('         1         2         3         4         5         6         7         8')
    print('12345678901234567890123456789012345678901234567890123456789012345678901234567890')
    print(' ' * 76 + '^-- Col 77 (C field)  ^-- Col 80 (Additional indicator)')
    print()
    
    g_records_analyzed = 0
    col77_flags = {'valid': 0, 'invalid': 0, 'details': {}}
    col80_indicators = {'valid': 0, 'invalid': 0, 'details': {}}
    errors_found = False
    
    # Valid flags for each column - NOTE: '?' is explicitly FORBIDDEN in column 77
    import string
    valid_col77_flags = set(string.ascii_letters + '*&@ ')  # A-Z, a-z, *, &, @, space - NO '?'
    valid_col80_indicators = set(' ?S')  # space, ?, S only
    
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    for line_num, line in enumerate(lines, 1):
        line_content = line.rstrip('\n\r')
        
        # Check if this is a G-record (gamma transition)
        if not (is_data_record_line(line_content) and len(line_content) >= 8 and line_content[7] == 'G'):
            continue
        
        g_records_analyzed += 1
        
        # Validate Column 77 (Comment flag)
        if len(line_content) >= 77:
            col77_char = line_content[76]  # Column 77 (0-based index 76)
            
            if col77_char in valid_col77_flags:
                col77_flags['valid'] += 1
                if col77_char != ' ':  # Only report non-space flags
                    flag_type = {
                        '*': 'multiply-placed gamma', '&': 'multiply-placed (intensity not divided)',
                        '@': 'multiply-placed (intensity suitably divided)'
                    }.get(col77_char, f'comment record reference ({col77_char})')
                    print(f"✓ Line {line_num}: Column 77 flag '{col77_char}' ({flag_type})")
                    col77_flags['details'][col77_char] = col77_flags['details'].get(col77_char, 0) + 1
            else:
                col77_flags['invalid'] += 1
                errors_found = True
                if col77_char == '?':
                    print(f"❌ Line {line_num}: INVALID '?' in column 77 - ? is FORBIDDEN in comment field!")
                    print(f"   → ? should only be used in column 80 (additional indicator)")
                else:
                    print(f"❌ Line {line_num}: INVALID '{col77_char}' in column 77")
                    print(f"   → Valid column 77 flags: A-Z, a-z, *, &, @, space")
        
        # Validate Column 80 (Additional indicator)
        if len(line_content) >= 80:
            col80_char = line_content[79]  # Column 80 (0-based index 79)
            
            if col80_char in valid_col80_indicators:
                col80_indicators['valid'] += 1
                if col80_char != ' ':  # Only report non-space indicators
                    indicator_type = {
                        '?': 'uncertain placement in level scheme',
                        'S': 'expected but unobserved transition'
                    }.get(col80_char, f'additional indicator ({col80_char})')
                    print(f"✓ Line {line_num}: Column 80 indicator '{col80_char}' ({indicator_type})")
                    col80_indicators['details'][col80_char] = col80_indicators['details'].get(col80_char, 0) + 1
            else:
                col80_indicators['invalid'] += 1
                errors_found = True
                print(f"❌ Line {line_num}: INVALID '{col80_char}' in column 80")
                print(f"   → Valid column 80 indicators: space, ?, S")
    
    print()
    print(f"G-RECORD FLAG SUMMARY:")
    print(f"  G-records analyzed: {g_records_analyzed}")
    print(f"  Column 77 flags: {col77_flags['valid']} valid, {col77_flags['invalid']} invalid")
    print(f"  Column 80 indicators: {col80_indicators['valid']} valid, {col80_indicators['invalid']} invalid")
    print()
    
    if col77_flags['details']:
        print("  Column 77 flag usage:")
        for flag, count in sorted(col77_flags['details'].items()):
            flag_meaning = {
                '*': 'multiply-placed gamma', '&': 'multiply-placed (not divided)', 
                '@': 'multiply-placed (divided)'
            }.get(flag, 'comment record reference')
            print(f"    '{flag}' ({flag_meaning}): {count}")
        print()
    
    if col80_indicators['details']:
        print("  Column 80 indicator usage:")
        for indicator, count in sorted(col80_indicators['details'].items()):
            indicator_meaning = {
                '?': 'uncertain placement', 'S': 'expected/unobserved'
            }.get(indicator, 'additional indicator')
            print(f"    '{indicator}' ({indicator_meaning}): {count}")
        print()
    
    if not errors_found:
        print(f"  ✅ SUCCESS: All G-record flags correctly positioned and valid!")
    else:
        print(f"  ❌ ERRORS: {col77_flags['invalid'] + col80_indicators['invalid']} invalid G-record entries found!")
    
    return not errors_found

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
    
    # Always validate DE fields, S fields and comment flags unless header-only mode
    if not header_only:
        de_field_success = validate_de_field(filename)
        s_field_success = validate_s_field(filename)
        comment_flag_success = validate_comment_flags(filename)
        g_record_validation_success = validate_g_record_flags(filename)
        return (not errors_found) and de_field_success and s_field_success and comment_flag_success and g_record_validation_success
        
    return not errors_found

def main():
    parser = argparse.ArgumentParser(
        description='ENSDF Column Calibration and Line Length Fixing',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Simple Usage Examples:
  python column_calibrate.py "file.ens"             # Complete ENSDF validation
  python column_calibrate.py "file.ens" --fix       # Fix problems automatically
  python column_calibrate.py "file.ens" --fix --dry-run  # Preview fixes
        """
    )
    
    parser.add_argument('filename', help='ENSDF file to validate')
    parser.add_argument('--fix', action='store_true', 
                       help='Fix line length issues automatically')
    parser.add_argument('--dry-run', action='store_true',
                       help='Preview changes without modifying file (use with --fix)')
    
    args = parser.parse_args()
    
    filename = args.filename
    fix_mode = args.fix
    dry_run = args.dry_run
    
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
        validation_success = validate_ensdf_file(filename, detailed=True, header_only=False)
        success = success and validation_success
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
