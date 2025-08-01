#!/usr/bin/env python3
"""
ENSDF Gamma Record Ordering Checker and Fixer
==============================================

This script checks and fixes G-record (gamma transition) ordering in ENSDF files.
According to ENSDF format requirements, ALL G-records following each L-record 
MUST be arranged in ASCENDING energy order.

Usage:
    python fix_gamma_ordering.py filename.ens [--check-only] [--verbose] [--backup]
    
Examples:
    python fix_gamma_ordering.py S35_34s_d_pg.ens --check-only    # Check only, no changes
    python fix_gamma_ordering.py S35_34s_d_pg.ens --backup        # Fix with backup
    python fix_gamma_ordering.py S35_34s_d_pg.ens --verbose       # Show all details
    
Author: ENSDF Evaluation Team
Date: August 2025
"""

import re
import sys
import argparse
from pathlib import Path
from typing import List, Tuple, Dict, Optional

class ENSDFGammaOrderer:
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.issues_found = []
        self.fixes_applied = []
        
    def log(self, message: str, force: bool = False):
        """Print message if verbose mode or force is True"""
        if self.verbose or force:
            print(message)
            
    def extract_gamma_energy(self, gamma_line: str) -> float:
        """Extract gamma energy from G-record line"""
        try:
            # Energy is in columns 10-19, left-justified
            energy_field = gamma_line[9:19].strip()
            
            if not energy_field:
                return 999999.0
            
            # Take first numeric value
            energy_clean = energy_field.split()[0]
            return float(energy_clean)
                
        except (ValueError, IndexError):
            return 999999.0
    
    def is_level_record(self, line: str) -> bool:
        """Check if line is an L-record (level record)"""
        if len(line) < 9:
            return False
        # Exact format: position 8 = 'L', position 9 = ' ', position 6 should be ' ' for main records
        return (line[7] == 'L' and line[8] == ' ' and 
                (len(line) <= 5 or line[5] == ' '))
    
    def is_gamma_record(self, line: str) -> bool:
        """Check if line is a G-record (gamma record)"""
        if len(line) < 9:
            return False
        # Exact format: position 8 = 'G', position 9 = ' ', position 6 should be ' ' for main records
        return (line[7] == 'G' and line[8] == ' ' and 
                (len(line) <= 5 or line[5] == ' '))
    
    def extract_level_energy(self, level_line: str) -> str:
        """Extract level energy from L-record"""
        try:
            energy_field = level_line[9:19].strip()
            if energy_field:
                return energy_field.split()[0]
            return "unknown"
        except:
            return "unknown"
    
    def process_file(self, filename: str, check_only: bool = False, create_backup: bool = False) -> bool:
        """Process an ENSDF file to check/fix gamma ordering"""
        filepath = Path(filename)
        
        if not filepath.exists():
            print(f"Error: File {filename} not found!")
            return False
            
        self.log(f"\n🔍 Processing: {filename}", force=True)
        
        # Read file
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except Exception as e:
            print(f"Error reading file: {e}")
            return False
        
        problems_found = 0
        fixes_made = 0
        new_lines = lines.copy()
        
        i = 0
        while i < len(lines):
            line = lines[i]
            
            # Look for L-records
            if self.is_level_record(line):
                level_energy = self.extract_level_energy(line)
                self.log(f"\n📍 Found level L {level_energy} at line {i+1}")
                
                # Collect consecutive G-records (ignoring comments in between)
                gamma_records = []
                j = i + 1
                
                while j < len(lines):
                    next_line = lines[j]
                    
                    if self.is_gamma_record(next_line):
                        gamma_energy = self.extract_gamma_energy(next_line)
                        gamma_records.append({
                            'line_idx': j,
                            'line': next_line,
                            'energy': gamma_energy
                        })
                        self.log(f"   G {gamma_energy} keV at line {j+1}")
                        
                    elif self.is_level_record(next_line):
                        # Hit next L-record, stop
                        break
                        
                    j += 1
                
                # Check ordering if we have multiple gammas
                if len(gamma_records) > 1:
                    energies = [g['energy'] for g in gamma_records]
                    sorted_energies = sorted(energies)
                    
                    if energies != sorted_energies:
                        problems_found += 1
                        problem_msg = f"L {level_energy}: G-records out of order: {energies} → should be {sorted_energies}"
                        self.log(f"⚠️  {problem_msg}", force=True)
                        self.issues_found.append(problem_msg)
                        
                        if not check_only:
                            # Sort gamma records by energy
                            sorted_gammas = sorted(gamma_records, key=lambda x: x['energy'])
                            
                            # Replace the lines
                            for idx, sorted_gamma in enumerate(sorted_gammas):
                                original_idx = gamma_records[idx]['line_idx']
                                new_lines[original_idx] = sorted_gamma['line']
                            
                            fixes_made += 1
                            fix_msg = f"✓ Fixed L {level_energy}: reordered {len(gamma_records)} gammas"
                            self.log(fix_msg, force=True)
                            self.fixes_applied.append(fix_msg)
                    else:
                        self.log(f"✅ L {level_energy}: {len(gamma_records)} gammas correctly ordered")
                elif len(gamma_records) == 1:
                    self.log(f"✅ L {level_energy}: 1 gamma (no ordering needed)")
                else:
                    self.log(f"➡️  L {level_energy}: No gamma records")
                        
                # Move to the end of this level's gamma records
                i = j
            else:
                i += 1
        
        # Report results
        if problems_found == 0:
            self.log("\\n✅ All gamma records are correctly ordered!", force=True)
        else:
            self.log(f"\\n📊 Summary: Found {problems_found} level groups with ordering issues", force=True)
            
        if check_only:
            self.log("📋 Check-only mode: No changes made.", force=True)
            return True
        
        if fixes_made == 0:
            if problems_found > 0:
                self.log("No fixes were applied.", force=True)
            return True
            
        # Create backup if requested
        if create_backup:
            backup_path = filepath.with_suffix(filepath.suffix + '.backup')
            try:
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.writelines(lines)
                self.log(f"💾 Backup created: {backup_path}", force=True)
            except Exception as e:
                print(f"Error creating backup: {e}")
                return False
        
        # Write fixed file
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
            self.log(f"✅ Applied {fixes_made} fixes to {filename}", force=True)
            return True
            
        except Exception as e:
            print(f"Error writing fixed file: {e}")
            return False

def main():
    parser = argparse.ArgumentParser(
        description="Check and fix G-record ordering in ENSDF files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python fix_gamma_ordering.py S35_34s_d_pg.ens --check-only
  python fix_gamma_ordering.py S35_34s_d_pg.ens --backup --verbose
  python fix_gamma_ordering.py *.ens --check-only
        """
    )
    
    parser.add_argument('files', nargs='+', help='ENSDF file(s) to process')
    parser.add_argument('--check-only', action='store_true', 
                       help='Only check for issues, do not fix')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Show detailed output')
    parser.add_argument('--backup', action='store_true',
                       help='Create backup before fixing')
    
    args = parser.parse_args()
    
    total_files = 0
    success_count = 0
    
    for filename in args.files:
        total_files += 1
        orderer = ENSDFGammaOrderer(verbose=args.verbose)
        
        if orderer.process_file(filename, args.check_only, args.backup):
            success_count += 1
        else:
            print(f"❌ Failed to process: {filename}")
    
    print(f"\\n🏁 Processed {success_count}/{total_files} files successfully")
    
    if success_count < total_files:
        sys.exit(1)

if __name__ == "__main__":
    main()
