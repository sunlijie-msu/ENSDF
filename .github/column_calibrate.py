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
    
    CORRECTED ENSDF Format Rule: DE field values must be in columns 20-21 EXACTLY.
    - Columns 20-21: Energy uncertainty (DE) field (2 characters total)
    - DE fields can be EMPTY (blank) - this is perfectly valid in ENSDF
    - Only check DE field positioning if there is actual content in columns 20-21
    - DO NOT confuse RI (Relative Intensity) fields with DE fields!
    
    CRITICAL FIX: Previous version incorrectly identified RI values as misplaced DE fields.
    
    Returns:
        bool: True if all DE fields are correctly positioned, False otherwise
    """
    print(f"\nDE FIELD VALIDATION: {filename}")
    print("=" * 60)
    print("Checking DE field positioning in columns 20-21...")
    print("CORRECTED ENSDF Rule: DE field values must be in columns 20-21 EXACTLY")
    print("NOTE: DE fields can be EMPTY (this is valid in ENSDF format)")
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
            
        # CORRECTED LOGIC: Only check DE field if there's actual content in columns 20-21
        # Extract exactly columns 20-21 (0-based indices 19-20)
        if len(line_content) >= 21:
            de_field_content = line_content[19:21]  # Columns 20-21 (0-based 19-20)
            
            # Only validate if DE field has content (not just spaces)
            if de_field_content.strip():
                de_fields_analyzed += 1
                de_value = de_field_content.strip()
                
                # Check if content is numeric (typical for uncertainty values)
                if not de_value.isdigit():
                    de_field_errors += 1
                    print(f"  ERROR: Line {line_num}: Non-numeric DE field '{de_value}' in columns 20-21")
                    print(f"         Line: {line_content}")
                    print(f"         Expected: Numeric uncertainty value or blank")
                    print()
            # If DE field is blank/empty, that's perfectly valid - no error
            
    print(f"DE FIELD SUMMARY:")
    print(f"  Total DE fields with content analyzed: {de_fields_analyzed}")
    print(f"  DE field content errors: {de_field_errors}")
    print()
    
    if de_field_errors == 0:
        print("[OK] SUCCESS: All DE fields correctly positioned and formatted (columns 20-21)")
        print("   Note: Empty DE fields are valid and were not flagged as errors")
    else:
        print(f"[ERROR] ERROR: {de_field_errors} DE field content errors found!")
        print("   CRITICAL: DE fields must contain only numeric uncertainties or be blank!")
        
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
                    print(f"[OK] OK: S field value '{s_value}' correctly LEFT-JUSTIFIED at column 65")
                else:
                    print(f"[ERROR] ERROR: S field value '{s_value}' starts at column {first_digit_pos} (should be 65)")
                    print(f"   Fix: Move '{s_value}' to start at column 65 (LEFT-JUSTIFIED)")
                    s_field_errors += 1
                
                # Check for field overflow (value extending beyond column 74)
                if len(s_value) > 10:
                    print(f"[ERROR] ERROR: S field value '{s_value}' is {len(s_value)} digits (max 10 for columns 65-74)")
                    s_field_errors += 1
                elif first_digit_pos and (first_digit_pos + len(s_value) - 1) > 74:
                    print(f"[ERROR] ERROR: S field value '{s_value}' extends beyond column 74")
                    s_field_errors += 1
                
                print()
    
    # Summary
    print(f"S FIELD SUMMARY:")
    print(f"  Total S fields analyzed: {s_fields_analyzed}")
    print(f"  S field positioning errors: {s_field_errors}")
    print()
    
    if s_field_errors == 0:
        print(f"[OK] SUCCESS: All S fields correctly positioned (LEFT-JUSTIFIED at column 65)")
        return True
    else:
        print(f"[ERROR] FAILED: {s_field_errors} S field positioning errors found")
        print(f"   CRITICAL: S field values must be LEFT-JUSTIFIED starting at column 65")
        print(f"   Current violations: Values starting at wrong columns instead of 65")
        return False

def validate_jp_field(filename):
    """
    Validate J-π (spin-parity) field positioning in L-records.
    
    ENSDF Format Rule: J-π field MUST be LEFT-JUSTIFIED starting at column 23.
    
    The J-π field occupies columns 23-39 and contains spin-parity assignments like:
    - 3/2+ (firm assignment)
    - (3/2+) (tentative assignment)
    - 3/2+,5/2+ (multiple possibilities)
    - 7/2(+) (firm spin, tentative parity)
    - (5/2,7/2)+ (multiple tentative spins, firm parity)
    
    CRITICAL: J-π values must START at column 23 with NO leading spaces!
    """
    print(f"\nJ-π FIELD VALIDATION: {filename}")
    print("=" * 60)
    print("Checking J-π field positioning in columns 23-39...")
    print("ENSDF Rule: J-π field values must be LEFT-JUSTIFIED starting at column 23")
    print()
    print('ENSDF 80-Column Ruler:')
    print('         1         2         3         4         5         6         7         8')
    print('12345678901234567890123456789012345678901234567890123456789012345678901234567890')
    print(' ' * 22 + '^----------------^ J-π field (columns 23-39)')
    print()
    
    jp_fields_analyzed = 0
    jp_field_errors = 0
    
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    for line_num, line in enumerate(lines, 1):
        line_content = line.rstrip('\n\r')
        
        # Only check L-records for J-π field validation
        if len(line_content) < 10 or ' L ' not in line_content[6:10]:
            continue
        
        # Skip comment lines
        if is_comment_line(line_content):
            continue
            
        # Extract J-π field area (columns 23-39)
        if len(line_content) >= 23:
            jp_field_area = line_content[22:39] if len(line_content) > 22 else line_content[22:]
            
            # Check if J-π field contains content (not just spaces)
            jp_field_stripped = jp_field_area.strip()
            if jp_field_stripped:
                jp_fields_analyzed += 1
                
                # Check if J-π field starts at column 23 (no leading space at index 22)
                if line_content[22] != ' ':  # Column 23 (0-based index 22)
                    print(f"[OK] Line {line_num:3d}: J-π='{jp_field_stripped}' correctly LEFT-JUSTIFIED at column 23")
                else:
                    # J-π has leading space(s) - this is an error!
                    # Find where it actually starts
                    first_nonspace = None
                    for i, char in enumerate(jp_field_area):
                        if char != ' ':
                            first_nonspace = 23 + i  # Convert to 1-based column
                            break
                    
                    print(f"[ERROR] Line {line_num:3d}: ERROR - J-π='{jp_field_stripped}' has leading space(s)")
                    print(f"   Current position: starts at column {first_nonspace}")
                    print(f"   Required position: must start at column 23 (LEFT-JUSTIFIED)")
                    print(f"   Line: {line_content}")
                    jp_field_errors += 1
                    print()
    
    # Summary
    print(f"J-π FIELD SUMMARY:")
    print(f"  Total J-π fields analyzed: {jp_fields_analyzed}")
    print(f"  J-π field positioning errors: {jp_field_errors}")
    print()
    
    if jp_field_errors == 0:
        print(f"[OK] SUCCESS: All J-π fields correctly LEFT-JUSTIFIED at column 23")
        return True
    else:
        print(f"[ERROR] FAILED: {jp_field_errors} J-π field positioning errors found")
        print(f"   CRITICAL: J-π field values must be LEFT-JUSTIFIED starting at column 23")
        print(f"   Current violations: J-π values have leading spaces instead of starting at column 23")
        return False

def is_comment_line(line):
    """
    Check if a line is a comment line (cL, cG, cE, etc.).
    Comment lines have lowercase 'c' followed by record type letter.
    
    Examples of comment lines:
    - ' 35CL  cL ...' (spaces, then 'c' at column 7, 'L' at column 8)
    - ' 35CL  cG ...' (spaces, then 'c' at column 7, 'G' at column 8)
    - ' 35CL2 cG ...' (digit at column 6, 'c' at column 7, 'G' at column 8)
    - ' 35CL5cG ...' (digit at column 6, 'c' at column 7, 'G' at column 8)
    
    The pattern is: lowercase 'c' at column 7 (0-based index 6) followed by
    a record type letter (L, G, E, B, etc.) at column 8 (0-based index 7).
    
    These lines should NEVER be checked for column 77 flags!
    """
    if len(line) < 8:
        return False
    
    # Check for 'c' at column 7 (0-based index 6) followed by letter at column 8
    if line[6] == 'c' and line[7].isalpha() and line[7].isupper():
        return True
        
    return False

def validate_mul_field(filename):
    """
    Validate MUL (Multipolarity) field positioning in G-records.
    
    ENSDF Format Rule: MUL field MUST be LEFT-JUSTIFIED starting at column 33.
    
    The MUL field occupies columns 33-41 and contains multipolarity assignments like:
    - E2 (pure electric quadrupole)
    - M1+E2 (mixed magnetic dipole + electric quadrupole)
    - D (dipole shorthand)
    - D(+Q) (predominantly dipole with small quadrupole)
    - M1(+E2) (predominantly M1 with small E2)
    
    CRITICAL: MUL values must START at column 33 with NO leading spaces!
    Column 32 MUST be a space (separator between DRI and MUL fields)!
    """
    print(f"\nMUL FIELD VALIDATION: {filename}")
    print("=" * 60)
    print("Checking MUL (Multipolarity) field positioning in columns 33-41...")
    print("ENSDF Rule: MUL field values must be LEFT-JUSTIFIED starting at column 33")
    print("           Column 32 MUST be a space separator")
    print()
    print('ENSDF 80-Column Ruler:')
    print('         1         2         3         4         5         6         7         8')
    print('12345678901234567890123456789012345678901234567890123456789012345678901234567890')
    print(' ' * 31 + '^--------^ MUL field (columns 33-41)')
    print()
    
    mul_fields_analyzed = 0
    mul_field_errors = 0
    
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    for line_num, line in enumerate(lines, 1):
        line_content = line.rstrip('\n\r')
        
        # Only check G-records for MUL field validation
        if len(line_content) < 10 or ' G ' not in line_content[6:10]:
            continue
        
        # Skip comment lines
        if is_comment_line(line_content):
            continue
            
        # Extract MUL field area (columns 33-41, 0-based indices 32-40)
        if len(line_content) >= 33:
            mul_field_area = line_content[32:41] if len(line_content) > 32 else line_content[32:]
            
            # Check if MUL field contains content (not just spaces)
            mul_field_stripped = mul_field_area.strip()
            if mul_field_stripped:
                mul_fields_analyzed += 1
                
                # Check if MUL field starts at column 33 (0-based index 32)
                # Column 32 (0-based index 31) MUST be a space separator
                if len(line_content) >= 33 and line_content[32] != ' ':  # Column 33 (0-based index 32)
                    print(f"[OK] Line {line_num:3d}: MUL='{mul_field_stripped}' correctly LEFT-JUSTIFIED at column 33")
                else:
                    # MUL has leading space(s) - this is an error!
                    # Find where it actually starts
                    first_nonspace = None
                    for i, char in enumerate(mul_field_area):
                        if char != ' ':
                            first_nonspace = 33 + i  # Convert to 1-based column
                            break
                    
                    # Check if column 32 (index 31) has content instead of space
                    col_32_char = line_content[31] if len(line_content) >= 32 else ' '
                    
                    print(f"[ERROR] Line {line_num:3d}: ERROR - MUL='{mul_field_stripped}' positioning error")
                    if col_32_char != ' ':
                        print(f"   CRITICAL: Column 32 contains '{col_32_char}' (should be SPACE separator)")
                        print(f"   MUL content starts at column 32 instead of column 33")
                    if first_nonspace and first_nonspace > 33:
                        print(f"   Current position: MUL starts at column {first_nonspace} (has leading spaces)")
                    print(f"   Required position: MUL must start at column 33 (LEFT-JUSTIFIED)")
                    print(f"   Line: {line_content}")
                    mul_field_errors += 1
                    print()
    
    # Summary
    print(f"MUL FIELD SUMMARY:")
    print(f"  Total MUL fields analyzed: {mul_fields_analyzed}")
    print(f"  MUL field positioning errors: {mul_field_errors}")
    print()
    
    if mul_field_errors == 0:
        print(f"[OK] SUCCESS: All MUL fields correctly LEFT-JUSTIFIED at column 33")
        return True
    else:
        print(f"[ERROR] FAILED: {mul_field_errors} MUL field positioning errors found")
        print(f"   CRITICAL: MUL field values must be LEFT-JUSTIFIED starting at column 33")
        print(f"   Column 32 must be a space separator (not MUL content)")
        return False

def validate_comment_flags(filename):
    """
    Validate comment flags in column 77 (C field) for DATA RECORDS ONLY.
    
    CRITICAL FIX: This function now properly excludes comment lines (cL, cG, cE, etc.)
    from validation. Only true data records (L, G, E, B, DP) are checked.
    
    ENSDF Format Rule: Comment flags (C field) must be in column 77 exactly.
    Common comment flags in DATA RECORDS include:
    - A-Z, a-z: Any single letter used to refer to a specific comment record
    - * (asterisk): Denotes a multiply-placed gamma ray
    - & (ampersand): Denotes a multiply-placed transition with intensity not divided
    - @ (at symbol): Denotes a multiply-placed transition with intensity suitably divided
    - Space: No comment flag
    
    IMPORTANT: Comment lines themselves (35CL cG, 35CL2cG, etc.) are NOT checked!
    """
    print(f"\nCOMMENT FLAG VALIDATION: {filename}")
    print("=" * 60)
    print("Checking comment flags in column 77 (C field) for DATA RECORDS ONLY...")
    print("Note: Comment lines (cL, cG, cE, etc.) are excluded from this check")
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
        
        # CRITICAL: Skip comment lines completely - they are NOT data records!
        if is_comment_line(line_content):
            continue
        
        # Check if this is a data record line (L, G, E, B, DP records)
        if not is_data_record_line(line_content):
            continue
        
        # Now we know this is a true data record (not a comment line)
        # Check column 77 for valid comment flags
        if len(line_content) >= 77:
            char = line_content[76]  # Column 77 (0-based index 76)
            
            # Only report non-space flags
            if char != ' ':
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
                
                print(f"[OK] Line {line_num}: Comment flag '{char}' ({flag_meaning}) in column 77")
                flag_summary[char]['correct'] += 1
    
    # Summary with flag type breakdown
    print()
    print(f"COMMENT FLAG SUMMARY:")
    print(f"  Total comment flags found in DATA RECORDS: {flags_analyzed}")
    print(f"  Flag types found: {', '.join(sorted(flag_summary.keys())) if flag_summary else 'None'}")
    print()
    
    if flag_summary:
        print("  Column 77 flag usage in DATA RECORDS:")
        for flag_type in sorted(flag_summary.keys()):
            correct_count = flag_summary[flag_type]['correct']
            
            # Add meaning for common flags according to ENSDF standards
            flag_meaning = {
                '*': '(multiply-placed gamma ray)',
                '&': '(multiply-placed transition, intensity not divided)', 
                '@': '(multiply-placed transition, intensity suitably divided)'
            }.get(flag_type, '(comment record reference)')
            
            print(f"    '{flag_type}' {flag_meaning}: {correct_count}")
        print()
    
    if flags_analyzed == 0:
        print(f"  Note: No comment flags found in data records (all spaces in column 77)")
    else:
        print(f"  [OK] SUCCESS: All comment flags correctly positioned in column 77")
    
    return True

def validate_g_record_flags(filename):
    """
    Validate G-record flags in columns 77 and 80 for TRUE G-RECORDS ONLY.
    
    CRITICAL FIX: This function now properly excludes comment lines (cG, cL, etc.)
    from validation. Only true G-record data lines are checked.
    
    ENSDF Format Rules for G-Records:
    - Column 77 (C field - Comment flags): A-Z, a-z, *, &, @, space
    - Column 80 (Q field - Additional indicator): space, ?, S
    
    🚨 CRITICAL RULES 🚨:
    - ? is FORBIDDEN in column 77 (comment flag field)
    - ? is ALLOWED only in column 80 (additional indicator)
    - Comment lines (cG, cL, etc.) are NOT G-records and should NOT be checked!
    """
    print(f"\nG-RECORD FLAG VALIDATION: {filename}")
    print("=" * 60)
    print("Checking G-record flags in columns 77 and 80 for TRUE G-RECORDS ONLY...")
    print("Note: Comment lines (cG, cL, etc.) are excluded from this check")
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
        
        # CRITICAL: Skip comment lines completely - they are NOT data records!
        if is_comment_line(line_content):
            continue
        
        # Check if this is a G-record (gamma transition data record)
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
                    print(f"[OK] Line {line_num}: Column 77 flag '{col77_char}' ({flag_type})")
                    col77_flags['details'][col77_char] = col77_flags['details'].get(col77_char, 0) + 1
            else:
                col77_flags['invalid'] += 1
                errors_found = True
                if col77_char == '?':
                    print(f"[ERROR] Line {line_num}: INVALID '?' in column 77 - ? is FORBIDDEN in comment field!")
                    print(f"   → ? should only be used in column 80 (additional indicator)")
                else:
                    print(f"[ERROR] Line {line_num}: INVALID '{col77_char}' in column 77")
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
                    print(f"[OK] Line {line_num}: Column 80 indicator '{col80_char}' ({indicator_type})")
                    col80_indicators['details'][col80_char] = col80_indicators['details'].get(col80_char, 0) + 1
            else:
                col80_indicators['invalid'] += 1
                errors_found = True
                print(f"[ERROR] Line {line_num}: INVALID '{col80_char}' in column 80")
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
        print(f"  [OK] SUCCESS: All G-record flags correctly positioned and valid!")
    else:
        print(f"  [ERROR] ERRORS: {col77_flags['invalid'] + col80_indicators['invalid']} invalid G-record entries found!")
    
    return not errors_found

def validate_dri_field(filename):
    """
    Validate DRI field (columns 30-31) in G-records.
    
    CRITICAL VALIDATION: Detects LT/GT markers appearing in RI field (columns 23-29)
    instead of DRI field (columns 30-31).
    
    ENSDF Format Rules for G-Records:
    - RI field (columns 23-29): Contains relative intensity VALUE only (left-justified)
    - DRI field (columns 30-31): Contains uncertainty OR limit markers (LT, GT, AP, SY, CA)
    
    CRITICAL ERROR PATTERN:
    - WRONG: "LT 0.2" in RI field (columns 23-29)
    - CORRECT: "0.2" in RI field, "LT" in DRI field (columns 30-31)
    
    Valid DRI field content:
    - Empty (blank spaces)
    - 1-2 digit uncertainty (e.g., "5", "12", "25")
    - Limit markers: "LT", "GT", "LE", "GE"
    - Special markers: "AP", "SY", "CA"
    """
    print(f"\nDRI FIELD VALIDATION: {filename}")
    print("=" * 60)
    print("Checking DRI field (columns 30-31) and detecting LT/GT in RI field...")
    print("ENSDF Rule: RI field contains VALUE, DRI field contains UNCERTAINTY or LT/GT")
    print()
    print('ENSDF 80-Column Ruler:')
    print('         1         2         3         4         5         6         7         8')
    print('12345678901234567890123456789012345678901234567890123456789012345678901234567890')
    print(' ' * 22 + '^------^ RI (cols 23-29)  ^^ DRI (cols 30-31)')
    print()
    
    g_records_analyzed = 0
    dri_field_errors = 0
    ri_field_errors = 0  # LT/GT appearing in RI field instead of DRI
    
    # Valid DRI field markers
    valid_dri_markers = ['LT', 'GT', 'LE', 'GE', 'AP', 'SY', 'CA']
    
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    for line_num, line in enumerate(lines, 1):
        line_content = line.rstrip('\n\r')
        
        # Only check G-records (TRUE G-records, not comment lines)
        if len(line_content) < 10 or ' G ' not in line_content[6:10]:
            continue
        
        # Skip comment lines (cG, cL, etc.)
        if is_comment_line(line_content):
            continue
        
        g_records_analyzed += 1
        
        # Extract RI field (columns 23-29)
        if len(line_content) >= 29:
            ri_field = line_content[22:29]  # Columns 23-29 (0-based 22:29)
            ri_field_stripped = ri_field.strip()
            
            # CRITICAL CHECK 1: Detect full markers LT/GT/LE/GE in RI field (WRONG!)
            has_full_marker = any(marker in ri_field for marker in ['LT', 'GT', 'LE', 'GE'])
            
            # CRITICAL CHECK 2: Detect partial markers (single letters from limit markers)
            # If RI field ends with 'L', 'G' and DRI starts with 'T', 'E', it's likely split marker
            has_suspicious_letter = False
            if ri_field_stripped and len(line_content) >= 31:
                last_char_ri = ri_field_stripped[-1] if ri_field_stripped else ''
                dri_field = line_content[29:31]  # Columns 30-31
                first_char_dri = dri_field[0] if dri_field else ''
                
                # Check for split marker patterns: "L" in RI + "T" in DRI = "LT" split
                if last_char_ri == 'L' and first_char_dri == 'T':
                    has_suspicious_letter = True
                elif last_char_ri == 'G' and first_char_dri in ['T', 'E']:
                    has_suspicious_letter = True
                elif last_char_ri == 'L' and first_char_dri == 'E':
                    has_suspicious_letter = True
            
            if has_full_marker or has_suspicious_letter:
                ri_field_errors += 1
                if has_full_marker:
                    print(f"[ERROR] Line {line_num}: ERROR - Limit marker in RI field (columns 23-29)!")
                    print(f"   RI field contains: '{ri_field}' (should contain VALUE only)")
                else:
                    print(f"[ERROR] Line {line_num}: ERROR - Split limit marker across RI/DRI fields!")
                    print(f"   RI field: '{ri_field}' | DRI field: '{line_content[29:31]}'")
                    print(f"   Appears to be '{last_char_ri}{first_char_dri}' marker split across fields")
                print(f"   -> Move limit marker from RI field to DRI field (columns 30-31)")
                print(f"   -> Example: 'LT 0.2' in RI -> '0.2' in RI, 'LT' in DRI")
        
        # Extract DRI field (columns 30-31)
        if len(line_content) >= 31:
            dri_field = line_content[29:31]  # Columns 30-31 (0-based 29:31)
            dri_field_stripped = dri_field.strip()
            
            # Check DRI field content if not empty
            if dri_field_stripped:
                # Valid DRI: digits (1-2 chars) OR special markers
                is_digit = dri_field_stripped.isdigit()
                is_marker = dri_field_stripped in valid_dri_markers
                
                if not (is_digit or is_marker):
                    dri_field_errors += 1
                    print(f"[ERROR] Line {line_num}: Invalid DRI field content '{dri_field_stripped}'")
                    print(f"   -> Valid DRI: digits (1-2), LT, GT, LE, GE, AP, SY, CA")
    
    print()
    print(f"DRI FIELD SUMMARY:")
    print(f"  G-records analyzed: {g_records_analyzed}")
    print(f"  LT/GT in RI field errors: {ri_field_errors}")
    print(f"  Invalid DRI content errors: {dri_field_errors}")
    print()
    
    if ri_field_errors == 0 and dri_field_errors == 0:
        print(f"[OK] SUCCESS: All DRI fields correct, no limit markers in RI field")
        return True
    else:
        total_errors = ri_field_errors + dri_field_errors
        print(f"[ERROR] ERRORS: {total_errors} DRI field validation errors found!")
        return False

def validate_gt_lt_placement(filename):
    """
    Validate GT/LT marker placement in ENSDF records (SEMANTIC VALIDATION).
    
    CRITICAL SEMANTIC CHECK: Ensures GT/LT limit markers are in UNCERTAINTY fields,
    not embedded in VALUE fields.
    
    ENSDF Standard (instructions.md lines 969-976):
    - Format: Value in main field, GT/LT marker LEFT-JUSTIFIED in uncertainty field
    - Examples:
      - <1.6 -> RI=1.6 (cols 23-29), DRI=LT (cols 30-31)
      - >5.2 -> RI=5.2 (cols 23-29), DRI=GT (cols 30-31)
    
    For L-records (Half-life T field):
    - T field (cols 40-49): Half-life value + units ONLY (e.g., "1000 FS")
    - DT field (cols 50-55): Uncertainty OR GT/LT marker (e.g., "GT")
    - WRONG: "GT 1000FS" in T field
    - CORRECT: "1000 FS" in T, "GT" in DT
    
    For G-records (Relative intensity RI field):
    - RI field (cols 23-29): Intensity value ONLY
    - DRI field (cols 30-31): Uncertainty OR GT/LT marker
    - WRONG: "GT 5.2" in RI field
    - CORRECT: "5.2" in RI, "GT" in DRI
    
    Returns:
        bool: True if all GT/LT markers correctly placed, False otherwise
    """
    import re
    
    print(f"\nGT/LT SEMANTIC VALIDATION: {filename}")
    print("=" * 60)
    print("Checking GT/LT marker placement in value vs. uncertainty fields...")
    print("ENSDF Rule: Value in main field, GT/LT marker in uncertainty field")
    print()
    print('ENSDF 80-Column Ruler:')
    print('         1         2         3         4         5         6         7         8')
    print('12345678901234567890123456789012345678901234567890123456789012345678901234567890')
    print('                      ^------^ RI  ^^ DRI | T---------^ DT----^')
    print('                      (23-29) (30-31)      (40-49)     (50-55)')
    print()
    
    # Regex pattern to detect GT/LT markers (whole words)
    GT_LT_PATTERN = r'\b(GT|LT|GE|LE)\b'
    
    l_records_checked = 0
    g_records_checked = 0
    l_field_errors = []
    g_field_errors = []
    
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    for line_num, line in enumerate(lines, 1):
        line_content = line.rstrip('\n\r')
        
        if len(line_content) < 10:
            continue
        
        record_type = line_content[7] if len(line_content) > 7 else ''
        
        # Skip comment lines
        if len(line_content) > 6 and line_content[6] in ['c', 'C', 'd', 'D', 't', 'T', 'p', 'P']:
            continue
        
        # L-RECORD CHECK: T field (cols 40-49) should NOT contain GT/LT markers
        if record_type == 'L':
            l_records_checked += 1
            
            if len(line_content) >= 49:
                T_field = line_content[39:49]  # Columns 40-49 (0-based 39:49)
                T_field_stripped = T_field.strip()
                
                # Check if GT/LT marker is embedded in T field
                if re.search(GT_LT_PATTERN, T_field_stripped):
                    DT_field = line_content[49:55] if len(line_content) >= 55 else ''
                    l_field_errors.append({
                        'line': line_num,
                        'T_field': T_field,
                        'DT_field': DT_field,
                        'full_line': line_content
                    })
        
        # G-RECORD CHECK: RI field (cols 23-29) should NOT contain GT/LT markers
        elif record_type == 'G':
            g_records_checked += 1
            
            if len(line_content) >= 29:
                RI_field = line_content[22:29]  # Columns 23-29 (0-based 22:29)
                RI_field_stripped = RI_field.strip()
                
                # Check if GT/LT marker is embedded in RI field
                if re.search(GT_LT_PATTERN, RI_field_stripped):
                    DRI_field = line_content[29:31] if len(line_content) >= 31 else ''
                    g_field_errors.append({
                        'line': line_num,
                        'RI_field': RI_field,
                        'DRI_field': DRI_field,
                        'full_line': line_content
                    })
    
    # Report L-record errors
    if l_field_errors:
        print("[ERROR] L-RECORD GT/LT PLACEMENT ERRORS FOUND:")
        print("=" * 60)
        for error in l_field_errors:
            print(f"Line {error['line']}: GT/LT marker in T field (cols 40-49) - MUST be in DT field (cols 50-55)")
            print(f"  Current T field (40-49): '{error['T_field']}'")
            print(f"  Current DT field (50-55): '{error['DT_field']}'")
            print(f"  -> FIX: Separate value and marker")
            print(f"     Example: 'GT 1000FS' -> T='1000 FS', DT='GT'")
            print(f"  Full line: {error['full_line']}")
            print()
    
    # Report G-record errors
    if g_field_errors:
        print("[ERROR] G-RECORD GT/LT PLACEMENT ERRORS FOUND:")
        print("=" * 60)
        for error in g_field_errors:
            print(f"Line {error['line']}: GT/LT marker in RI field (cols 23-29) - MUST be in DRI field (cols 30-31)")
            print(f"  Current RI field (23-29): '{error['RI_field']}'")
            print(f"  Current DRI field (30-31): '{error['DRI_field']}'")
            print(f"  -> FIX: Separate value and marker")
            print(f"     Example: 'LT 0.2' -> RI='0.2', DRI='LT'")
            print(f"  Full line: {error['full_line']}")
            print()
    
    # Summary
    print(f"GT/LT SEMANTIC VALIDATION SUMMARY:")
    print(f"  L-records checked: {l_records_checked}")
    print(f"  G-records checked: {g_records_checked}")
    print(f"  L-record T field errors: {len(l_field_errors)}")
    print(f"  G-record RI field errors: {len(g_field_errors)}")
    print()
    
    total_errors = len(l_field_errors) + len(g_field_errors)
    
    if total_errors == 0:
        print(f"[OK] SUCCESS: All GT/LT markers correctly placed in uncertainty fields!")
        return True
    else:
        print(f"[ERROR] ERRORS: {total_errors} GT/LT placement errors found!")
        print()
        print("EXPLANATION: Why column_calibrate.py didn't catch these before:")
        print("  - Tool validates POSITION (what columns) not SEMANTICS (what belongs where)")
        print("  - 'GT 1000FS' in T field passes position check (text in cols 40-49)")
        print("  - Tool didn't know GT should be EXTRACTED and placed in DT field")
        print("  - This enhancement adds semantic understanding of GT/LT as special markers")
        print()
        return False

def validate_band_flags(filename):
    """
    DEPRECATED: Use validate_comment_flags() instead.
    This function only checked limited band flags and missed P, D, and other comment flags.
    """
    print(f"\n[WARNING]  WARNING: validate_band_flags() is deprecated")
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
    
    # Always validate DE fields, S fields, J-pi fields, MUL fields, DRI fields, GT/LT placement, and comment flags unless header-only mode
    if not header_only:
        de_field_success = validate_de_field(filename)
        s_field_success = validate_s_field(filename)
        jp_field_success = validate_jp_field(filename)
        mul_field_success = validate_mul_field(filename)
        dri_field_success = validate_dri_field(filename)
        gt_lt_placement_success = validate_gt_lt_placement(filename)  # NEW SEMANTIC VALIDATION
        comment_flag_success = validate_comment_flags(filename)
        g_record_validation_success = validate_g_record_flags(filename)
        return (not errors_found) and de_field_success and s_field_success and jp_field_success and mul_field_success and dri_field_success and gt_lt_placement_success and comment_flag_success and g_record_validation_success
        
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
