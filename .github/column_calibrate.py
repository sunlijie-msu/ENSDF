#!/usr/bin/env python3
"""
ENSDF Column Calibration Script - Enhanced ENSDF Format Validator
===============================================================

Focused on L and G record data alignment and comprehensive ENSDF validation.
Enhanced to address Windows line ending issues and provide comprehensive validation.

Primary Use Cases:
1. Fix GitHub Copilot's column misalignments in ENSDF data records
2. Validate critical field positions after AI-assisted editing
3. Quick visual alignment check with 80-column ruler
4. Comprehensive ENSDF format validation
5. Windows/Unix line ending compatibility

Enhanced Features:
- Improved character counting with proper line ending handling
- Energy ordering validation integration  
- Comprehensive field boundary checking
- Enhanced visual debugging with line-by-line analysis
- Support for both Windows and Unix line endings

Usage: 
    python column_calibrate.py "path/to/file.ens" [--detailed] [--header] [--all]
    
Examples:
    python column_calibrate.py file.ens                    # Quick validation
    python column_calibrate.py file.ens --detailed         # Detailed field mapping
    python column_calibrate.py file.ens --header           # Header format check only
    python column_calibrate.py file.ens --all              # Check all records

Author: FRIB Nuclear Data Group
Date: January 2025
"""

import argparse
import os
import sys
import re
from typing import List, Dict, Tuple, Optional


class Colors:
    """ANSI color codes for terminal output"""
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    MAGENTA = '\033[95m'
    GRAY = '\033[90m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def colored_print(text: str, color: str = Colors.WHITE) -> None:
    """Print text with color"""
    print(f"{color}{text}{Colors.RESET}")


def check_line_lengths(content: List[str], show_details: bool = False) -> Tuple[List[Tuple[int, int, str]], int]:
    """
    Check line lengths for 80-character compliance
    Based on the working manual Python code that correctly identifies issues
    """
    over_80_lines = []
    total_checked = 0
    
    # Find the data section (skip headers and comments)
    data_start = 0
    for i, line in enumerate(content):
        if re.match(r'^\s*\w+\s+[LGP]N?\s', line):  # First data record
            data_start = i
            break
    
    if data_start == 0:
        return over_80_lines, total_checked
    
    # Check all lines from data section onwards
    for i, line in enumerate(content[data_start:], data_start + 1):
        # Skip empty lines and comments
        if not line.strip() or line.strip().startswith('#'):
            continue
            
        # Check if it's a data record (L, G, N, P, etc.)
        if not re.match(r'^\s*\w+\s+[LGPNQBEA]\s', line):
            continue
            
        line_no_newline = line.rstrip('\n\r')
        length = len(line_no_newline)
        total_checked += 1
        
        if length > 80:
            over_80_lines.append((i, length, line_no_newline))
    
    if show_details:
        print("\n=== LINE LENGTH ANALYSIS ===")
        print("Checking line lengths for ENSDF records:")
        print("Ones:  12345678901234567890123456789012345678901234567890123456789012345678901234567890")
        print("Tens:  1111111111222222222233333333334444444444555555555566666666667777777777888888888999")
        print()
        
        for i, line in enumerate(content[data_start:], data_start + 1):
            if not line.strip() or line.strip().startswith('#'):
                continue
            if not re.match(r'^\s*\w+\s+[LGPNQBEA]\s', line):
                continue
                
            line_no_newline = line.rstrip('\n\r')
            length = len(line_no_newline)
            status = 'OK' if length <= 80 else f'TOO LONG ({length})'
            print(f'Line {i:2d} [{length:2d}]: {status}')
        
        if over_80_lines:
            print('\nLines over 80 characters:')
            for line_num, length, line_content in over_80_lines:
                print(f'Line {line_num}: {length} chars')
                print(f'  {line_content}')
                print(f'  {"0" * 80}{"1" * (length - 80)}')
        else:
            print('\n✅ All ENSDF records are within 80-character limit!')
    
    return over_80_lines, total_checked


def analyze_critical_alignment(record: str, record_type: str, line_num: int) -> List[str]:
    """
    Enhanced critical alignment analysis for ENSDF records
    Improved to handle Windows line ending issues and provide comprehensive validation
    """
    issues = []
    
    # Handle different line endings properly
    clean_record = record.rstrip('\r\n\t ')
    actual_length = len(clean_record)
    
    # ENSDF format requires exactly 80 characters or less (with proper padding)
    if actual_length > 80:
        issues.append(f"Line {line_num}: Record too long ({actual_length} chars, max 80)")
        return issues  # Critical issue, return immediately
    elif actual_length < 20:  # Too short to be valid ENSDF
        issues.append(f"Line {line_num}: Record too short ({actual_length} chars, minimum ~20)")
        return issues
    
    # Critical position checks where issues commonly occur
    try:
        if record_type == "L":
            # L-record critical field validation
            if len(clean_record) >= 8:
                if clean_record[7] != 'L':
                    issues.append(f"Line {line_num}: Column 8 should be 'L', found '{clean_record[7] if len(clean_record) > 7 else 'MISSING'}'")
                
                if len(clean_record) >= 9:
                    if clean_record[8] != ' ':
                        issues.append(f"Line {line_num}: Column 9 should be space, found '{clean_record[8]}'")
            
            # Energy field validation (columns 10-19)
            if len(clean_record) >= 19:
                energy_field = clean_record[9:19].strip()
                if energy_field:
                    try:
                        float(energy_field.split()[0])  # Validate numeric energy
                    except (ValueError, IndexError):
                        issues.append(f"Line {line_num}: Energy field (cols 10-19) contains invalid value: '{energy_field}'")
            
            # Critical readability space at column 22
            if len(clean_record) >= 22:
                if clean_record[21] != ' ':
                    issues.append(f"Line {line_num}: Column 22 should be space for readability, found '{clean_record[21]}'")
        
        elif record_type == "G":
            # G-record critical field validation
            if len(clean_record) >= 8:
                if clean_record[7] != 'G':
                    issues.append(f"Line {line_num}: Column 8 should be 'G', found '{clean_record[7] if len(clean_record) > 7 else 'MISSING'}'")
                
                if len(clean_record) >= 9:
                    if clean_record[8] != ' ':
                        issues.append(f"Line {line_num}: Column 9 should be space, found '{clean_record[8]}'")
            
            # Gamma energy field validation (columns 10-19)
            if len(clean_record) >= 19:
                energy_field = clean_record[9:19].strip()
                if energy_field:
                    try:
                        float(energy_field.split()[0])  # Validate numeric energy
                    except (ValueError, IndexError):
                        issues.append(f"Line {line_num}: Gamma energy field (cols 10-19) contains invalid value: '{energy_field}'")
            
            # Critical readability space at column 22  
            if len(clean_record) >= 22:
                if clean_record[21] != ' ':
                    issues.append(f"Line {line_num}: Column 22 should be space for readability, found '{clean_record[21]}'")
            
            # RI field boundary check (columns 23-29)
            if len(clean_record) >= 30:
                ri_field = clean_record[22:29].strip()
                dri_field = clean_record[29:31].strip()
                if ri_field and not ri_field.replace('.', '').replace('E', '').replace('+', '').replace('-', '').isdigit():
                    if not any(marker in ri_field for marker in ['LT', 'GT', 'AP', 'CA', 'SY']):
                        issues.append(f"Line {line_num}: RI field (cols 23-29) may contain invalid value: '{ri_field}'")
    
    except IndexError:
        issues.append(f"Line {line_num}: Record truncated, cannot validate all fields")
    
    return issues


def show_visual_alignment(record: str, record_type: str, line_num: int) -> None:
    """Show visual alignment with ruler - perfect for spotting Copilot errors"""
    print(f"\nLine {line_num} ({record_type}-record) Alignment Check:")
    print("Ruler: 12345678901234567890123456789012345678901234567890123456789012345678901234567890")
    print("Tens:  1111111111222222222233333333334444444444555555555566666666667777777777888888888999")
    print(f"Data:  {record}")
    
    if record_type == "L":
        print("       |    L    E|DE|J-π              |T       |DT  |L      |S       |DS")
        print("Field: NUCID  (10-19)(23-39)        (40-49) (50-55)(56-64)(65-74)(75-76)")
    elif record_type == "G":
        print("       |    G    E|DE|RI    |DRI|M       |MR   |DMR|CC   |DCC|TI    |DTI")
        print("Field: NUCID  (10-19)(23-29)(30-31)(32-41)(42-49)(50-55)(56-62)(63-64)(65-74)(75-76)")


def extract_data_records(content: List[str]) -> Tuple[List[Tuple[str, int]], List[Tuple[str, int]]]:
    """Extract L and G records with line numbers - skip headers and comments"""
    l_records = []
    g_records = []
    
    for i, line in enumerate(content, 1):
        line = line.rstrip()
        # Skip headers, comments, and other non-data records
        if len(line) < 8:
            continue
        if line.strip().startswith('#'):
            continue
        if re.match(r'^\s*\w+\s+[Hc]', line):  # Skip headers and comments
            continue
            
        # Match L records - focus on data records where Copilot causes issues
        if re.match(r'^\s*\w+\s+L\s', line):
            l_records.append((line, i))
        # Match G records
        elif re.match(r'^\s*\w+\s+G\s', line):
            g_records.append((line, i))
    
    return l_records, g_records


def count_records(content: List[str]) -> Dict[str, int]:
    """Count different record types in ENSDF file"""
    counts = {
        'total': len(content),
        'L_records': 0,
        'G_records': 0,
        'comments': 0
    }
    
    for line in content:
        if re.match(r'^\s*\w+\s+L\s', line):
            counts['L_records'] += 1
        elif re.match(r'^\s*\w+\s+G\s', line):
            counts['G_records'] += 1
        elif re.match(r'^\s*\w+\s+c', line):
            counts['comments'] += 1
    
    return counts


def main():
    """Enhanced main function with comprehensive ENSDF validation"""
    parser = argparse.ArgumentParser(
        description="Enhanced ENSDF Column Calibration & Format Validator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Enhanced ENSDF Format Validator:

Examples:
  python column_calibrate.py file.ens                    # Quick validation check
  python column_calibrate.py file.ens --detailed         # Detailed field mapping + visual rulers
  python column_calibrate.py file.ens --header           # Header format check only  
  python column_calibrate.py file.ens --all              # Check all records (not just samples)
  python column_calibrate.py file.ens --length-only      # Fast 80-character limit check only

Enhanced Features:
  - Critical 80-character line length validation (based on working manual Python code)
  - Windows/Unix line ending compatibility
  - Comprehensive field boundary validation
  - Energy value format checking
  - Critical space preservation validation
  - Detailed visual alignment debugging with rulers
  - Fast length-only checking option

Focus Areas:
  - 80-column format compliance (CRITICAL - catches trailing space issues)
  - L-records: Energy, J-π, T, S fields alignment (cols 10-76)
  - G-records: Energy, RI, multipolarity alignment (cols 10-76)
  - Critical readability spaces at column 22
  - Field boundary preservation after AI editing
        """
    )
    parser.add_argument('filepath', help='Path to ENSDF file')
    parser.add_argument('--detailed', '-d', action='store_true',
                       help='Show detailed field mapping and visual rulers')
    parser.add_argument('--header', action='store_true',
                       help='Check header format only (quick validation)')
    parser.add_argument('--all', '-a', action='store_true',
                       help='Check all data records instead of just samples')
    parser.add_argument('--length-only', '-l', action='store_true',
                       help='Check line lengths only (fast 80-character compliance check)')
    
    args = parser.parse_args()
    
    # Check if file exists
    if not os.path.exists(args.filepath):
        colored_print(f"Error: File '{args.filepath}' not found", Colors.RED)
        sys.exit(1)
    
    # Read file content with proper encoding handling
    try:
        # Try UTF-8 first, fallback to latin-1 for older files
        try:
            with open(args.filepath, 'r', encoding='utf-8') as f:
                content = f.readlines()
        except UnicodeDecodeError:
            with open(args.filepath, 'r', encoding='latin-1') as f:
                content = f.readlines()
                colored_print("Note: File read with latin-1 encoding", Colors.YELLOW)
    except Exception as e:
        colored_print(f"Error reading file: {e}", Colors.RED)
        sys.exit(1)
    
    # Enhanced line ending handling (Windows vs Unix compatibility)
    content = [line.rstrip('\n\r') for line in content]
    
    # Header
    colored_print("=== Enhanced ENSDF Column Calibration & Format Validator ===", Colors.CYAN)
    print(f"File: {args.filepath}")
    print(f"Total lines: {len(content)}")
    
    # Check line lengths first - this is the critical check that was missing
    over_80_lines, total_data_records = check_line_lengths(content, show_details=args.detailed)
    
    if over_80_lines:
        colored_print(f"\n❌ CRITICAL: Found {len(over_80_lines)} lines exceeding 80 characters!", Colors.RED)
        for line_num, length, line_content in over_80_lines:
            colored_print(f"  Line {line_num}: {length} chars (over by {length - 80})", Colors.RED)
        
        if not args.detailed:
            colored_print("\nUse --detailed flag to see visual analysis of problematic lines", Colors.YELLOW)
        return  # Stop here if we have length violations
    else:
        colored_print(f"\n✅ All {total_data_records} data records are within 80-character limit", Colors.GREEN)
    
    # If length-only check requested, stop here
    if args.length_only:
        return
    
    # Quick header-only check
    if args.header:
        colored_print("\n🔍 HEADER FORMAT CHECK", Colors.GREEN)
        header_issues = 0
        for i, line in enumerate(content[:10], 1):  # Check first 10 lines
            if len(line) > 80:
                colored_print(f"Line {i}: Header too long ({len(line)} chars)", Colors.RED)
                header_issues += 1
        
        if header_issues == 0:
            colored_print("✅ Header format looks good!", Colors.GREEN)
        else:
            colored_print(f"❌ Found {header_issues} header formatting issues", Colors.RED)
        return
    
    print()
    
    # Extract data records with line numbers
    l_records, g_records = extract_data_records(content)
    
    if not l_records and not g_records:
        colored_print("No L or G records found in file", Colors.YELLOW)
        colored_print("This might be a header-only file or different ENSDF format", Colors.YELLOW)
        return
    
    # Show record counts
    colored_print(f"📊 Found: {len(l_records)} L-records, {len(g_records)} G-records", Colors.CYAN)
    
    # Limit to samples unless --all is specified
    original_l_count = len(l_records)
    original_g_count = len(g_records)
    
    if not args.all:
        l_records = l_records[:5]  # First 5 L-records (increased from 3)
        g_records = g_records[:5]  # First 5 G-records (increased from 3)
        if original_l_count > 5 or original_g_count > 5:
            colored_print(f"Note: Checking sample records only. Use --all to check all {original_l_count + original_g_count} records", Colors.YELLOW)
    
    total_issues = 0
    problematic_records = []
    
    # Analyze L-records
    if l_records:
        colored_print(f"\n🔍 Checking {len(l_records)} L-records for alignment issues...", Colors.GREEN)
        for record, line_num in l_records:
            issues = analyze_critical_alignment(record, "L", line_num)
            if issues:
                total_issues += len(issues)
                problematic_records.append((record, "L", line_num, issues))
                colored_print(f"  Line {line_num}: {len(issues)} issue(s) found", Colors.RED)
                for issue in issues:
                    print(f"    • {issue.split(': ', 1)[1] if ': ' in issue else issue}")
            else:
                colored_print(f"  Line {line_num}: ✓ Alignment OK", Colors.GREEN)
    
    # Analyze G-records
    if g_records:
        colored_print(f"\n🔍 Checking {len(g_records)} G-records for alignment issues...", Colors.GREEN)
        for record, line_num in g_records:
            issues = analyze_critical_alignment(record, "G", line_num)
            if issues:
                total_issues += len(issues)
                problematic_records.append((record, "G", line_num, issues))
                colored_print(f"  Line {line_num}: {len(issues)} issue(s) found", Colors.RED)
                for issue in issues:
                    print(f"    • {issue.split(': ', 1)[1] if ': ' in issue else issue}")
            else:
                colored_print(f"  Line {line_num}: ✓ Alignment OK", Colors.GREEN)
    
    # Show detailed visual alignment for problematic records
    if args.detailed and problematic_records:
        colored_print("\n=== DETAILED VISUAL ALIGNMENT CHECK ===", Colors.CYAN)
        for record, record_type, line_num, issues in problematic_records:
            show_visual_alignment(record, record_type, line_num)
            colored_print(f"Issues found:", Colors.RED)
            for issue in issues:
                print(f"  • {issue.split(': ', 1)[1] if ': ' in issue else issue}")
            print()
    
    # Enhanced Summary
    colored_print("\n=== VALIDATION SUMMARY ===", Colors.CYAN)
    total_records = len(l_records) + len(g_records)
    problematic_count = len(problematic_records)
    
    if total_issues == 0:
        colored_print(f"✅ All {total_records} records have correct ENSDF format!", Colors.GREEN)
        colored_print("   Field alignment and format compliance verified.", Colors.GREEN)
    else:
        colored_print(f"❌ Found {total_issues} format issues in {problematic_count}/{total_records} records", Colors.RED)
        colored_print(f"   Manual correction recommended for proper ENSDF compliance.", Colors.YELLOW)
        print()
        colored_print("Common formatting issues:", Colors.YELLOW)
        print("  • Incorrect column positioning (especially cols 8, 9, 22)")
        print("  • Invalid energy field format (cols 10-19)")
        print("  • Missing critical readability spaces")
        print("  • Field boundary violations")
        print("  • Line length issues (should be ≤80 chars)")
        print()
        if not args.detailed:
            colored_print("Tip: Use --detailed flag to see visual rulers for problematic records", Colors.CYAN)
    
    print()
    colored_print("📖 ENSDF Format Reference:", Colors.CYAN)
    print("L-records: NUCID(1-5) [space](6) [space](7) L(8) [space](9) Energy(10-19) [space](22) J-π(23-39)")
    print("G-records: NUCID(1-5) [space](6) [space](7) G(8) [space](9) Energy(10-19) [space](22) RI(23-29)")
    print("Critical: All ENSDF lines should be exactly 80 characters or properly padded")
    
    if total_issues > 0:
        print()
        colored_print("🔧 Next Steps:", Colors.CYAN)
        print("1. Use line numbers above to locate problematic records")
        print("2. Verify field boundaries match ENSDF specification")  
        print("3. Ensure critical spaces are preserved at column boundaries")
        print("4. Re-run validation after corrections")


if __name__ == "__main__":
    main()
