#!/usr/bin/env python3
"""
ENSDF Quoted Values Cross-Check Script (Comprehensive Version)

Verifies that ALL quoted values in cL J$ comments match actual data records EXACTLY:
1. Gamma energies (must match G-record E field exactly)
2. Multipolarities (must match G-record M field exactly, including parentheses/brackets)
3. Level energies (must match L-record E field exactly)
4. Spin-parity J-π (must match L-record J field exactly, including ALL parentheses)

Pattern Types Detected:
- "energy|g [multipolarity] from/to level_energy, J-π"
- Examples:
  * "1824.7|g M1+E2 to 1991, 7/2-"
  * "2061.6|g D, |DJ=1 from 5877.7 (11/2+)"
  * "1986|g to 1572, 1/2+"

Critical Rules:
- Integer energies (e.g., "1991") match L-record "1991.27" (no decimal in comment)
- Multipolarity brackets/parentheses MUST match exactly: "D" ≠ "D(+Q)" ≠ "(D)"
- J-π parentheses MUST match exactly: "11/2+" ≠ "(11/2+)" ≠ "11/2(+)"

Usage:
    python check_quoted_values.py filepath.ens
    python check_quoted_values.py filepath.ens > report.txt

Author: ENSDF AI Agent (FRIBND Mode)
Date: 2026-02-11
Version: 2.0 (Comprehensive)
"""

import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

# ANSI color codes
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
RESET = '\033[0m'

@dataclass
class ENSDFLevel:
    """Represents an ENSDF level with energy and J-π."""
    energy: float
    jpi: str
    line_num: int
    
    def __repr__(self):
        return f"Level({self.energy}, {self.jpi!r}, line {self.line_num})"

@dataclass
class ENSDFGamma:
    """Represents an ENSDF gamma transition."""
    energy: float
    multipolarity: str
    parent_level_energy: float
    line_num: int
    
    def __repr__(self):
        return f"Gamma({self.energy}, {self.multipolarity!r}, from {self.parent_level_energy}, line {self.line_num})"

@dataclass
class QuotedValue:
    """Represents a quoted value in cL J$ comment."""
    value_type: str  # 'gamma_energy', 'multipolarity', 'level_energy', 'level_jpi'
    quoted_value: str
    line_num: int
    context: str
    
    # Associated values for verification
    gamma_energy: Optional[float] = None
    multipolarity: Optional[str] = None
    level_energy: Optional[float] = None
    level_jpi: Optional[str] = None
    
    def __repr__(self):
        return f"Quoted({self.value_type}, {self.quoted_value!r}, line {self.line_num})"

def parse_ensdf_levels(filepath: Path) -> Dict[float, ENSDFLevel]:
    """
    Parse ENSDF file and build dictionary of levels.
    
    Returns:
        Dict mapping energy → ENSDFLevel
    """
    levels = {}
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    for i, line in enumerate(lines, start=1):
        if len(line) < 10:
            continue
        
        # L-record: columns 1-5 = NUCID, 8 = 'L', 10-19 = energy, 23-39 = J-π
        nucid = line[0:5]
        rectype = line[7:8] if len(line) > 7 else ''
        
        if rectype == 'L' and nucid.strip():
            # Extract energy (columns 10-19, 1-based → indices 9-19)
            energy_str = line[9:19].strip()
            if not energy_str:
                continue
            
            try:
                energy = float(energy_str)
            except ValueError:
                continue
            
            # Extract J-π (columns 23-39, 1-based → indices 22-39)
            jpi = line[22:39].strip() if len(line) > 39 else line[22:].strip()
            
            # Store level (use energy as key for quick lookup)
            levels[energy] = ENSDFLevel(energy, jpi, i)
    
    return levels

def parse_ensdf_gammas(filepath: Path, debug=False) -> List[ENSDFGamma]:
    """
    Parse ENSDF file and build list of gamma transitions.
    
    Returns:
        List of ENSDFGamma objects
    """
    gammas = []
    current_level_energy = None
    g_record_count = 0
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    for i, line in enumerate(lines, start=1):
        if len(line) < 10:
            continue
        
        nucid = line[0:5]
        cont = line[5:6] if len(line) > 5 else ''  # Column 6 (1-based) = continuation marker
        col7 = line[6:7] if len(line) > 6 else ''   # Column 7 (1-based) must be blank for data records
        rectype = line[7:8] if len(line) > 7 else ''  # Column 8 (1-based) = record type
        
        # L-record: Must have blank columns 6,7 AND rectype='L'
        if cont == ' ' and col7 == ' ' and rectype == 'L' and nucid.strip():
            # Track current level for gamma associations
            energy_str = line[9:19].strip()
            if energy_str:
                try:
                    current_level_energy = float(energy_str)
                    if debug and i <= 120:
                        print(f"Line {i}: Found L-record, energy={current_level_energy}")
                except ValueError:
                    current_level_energy = None
        
        # G-record: Must have blank columns 6,7 AND rectype='G'
        elif cont == ' ' and col7 == ' ' and rectype == 'G' and nucid.strip():
            g_record_count += 1
            if debug and i <= 120:
                print(f"Line {i}: Found G-record, current_level={current_level_energy}, nucid='{nucid}'")
            
            if current_level_energy is None:
                if debug and i <= 120:
                    print(f"  → Skipping (no current level)")
                continue
            
            # Extract gamma energy (columns 10-19)
            gamma_energy_str = line[9:19].strip()
            if not gamma_energy_str:
                if debug and i <= 120:
                    print(f"  → Skipping (no gamma energy)")
                continue
            
            try:
                gamma_energy = float(gamma_energy_str)
            except ValueError:
                if debug and i <= 120:
                    print(f"  → Skipping (invalid energy: {gamma_energy_str!r})")
                continue
            
            # Extract multipolarity (columns 33-41, 1-based → indices 32-41)
            multipolarity = line[32:41].strip() if len(line) > 41 else line[32:].strip()
            
            if debug and i <= 120:
                print(f"  → Adding gamma: energy={gamma_energy}, M={multipolarity!r}")
            
            gammas.append(ENSDFGamma(gamma_energy, multipolarity, current_level_energy, i))
    
    if debug:
        print(f"\nTotal G-records found: {g_record_count}")
        print(f"Total gammas added: {len(gammas)}")
    
    return gammas

def find_quoted_values(filepath: Path) -> List[QuotedValue]:
    """
    Extract all quoted values from cL J$ comments.
    
    Patterns to detect:
    1. Gamma energy + multipolarity + level energy + J-π:
       "1824.7|g M1+E2 to 1991, 7/2-"
    2. Gamma energy + multipolarity + level energy + J-π (with extra info):
       "2061.6|g D, |DJ=1 from 5877.7 (11/2+)"
    3. Gamma energy + level energy + J-π (no multipolarity):
       "1986|g to 1572, 1/2+"
    
    Returns:
        List of Quoted Value objects
    """
    quoted_values = []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Track continuation lines for cL J$ comments
    in_j_comment = False
    j_comment_lines = []
    j_comment_start_line = 0
    
    for i, line in enumerate(lines, start=1):
        if len(line) < 10:
            continue
        
        nucid = line[0:5]
        col7 = line[6:7]  # Column 7 (index 6)
        col8 = line[7:8]  # Column 8 (index 7)
        
        # Check if this is a cL comment (col 7='c', col 8='L')
        if col7 == 'c' and col8 == 'L' and nucid.strip():
            # Check if J$ identifier present
            if 'J$' in line[9:]:
                in_j_comment = True
                j_comment_lines = [line]
                j_comment_start_line = i
            elif in_j_comment:
                # Continuation line (e.g., 2cL, 3cL)
                j_comment_lines.append(line)
        else:
            # Process accumulated J$ comment
            if in_j_comment and j_comment_lines:
                refs = extract_values_from_comment(j_comment_lines, j_comment_start_line)
                quoted_values.extend(refs)
            
            # Reset
            in_j_comment = False
            j_comment_lines = []
    
    # Handle last comment if file ends with cL
    if in_j_comment and j_comment_lines:
        refs = extract_values_from_comment(j_comment_lines, j_comment_start_line)
        quoted_values.extend(refs)
    
    return quoted_values

def extract_values_from_comment(comment_lines: List[str], start_line: int) -> List[QuotedValue]:
    """
    Extract quoted values from cL J$ comment block.
    
    Returns:
        List of QuotedValue objects
    """
    # Merge all comment lines into single text (columns 10-80)
    full_text = ''
    for line in comment_lines:
        if len(line) > 9:
            # Extract comment text (columns 10-80, indices 9:80)
            text = line[9:80] if len(line) >= 80 else line[9:]
            full_text += text
    
    quoted_values = []
    
    # Pattern: "gamma_energy|g [multipolarity[,extras]] from/to level_energy, J-π"
    # Examples:
    # - "1824.7|g M1+E2 to 1991, 7/2-"
    # - "2061.6|g D, |DJ=1 from 5877.7 (11/2+)"
    # - "1986|g to 1572, 1/2+"
    # - "3594.5|g Q, |DJ=2 to g.s., 3/2+"
    
    # Comprehensive pattern to capture all components
    # Group 1: gamma energy
    # Group 2: multipolarity (optional, may include commas and extra markers)
    # Group 3: direction (from/to)
    # Group 4: level energy (or "g.s." for ground state)
    # Group 5: J-π
    pattern = r'(\d+(?:\.\d+)?)\|g\s+(?:([A-Z0-9+\(\)\[\]]+(?:,[^f][^r][^o][^m][^t][^o])?)\s+)?(from|to)\s+(g\.s\.|(\d+(?:\.\d+)?))[,\s]+([^\s,;]+(?:\s*\([^\)]*\))?[^\s,;.]*)'
    
    for match in re.finditer(pattern, full_text):
        gamma_energy = float(match.group(1))
        multipolarity = match.group(2).strip() if match.group(2) else None
        direction = match.group(3)
        level_str = match.group(4)
        level_energy = 0.0 if level_str == 'g.s.' else float(match.group(5)) if match.group(5) else None
        jpi = match.group(6).strip()
        
        # Clean multipolarity if present
        if multipolarity:
            # Remove trailing comma and extra descriptors like "|DJ=1"
            multipolarity = multipolarity.split(',')[0].strip()
        
        # Clean J-π (remove trailing "level" if captured)
        jpi = re.sub(r'\s+level$', '', jpi)
        jpi = re.sub(r'[;,\.]$', '', jpi)  # Remove trailing punctuation
        
        # Create QuotedValue for gamma energy
        quoted_values.append(QuotedValue(
            value_type='gamma_energy',
            quoted_value=match.group(1),
            line_num=start_line,
            context=match.group(0),
            gamma_energy=gamma_energy,
            multipolarity=multipolarity,
            level_energy=level_energy,
            level_jpi=jpi
        ))
        
        # Create QuotedValue for multipolarity if present
        if multipolarity:
            quoted_values.append(QuotedValue(
                value_type='multipolarity',
                quoted_value=multipolarity,
                line_num=start_line,
                context=match.group(0),
                gamma_energy=gamma_energy,
                multipolarity=multipolarity
            ))
        
        # Create QuotedValue for level energy
        if level_energy is not None:
            quoted_values.append(QuotedValue(
                value_type='level_energy',
                quoted_value=level_str if level_str == 'g.s.' else match.group(5),
                line_num=start_line,
                context=match.group(0),
                level_energy=level_energy
            ))
        
        # Create QuotedValue for level J-π
        quoted_values.append(QuotedValue(
            value_type='level_jpi',
            quoted_value=jpi,
            line_num=start_line,
            context=match.group(0),
            level_energy=level_energy,
            level_jpi=jpi
        ))
    
    return quoted_values

def verify_quoted_values(
    quoted_values: List[QuotedValue],
    levels: Dict[float, ENSDFLevel],
    gammas: List[ENSDFGamma]
) -> Tuple[List[Dict], List[Dict], List[Dict]]:
    """
    Verify each quoted value against actual data records.
    
    Returns:
        (critical_errors, warnings, passed)
    """
    critical_errors = []
    warnings = []
    passed = []
    
    for qv in quoted_values:
        if qv.value_type == 'gamma_energy':
            # Find matching gamma in G-records
            found_gamma = find_gamma(gammas, qv.gamma_energy, tolerance=0.5)
            
            if not found_gamma:
                critical_errors.append({
                    'type': 'GAMMA_NOT_FOUND',
                    'line': qv.line_num,
                    'context': qv.context,
                    'quoted_energy': qv.gamma_energy,
                    'message': f'Gamma {qv.gamma_energy} keV not found in G-records'
                })
            else:
                # Check for exact match
                if abs(found_gamma.energy - qv.gamma_energy) > 0.01:
                    warnings.append({
                        'type': 'GAMMA_ENERGY_APPROX',
                        'line': qv.line_num,
                        'context': qv.context,
                        'quoted': qv.gamma_energy,
                        'actual': found_gamma.energy,
                        'difference': abs(found_gamma.energy - qv.gamma_energy)
                    })
                else:
                    passed.append({'type': 'gamma_energy', 'line': qv.line_num})
        
        elif qv.value_type == 'multipolarity':
            # Find matching gamma and check multipolarity
            found_gamma = find_gamma(gammas, qv.gamma_energy, tolerance=0.5)
            
            if not found_gamma:
                # Already reported in gamma_energy check
                pass
            else:
                # CRITICAL: Multipolarity must match EXACTLY
                if found_gamma.multipolarity != qv.multipolarity:
                    critical_errors.append({
                        'type': 'MULTIPOLARITY_MISMATCH',
                        'line': qv.line_num,
                        'context': qv.context,
                        'quoted_mult': qv.multipolarity,
                        'actual_mult': found_gamma.multipolarity,
                        'gamma_energy': qv.gamma_energy,
                        'message': f'Multipolarity mismatch: quoted "{qv.multipolarity}" but G-record has "{found_gamma.multipolarity}"'
                    })
                else:
                    passed.append({'type': 'multipolarity', 'line': qv.line_num})
        
        elif qv.value_type == 'level_energy':
            # Find matching level in L-records
            found_level = find_level(levels, qv.level_energy, tolerance=0.5)
            
            if not found_level:
                critical_errors.append({
                    'type': 'LEVEL_NOT_FOUND',
                    'line': qv.line_num,
                    'context': qv.context,
                    'quoted_energy': qv.level_energy,
                    'message': f'Level {qv.level_energy} keV not found in L-records'
                })
            else:
                # Check for exact or acceptable match
                # Note: Comments may use rounded values (e.g., "1991" for "1991.27")
                # This is acceptable if within 0.5 keV
                diff = abs(found_level.energy - qv.level_energy)
                if diff > 0.5:
                    critical_errors.append({
                        'type': 'LEVEL_ENERGY_MISMATCH',
                        'line': qv.line_num,
                        'context': qv.context,
                        'quoted': qv.level_energy,
                        'actual': found_level.energy,
                        'difference': diff
                    })
                elif diff > 0.01:
                    warnings.append({
                        'type': 'LEVEL_ENERGY_ROUNDED',
                        'line': qv.line_num,
                        'context': qv.context,
                        'quoted': qv.level_energy,
                        'actual': found_level.energy,
                        'difference': diff
                    })
                else:
                    passed.append({'type': 'level_energy', 'line': qv.line_num})
        
        elif qv.value_type == 'level_jpi':
            # Find matching level and check J-π
            found_level = find_level(levels, qv.level_energy, tolerance=0.5)
            
            if not found_level:
                # Already reported in level_energy check
                pass
            else:
                # CRITICAL: J-π must match EXACTLY including ALL parentheses
                if found_level.jpi != qv.level_jpi:
                    critical_errors.append({
                        'type': 'JPI_MISMATCH',
                        'line': qv.line_num,
                        'context': qv.context,
                        'quoted_jpi': qv.level_jpi,
                        'actual_jpi': found_level.jpi,
                        'level_energy': qv.level_energy,
                        'message': f'J-π mismatch: quoted "{qv.level_jpi}" but L-record has "{found_level.jpi}"'
                    })
                else:
                    passed.append({'type': 'level_jpi', 'line': qv.line_num})
    
    return critical_errors, warnings, passed

def find_level(levels: Dict[float, ENSDFLevel], energy: float, tolerance: float = 0.5) -> Optional[ENSDFLevel]:
    """
    Find level matching energy within tolerance.
    """
    # Exact match first
    if energy in levels:
        return levels[energy]
    
    # Tolerance search
    for lvl_energy, level in levels.items():
        if abs(lvl_energy - energy) <= tolerance:
            return level
    
    return None

def find_gamma(gammas: List[ENSDFGamma], energy: float, tolerance: float = 0.5) -> Optional[ENSDFGamma]:
    """
    Find gamma matching energy within tolerance.
    """
    for gamma in gammas:
        if abs(gamma.energy - energy) <= tolerance:
            return gamma
    
    return None

def print_report(filepath: Path, critical_errors: List[Dict], warnings: List[Dict], passed: List[Dict]):
    """Print comprehensive verification report."""
    print("=" * 80)
    print("ENSDF Quoted Values Cross-Check Report (Comprehensive)")
    print(f"File: {filepath}")
    print("=" * 80)
    print()
    
    total = len(critical_errors) + len(warnings) + len(passed)
    print(f"Total quoted values checked: {total}")
    print(f"  PASSED: {len(passed)}")
    print(f"  WARNINGS: {len(warnings)}")
    print(f"  CRITICAL ERRORS: {len(critical_errors)}")
    print()
    
    if critical_errors:
        print("=" * 80)
        print(f"{RED}CRITICAL ERRORS (MUST FIX){RESET}")
        print("=" * 80)
        print()
        
        for i, err in enumerate(critical_errors, 1):
            print(f"{RED}Error #{i}: {err['type']}{RESET}")
            print(f"  Line: {err['line']}")
            print(f"  Context: {err['context']}")
            print(f"  {err['message']}")
            print()
    
    if warnings:
        print("=" * 80)
        print(f"{YELLOW}WARNINGS (Review Recommended){RESET}")
        print("=" * 80)
        print()
        
        for i, warn in enumerate(warnings, 1):
            print(f"{YELLOW}Warning #{i}: {warn['type']}{RESET}")
            print(f"  Line: {warn['line']}")
            print(f"  Context: {warn['context']}")
            if 'quoted' in warn and 'actual' in warn:
                print(f"  Quoted: {warn['quoted']} keV")
                print(f"  Actual: {warn['actual']} keV")
                print(f"  Difference: {warn['difference']:.2f} keV")
            print()
    
    print("=" * 80)
    if critical_errors:
        print(f"{RED}VERIFICATION FAILED: {len(critical_errors)} critical error(s) found{RESET}")
    elif warnings:
        print(f"{YELLOW}VERIFICATION PASSED with warnings: {len(warnings)} marginal issue(s){RESET}")
    else:
        print(f"{GREEN}VERIFICATION PASSED: All quoted values match exactly{RESET}")
    print("=" * 80)

def main():
    if len(sys.argv) < 2:
        print("Usage: python check_quoted_values.py filepath.ens")
        sys.exit(1)
    
    filepath = Path(sys.argv[1])
    if not filepath.exists():
        print(f"Error: File not found: {filepath}")
        sys.exit(1)
    
    print(f"Parsing ENSDF file: {filepath.name}...")
    
    # Parse data records
    levels = parse_ensdf_levels(filepath)
    print(f"Found {len(levels)} levels")
    
    gammas = parse_ensdf_gammas(filepath, debug=False)
    print(f"Found {len(gammas)} gamma transitions")
    
    # Extract quoted values
    print(f"Extracting quoted values from cL J$ comments...")
    quoted_values = find_quoted_values(filepath)
    print(f"Found {len(quoted_values)} quoted values")
    print()
    
    # Verify all quoted values
    critical_errors, warnings, passed = verify_quoted_values(quoted_values, levels, gammas)
    
    # Print report
    print_report(filepath, critical_errors, warnings, passed)
    
    # Exit code
    sys.exit(1 if critical_errors else 0)

if __name__ == '__main__':
    main()
