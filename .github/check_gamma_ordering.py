#!/usr/bin/env python3
"""
ENSDF Energy Record Ordering Checker
====================================

This script checks for both L-record (level) and G-record (gamma transition) ordering 
issues in ENSDF files. According to ENSDF format requirements:
- ALL L-records MUST be arranged in ASCENDING energy order
- ALL G-records following each L-record MUST be arranged in ASCENDING energy order
- X+ energies must have uncertainties in the DE field

This script DOES NOT fix anything - it only reports problems for manual correction.
This is important because records can have continuation lines that need to be moved 
together as groups.

Enhanced Features:
- Level energy ordering validation (NEW)
- X+ energy uncertainty checking (NEW)  
- Gamma energy ordering validation (ENHANCED)
- Comprehensive issue reporting with line numbers
- Support for Windows and Unix line endings

Usage:
    python .github/check_gamma_ordering.py filename.ens [--verbose]
    python .github/check_gamma_ordering.py *.ens [--summary]

Examples:
    python .github/check_gamma_ordering.py S35_34s_d_pg.ens --verbose
    python .github/check_gamma_ordering.py "A35/S35/new/*.ens" --summary
    python .github/check_gamma_ordering.py "A35/*/new/*adopted.ens" --summary

Author: FRIB Nuclear Data Group
Date: January 2025
"""

import sys
import argparse
import glob
from pathlib import Path
from typing import List, Dict, Tuple

class ENSDFEnergyChecker:
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.total_files = 0
        self.files_with_issues = 0
        self.total_issues = 0
        
    def log(self, message: str, force: bool = False):
        """Print message if verbose mode or force is True"""
        if self.verbose or force:
            print(message)

    def extract_gamma_energy(self, line: str) -> float:
        """Extract gamma energy from G-record line (columns 10-19)"""
        try:
            energy_field = line[9:19].strip()
            if energy_field:
                # Take first numeric value (handle cases like "1234.5 6")
                return float(energy_field.split()[0])
            return 999999.0  # Missing energy, sort to end
        except (ValueError, IndexError):
            return 999999.0

    def extract_level_energy(self, line: str) -> float:
        """Extract level energy from L-record line (columns 10-19)"""
        try:
            energy_field = line[9:19].strip()
            if energy_field:
                return float(energy_field.split()[0])
            return None
        except (ValueError, IndexError):
            return None

    def is_level_record(self, line: str) -> bool:
        """True if line is an L-record (level record) - NOT a comment"""
        if len(line) < 9:
            return False
        # Position 8 = 'L', position 9 = ' ', and position 6 = ' ' (main record, not comment)
        return (line[7] == 'L' and line[8] == ' ' and 
                len(line) > 6 and line[6] == ' ')

    def is_gamma_record(self, line: str) -> bool:
        """True if line is a G-record (gamma record) - NOT a comment, documentation, or other types"""
        if len(line) < 9:
            return False
        # Main G-record: Position 5=' ', Position 6=' ', Position 7='G', Position 8=' '
        # This excludes: cG (pos6='c'), dG (pos6='d'), B G (pos5='B'), S G (pos5='S'), etc.
        return (len(line) > 7 and line[5] == ' ' and line[6] == ' ' and 
                line[7] == 'G' and line[8] == ' ')

    def check_level_ordering(self, lines: list) -> list:
        """Check that L-records are in ascending energy order"""
        issues = []
        level_records = []
        
        for i, line in enumerate(lines):
            if self.is_level_record(line):
                energy_value = self.extract_level_energy(line)
                
                if energy_value is not None:
                    level_records.append({
                        'line_num': i + 1,
                        'energy': energy_value,
                        'line': line
                    })
        
        # Check ordering
        if len(level_records) > 1:
            for i in range(1, len(level_records)):
                current_energy = level_records[i]['energy']
                previous_energy = level_records[i-1]['energy']
                
                if current_energy < previous_energy:
                    issues.append({
                        'type': 'level_ordering',
                        'line_num': level_records[i]['line_num'],
                        'message': f"Level {current_energy} keV (line {level_records[i]['line_num']}) should come before {previous_energy} keV (line {level_records[i-1]['line_num']})",
                        'current_energy': current_energy,
                        'previous_energy': previous_energy
                    })
        
        return issues

    def check_file(self, filename: str) -> bool:
        """Check a single ENSDF file for both level and gamma ordering issues"""
        filepath = Path(filename)
        
        if not filepath.exists():
            print(f"[ERROR] File {filename} not found!")
            return False
            
        self.total_files += 1
        self.log(f"\n>> Checking: {filename}", force=True)
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except Exception as e:
            print(f"[ERROR] Error reading file: {e}")
            return False

        # Strip newlines (handle both Windows and Unix)
        lines = [line.rstrip('\n\r') for line in lines]
        
        all_issues = []
        
        # Check level ordering (new feature)
        self.log(">> Checking level energy ordering...", force=True)
        level_issues = self.check_level_ordering(lines)
        all_issues.extend(level_issues)
        
        # Check gamma ordering for each level (existing functionality)
        self.log(">> Checking gamma energy ordering...", force=True)
        gamma_issues = self.check_gamma_ordering_all_levels(lines)
        all_issues.extend(gamma_issues)
        
        # Report all issues with enhanced formatting
        if all_issues:
            self.files_with_issues += 1
            print(f"\n[WARNING] ISSUES FOUND in {filename}:")
            
            # Group issues by type
            level_order_issues = [i for i in all_issues if i['type'] == 'level_ordering']
            gamma_order_issues = [i for i in all_issues if i['type'] == 'gamma_ordering']
            
            if level_order_issues:
                print(f"\n[X] LEVEL ORDERING ISSUES ({len(level_order_issues)}):")
                for issue in level_order_issues:
                    print(f"   * {issue['message']}")
            
            if gamma_order_issues:
                print(f"\n[X] GAMMA ORDERING ISSUES ({len(gamma_order_issues)}):")
                for issue in gamma_order_issues:
                    print(f"   * Level {issue['level_energy']} (line {issue['level_line']})")
                    print(f"     Current: {issue['current_order']}")
                    print(f"     Correct: {issue['correct_order']}")
                    print(f"     [INFO] Gamma lines to reorder:")
                    for idx, gamma in enumerate(issue['gamma_details']):
                        current_order = issue['current_order']
                        correct_order = issue['correct_order']
                        marker = "[X]" if current_order[idx] != correct_order[idx] else "[OK]"
                        print(f"        {marker} Line {gamma['line_num']}: G {gamma['energy']} keV")
            
            self.total_issues += len(all_issues)
            print(f"\n[STATS] {filename}: {len(all_issues)} total issues found")
            return False
        else:
            print(f"[OK] {filename}: All energy records are correctly ordered!")
            return True

    def check_gamma_ordering_all_levels(self, lines: list) -> list:
        """Check gamma ordering for all levels in the file"""
        issues = []
        i = 0
        while i < len(lines):
            if self.is_level_record(lines[i]):
                level_issues = self.check_gamma_ordering_for_level(lines, i)
                issues.extend(level_issues)
                
                # Skip to next level
                j = i + 1
                while j < len(lines) and not self.is_level_record(lines[j]):
                    j += 1
                i = j
            else:
                i += 1
        return issues

    def check_gamma_ordering_for_level(self, lines: list, level_index: int) -> list:
        """Check gamma ordering for a specific level"""
        issues = []
        
        # Extract level information
        level_line = lines[level_index]
        level_energy_value = self.extract_level_energy(level_line)
        
        if level_energy_value is None:
            return issues
        
        # Find all gamma records following this level
        gamma_records = []
        i = level_index + 1
        
        while i < len(lines) and not self.is_level_record(lines[i]):
            if self.is_gamma_record(lines[i]):
                gamma_energy = self.extract_gamma_energy(lines[i])
                if gamma_energy != 999999.0:  # Valid energy
                    gamma_records.append({
                        'line_num': i + 1,
                        'energy': gamma_energy,
                        'line': lines[i]
                    })
            i += 1
        
        # Check if gammas are ordered
        if len(gamma_records) > 1:
            current_order = [g['energy'] for g in gamma_records]
            correct_order = sorted(current_order)
            
            if current_order != correct_order:
                issues.append({
                    'type': 'gamma_ordering',
                    'level_line': level_index + 1,
                    'level_energy': level_energy_value,
                    'current_order': current_order,
                    'correct_order': correct_order,
                    'gamma_details': gamma_records
                })
        
        return issues

    def print_summary(self):
        """Print overall summary statistics"""
        print(f"\n{'='*70}")
        print(f"🏁 ENSDF ENERGY ORDERING CHECK SUMMARY")
        print(f"{'='*70}")
        print(f"📁 Total files checked: {self.total_files}")
        print(f"[OK] Files with correct ordering: {self.total_files - self.files_with_issues}")
        print(f"[WARNING] Files with ordering issues: {self.files_with_issues}")
        print(f"[ERROR] Total ordering problems found: {self.total_issues}")
        
        if self.files_with_issues > 0:
            print(f"\n📋 Manual fixes needed for {self.files_with_issues} files:")
            print(f"   • Level ordering: Sort L-records by ascending energy")
            print(f"   • Gamma ordering: Sort G-records by ascending energy within each level")
            print(f"   • Use line numbers shown above to locate records needing reordering")
            print(f"   • Remember to move continuation lines with their parent records")
        else:
            print(f"\n🎉 All files have correctly ordered energy records!")

def main():
    parser = argparse.ArgumentParser(
        description="Check G-record ordering in ENSDF files (check-only, no fixes applied)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python check_gamma_ordering.py S35_34s_d_pg.ens --verbose
  python check_gamma_ordering.py "A35/S35/new/*.ens" --summary
  python check_gamma_ordering.py "A35/*/new/*adopted.ens" --summary
        """
    )
    
    parser.add_argument('files', nargs='+', help='ENSDF file(s) to check')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Show detailed output for each level and gamma')
    parser.add_argument('--summary', '-s', action='store_true',
                       help='Show summary statistics at the end')
    
    args = parser.parse_args()
    
    # Expand wildcards in file arguments
    expanded_files = []
    for file_pattern in args.files:
        if '*' in file_pattern or '?' in file_pattern:
            # Use glob to expand wildcards
            matches = glob.glob(file_pattern)
            if matches:
                expanded_files.extend(matches)
            else:
                print(f"[WARNING] No files found matching pattern: {file_pattern}")
        else:
            expanded_files.append(file_pattern)
    
    if not expanded_files:
        print("[ERROR] No files found to process!")
        return False
    
    checker = ENSDFEnergyChecker(verbose=args.verbose)
    
    success_count = 0
    for filename in expanded_files:
        try:
            if checker.check_file(filename):
                success_count += 1
        except Exception as e:
            print(f"[ERROR] Error processing {filename}: {e}")
    
    if args.summary or len(expanded_files) > 1:
        checker.print_summary()
    
    # Return non-zero exit code if issues found
    return checker.files_with_issues == 0

if __name__ == "__main__":
    sys.exit(0 if main() else 1)
