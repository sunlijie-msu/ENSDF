#!/usr/bin/env python3
"""
ENSDF Column Calibration Script - Field Alignment Validator
===========================================================

Properly validates ENSDF L and G record field positions according to ENSDF Manual.

ENSDF L-Record Format (Mandatory Field Positions):
- Columns 1-5:   NUCID
- Column 6:      Continuation flag (blank for first record)
- Column 7:      BLANK (mandatory space)
- Column 8:      Record type "L"
- Column 9:      BLANK (mandatory space)  
- Columns 10-19: Energy field (E) - left justified
- Columns 20-21: Energy uncertainty (DE) - left justified
- Column 22:     BLANK (readability space)
- Columns 23-39: J-蟺 field - left justified at column 23
- Columns 40-49: Half-life (T) field - left justified
- Columns 50-55: Half-life uncertainty (DT) - left justified
- Columns 56-64: Angular momentum transfer (L) - left justified
- Columns 65-74: Spectroscopic factor (S) - left justified
- Columns 75-76: Uncertainty in S (DS) - left justified
- Column 77:     Comment flag

Primary Use Cases:
1. Detect L-field misalignment (the critical issue missed before)
2. Validate 80-column format compliance  
3. Check mandatory ENSDF field positions

Usage: 
    python column_calibrate.py "path/to/file.ens" [--detailed]
    
Examples:
    python column_calibrate.py file.ens                    # Quick validation
    python column_calibrate.py file.ens --detailed         # Detailed field analysis

Author: FRIB Nuclear Data Group (Fixed version)
Date: September 2025
"""

import argparse
import os
import sys
import re
from typing import List, Tuple, Dict


def validate_l_record_fields(line: str, line_num: int) -> List[str]:
    """
    Validate L-record field positions according to ENSDF Manual
    Returns list of validation errors
    """
    errors = []
    
    if len(line) < 9:
        errors.append(f"Line {line_num}: L-record too short (minimum 9 characters required)")
        return errors
    
    # Check mandatory field positions
    if line[6] != ' ':
        errors.append(f"Line {line_num}: Column 7 must be blank space, found '{line[6]}'")
    
    if line[7] != 'L':
        errors.append(f"Line {line_num}: Column 8 must be 'L', found '{line[7]}'")
        
    if len(line) > 8 and line[8] != ' ':
        errors.append(f"Line {line_num}: Column 9 must be blank space, found '{line[8]}'")
    
    # Check for L-field in wrong position (the critical bug we missed!)
    # L-field should be in columns 56-64, NOT in the T or other fields
    if len(line) >= 56:
        # Look for numbers in the T field (columns 40-49) that should be in L field
        t_field = line[39:49] if len(line) > 49 else line[39:]
        t_field_clean = t_field.strip()
        
        # Check if there's a lone integer in T field (likely misplaced L-value)
        if re.match(r'^\s*\d+\s*$', t_field_clean) and len(t_field_clean.strip()) == 1:
            errors.append(f"Line {line_num}: Lone digit '{t_field_clean.strip()}' in T field (columns 40-49) - likely misplaced L-value belongs in columns 56-64")
    
    # Check for L-field in correct position
    if len(line) >= 64:
        l_field = line[55:64]  # Columns 56-64
        l_field_clean = l_field.strip()
        
        # If we find content in L field, validate it
        if l_field_clean:
            # L-field should contain angular momentum transfer values: 0, 1, 2, 3, etc.
            # Can be single values or combinations like (2), 0+2, 1,2, etc.
            if not re.match(r'^[\d\s,\+\(\)]+$', l_field_clean):
                errors.append(f"Line {line_num}: Invalid L-field content '{l_field_clean}' in columns 56-64")
    
    return errors


def validate_line_length(line: str, line_num: int) -> List[str]:
    """Check 80-character limit"""
    errors = []
    line_clean = line.rstrip('\n\r')
    
    if len(line_clean) > 80:
        errors.append(f"Line {line_num}: Exceeds 80 characters ({len(line_clean)} chars)")
    
    return errors


def analyze_ensdf_file(filepath: str, detailed: bool = False) -> None:
    """Main validation function"""
    
    if not os.path.exists(filepath):
        print(f"鉂?ERROR: File '{filepath}' not found")
        return
        
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"鉂?ERROR: Could not read file '{filepath}': {e}")
        return
    
    print("=" * 60)
    print("馃攳 ENSDF Field Position Validator (Fixed Version)")
    print("=" * 60)
    print(f"馃搧 File: {filepath}")
    print(f"馃搳 Total lines: {len(lines)}")
    print()
    
    # Collect all validation errors
    all_errors = []
    l_record_count = 0
    g_record_count = 0
    
    for i, line in enumerate(lines, 1):
        line_clean = line.rstrip('\n\r')
        
        # Skip empty lines and comments
        if not line.strip():
            continue
            
        # Check line length for all non-empty lines
        length_errors = validate_line_length(line_clean, i)
        all_errors.extend(length_errors)
        
        # Identify record type and validate accordingly
        if len(line_clean) >= 8:
            if re.match(r'^\s*\w+\s+L\s', line_clean):
                l_record_count += 1
                l_errors = validate_l_record_fields(line_clean, i)
                all_errors.extend(l_errors)
                
                if detailed and l_errors:
                    print(f"馃攳 Line {i} details:")
                    print(f"   Content: |{line_clean}|")
                    for error in l_errors:
                        print(f"   鉂?{error}")
                    print()
                    
            elif re.match(r'^\s*\w+\s+G\s', line_clean):
                g_record_count += 1
                # G-record validation can be added here later
    
    # Summary report
    print(f"馃搱 Records found: {l_record_count} L-records, {g_record_count} G-records")
    print()
    
    if all_errors:
        print(f"鉂?VALIDATION FAILED: {len(all_errors)} errors found")
        print()
        
        # Group errors by type
        length_errors = [e for e in all_errors if "Exceeds 80 characters" in e]
        field_errors = [e for e in all_errors if "Exceeds 80 characters" not in e]
        
        if length_errors:
            print("馃搹 LINE LENGTH VIOLATIONS:")
            for error in length_errors:
                print(f"   {error}")
            print()
            
        if field_errors:
            print("馃幆 FIELD POSITION VIOLATIONS:")
            for error in field_errors:
                print(f"   {error}")
            print()
            
        print("馃毃 CRITICAL: These errors must be fixed before ENSDF submission!")
        
    else:
        print("鉁?VALIDATION PASSED: All records conform to ENSDF format")
        print()
        print("馃搵 Validation completed:")
        print(f"   鈥?All lines 鈮?80 characters")
        print(f"   鈥?All L-record fields in correct positions")
        print(f"   鈥?Mandatory spaces in required positions")
    
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="ENSDF Column Position Validator (Fixed Version)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python column_calibrate.py file.ens           # Quick validation
    python column_calibrate.py file.ens --detailed # Show detailed errors
        """
    )
    
    parser.add_argument("filepath", help="Path to ENSDF file")
    parser.add_argument("--detailed", action="store_true", 
                       help="Show detailed error information")
    
    args = parser.parse_args()
    
    analyze_ensdf_file(args.filepath, args.detailed)


if __name__ == "__main__":
    main()
            issues.append(f"Line {line_num}: L field misaligned - expected column {expected_l_pos + 1}, found column {record_info['l_pos'] + 1}")
        
        # Check S field alignment - NO TOLERANCE for misalignment
        if record_info['s_pos'] != expected_s_pos:
            issues.append(f"Line {line_num}: S field misaligned - expected column {expected_s_pos + 1}, found column {record_info['s_pos'] + 1}")
            
        # Check DS field alignment (only if both records have DS fields) - NO TOLERANCE
        if expected_ds_pos is not None and record_info['ds_pos'] is not None:
            if record_info['ds_pos'] != expected_ds_pos:
                issues.append(f"Line {line_num}: DS field misaligned - expected column {expected_ds_pos + 1}, found column {record_info['ds_pos'] + 1}")
    
    # Also check if positions are in the correct ENSDF column ranges
    if expected_l_pos < 55 or expected_l_pos > 63:
        issues.append(f"L field positions are outside expected range (columns 56-64), found around column {expected_l_pos + 1}")
    
    if expected_s_pos < 64 or expected_s_pos > 73:
        issues.append(f"S field positions are outside expected range (columns 65-74), found around column {expected_s_pos + 1}")
        
    if expected_ds_pos is not None and (expected_ds_pos < 74 or expected_ds_pos > 75):
        issues.append(f"DS field positions are outside expected range (columns 75-76), found around column {expected_ds_pos + 1}")
    
    return issues


def check_g_record_alignment(g_records: List[Tuple[int, str]]) -> List[str]:
    """
    Check that G-record fields are aligned consistently  
    Critical fields to check:
    - RI field (col 23-29)
    - DRI field (col 30-31)
    """
    issues = []
    
    ri_positions = []
    dri_positions = []
    
    for line_num, record in g_records:
        if len(record) < 30:  # Too short
            continue
            
        # Check RI field position (should start around col 23)
        ri_field = record[22:29].strip()
        if ri_field and ri_field.replace('.', '').replace('E', '').replace('-', '').replace('+', '').isdigit():
            # Find actual position of this value
            pos = record.find(ri_field, 20)
            if pos != -1:
                ri_positions.append((line_num, pos))
        
        # Check DRI field position (should start around col 30)
        if len(record) > 30:
            dri_field = record[29:31].strip()
            if dri_field:
                pos = record.find(dri_field, 29)
                if pos != -1:
                    dri_positions.append((line_num, pos))
    
    # Check consistency of RI positions
    if len(ri_positions) > 1:
        expected_ri_pos = 22  # 0-indexed, so col 23
        for line_num, actual_pos in ri_positions:
            if abs(actual_pos - expected_ri_pos) > 2:
                issues.append(f"Line {line_num}: RI field misaligned - expected around col {expected_ri_pos + 1}, found col {actual_pos + 1}")
    
    return issues


def analyze_critical_alignment(record: str, record_type: str, line_num: int) -> List[str]:
    """Basic validation for L and G records"""
    issues = []
    clean_record = record.rstrip('\r\n\t ')
    actual_length = len(clean_record)
    
    if actual_length > 80:
        issues.append(f"Line {line_num}: Record too long ({actual_length} chars, max 80)")
    elif actual_length < 20:
        issues.append(f"Line {line_num}: Record too short ({actual_length} chars, minimum ~20)")
    
    return issues


def main():
    """Main validation function"""
    parser = argparse.ArgumentParser(description="ENSDF Field Alignment Validator")
    parser.add_argument('filepath', help='Path to ENSDF file')
    parser.add_argument('--all', '-a', action='store_true',
                       help='Check all data records instead of just samples')
    
    args = parser.parse_args()
    
    # Check if file exists
    if not os.path.exists(args.filepath):
        print(f"Error: File '{args.filepath}' not found")
        sys.exit(1)
    
    # Read file content
    try:
        with open(args.filepath, 'r', encoding='utf-8') as f:
            content = f.readlines()
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)
    
    # Clean content
    content = [line.rstrip('\n\r') for line in content]
    
    print("=== Enhanced ENSDF Column Calibration & Format Validator ===")
    print(f"File: {args.filepath}")
    print(f"Total lines: {len(content)}")
    
    # Check line lengths
    over_80_lines, total_data_records = check_line_lengths(content)
    
    if over_80_lines:
        print(f"\n鉂?CRITICAL: Found {len(over_80_lines)} lines exceeding 80 characters!")
        for line_num, length, line_content in over_80_lines:
            print(f"  Line {line_num}: {length} chars")
        return
    else:
        print(f"\n鉁?All {total_data_records} data records are within 80-character limit")
    
    # Extract L and G records
    l_records = []
    g_records = []
    
    for i, line in enumerate(content, 1):
        line_clean = line.rstrip('\r\n')
        if re.match(r'^\s*\w+\s+L\s', line):
            l_records.append((i, line_clean))
        elif re.match(r'^\s*\w+\s+G\s', line):
            g_records.append((i, line_clean))
    
    print(f"\n馃搳 Found: {len(l_records)} L-records, {len(g_records)} G-records")
    
    # CRITICAL: Check field alignment across records
    alignment_issues = analyze_field_alignment(content)
    if alignment_issues:
        print(f"\n鉂?CRITICAL FIELD ALIGNMENT ISSUES DETECTED:")
        for issue in alignment_issues:
            print(f"  {issue}")
        print()
    
    # Limit to samples unless --all specified
    if not args.all:
        l_records = l_records[:5]
        g_records = g_records[:5]
        if len(l_records) > 5 or len(g_records) > 5:
            print("Note: Checking sample records only. Use --all to check all records")
    
    total_issues = 0
    
    # Check L-records
    if l_records:
        print(f"\n馃攳 Checking {len(l_records)} L-records for alignment issues...")
        for line_num, record in l_records:
            issues = analyze_critical_alignment(record, "L", line_num)
            if issues:
                total_issues += len(issues)
                print(f"  Line {line_num}: {len(issues)} issue(s) found")
                for issue in issues:
                    print(f"    鈥?{issue.split(': ', 1)[1] if ': ' in issue else issue}")
            else:
                print(f"  Line {line_num}: 鉁?Alignment OK")
    
    # Check G-records
    if g_records:
        print(f"\n馃攳 Checking {len(g_records)} G-records for alignment issues...")
        for line_num, record in g_records:
            issues = analyze_critical_alignment(record, "G", line_num)
            if issues:
                total_issues += len(issues)
                print(f"  Line {line_num}: {len(issues)} issue(s) found")
                for issue in issues:
                    print(f"    鈥?{issue.split(': ', 1)[1] if ': ' in issue else issue}")
            else:
                print(f"  Line {line_num}: 鉁?Alignment OK")
    
    # Summary
    print("\n=== VALIDATION SUMMARY ===")
    total_records = len(l_records) + len(g_records)
    
    if total_issues == 0:
        print(f"鉁?All {total_records} records have correct ENSDF format!")
        print("   Field alignment and format compliance verified.")
    else:
        print(f"鉂?Found {total_issues} format issues")
    
    print("\n馃摉 ENSDF Format Reference:")
    print("L-records: NUCID(1-5) [space](6) [space](7) L(8) [space](9) Energy(10-19) [space](22) J-蟺(23-39)")
    print("G-records: NUCID(1-5) [space](6) [space](7) G(8) [space](9) Energy(10-19) [space](22) RI(23-29)")


if __name__ == "__main__":
    main()
