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
- Line length compliance (80 characters for ALL record types: H, L, G, E, B, DP)
- L-field positioning (columns 56-64)
- S-field positioning (columns 65-74) 
- Comment flag positioning (column 77)
- Field boundary validation
- Left-justification requirements
- Includes H (History/Header) records in line length validation
"""

import sys
import os
import argparse
from functools import lru_cache
from typing import List


@lru_cache(maxsize=16)
def _read_file_cached(filename: str) -> tuple:
    """Return raw file lines with simple LRU caching to avoid repeated disk reads."""
    with open(filename, 'r', encoding='utf-8') as handle:
        return tuple(handle.readlines())


def get_file_lines(filename: str) -> List[str]:
    """Return a mutable list of raw lines (including newline characters)."""
    return list(_read_file_cached(filename))


def get_stripped_lines(filename: str) -> List[str]:
    """Return file lines stripped of trailing newlines/carriage returns."""
    return [line.rstrip('\n\r') for line in _read_file_cached(filename)]


def invalidate_file_cache(filename: str) -> None:
    """Clear the cached copy after modifying a file on disk."""
    _read_file_cached.cache_clear()

def is_data_record_line(line):
    """
    Check if a line is a record line that must be exactly 80 characters.
    ENSDF standard: ALL record types (H, L, G, E, B, DP, etc.) must be 80 columns.
    
    H records: History records (metadata, author, citation info)
    L records: Level records (nuclear energy levels)
    G records: Gamma transition records
    E records: Electron capture/beta-plus decay records
    B records: Beta-minus decay records
    DP records: Delayed particle records
    """
    if len(line) < 8:
        return False
    
    # Check for record types in column 8 (0-based index 7)
    # H-records have H at column 8 (index 7)
    # L/G/E/B records have those letters at column 8
    # DP records have D at column 8 and P at column 9
    
    record_type = line[7] if len(line) > 7 else ' '
    
    # Include H records (History/Header records) - they must also be 80 columns
    all_record_types = ['H', 'L', 'G', 'E', 'B']  # All standard record types
    
    # Also check for DP records (delayed proton)
    if len(line) > 8 and line[7:9] == 'DP':
        return True
        
    return record_type in all_record_types

def fix_line_lengths(filename, dry_run=False):
    """
    Fix ENSDF file line lengths to be exactly 80 characters.
    Processes ALL record lines (H, L, G, E, B, DP records).
    ENSDF standard requires ALL record types to be exactly 80 columns.
    Comment lines (starting with c) are NOT padded - only actual records.
    
    Args:
        filename: Path to ENSDF file
        dry_run: If True, only report what would be changed without modifying file
        
    Returns:
        tuple: (lines_fixed, errors_found)
    """
    
    if not os.path.exists(filename):
        print(f"ERROR: File {filename} not found!")
        return 0, 1
        
    print(f"{'DRY RUN - ' if dry_run else ''}Fixing record line lengths in: {filename}")
    print("=" * 70)
    print("Note: Checking and fixing ALL record lines (H, L, G, E, B, DP)")
    print("      ENSDF standard: ALL records must be exactly 80 characters")
    print("      Comment lines (c at column 6) are NOT modified")
    print()
    
    lines = get_file_lines(filename)
    
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
        with open(filename, 'w', encoding='utf-8') as f:
            f.writelines(fixed_lines)
        invalidate_file_cache(filename)
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
    
    lines = get_stripped_lines(filename)
    
    for line_num, line_content in enumerate(lines, 1):
        
        # Skip continuation records (XREF, FLAG, etc.) - they are NOT primary data records
        if is_continuation_record(line_content):
            continue
        
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

                # LEFT-JUSTIFICATION CHECK
                if de_field_content[0] == ' ':
                    de_field_errors += 1
                    print(f"  ERROR: Line {line_num}: DE field '{de_field_content}' is NOT left-justified. Must start at column 20.")
                    print(f"         Line: {line_content}")

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
    
    lines = get_stripped_lines(filename)
    
    for line_num, line_content in enumerate(lines, 1):
        
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
                    if char.isdigit() or char in ".-+":
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
        s_validation_passed = True
    else:
        print(f"[ERROR] FAILED: {s_field_errors} S field positioning errors found")
        print(f"   CRITICAL: S field values must be LEFT-JUSTIFIED starting at column 65")
        print(f"   Current violations: Values starting at wrong columns instead of 65")
        s_validation_passed = False

    # DS FIELD VALIDATION FOR L-RECORDS
    print(f"\nDS FIELD VALIDATION: {filename}")
    print("=" * 60)
    print("Checking DS field positioning in columns 75-76 for L-records...")
    print("ENSDF Rule: DS field MUST contain uncertainty, SEPARATE from S field")
    print()
    print('ENSDF 80-Column Ruler:')
    print('         1         2         3         4         5         6         7         8')
    print('12345678901234567890123456789012345678901234567890123456789012345678901234567890')
    print(' ' * 64 + '^---------^--^ S field (65-74) DS field (75-76)')
    print()
    
    ds_fields_analyzed = 0
    ds_field_errors = 0
    
    lines = get_stripped_lines(filename)
    
    for line_num, line_content in enumerate(lines, 1):
        
        # Only check L-records for DS field validation
        if len(line_content) < 10 or ' L ' not in line_content[6:10]:
            continue
        
        # Check if S field has content (indicating L-record with spectroscopic data)
        if len(line_content) >= 74:
            s_field = line_content[64:74]
            s_stripped = s_field.strip()
            
            # Only validate DS if S-field contains numerical data
            if s_stripped and any(c.isdigit() for c in s_stripped):
                ds_fields_analyzed += 1
                
                # Extract DS field (columns 75-76)
                if len(line_content) >= 76:
                    ds_field = line_content[74:76]
                else:
                    ds_field = line_content[74:] if len(line_content) > 74 else "  "
                
                ds_stripped = ds_field.strip()
                
                # Check if DS field contains uncertainty
                if not ds_stripped:
                    # Empty DS is valid if no uncertainty is provided
                    pass
                elif not ds_field[0].isdigit() and ds_field[0] != ' ':
                    print(f"LINE {line_num}: DS field analysis")
                    print(f"Line:  {line_content}")
                    print(f"S field (65-74):  '{s_field}'")
                    print(f"DS field (75-76): '{ds_field}'")
                    print(f"[ERROR] ERROR: DS field does not start with digit or space - got '{ds_field[0]}'")
                    print(f"   Expected: LEFT-JUSTIFIED digit (e.g., '1 ', '12')")
                    ds_field_errors += 1
                    print()
                elif ds_stripped:
                    # Check if it's left-justified
                    # ANY content in DS field must start at Column 75 (ds_field[0])
                    # If ds_field[0] is space, but field has content, it is an error (either alignment or garbage)
                    if ds_field[0] == ' ':
                         print(f"LINE {line_num}: DS field analysis")
                         print(f"Line:  {line_content}")
                         print(f"S field (65-74):  '{s_field}'")
                         print(f"DS field (75-76): '{ds_field}'")
                         print(f"[ERROR] ERROR: DS field content '{ds_stripped}' is not LEFT-JUSTIFIED or contains INVALID leading space")
                         print(f"   Expected: Content should start at column 75. Found '{ds_field}'")
                         ds_field_errors += 1
                         print()
                else:
                    # Valid DS field
                    pass
            else:
                # S field is empty or non-numeric. DS field should be empty.
                # Check if DS field contains a letter (misplaced flag)
                if len(line_content) >= 76:
                    ds_field = line_content[74:76]
                    ds_stripped = ds_field.strip()
                    if ds_stripped and ds_stripped[0].isalpha():
                         print(f"[ERROR] Line {line_num}: Misplaced flag in DS field (columns 75-76)")
                         print(f"   Found '{ds_stripped}' in DS field. Should be in Flag field (column 77)")
                         print(f"   Line: {line_content}")
                         ds_field_errors += 1
                         print()
    
    # DS Summary
    print(f"DS FIELD SUMMARY:")
    print(f"  Total L-records with S-field analyzed: {ds_fields_analyzed}")
    print(f"  DS field positioning errors: {ds_field_errors}")
    print()
    
    if ds_field_errors == 0:
        print(f"[OK] SUCCESS: All DS fields correctly positioned (uncertainty in columns 75-76)")
        ds_validation_passed = True
    else:
        print(f"[ERROR] FAILED: {ds_field_errors} DS field errors found")
        print(f"   CRITICAL: Uncertainty must be in DS field (75-76), NOT embedded in S field")
        print(f"   Typical error: S='832      1', DS='  ' should be S='832       ', DS='1 '")
        ds_validation_passed = False
    
    return s_validation_passed and ds_validation_passed

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
    
    lines = get_stripped_lines(filename)
    
    for line_num, line_content in enumerate(lines, 1):
        
        # Skip continuation records (XREF, FLAG, etc.) - they are NOT primary data records
        if is_continuation_record(line_content):
            continue
        
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
                # AND check that column 22 (index 21) is a SPACE (no left shift)
                col22_char = line_content[21] if len(line_content) > 21 else ' '
                
                if col22_char != ' ':
                    print(f"[ERROR] Line {line_num:3d}: ERROR - J-π shifted left - column 22 contains '{col22_char}' (should be SPACE)")
                    print(f"   Current position: starts at column 22 (or earlier)")
                    print(f"   Required position: must start at column 23 (LEFT-JUSTIFIED)")
                    print(f"   Line: {line_content}")
                    jp_field_errors += 1
                    print()
                elif line_content[22] != ' ':  # Column 23 (0-based index 22)
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

def is_continuation_record(line):
    """
    Check if a line is a continuation record (column 6 not blank).
    
    Continuation records have a non-blank character in column 6 (0-based index 5):
    - ' 35P X L XREF=...' (X at column 6 = XREF continuation for L-record)
    - ' 35P S G CC=...' (S at column 6 = continuation for G-record, conversion coefficients)
    - ' 35P F L FLAG=...' (F at column 6 = FLAG continuation for L-record)
    - ' 35P 2 L ...' (2 at column 6 = second continuation of L-record)
    - ' 35P H TYP=...' (H-record, not a continuation but column 6 is blank)
    - ' 35P 2 H CIT=...' (2 at column 6 = H-record continuation)
    
    These continuation records should NOT be validated for primary field positioning
    because they extend or modify the previous record, not standalone data records.
    """
    if len(line) < 6:
        return False
    
    # Column 6 (0-based index 5) should be blank for primary records
    # Non-blank = continuation record
    col6_char = line[5]
    
    # Primary records have column 6 = space
    # Continuation records have column 6 = alphanumeric or special character
    return col6_char != ' '

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
    
    lines = get_stripped_lines(filename)
    
    for line_num, line_content in enumerate(lines, 1):
        
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
    
    lines = get_stripped_lines(filename)
    
    for line_num, line_content in enumerate(lines, 1):
        
        # CRITICAL: Skip comment lines completely - they are NOT data records!
        if is_comment_line(line_content):
            continue
        
        # Check if this is a data record line (L, G, E, B, DP records)
        if not is_data_record_line(line_content):
            continue
        
        # Now we know this is a true data record (not a comment line)
        
        # CRITICAL VALIDATION: Check for misplaced flags in columns 77-80
        # Comment flags must be EXACTLY at column 77, not at columns 78 or 79
        if len(line_content) >= 80:
            col77_char = line_content[76]  # Column 77 (0-based index 76)
            col78_char = line_content[77]  # Column 78 (0-based index 77)
            col79_char = line_content[78]  # Column 79 (0-based index 78)
            
            # Check for misplaced comment flags in columns 78-79
            for pos, idx, char in [(78, 77, col78_char), (79, 78, col79_char)]:
                if char != ' ' and char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz*&@':
                    print(f"[ERROR] Line {line_num}: Comment flag '{char}' at column {pos} - MUST be at column 77!")
                    print(f"   → Line content: {line_content}")
                    print(f"   → Position: {' ' * (pos-1)}^")
                    if char not in flag_summary:
                        flag_summary[char] = {'correct': 0, 'incorrect': []}
                    flag_summary[char]['incorrect'].append(line_num)
        
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
    
    lines = get_stripped_lines(filename)
    
    for line_num, line_content in enumerate(lines, 1):
        
        # CRITICAL: Skip comment lines completely - they are NOT data records!
        if is_comment_line(line_content):
            continue
        
        # CRITICAL: Skip continuation records (H continuation '2', S continuation, etc.)
        if is_continuation_record(line_content):
            continue
        
        # Check if this is a G-record (gamma transition data record)
        # CRITICAL: Column 7 must be blank, column 8 must be 'G', column 9 must be blank
        # This excludes drawing commands like 'dG', 'dL', etc.
        is_g_record = (len(line_content) >= 9 and 
                       line_content[6] == ' ' and  # Column 7 must be blank
                       line_content[7] == 'G' and  # Column 8 must be 'G'
                       line_content[8] == ' ')     # Column 9 must be blank
        
        if not is_g_record:
            continue
        
        g_records_analyzed += 1
        
        # CRITICAL VALIDATION: Check for misplaced flags in columns 77-80
        # Flags must be EXACTLY at column 77, not at 78 or 79
        if len(line_content) >= 80:
            col77_char = line_content[76]  # Column 77 (0-based index 76)
            col78_char = line_content[77]  # Column 78 (0-based index 77)
            col79_char = line_content[78]  # Column 79 (0-based index 78)
            
            # Check for misplaced comment flags in columns 78-79
            for pos, idx, char in [(78, 77, col78_char), (79, 78, col79_char)]:
                if char != ' ' and char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz*&@':
                    col77_flags['invalid'] += 1
                    errors_found = True
                    print(f"[ERROR] Line {line_num}: Comment flag '{char}' at column {pos} - MUST be at column 77!")
                    print(f"   → Line content: {line_content}")
                    print(f"   → Position: {' ' * (pos-1)}^")
        
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
    
    lines = get_stripped_lines(filename)
    
    for line_num, line_content in enumerate(lines, 1):
        
        # Skip continuation records (S continuation for conversion coefficients, etc.)
        if is_continuation_record(line_content):
            continue
        
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
                # LEFT-JUSTIFICATION CHECK
                if dri_field[0] == ' ':
                    dri_field_errors += 1
                    print(f"[ERROR] Line {line_num}: DRI field '{dri_field}' is NOT left-justified. Must start at column 30.")
                
                # Valid DRI: digits (1-2 chars) OR special markers
                is_digit = dri_field_stripped.isdigit()
                is_marker = dri_field_stripped in valid_dri_markers
                
                # Check if this might be a partial marker (e.g., 'L' from 'LT' extending to col 32)
                is_partial_marker = False
                if len(dri_field_stripped) == 1 and len(line_content) >= 32:
                    # Check if combining with next character makes a valid marker
                    extended = dri_field_stripped + line_content[31]
                    is_partial_marker = extended in valid_dri_markers
                
                if not (is_digit or is_marker or is_partial_marker):
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

def validate_e_field(filename):
    """
    Validate E field (columns 10-19) positioning in L and G records.
    
    CRITICAL VALIDATION: Ensures energy values are LEFT-JUSTIFIED at column 10.
    
    ENSDF Format (applies to both L and G records):
    - Columns 1-5: NUCID
    - Columns 6-9: Must be blank
    - Columns 10-19: Energy (E field) - LEFT-JUSTIFIED at column 10
    - Columns 20-21: Energy uncertainty (DE field)
    
    Common Error: Energy values shifted right (not starting at column 10)
    """
    print(f"\nE FIELD POSITIONING VALIDATION: {filename}")
    print("=" * 60)
    print("Checking E field (energy) LEFT-JUSTIFICATION at column 10...")
    print("ENSDF Rule: Energy values must start at column 10 (L and G records)")
    print()
    print('ENSDF 80-Column Ruler:')
    print('         1         2         3         4         5         6         7         8')
    print('12345678901234567890123456789012345678901234567890123456789012345678901234567890')
    print(' ' * 9 + '^---------^ ^^')
    print(' ' * 9 + '10-19 (E)   20-21 (DE)')
    print(' ' * 9 + '^- Energy must start at column 10')
    print()
    
    records_analyzed = 0
    e_errors = 0
    error_details = []
    
    lines = get_stripped_lines(filename)
    
    for line_num, line_content in enumerate(lines, 1):
        
        # Check for L or G records (column 8='L' or 'G', columns 6-7 are blank)
        if len(line_content) < 20:
            continue
        
        record_type = line_content[7] if len(line_content) > 7 else ''
        if record_type not in ['L', 'G']:
            continue
        
        # Skip comment lines (cL, cG)
        if line_content[5] != ' ' or line_content[6] != ' ':
            continue
        
        records_analyzed += 1
        
        # Extract E field area (columns 10-19, 0-based index 9:19)
        e_field = line_content[9:19]
        
        # Skip if E field is completely empty
        if not e_field.strip():
            continue
        
        # Check if energy value is LEFT-JUSTIFIED (starts at column 10)
        # Column 10 should have a digit or decimal point, not a space
        col10_char = line_content[9]  # Column 10 (0-based index 9)
        
        if col10_char == ' ' and e_field.strip():
            # Energy value is shifted right (doesn't start at column 10)
            e_errors += 1
            
            # Find where it actually starts
            actual_start = 10
            for i, char in enumerate(e_field):
                if char not in [' ', '']:
                    actual_start = 10 + i
                    break
            
            error_details.append({
                'line_num': line_num,
                'line': line_content,
                'record_type': record_type,
                'e_field': e_field,
                'actual_start': actual_start
            })
            
            if e_errors <= 10:  # Show first 10 errors
                print(f"[ERROR] Line {line_num}: {record_type}-record energy shifted right")
                print(f"   E field (cols 10-19): [{e_field}]")
                print(f"   Energy starts at column {actual_start} (should be 10)")
                print(f"   Full line: {line_content}")
                print(f"   FIX: Remove leading spaces to LEFT-JUSTIFY at column 10")
                print()
    
    if e_errors > 10:
        print(f"... and {e_errors - 10} more errors (showing first 10 only)")
        print()
    
    print(f"E FIELD SUMMARY:")
    print(f"  L/G records analyzed: {records_analyzed}")
    print(f"  Energy positioning errors: {e_errors}")
    print()
    
    if e_errors == 0:
        print(f"[OK] SUCCESS: All energy values correctly LEFT-JUSTIFIED at column 10")
        return True
    else:
        print(f"[ERROR] ERRORS: {e_errors} energy field positioning errors found!")
        return False

def validate_ri_field(filename):
    """
    Validate RI field (columns 23-29) positioning in G-records.
    
    CRITICAL VALIDATION: Ensures RI values start at column 23 (LEFT-JUSTIFIED)
    and that column 22 is a SPACE (readability space between DE and RI fields).
    
    ENSDF G-Record Format:
    - Columns 10-19: Energy (E field)
    - Columns 20-21: Energy uncertainty (DE field)
    - Column 22: MUST BE SPACE (readability space)
    - Columns 23-29: Relative intensity (RI field) - LEFT-JUSTIFIED at column 23
    - Columns 30-31: RI uncertainty (DRI field)
    
    Common Error: RI values shifted left by 1 column (starting at column 22)
    This causes column 22 to contain a digit instead of a space.
    """
    print(f"\nRI FIELD POSITIONING VALIDATION: {filename}")
    print("=" * 60)
    print("Checking RI field LEFT-JUSTIFICATION at column 23...")
    print("ENSDF Rule: Column 22 = SPACE, RI value starts at column 23")
    print()
    print('ENSDF 80-Column Ruler:')
    print('         1         2         3         4         5         6         7         8')
    print('12345678901234567890123456789012345678901234567890123456789012345678901234567890')
    print(' ' * 19 + '^^^ ^^^^^^^^^^')
    print(' ' * 19 + '20  23-29 (RI field)')
    print(' ' * 19 + 'DE  Must start at col 23')
    print(' ' * 21 + '^- Column 22 MUST be SPACE')
    print()
    
    g_records_analyzed = 0
    ri_errors = 0
    error_details = []
    
    lines = get_stripped_lines(filename)
    
    for line_num, line_content in enumerate(lines, 1):
        
        # Only check G-records (column 8='G', columns 6-7 are blank spaces)
        if len(line_content) < 32:
            continue
        if not (line_content[7] == 'G' and line_content[5] == ' ' and line_content[6] == ' '):
            continue
        
        g_records_analyzed += 1
        
        # Extract RI field area (columns 23-29, 0-based index 22:29)
        ri_field = line_content[22:29]
        
        # Skip if RI field is completely empty
        if not ri_field.strip():
            continue
        
        # CRITICAL CHECK: Column 22 must be a SPACE
        col22_char = line_content[21] if len(line_content) > 21 else ' '  # Column 22 (0-based index 21)
        
        if col22_char != ' ':
            # RI is shifted left - column 22 has content (should be space)
            ri_errors += 1
            error_details.append({
                'line_num': line_num,
                'line': line_content,
                'col22_char': col22_char,
                'ri_field': ri_field
            })
            
            if ri_errors <= 10:  # Show first 10 errors
                print(f"[ERROR] Line {line_num}: RI shifted left - column 22 contains '{col22_char}' (should be SPACE)")
                print(f"   RI field (cols 23-29): [{ri_field}]")
                print(f"   Full line: {line_content}")
                print(f"   FIX: Insert space at column 22 to shift RI right to column 23")
                print()
        
        # SECONDARY CHECK: RI should be LEFT-JUSTIFIED (start at column 23, not 24+)
        elif line_content[22] == ' ' and ri_field[1:].strip():
            # First character (col 23) is space but there's content later - shifted right
            ri_errors += 1
            error_details.append({
                'line_num': line_num,
                'line': line_content,
                'error_type': 'RI shifted right',
                'ri_field': ri_field
            })
            
            if ri_errors <= 10:
                print(f"[ERROR] Line {line_num}: RI shifted right - starts after column 23")
                print(f"   RI field (cols 23-29): [{ri_field}]")
                print(f"   Full line: {line_content}")
                print(f"   FIX: Remove leading space(s) to LEFT-JUSTIFY at column 23")
                print()
    
    if ri_errors > 10:
        print(f"... and {ri_errors - 10} more errors (showing first 10 only)")
        print()
    
    print(f"RI FIELD SUMMARY:")
    print(f"  G-records analyzed: {g_records_analyzed}")
    print(f"  RI positioning errors: {ri_errors}")
    print()
    
    if ri_errors == 0:
        print(f"[OK] SUCCESS: All RI fields correctly positioned at column 23")
        return True
    else:
        print(f"[ERROR] ERRORS: {ri_errors} RI field positioning errors found!")
        print()
        print("CRITICAL FIX NEEDED:")
        print("  Run: python .github/fix_ri_positioning.py \"filename.ens\"")
        print("  Or manually insert space at column 22 for each error")
        print()
        return False

def validate_m_field(filename):
    """
    Validate M field (columns 33-41) positioning in G-records.
    
    CRITICAL VALIDATION: Ensures multipolarity values are LEFT-JUSTIFIED at column 33.
    
    ENSDF G-Record Format:
    - Columns 23-29: Relative intensity (RI field)
    - Columns 30-31: RI uncertainty (DRI field)
    - Column 32: MUST BE SPACE (readability space)
    - Columns 33-41: Multipolarity (M field) - LEFT-JUSTIFIED at column 33
    - Columns 42-49: Mixing ratio (MR field)
    
    Common multipolarity values: E1, E2, E3, M1, M2, M3, D, Q, O, M1+E2, D+Q, etc.
    """
    print(f"\nM FIELD POSITIONING VALIDATION: {filename}")
    print("=" * 60)
    print("Checking M field (multipolarity) LEFT-JUSTIFICATION at column 33...")
    print("ENSDF Rule: Multipolarity values must start at column 33")
    print()
    print('ENSDF 80-Column Ruler:')
    print('         1         2         3         4         5         6         7         8')
    print('12345678901234567890123456789012345678901234567890123456789012345678901234567890')
    print(' ' * 32 + '^--------^')
    print(' ' * 32 + '33-41 (M field)')
    print(' ' * 32 + '^- Multipolarity must start at column 33')
    print()
    
    g_records_analyzed = 0
    m_errors = 0
    error_details = []
    
    lines = get_stripped_lines(filename)
    
    for line_num, line_content in enumerate(lines, 1):
        
        # Only check G-records (column 8='G', columns 6-7 are blank)
        if len(line_content) < 42:
            continue
        if not (line_content[7] == 'G' and line_content[5] == ' ' and line_content[6] == ' '):
            continue
        
        g_records_analyzed += 1
        
        # Extract M field area (columns 33-41, 0-based index 32:41)
        m_field = line_content[32:41]
        
        # Skip if M field is completely empty
        if not m_field.strip():
            continue
        
        # Check if M value is LEFT-JUSTIFIED (starts at column 33)
        col33_char = line_content[32]  # Column 33 (0-based index 32)
        
        if col33_char == ' ' and m_field.strip():
            # M value is shifted right (doesn't start at column 33)
            m_errors += 1
            
            # Find where it actually starts
            actual_start = 33
            for i, char in enumerate(m_field):
                if char not in [' ', '']:
                    actual_start = 33 + i
                    break
            
            error_details.append({
                'line_num': line_num,
                'line': line_content,
                'm_field': m_field,
                'actual_start': actual_start
            })
            
            if m_errors <= 10:
                print(f"[ERROR] Line {line_num}: Multipolarity shifted right")
                print(f"   M field (cols 33-41): [{m_field}]")
                print(f"   M starts at column {actual_start} (should be 33)")
                print(f"   Full line: {line_content}")
                print(f"   FIX: Remove leading spaces to LEFT-JUSTIFY at column 33")
                print()
    
    if m_errors > 10:
        print(f"... and {m_errors - 10} more errors (showing first 10 only)")
        print()
    
    print(f"M FIELD SUMMARY:")
    print(f"  G-records with M field analyzed: {sum(1 for _, line in enumerate(open(filename)) if len(line) >= 42 and line[7] == 'G' and line[5] == ' ' and line[6] == ' ' and line[32:41].strip())}")
    print(f"  Multipolarity positioning errors: {m_errors}")
    print()
    
    if m_errors == 0:
        print(f"[OK] SUCCESS: All multipolarity values correctly LEFT-JUSTIFIED at column 33")
        return True
    else:
        print(f"[ERROR] ERRORS: {m_errors} multipolarity field positioning errors found!")
        return False

def validate_mr_field(filename):
    """
    Validate MR field (columns 42-49) positioning in G-records.
    
    CRITICAL VALIDATION: Ensures mixing ratio values are LEFT-JUSTIFIED at column 42.
    
    ENSDF G-Record Format:
    - Columns 33-41: Multipolarity (M field)
    - Columns 42-49: Mixing ratio (MR field) - LEFT-JUSTIFIED at column 42
    - Columns 50-55: MR uncertainty (DMR field)
    
    Mixing ratio format: +1.23, -0.45, >+2.1, <-0.8, etc.
    Always include sign (+ or -)
    """
    print(f"\nMR FIELD POSITIONING VALIDATION: {filename}")
    print("=" * 60)
    print("Checking MR field (mixing ratio) LEFT-JUSTIFICATION at column 42...")
    print("ENSDF Rule: Mixing ratio values must start at column 42")
    print()
    print('ENSDF 80-Column Ruler:')
    print('         1         2         3         4         5         6         7         8')
    print('12345678901234567890123456789012345678901234567890123456789012345678901234567890')
    print(' ' * 41 + '^-------^')
    print(' ' * 41 + '42-49 (MR field)')
    print(' ' * 41 + '^- Mixing ratio must start at column 42')
    print()
    
    g_records_analyzed = 0
    mr_errors = 0
    error_details = []
    
    lines = get_stripped_lines(filename)
    
    for line_num, line_content in enumerate(lines, 1):
        
        # Only check G-records (column 8='G', columns 6-7 are blank)
        if len(line_content) < 50:
            continue
        if not (line_content[7] == 'G' and line_content[5] == ' ' and line_content[6] == ' '):
            continue
        
        g_records_analyzed += 1
        
        # Extract MR field area (columns 42-49, 0-based index 41:49)
        mr_field = line_content[41:49]
        
        # Skip if MR field is completely empty
        if not mr_field.strip():
            continue
        
        # Check if MR value is LEFT-JUSTIFIED (starts at column 42)
        col42_char = line_content[41]  # Column 42 (0-based index 41)
        
        if col42_char == ' ' and mr_field.strip():
            # MR value is shifted right (doesn't start at column 42)
            mr_errors += 1
            
            # Find where it actually starts
            actual_start = 42
            for i, char in enumerate(mr_field):
                if char not in [' ', '']:
                    actual_start = 42 + i
                    break
            
            error_details.append({
                'line_num': line_num,
                'line': line_content,
                'mr_field': mr_field,
                'actual_start': actual_start
            })
            
            if mr_errors <= 10:
                print(f"[ERROR] Line {line_num}: Mixing ratio shifted right")
                print(f"   MR field (cols 42-49): [{mr_field}]")
                print(f"   MR starts at column {actual_start} (should be 42)")
                print(f"   Full line: {line_content}")
                print(f"   FIX: Remove leading spaces to LEFT-JUSTIFY at column 42")
                print()
    
    if mr_errors > 10:
        print(f"... and {mr_errors - 10} more errors (showing first 10 only)")
        print()
    
    print(f"MR FIELD SUMMARY:")
    print(f"  G-records with MR field analyzed: {sum(1 for _, line in enumerate(open(filename)) if len(line) >= 50 and line[7] == 'G' and line[5] == ' ' and line[6] == ' ' and line[41:49].strip())}")
    print(f"  Mixing ratio positioning errors: {mr_errors}")
    print()
    
    if mr_errors == 0:
        print(f"[OK] SUCCESS: All mixing ratio values correctly LEFT-JUSTIFIED at column 42")
        return True
    else:
        print(f"[ERROR] ERRORS: {mr_errors} mixing ratio field positioning errors found!")
        return False

def validate_cc_field(filename):
    """
    Validate CC field (columns 56-62) positioning in G-records.
    
    CRITICAL VALIDATION: Ensures conversion coefficient values are LEFT-JUSTIFIED at column 56.
    
    ENSDF G-Record Format:
    - Columns 50-55: MR uncertainty (DMR field)
    - Columns 56-62: Conversion coefficient (CC field) - LEFT-JUSTIFIED at column 56
    - Columns 63-64: CC uncertainty (DCC field)
    
    Conversion coefficient examples: 0.090, 0.05, 1.23, etc.
    """
    print(f"\nCC FIELD POSITIONING VALIDATION: {filename}")
    print("=" * 60)
    print("Checking CC field (conversion coefficient) LEFT-JUSTIFICATION at column 56...")
    print("ENSDF Rule: Conversion coefficient values must start at column 56")
    print()
    print('ENSDF 80-Column Ruler:')
    print('         1         2         3         4         5         6         7         8')
    print('12345678901234567890123456789012345678901234567890123456789012345678901234567890')
    print(' ' * 55 + '^------^')
    print(' ' * 55 + '56-62 (CC field)')
    print(' ' * 55 + '^- CC must start at column 56')
    print()
    
    g_records_analyzed = 0
    cc_errors = 0
    
    lines = get_stripped_lines(filename)
    
    for line_num, line_content in enumerate(lines, 1):
        
        # Only check G-records
        if len(line_content) < 63:
            continue
        if not (line_content[7] == 'G' and line_content[5] == ' ' and line_content[6] == ' '):
            continue
        
        g_records_analyzed += 1
        
        # Extract CC field area (columns 56-62, 0-based index 55:62)
        cc_field = line_content[55:62]
        
        # Skip if CC field is completely empty
        if not cc_field.strip():
            continue
        
        # Check if CC value is LEFT-JUSTIFIED (starts at column 56)
        col56_char = line_content[55]  # Column 56 (0-based index 55)
        
        if col56_char == ' ' and cc_field.strip():
            # CC value is shifted right
            cc_errors += 1
            
            if cc_errors <= 10:
                print(f"[ERROR] Line {line_num}: Conversion coefficient shifted right")
                print(f"   CC field (cols 56-62): [{cc_field}]")
                print(f"   Full line: {line_content}")
                print(f"   FIX: Remove leading spaces to LEFT-JUSTIFY at column 56")
                print()
    
    if cc_errors > 10:
        print(f"... and {cc_errors - 10} more errors (showing first 10 only)")
        print()
    
    print(f"CC FIELD SUMMARY:")
    print(f"  G-records with CC field: {sum(1 for _, line in enumerate(open(filename)) if len(line) >= 63 and line[7] == 'G' and line[5] == ' ' and line[6] == ' ' and line[55:62].strip())}")
    print(f"  CC positioning errors: {cc_errors}")
    print()
    
    if cc_errors == 0:
        print(f"[OK] SUCCESS: All conversion coefficient values correctly LEFT-JUSTIFIED at column 56")
        return True
    else:
        print(f"[ERROR] ERRORS: {cc_errors} CC field positioning errors found!")
        return False

def validate_ti_field(filename):
    """
    Validate TI field (columns 65-74) positioning in G-records.
    
    CRITICAL VALIDATION: Ensures total intensity values are LEFT-JUSTIFIED at column 65.
    
    ENSDF G-Record Format:
    - Columns 63-64: CC uncertainty (DCC field)
    - Columns 65-74: Total transition intensity (TI field) - LEFT-JUSTIFIED at column 65
    - Columns 75-76: TI uncertainty (DTI field)
    
    Total intensity examples: 71.0, 5.1, 100.0, etc.
    """
    print(f"\nTI FIELD POSITIONING VALIDATION: {filename}")
    print("=" * 60)
    print("Checking TI field (total intensity) LEFT-JUSTIFICATION at column 65...")
    print("ENSDF Rule: Total intensity values must start at column 65")
    print()
    print('ENSDF 80-Column Ruler:')
    print('         1         2         3         4         5         6         7         8')
    print('12345678901234567890123456789012345678901234567890123456789012345678901234567890')
    print(' ' * 64 + '^---------^')
    print(' ' * 64 + '65-74 (TI field)')
    print(' ' * 64 + '^- TI must start at column 65')
    print()
    
    g_records_analyzed = 0
    ti_errors = 0
    
    lines = get_stripped_lines(filename)
    
    for line_num, line_content in enumerate(lines, 1):
        
        # Only check G-records
        if len(line_content) < 75:
            continue
        if not (line_content[7] == 'G' and line_content[5] == ' ' and line_content[6] == ' '):
            continue
        
        g_records_analyzed += 1
        
        # Extract TI field area (columns 65-74, 0-based index 64:74)
        ti_field = line_content[64:74]
        
        # Skip if TI field is completely empty
        if not ti_field.strip():
            continue
        
        # Check if TI value is LEFT-JUSTIFIED (starts at column 65)
        col65_char = line_content[64]  # Column 65 (0-based index 64)
        
        if col65_char == ' ' and ti_field.strip():
            # TI value is shifted right
            ti_errors += 1
            
            if ti_errors <= 10:
                print(f"[ERROR] Line {line_num}: Total intensity shifted right")
                print(f"   TI field (cols 65-74): [{ti_field}]")
                print(f"   Full line: {line_content}")
                print(f"   FIX: Remove leading spaces to LEFT-JUSTIFY at column 65")
                print()
    
    if ti_errors > 10:
        print(f"... and {ti_errors - 10} more errors (showing first 10 only)")
        print()
    
    print(f"TI FIELD SUMMARY:")
    print(f"  G-records with TI field: {sum(1 for _, line in enumerate(open(filename)) if len(line) >= 75 and line[7] == 'G' and line[5] == ' ' and line[6] == ' ' and line[64:74].strip())}")
    print(f"  TI positioning errors: {ti_errors}")
    print()
    
    if ti_errors == 0:
        print(f"[OK] SUCCESS: All total intensity values correctly LEFT-JUSTIFIED at column 65")
        return True
    else:
        print(f"[ERROR] ERRORS: {ti_errors} TI field positioning errors found!")
        return False

def validate_dti_field(filename):
    """
    Validate DTI field (TI uncertainty) positioning in columns 75-76 for G-records.
    
    ENSDF Rule: DTI field is 2 columns (75-76).
    Content must be numeric or standard markers (LT/GT).
    Any Alphabetic character (A-Z) in this field is likely a shifted flag.
    """
    print(f"\nDTI FIELD VALIDATION: {filename}")
    print("=" * 60)
    print("Checking DTI field content in columns 75-76...")
    print("ENSDF Rule: DTI field must contain uncertainty (digits) or markers.")
    print("           It must NOT contain comment flags (A-Z).")
    print()
    
    dti_errors = 0
    dti_analyzed = 0
    
    lines = get_stripped_lines(filename)
    
    for line_num, line_content in enumerate(lines, 1):
        if len(line_content) < 76 or line_content[7] != 'G':
            continue
            
        # Skip comment lines (cG)
        if line_content[5] != ' ' or line_content[6] != ' ':
            continue

        # Extract DTI (cols 75-76, index 74-76)
        dti_field = line_content[74:76]
        dti_stripped = dti_field.strip()
        
        if dti_stripped:
            dti_analyzed += 1
            # Check for invalid characters (Shifted Flags)
            # Allowed: Digits, space, 'L', 'T', 'G' (LT/GT), '<', '>' (if used?)
            # ENSDF usually uses LT/GT codes in uncertainty fields, or just digits.
            # If we see any other alpha char, it's an error.
            if any(c.isalpha() and c not in {'L', 'T', 'G'} for c in dti_stripped):
                 print(f"[ERROR] Line {line_num}: Invalid character in DTI field (columns 75-76)")
                 print(f"   Found '{dti_stripped}' in DTI field.")
                 print(f"   If this is a Flag (e.g. 'A', 'X'), it must be in Column 77.")
                 print(f"   Line: {line_content}")
                 dti_errors += 1
            
            # Check Left-Justification (if it starts with space but has content)
            if dti_field[0] == ' ' and len(dti_stripped) > 0:
                 # Strictly enforce left justification?
                 # If " 3", technically readable but standard prefers "3 ".
                 # We will warn or error.
                 # Given user strictness: ERROR.
                 print(f"[ERROR] Line {line_num}: DTI field not LEFT-JUSTIFIED")
                 print(f"   Found '{dti_field}'. Content '{dti_stripped}' should start at Column 75.")
                 print(f"   Line: {line_content}")
                 dti_errors += 1

    print(f"DTI FIELD SUMMARY:")
    print(f"  G-records with DTI: {dti_analyzed}")
    print(f"  DTI errors: {dti_errors}")
    print()
    
    return dti_errors == 0

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
    
    lines = get_stripped_lines(filename)
    
    for line_num, line_content in enumerate(lines, 1):
        
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
    
    lines = get_file_lines(filename)
    
    # Check for line length issues in data record lines only
    length_issues = []
    tab_issues = []
    for line_num, line in enumerate(lines, 1):
        line_content = line.rstrip('\n\r')
        length = len(line_content)
        
        # Only check data record lines for 80-character compliance
        if is_data_record_line(line_content):
            if length != 80:
                length_issues.append((line_num, length, line_content[7] if len(line_content) > 7 else '?'))
            if '\t' in line_content:
                tab_issues.append((line_num, line_content[7] if len(line_content) > 7 else '?'))
    
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

    if tab_issues:
        print("DATA RECORD TAB CHARACTER ISSUES DETECTED:")
        for line_num, record_type in tab_issues:
            print(f"  Line {line_num}: {record_type} record contains tab characters; ENSDF requires spaces only")
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
        if length_issues == [] and tab_issues == []:
            print("SUCCESS: All data record lines are exactly 80 characters and contain no tabs!")
    else:
        print("ERROR: Field positioning errors found - see details above")
    
    # Always validate all field positions unless header-only mode
    if not header_only:
        validation_checks = [
            ("Energy field (E)", validate_e_field(filename)),
            ("Energy uncertainty (DE)", validate_de_field(filename)),
            ("Spectroscopic factor (S)", validate_s_field(filename)),
            ("Spin/Parity (J|p)", validate_jp_field(filename)),
            ("Gamma RI field", validate_ri_field(filename)),
            ("Gamma DRI field", validate_dri_field(filename)),
            ("Multipolarity (M)", validate_m_field(filename)),
            ("Mixing ratio (MR)", validate_mr_field(filename)),
            ("MUL tag", validate_mul_field(filename)),
            ("Conversion coefficient (CC)", validate_cc_field(filename)),
            ("Transition intensity (TI)", validate_ti_field(filename)),
            ("Transition intensity uncertainty (DTI)", validate_dti_field(filename)),
            ("GT/LT placement", validate_gt_lt_placement(filename)),
            ("Comment flags", validate_comment_flags(filename)),
            ("G-record flags", validate_g_record_flags(filename)),
        ]

        print("\nField Validation Summary:")
        max_name = max(len(name) for name, _ in validation_checks)
        for name, result in validation_checks:
            status = "PASS" if result else "FAIL"
            print(f"  [{status:<4}] {name.ljust(max_name)}")

        all_validation_success = all(result for _, result in validation_checks)
        return (not errors_found) and all_validation_success
        
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
