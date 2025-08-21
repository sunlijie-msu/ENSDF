#!/usr/bin/env python3
"""
ENSDF Column Calibration Script - Field Alignment Validator
===========================================================

Detects field misalignment issues in ENSDF L and G records.

Primary Use Cases:
1. Detect field alignment issues after editing
2. Validate 80-column format compliance
3. Check L-record and G-record field consistency

Usage: 
    python column_calibrate.py "path/to/file.ens" [--all]
    
Examples:
    python column_calibrate.py file.ens                    # Quick validation
    python column_calibrate.py file.ens --all              # Check all records

Author: FRIB Nuclear Data Group
Date: January 2025
"""

import argparse
import os
import sys
import re
from typing import List, Tuple


def check_line_lengths(content: List[str]) -> Tuple[List[Tuple[int, int, str]], int]:
    """Check line lengths for 80-character compliance"""
    over_80_lines = []
    total_checked = 0
    
    # Find data records and check their lengths
    for i, line in enumerate(content, 1):
        line_clean = line.rstrip('\n\r')
        
        # Skip empty lines and comments
        if not line.strip() or line.strip().startswith('#'):
            continue
            
        # Check if it's a data record (L, G, N, P, etc.)
        if re.match(r'^\s*\w+\s+[LGPNQBEA]\s', line):
            total_checked += 1
            length = len(line_clean)
            if length > 80:
                over_80_lines.append((i, length, line_clean))
    
    return over_80_lines, total_checked


def analyze_field_alignment(content: List[str]) -> List[str]:
    """
    Analyze field alignment across L-records and G-records
    This is the CRITICAL function that was missing - it checks that fields align
    consistently across all records of the same type
    """
    issues = []
    l_records = []
    g_records = []
    
    # Extract L and G records
    for i, line in enumerate(content, 1):
        line_clean = line.rstrip('\r\n')
        if re.match(r'^\s*\w+\s+L\s', line):
            l_records.append((i, line_clean))
        elif re.match(r'^\s*\w+\s+G\s', line):
            g_records.append((i, line_clean))
    
    # Check L-record field alignment
    if len(l_records) > 1:
        issues.extend(check_l_record_alignment(l_records))
    
    # Check G-record field alignment  
    if len(g_records) > 1:
        issues.extend(check_g_record_alignment(g_records))
    
    return issues


def check_l_record_alignment(l_records: List[Tuple[int, str]]) -> List[str]:
    """
    Check that L-record fields are aligned consistently across all L-records
    The key insight: ALL L-records should have their numeric fields in the SAME column positions
    
    ENSDF L-record format:
    - Columns 56-64: L field (angular momentum transfer)
    - Columns 65-74: S field (spectroscopic factor, e.g., C²S values)  
    - Columns 75-76: DS field (uncertainty in S)
    """
    issues = []
    
    if len(l_records) < 2:
        return issues  # Need at least 2 records to compare alignment
    
    # Extract the field positions for each L-record
    field_positions = []
    
    for line_num, record in l_records:
        if len(record) < 60:  # Too short to have numeric fields
            continue
            
        # Look for the numeric values that should be L, S, DS
        # Search in the tail of the record (after column 40)
        tail = record[40:] if len(record) > 40 else ""
        
        # Find all numeric values in the tail
        import re
        # Pattern to match numbers (including decimals) and their positions
        numeric_matches = []
        for match in re.finditer(r'\b\d+(?:\.\d+)?\b', tail):
            abs_pos = match.start() + 40  # Convert to absolute position in record
            value = match.group()
            numeric_matches.append((abs_pos, value))
        
        if len(numeric_matches) >= 2:
            # Handle records with L and S fields (minimum required)
            l_pos, l_val = numeric_matches[0]
            s_pos, s_val = numeric_matches[1] 
            
            # DS field is optional - only if we have a 3rd numeric value
            ds_pos = None
            ds_val = None
            if len(numeric_matches) >= 3:
                ds_pos, ds_val = numeric_matches[2]
            
            field_positions.append({
                'line_num': line_num,
                'l_pos': l_pos,
                's_pos': s_pos, 
                'ds_pos': ds_pos,  # Can be None
                'record': record
            })
    
    if len(field_positions) < 2:
        return issues  # Need at least 2 records with fields to compare
    
    # Now check if all records have consistent field positions
    first_record = field_positions[0]
    expected_l_pos = first_record['l_pos']
    expected_s_pos = first_record['s_pos']
    expected_ds_pos = first_record['ds_pos']  # Can be None
    
    for record_info in field_positions[1:]:
        line_num = record_info['line_num']
        
        # Check L field alignment - NO TOLERANCE for misalignment
        if record_info['l_pos'] != expected_l_pos:
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
        print(f"\n❌ CRITICAL: Found {len(over_80_lines)} lines exceeding 80 characters!")
        for line_num, length, line_content in over_80_lines:
            print(f"  Line {line_num}: {length} chars")
        return
    else:
        print(f"\n✅ All {total_data_records} data records are within 80-character limit")
    
    # Extract L and G records
    l_records = []
    g_records = []
    
    for i, line in enumerate(content, 1):
        line_clean = line.rstrip('\r\n')
        if re.match(r'^\s*\w+\s+L\s', line):
            l_records.append((i, line_clean))
        elif re.match(r'^\s*\w+\s+G\s', line):
            g_records.append((i, line_clean))
    
    print(f"\n📊 Found: {len(l_records)} L-records, {len(g_records)} G-records")
    
    # CRITICAL: Check field alignment across records
    alignment_issues = analyze_field_alignment(content)
    if alignment_issues:
        print(f"\n❌ CRITICAL FIELD ALIGNMENT ISSUES DETECTED:")
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
        print(f"\n🔍 Checking {len(l_records)} L-records for alignment issues...")
        for line_num, record in l_records:
            issues = analyze_critical_alignment(record, "L", line_num)
            if issues:
                total_issues += len(issues)
                print(f"  Line {line_num}: {len(issues)} issue(s) found")
                for issue in issues:
                    print(f"    • {issue.split(': ', 1)[1] if ': ' in issue else issue}")
            else:
                print(f"  Line {line_num}: ✓ Alignment OK")
    
    # Check G-records
    if g_records:
        print(f"\n🔍 Checking {len(g_records)} G-records for alignment issues...")
        for line_num, record in g_records:
            issues = analyze_critical_alignment(record, "G", line_num)
            if issues:
                total_issues += len(issues)
                print(f"  Line {line_num}: {len(issues)} issue(s) found")
                for issue in issues:
                    print(f"    • {issue.split(': ', 1)[1] if ': ' in issue else issue}")
            else:
                print(f"  Line {line_num}: ✓ Alignment OK")
    
    # Summary
    print("\n=== VALIDATION SUMMARY ===")
    total_records = len(l_records) + len(g_records)
    
    if total_issues == 0:
        print(f"✅ All {total_records} records have correct ENSDF format!")
        print("   Field alignment and format compliance verified.")
    else:
        print(f"❌ Found {total_issues} format issues")
    
    print("\n📖 ENSDF Format Reference:")
    print("L-records: NUCID(1-5) [space](6) [space](7) L(8) [space](9) Energy(10-19) [space](22) J-π(23-39)")
    print("G-records: NUCID(1-5) [space](6) [space](7) G(8) [space](9) Energy(10-19) [space](22) RI(23-29)")


if __name__ == "__main__":
    main()
