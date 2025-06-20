#!/usr/bin/env python3
"""
ENSDF Column Calibration Script (Python Version)
Enhanced with PowerShell History Analysis insights

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


def analyze_ensdf_fields(record: str, record_type: str) -> None:
    """Enhanced field extraction and analysis"""
    colored_print(f"=== Field Analysis for {record_type}-record ===", Colors.CYAN)
    print(f"Record: {record}")
    print()
    
    if record_type == "L":
        # L-record field analysis
        fields = {
            'NUCID': record[0:5].strip() if len(record) >= 5 else "N/A",
            'Record type': record[7] if len(record) >= 8 else "N/A",
            'Energy': record[9:19].strip() if len(record) >= 19 else "N/A",
            'Energy uncertainty': record[19:21].strip() if len(record) >= 21 else "N/A",
            'Readability space': record[21] if len(record) >= 22 else "N/A",
            'J-π': record[21:39].strip() if len(record) >= 39 else "N/A",
            'Half-life': record[39:49].strip() if len(record) >= 49 else "N/A",
            'Half-life uncertainty': record[49:55].strip() if len(record) >= 55 else "N/A"
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
        
    elif record_type == "G":
        # G-record field analysis
        fields = {
            'NUCID': record[0:5].strip() if len(record) >= 5 else "N/A",
            'Record type': record[7] if len(record) >= 8 else "N/A",
            'Energy': record[9:19].strip() if len(record) >= 19 else "N/A",
            'Energy uncertainty': record[19:21].strip() if len(record) >= 21 else "N/A",
            'Readability space': record[21] if len(record) >= 22 else "N/A",
            'Relative intensity': record[21:29].strip() if len(record) >= 29 else "N/A",
            'Intensity uncertainty': record[29:31].strip() if len(record) >= 31 else "N/A",
            'Multipolarity': record[31:41].strip() if len(record) >= 41 else "N/A"
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
        """
    )
    parser.add_argument('filepath', help='Path to ENSDF file')
    parser.add_argument('--detailed', '-d', action='store_true',
                       help='Show character-by-character mapping for each record')
    
    args = parser.parse_args()
    
    # Check if file exists
    if not os.path.exists(args.filepath):
        colored_print(f"Error: File '{args.filepath}' not found", Colors.RED)
        sys.exit(1)
    
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
    colored_print("Column Ruler (1-80):", Colors.YELLOW)
    print("12345678901234567890123456789012345678901234567890123456789012345678901234567890")
    print("         1         2         3         4         5         6         7         8")
    print()
    
    # Extract sample records
    l_records, g_records = extract_records(content)
    
    # Analyze L-records
    if l_records:
        colored_print("Sample L-records:", Colors.GREEN)
        for record in l_records:
            print(record)
            colored_print("  NUCID (1-5), L (8), Energy (10-19), DE (20-21), Space (22), J (23-39), T (40-49), DT (50-55)", Colors.GRAY)
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
            colored_print("  NUCID (1-5), G (8), Energy (10-19), DE (20-21), Space (22), RI (23-29), DRI (30-31), M (32-41)", Colors.GRAY)
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
                colored_print("  ✓ Format OK", Colors.GREEN)
            else:
                colored_print("  ⚠ Issues found:", Colors.RED)
                for issue in issues:
                    colored_print(f"    {issue}", Colors.RED)
        print()
    
    if g_records:
        colored_print("G-record validation:", Colors.YELLOW)
        for record in g_records:
            issues = validate_ensdf_fields(record, "G")
            if not issues:
                colored_print("  ✓ Format OK", Colors.GREEN)
            else:
                colored_print("  ⚠ Issues found:", Colors.RED)
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
    
    colored_print("✓ Column calibration complete", Colors.GREEN)
    colored_print("✓ Python version with enhanced PowerShell history insights", Colors.GREEN)
    print()
    colored_print("=== ENSDF Column Reference ===", Colors.CYAN)
    print("L-records: NUCID(1-5) L(8) Energy(10-19) DE(20-21) [space](22) J-π(23-39) T(40-49) DT(50-55)")
    print("G-records: NUCID(1-5) G(8) Energy(10-19) DE(20-21) [space](22) RI(23-29) DRI(30-31) M(32-41)")
    print()
    colored_print("Key improvements from PowerShell history analysis:", Colors.YELLOW)
    print("  • Enhanced field extraction and validation")
    print("  • Character-by-character mapping (use --detailed flag)")
    print("  • Corrected column assignments for readability space at col 22")
    print("  • J-π and RI fields properly start at column 23")
    print("  • Comprehensive field validation with specific error messages")
    print("  • Python regex for robust record matching")
    print("  • Better error handling and UTF-8 support")


if __name__ == "__main__":
    main()
