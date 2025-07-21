#!/usr/bin/env python3
"""
ENSDF Column Calibration Script - GitHub Copilot Alignment Fixer
Focused on L and G record data alignment where Copilot typically fails

Primary Use Cases:
1. Fix GitHub Copilot's column misalignments in ENSDF data records
2. Validate critical field positions after AI-assisted editing
3. Quick visual alignment check with 80-column ruler

Usage: python column_calibrate.py "path/to/file.ens" [--all] [--visual]
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


def analyze_critical_alignment(record: str, record_type: str, line_num: int) -> List[str]:
    """
    Analyze critical alignment issues that GitHub Copilot commonly creates
    Focus on the most error-prone field boundaries
    """
    issues = []
    
    if len(record) < 80:
        issues.append(f"Line {line_num}: Record too short ({len(record)} chars, need 80)")
        return issues
    
    # Critical position checks where Copilot fails most often
    if record_type == "L":
        # Check readability space at position 22 (Copilot often removes this)
        if record[21] != ' ':
            issues.append(f"Line {line_num}: Missing readability space at col 22 (found: '{record[21]}')")
        
        # Check if J-π field starts correctly at position 23
        j_pi_start = 22  # 0-indexed position 22 = column 23
        if len(record) > j_pi_start and record[j_pi_start] != ' ' and record[9:19].strip():
            # Only warn if there's an energy value (real L-record)
            pass  # J-π can start with non-space
        
        # Check S field (columns 65-74) - critical for nuclear data
        s_field = record[64:74] if len(record) >= 74 else ""
        if s_field and not s_field[0].isdigit() and s_field[0] != '-' and s_field[0] != ' ':
            issues.append(f"Line {line_num}: S field (col 65-74) may be misaligned: '{s_field}'")
        
        # Check uncertainty field (columns 75-76) - often displaced by Copilot
        if len(record) >= 76:
            unc_field = record[74:76]
            if unc_field.strip() and not unc_field.strip().isdigit():
                issues.append(f"Line {line_num}: Uncertainty field (col 75-76) suspicious: '{unc_field}'")
    
    elif record_type == "G":
        # Check readability space at position 22
        if record[21] != ' ':
            issues.append(f"Line {line_num}: Missing readability space at col 22 (found: '{record[21]}')")
        
        # Check RI field alignment (columns 23-29) - Copilot often shifts this
        ri_field = record[22:29] if len(record) >= 29 else ""
        if ri_field.strip() and record[9:19].strip():  # Only if there's energy and RI
            # Check if RI starts properly at column 23
            if ri_field[0] != ' ' and not ri_field[0].isdigit() and ri_field[0] != '<':
                issues.append(f"Line {line_num}: RI field (col 23-29) may be misaligned: '{ri_field}'")
        
        # Check DRI field (columns 30-31) - often displaced
        if len(record) >= 31:
            dri_field = record[29:31]
            if dri_field.strip() and not dri_field.strip().isdigit() and dri_field.strip() not in ['GT', 'LT']:
                issues.append(f"Line {line_num}: DRI field (col 30-31) suspicious: '{dri_field}'")
    
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
    """Main function - Focus on fixing GitHub Copilot alignment issues"""
    parser = argparse.ArgumentParser(
        description="ENSDF Column Calibration - Fix GitHub Copilot Alignment Issues",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
GitHub Copilot Alignment Fixer for ENSDF Files:

Examples:
  python column_calibrate.py file.ens                # Quick alignment check
  python column_calibrate.py file.ens --visual       # Show visual rulers for misaligned records
  python column_calibrate.py file.ens --all          # Check all data records (not just samples)

Focus Areas:
  - L-records: Energy, J-π, T, S fields alignment (cols 10-76)
  - G-records: Energy, RI, multipolarity alignment (cols 10-76)
  - Critical readability spaces at column 22
  - Field boundary preservation after AI editing
        """
    )
    parser.add_argument('filepath', help='Path to ENSDF file')
    parser.add_argument('--visual', '-v', action='store_true',
                       help='Show visual alignment rulers for problematic records')
    parser.add_argument('--all', '-a', action='store_true',
                       help='Check all data records instead of just samples')
    
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
    
    # Strip newlines
    content = [line.rstrip('\n\r') for line in content]
    
    # Header
    colored_print("=== ENSDF Column Calibration - GitHub Copilot Fixer ===", Colors.CYAN)
    print(f"File: {args.filepath}")
    print()
    
    # Extract data records with line numbers
    l_records, g_records = extract_data_records(content)
    
    if not l_records and not g_records:
        colored_print("No L or G records found in file", Colors.YELLOW)
        return
    
    # Limit to samples unless --all is specified
    if not args.all:
        l_records = l_records[:3]  # First 3 L-records
        g_records = g_records[:3]  # First 3 G-records
    
    total_issues = 0
    problematic_records = []
    
    # Analyze L-records
    if l_records:
        colored_print(f"Checking {len(l_records)} L-records for alignment issues...", Colors.GREEN)
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
        print()
    
    # Analyze G-records
    if g_records:
        colored_print(f"Checking {len(g_records)} G-records for alignment issues...", Colors.GREEN)
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
        print()
    
    # Show visual alignment for problematic records
    if args.visual and problematic_records:
        colored_print("=== VISUAL ALIGNMENT CHECK ===", Colors.CYAN)
        for record, record_type, line_num, issues in problematic_records:
            show_visual_alignment(record, record_type, line_num)
            colored_print(f"Issues found:", Colors.RED)
            for issue in issues:
                print(f"  • {issue.split(': ', 1)[1] if ': ' in issue else issue}")
            print()
    
    # Summary
    colored_print("=== SUMMARY ===", Colors.CYAN)
    total_records = len(l_records) + len(g_records)
    problematic_count = len(problematic_records)
    
    if total_issues == 0:
        colored_print(f"✅ All {total_records} records have correct alignment!", Colors.GREEN)
        colored_print("   GitHub Copilot didn't mess up the columns this time.", Colors.GREEN)
    else:
        colored_print(f"❌ Found {total_issues} alignment issues in {problematic_count}/{total_records} records", Colors.RED)
        colored_print(f"   GitHub Copilot likely misaligned these fields during editing.", Colors.YELLOW)
        print()
        colored_print("Common Copilot mistakes:", Colors.YELLOW)
        print("  • Removing readability spaces at column 22")
        print("  • Shifting S field values (columns 65-74)")
        print("  • Misaligning uncertainty fields (columns 75-76)")
        print("  • Moving RI values outside columns 23-29")
        print()
        if not args.visual:
            colored_print("Tip: Use --visual flag to see alignment rulers for problematic records", Colors.CYAN)
    
    print()
    colored_print("Quick Reference:", Colors.CYAN)
    print("L-records: Energy(10-19) [space](22) J-π(23-39) T(40-49) L(56-64) S(65-74) DS(75-76)")
    print("G-records: Energy(10-19) [space](22) RI(23-29) DRI(30-31) M(32-41) MR(42-49)")


if __name__ == "__main__":
    main()
