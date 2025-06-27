#!/usr/bin/env python3
"""
ENSDF Column Calibration Script (Python Version)
Enhanced with PowerShell History Analysis insights
Complete L and G record field extraction

Usage: python column_calibrate.py "path/to/file.ens" [--detailed]
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


def show_character_mapping(record: str, record_type: str) -> None:
    """Show character-by-character mapping for detailed analysis"""
    colored_print(f"Character-by-character mapping for {record_type}-record:", Colors.YELLOW)
    
    for i, char in enumerate(record[:80]):  # ENSDF records are 80 characters
        pos = i + 1
        display_char = 'SP' if char == ' ' else repr(char).strip("'")
        print(f"{pos:2}: '{display_char}'")
    print()


def quick_header_analysis(filepath: str) -> None:
    """Quick header analysis with visual ruler - perfect for debugging alignment issues"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            header = f.readline().rstrip()
    except Exception as e:
        colored_print(f"Error reading file: {e}", Colors.RED)
        return
    
    colored_print("=== QUICK HEADER ANALYSIS (80-Column Debug) ===", Colors.CYAN)
    print()
    colored_print("ENSDF 80-Column Ruler:", Colors.YELLOW)
    colored_print("Ones:  12345678901234567890123456789012345678901234567890123456789012345678901234567890", Colors.WHITE)
    colored_print("Tens:  1111111111222222222233333333334444444444555555555566666666667777777777888888888999", Colors.CYAN)
    colored_print("Header:", Colors.GREEN)
    print(f"       {header}")
    print()
    print(f"Length: {len(header)} chars (should be 80)")
    print()
    colored_print("ENSDF Header Field Analysis:", Colors.YELLOW)
    print(f"Cols 1-5 (NUCID):  '{header[0:5] if len(header) >= 5 else 'N/A'}'")
    print(f"Cols 6-9 (blank):  '{header[5:9] if len(header) >= 9 else 'N/A'}'")
    print(f"Cols 10-39 (DSID): '{header[9:39] if len(header) >= 39 else 'N/A'}'")
    print(f"Cols 40-65 (DSREF):'{header[39:65] if len(header) >= 65 else 'N/A'}'")
    print(f"Cols 66-74 (PUB):  '{header[65:74] if len(header) >= 74 else 'N/A'}'")
    print(f"Cols 75-80 (DATE): '{header[74:80] if len(header) >= 80 else 'N/A'}'")
    print()
    
    # Validation
    issues = []
    if len(header) != 80:
        issues.append(f"Length is {len(header)}, should be exactly 80")
    if len(header) >= 9 and header[5:9] != "    ":
        issues.append("Cols 6-9 should be blank spaces")
    
    if issues:
        colored_print("❌ ISSUES FOUND:", Colors.RED)
        for issue in issues:
            colored_print(f"   • {issue}", Colors.RED)
    else:
        colored_print("✅ Header format looks good!", Colors.GREEN)
    print()


def analyze_ensdf_fields(record: str, record_type: str) -> None:
    """Enhanced field extraction and analysis"""
    colored_print(f"=== Field Analysis for {record_type}-record ===", Colors.CYAN)
    print(f"Record: {record}")
    print()
    
    if record_type == "L":
        # L-record field analysis - Complete ENSDF format
        fields = {
            'NUCID': record[0:5].strip() if len(record) >= 5 else "N/A",
            'Record type': record[7] if len(record) >= 8 else "N/A",
            'Energy': record[9:19].strip() if len(record) >= 19 else "N/A",
            'Energy uncertainty': record[19:21].strip() if len(record) >= 21 else "N/A",
            'Readability space': record[21] if len(record) >= 22 else "N/A",
            'J-π': record[21:39].strip() if len(record) >= 39 else "N/A",
            'Half-life': record[39:49].strip() if len(record) >= 49 else "N/A",
            'Half-life uncertainty': record[49:55].strip() if len(record) >= 55 else "N/A",
            'L (Angular momentum)': record[55:64].strip() if len(record) >= 64 else "N/A",
            'S (Spectroscopic strength)': record[64:74].strip() if len(record) >= 74 else "N/A",
            'DS (Uncertainty in S)': record[74:76].strip() if len(record) >= 76 else "N/A"
        }
        
        colored_print("Field Analysis:", Colors.GREEN)
        print(f"  NUCID (cols 1-5): '{fields['NUCID']}'")
        print(f"  Record type (col 8): '{fields['Record type']}'")
        print(f"  Energy (cols 10-19): '{fields['Energy']}'")
        print(f"  Energy uncertainty (cols 20-21): '{fields['Energy uncertainty']}'")
        print(f"  Readability space (col 22): '{fields['Readability space']}'")
        print(f"  J-π (cols 22-39): '{fields['J-π']}'")
        print(f"  Half-life (cols 40-49): '{fields['Half-life']}'")
        print(f"  Half-life uncertainty (cols 50-55): '{fields['Half-life uncertainty']}'")
        print(f"  L (Angular momentum) (cols 56-64): '{fields['L (Angular momentum)']}'")
        print(f"  S (Spectroscopic strength) (cols 65-74): '{fields['S (Spectroscopic strength)']}'")
        print(f"  DS (Uncertainty in S) (cols 75-76): '{fields['DS (Uncertainty in S)']}'")
        
    elif record_type == "G":
        # G-record field analysis - Complete ENSDF format
        fields = {
            'NUCID': record[0:5].strip() if len(record) >= 5 else "N/A",
            'Record type': record[7] if len(record) >= 8 else "N/A",
            'Energy': record[9:19].strip() if len(record) >= 19 else "N/A",
            'Energy uncertainty': record[19:21].strip() if len(record) >= 21 else "N/A",
            'Readability space': record[21] if len(record) >= 22 else "N/A",
            'Relative intensity': record[21:29].strip() if len(record) >= 29 else "N/A",
            'Intensity uncertainty': record[29:31].strip() if len(record) >= 31 else "N/A",
            'Multipolarity': record[31:41].strip() if len(record) >= 41 else "N/A",
            'Mixing ratio': record[41:49].strip() if len(record) >= 49 else "N/A",
            'Mixing ratio uncertainty': record[49:55].strip() if len(record) >= 55 else "N/A",
            'Conversion coefficient': record[55:62].strip() if len(record) >= 62 else "N/A",
            'CC uncertainty': record[62:64].strip() if len(record) >= 64 else "N/A",
            'Total conversion coefficient': record[64:72].strip() if len(record) >= 72 else "N/A",
            'TCC uncertainty': record[72:76].strip() if len(record) >= 76 else "N/A",
            'Continuation': record[76:77].strip() if len(record) >= 77 else "N/A",
            'Coincidence flag': record[77:78].strip() if len(record) >= 78 else "N/A",
            'Question flag': record[78:79].strip() if len(record) >= 79 else "N/A",
            'Footnote flag': record[79:80].strip() if len(record) >= 80 else "N/A"
        }
        
        colored_print("Field Analysis:", Colors.GREEN)
        print(f"  NUCID (cols 1-5): '{fields['NUCID']}'")
        print(f"  Record type (col 8): '{fields['Record type']}'")
        print(f"  Energy (cols 10-19): '{fields['Energy']}'")
        print(f"  Energy uncertainty (cols 20-21): '{fields['Energy uncertainty']}'")
        print(f"  Readability space (col 22): '{fields['Readability space']}'")
        print(f"  Relative intensity (cols 22-29): '{fields['Relative intensity']}'")
        print(f"  Intensity uncertainty (cols 30-31): '{fields['Intensity uncertainty']}'")
        print(f"  Multipolarity (cols 32-41): '{fields['Multipolarity']}'")
        print(f"  Mixing ratio (cols 42-49): '{fields['Mixing ratio']}'")
        print(f"  Mixing ratio uncertainty (cols 50-55): '{fields['Mixing ratio uncertainty']}'")
        print(f"  Conversion coefficient (cols 56-62): '{fields['Conversion coefficient']}'")
        print(f"  CC uncertainty (cols 63-64): '{fields['CC uncertainty']}'")
        print(f"  Total conversion coefficient (cols 65-72): '{fields['Total conversion coefficient']}'")
        print(f"  TCC uncertainty (cols 73-76): '{fields['TCC uncertainty']}'")
        print(f"  Continuation (col 77): '{fields['Continuation']}'")
        print(f"  Coincidence flag (col 78): '{fields['Coincidence flag']}'")
        print(f"  Question flag (col 79): '{fields['Question flag']}'")
        print(f"  Footnote flag (col 80): '{fields['Footnote flag']}'")
    
    print()


def validate_ensdf_fields(record: str, record_type: str) -> List[str]:
    """Enhanced field validation function"""
    issues = []
    
    # Basic length check
    if len(record) < 80:
        issues.append(f"Record too short: {len(record)} chars (should be 80)")
    
    # Check NUCID field (columns 1-5)
    if len(record) >= 5:
        nucid = record[0:5]
        if not nucid.strip():
            issues.append("NUCID field (cols 1-5) is empty")
    
    # Check record type position (column 8)
    if len(record) >= 8:
        if record_type == "L" and record[7] != 'L':
            issues.append(f"Record type not 'L' at position 8 (found: '{record[7]}')")
        elif record_type == "G" and record[7] != 'G':
            issues.append(f"Record type not 'G' at position 8 (found: '{record[7]}')")
    
    # Check energy field (columns 10-19) - should not be all spaces
    if len(record) >= 19:
        energy_field = record[9:19]
        if not energy_field.strip():
            issues.append("Energy field (cols 10-19) is empty")
    
    # Check readability space at column 22 (critical for human reading)
    if len(record) >= 22 and record[21] != ' ':
        issues.append(f"Column 22 should be space for readability (found: '{record[21]}')")
    
    # Record type specific validations
    if record_type == "L":
        # For L-records, J-π field starts at column 23 (after readability space)
        if len(record) >= 39:
            j_pi_field = record[22:39]  # starts at 23 (index 22)
            if not j_pi_field.strip():
                issues.append("J-π field (cols 23-39) appears empty")
    elif record_type == "G":
        # For G-records, relative intensity starts at column 23 (after readability space)
        if len(record) >= 29:
            intensity_field = record[22:29]  # starts at 23 (index 22)
            if not intensity_field.strip():
                issues.append("Relative intensity field (cols 23-29) appears empty")
    
    return issues


def extract_records(content: List[str]) -> Tuple[List[str], List[str]]:
    """Extract L and G records from ENSDF content"""
    l_records = []
    g_records = []
    
    for line in content:
        # Match L records: whitespace + NUCID + whitespace + L + whitespace
        if re.match(r'^\s*\w+\s+L\s', line):
            l_records.append(line.rstrip())
        # Match G records: whitespace + NUCID + whitespace + G + whitespace
        elif re.match(r'^\s*\w+\s+G\s', line):
            g_records.append(line.rstrip())
    
    return l_records[:2], g_records[:2]  # Take first 2 of each type


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
    """Main function"""
    parser = argparse.ArgumentParser(
        description="ENSDF Column Calibration Script (Python Version)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python column_calibrate.py file.ens
  python column_calibrate.py file.ens --detailed
  python column_calibrate.py file.ens --header    # Quick header analysis with 80-column ruler
        """
    )
    parser.add_argument('filepath', help='Path to ENSDF file')
    parser.add_argument('--detailed', '-d', action='store_true',
                       help='Show character-by-character mapping for each record')
    parser.add_argument('--header', action='store_true',
                       help='Quick header analysis with 80-column ruler (perfect for debugging alignment)')
    
    args = parser.parse_args()
    
    # Check if file exists
    if not os.path.exists(args.filepath):
        colored_print(f"Error: File '{args.filepath}' not found", Colors.RED)
        sys.exit(1)
    
    # Quick header analysis mode
    if args.header:
        quick_header_analysis(args.filepath)
        return
    
    # Read file content
    try:
        with open(args.filepath, 'r', encoding='utf-8') as f:
            content = f.readlines()
    except Exception as e:
        colored_print(f"Error reading file: {e}", Colors.RED)
        sys.exit(1)
    
    # Strip newlines but preserve the content
    content = [line.rstrip('\n\r') for line in content]
    
    # Header
    colored_print("=== ENSDF Column Calibration (Python Enhanced) ===", Colors.CYAN)
    print()
    colored_print("ENSDF 80-Column Ruler (CRITICAL for alignment debugging):", Colors.YELLOW)
    colored_print("Ones:  12345678901234567890123456789012345678901234567890123456789012345678901234567890", Colors.WHITE)
    colored_print("Tens:  1111111111222222222233333333334444444444555555555566666666667777777777888888888999", Colors.CYAN)
    colored_print("       1         2         3         4         5         6         7         8", Colors.GRAY)
    print()
    
    # Extract sample records
    l_records, g_records = extract_records(content)
    
    # Analyze L-records
    if l_records:
        colored_print("Sample L-records:", Colors.GREEN)
        for record in l_records:
            print(record)
            colored_print("  NUCID (1-5), L (8), Energy (10-19), DE (20-21), Space (22), J (23-39), T (40-49), DT (50-55), L (56-64), S (65-74), DS (75-76)", Colors.GRAY)
            print()
            
            # Show detailed field analysis
            analyze_ensdf_fields(record, "L")
            
            # Optional character-by-character mapping
            if args.detailed:
                show_character_mapping(record, "L")
    
    # Analyze G-records
    if g_records:
        colored_print("Sample G-records:", Colors.GREEN)
        for record in g_records:
            print(record)
            colored_print("  NUCID (1-5), G (8), Energy (10-19), DE (20-21), Space (22), RI (23-29), DRI (30-31), M (32-41), MR (42-49), DMR (50-55), CC (56-62), DCC (63-64), TCC (65-72), DTCC (73-76), C (77), [+] (78), [?] (79), [*] (80)", Colors.GRAY)
            print()
            
            # Show detailed field analysis
            analyze_ensdf_fields(record, "G")
            
            # Optional character-by-character mapping
            if args.detailed:
                show_character_mapping(record, "G")
    
    # Validate sample records
    if l_records:
        colored_print("L-record validation:", Colors.YELLOW)
        for record in l_records:
            issues = validate_ensdf_fields(record, "L")
            if not issues:
                colored_print("  [OK] Format OK", Colors.GREEN)
            else:
                colored_print("  [!] Issues found:", Colors.RED)
                for issue in issues:
                    colored_print(f"    {issue}", Colors.RED)
        print()
    
    if g_records:
        colored_print("G-record validation:", Colors.YELLOW)
        for record in g_records:
            issues = validate_ensdf_fields(record, "G")
            if not issues:
                colored_print("  [OK] Format OK", Colors.GREEN)
            else:
                colored_print("  [!] Issues found:", Colors.RED)
                for issue in issues:
                    colored_print(f"    {issue}", Colors.RED)
        print()
    
    # Summary statistics
    stats = count_records(content)
    colored_print("File Statistics:", Colors.CYAN)
    print(f"  Total lines: {stats['total']}")
    print(f"  L-records (levels): {stats['L_records']}")
    print(f"  G-records (gammas): {stats['G_records']}")
    print(f"  Comment lines: {stats['comments']}")
    print()
    
    colored_print("[OK] Column calibration complete", Colors.GREEN)
    colored_print("[OK] Python version with enhanced PowerShell history insights", Colors.GREEN)
    print()
    
    colored_print("=== ENSDF Column Reference ===", Colors.CYAN)
    print("L-records: NUCID(1-5) L(8) Energy(10-19) DE(20-21) [space](22) J-π(23-39) T(40-49) DT(50-55) L(56-64) S(65-74) DS(75-76)")
    print("G-records: NUCID(1-5) G(8) Energy(10-19) DE(20-21) [space](22) RI(23-29) DRI(30-31) M(32-41) MR(42-49) DMR(50-55) CC(56-62) DCC(63-64) TCC(65-72) DTCC(73-76) C(77) [+](78) [?](79) [*](80)")
    print()
    colored_print("Key improvements from PowerShell history analysis:", Colors.YELLOW)
    print("  - Enhanced field extraction and validation")
    print("  - Character-by-character mapping (use --detailed flag)")
    print("  - Corrected column assignments for readability space at col 22")
    print("  - J-π and RI fields properly start at column 23")
    print("  - Complete L-record field extraction including L, S, and DS fields")
    print("  - Complete G-record field extraction including all fields to column 80")
    print("  - Comprehensive field validation with specific error messages")
    print("  - Python regex for robust record matching")
    print("  - Better error handling and UTF-8 support")


if __name__ == "__main__":
    main()
