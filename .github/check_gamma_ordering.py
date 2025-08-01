#!/usr/bin/env python3
"""
ENSDF Gamma Record Ordering Checker
===================================

This script ONLY CHECKS for G-record (gamma transition) ordering issues in ENSDF files.
According to ENSDF format requirements, ALL G-records following each L-record 
MUST be arranged in ASCENDING energy order.

This script DOES NOT fix anything - it only reports problems for manual correction.
This is important because G-records can have continuation lines (cG, S G, B G, etc.)
that need to be moved together as groups.

Usage:
    python .github/check_gamma_ordering.py filename.ens [--verbose]
    python .github/check_gamma_ordering.py *.ens [--summary]

Examples:
    python .github/check_gamma_ordering.py S35_34s_d_pg.ens --verbose
    python .github/check_gamma_ordering.py A35/S35/new/*.ens --summary

Author: FRIB Nuclear Data Group
Date: August 2025
"""

import sys
import argparse
from pathlib import Path
from typing import List, Dict, Tuple

class ENSDFGammaChecker:
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

    def extract_level_energy(self, line: str) -> str:
        """Extract level energy from L-record line (columns 10-19)"""
        try:
            energy_field = line[9:19].strip()
            return energy_field.split()[0] if energy_field else "unknown"
        except:
            return "unknown"

    def is_level_record(self, line: str) -> bool:
        """True if line is an L-record (level record) - NOT a comment"""
        if len(line) < 9:
            return False
        # Position 8 = 'L', position 9 = ' ', and not a comment line
        return (line[7] == 'L' and line[8] == ' ' and 
                (len(line) <= 6 or (line[5] == ' ' and line[6] != 'c')))

    def is_gamma_record(self, line: str) -> bool:
        """True if line is a G-record (gamma record) - NOT a comment"""
        if len(line) < 9:
            return False
        # Position 8 = 'G', position 9 = ' ', and not a comment line
        return (line[7] == 'G' and line[8] == ' ' and 
                (len(line) <= 6 or (line[5] == ' ' and line[6] != 'c')))

    def check_file(self, filename: str) -> bool:
        """Check a single ENSDF file for gamma ordering issues"""
        filepath = Path(filename)
        
        if not filepath.exists():
            print(f"❌ Error: File {filename} not found!")
            return False
            
        self.total_files += 1
        self.log(f"\n🔍 Checking: {filename}", force=True)
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except Exception as e:
            print(f"❌ Error reading file: {e}")
            return False

        file_issues = []
        
        i = 0
        while i < len(lines):
            line = lines[i]
            
            if self.is_level_record(line):
                level_energy = self.extract_level_energy(line)
                self.log(f"\n📍 Level L {level_energy} at line {i+1}")
                
                # Find all G-records for this level
                gamma_records = []
                j = i + 1
                
                while j < len(lines) and not self.is_level_record(lines[j]):
                    if self.is_gamma_record(lines[j]):
                        energy = self.extract_gamma_energy(lines[j])
                        gamma_records.append({
                            'line_num': j + 1,
                            'energy': energy,
                            'line_content': lines[j].rstrip()
                        })
                        self.log(f"   G {energy} keV at line {j+1}")
                    j += 1
                
                # Check ordering if multiple gammas exist
                if len(gamma_records) > 1:
                    energies = [g['energy'] for g in gamma_records]
                    sorted_energies = sorted(energies)
                    
                    if energies != sorted_energies:
                        issue = {
                            'level_energy': level_energy,
                            'level_line': i + 1,
                            'current_order': energies,
                            'correct_order': sorted_energies,
                            'gamma_details': gamma_records
                        }
                        file_issues.append(issue)
                        self.total_issues += 1
                        
                        print(f"⚠️  ORDERING ISSUE: Level L {level_energy} (line {i+1})")
                        print(f"   Current gamma order: {energies}")
                        print(f"   Correct order should be: {sorted_energies}")
                        
                        # Show specific line numbers for manual fixing
                        print(f"   📋 Gamma lines to reorder:")
                        for idx, gamma in enumerate(gamma_records):
                            marker = "🔴" if energies[idx] != sorted_energies[idx] else "✅"
                            print(f"      {marker} Line {gamma['line_num']}: G {gamma['energy']} keV")
                        print()
                        
                    else:
                        self.log(f"✅ L {level_energy}: {len(gamma_records)} gammas correctly ordered")
                        
                elif len(gamma_records) == 1:
                    self.log(f"✅ L {level_energy}: 1 gamma (no ordering needed)")
                else:
                    self.log(f"➡️  L {level_energy}: No gamma records")
                        
                i = j
            else:
                i += 1

        # File summary
        if file_issues:
            self.files_with_issues += 1
            print(f"📊 {filename}: Found {len(file_issues)} level groups with ordering issues")
            return False
        else:
            print(f"✅ {filename}: All gamma records are correctly ordered!")
            return True

    def print_summary(self):
        """Print overall summary statistics"""
        print(f"\n{'='*60}")
        print(f"🏁 GAMMA ORDERING CHECK SUMMARY")
        print(f"{'='*60}")
        print(f"📁 Total files checked: {self.total_files}")
        print(f"✅ Files with correct ordering: {self.total_files - self.files_with_issues}")
        print(f"⚠️  Files with ordering issues: {self.files_with_issues}")
        print(f"🔴 Total ordering problems found: {self.total_issues}")
        
        if self.files_with_issues > 0:
            print(f"\n📋 Manual fixes needed for {self.files_with_issues} files")
            print(f"   Use the line numbers shown above to locate and reorder gamma records")
            print(f"   Remember to move continuation lines (cG, S G, B G) with their parent G-records")
        else:
            print(f"\n🎉 All files have correctly ordered gamma records!")

def main():
    parser = argparse.ArgumentParser(
        description="Check G-record ordering in ENSDF files (check-only, no fixes applied)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python check_gamma_ordering.py S35_34s_d_pg.ens --verbose
  python check_gamma_ordering.py A35/S35/new/*.ens --summary
  python check_gamma_ordering.py *.ens
        """
    )
    
    parser.add_argument('files', nargs='+', help='ENSDF file(s) to check')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Show detailed output for each level and gamma')
    parser.add_argument('--summary', '-s', action='store_true',
                       help='Show summary statistics at the end')
    
    args = parser.parse_args()
    
    checker = ENSDFGammaChecker(verbose=args.verbose)
    
    success_count = 0
    for filename in args.files:
        try:
            if checker.check_file(filename):
                success_count += 1
        except Exception as e:
            print(f"❌ Error processing {filename}: {e}")
    
    if args.summary or len(args.files) > 1:
        checker.print_summary()
    
    # Return non-zero exit code if issues found
    return checker.files_with_issues == 0

if __name__ == "__main__":
    sys.exit(0 if main() else 1)
