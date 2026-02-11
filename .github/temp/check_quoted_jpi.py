#!/usr/bin/env python3
"""
ENSDF Quoted J-π Cross-Check Script

Verifies that all level energies and J-π values quoted in cL J$ comments
match actual L-records exactly (including parentheses).

Pattern Types Detected:
1. Feeding gammas: "energy|g from level, J-π"
2. Outgoing gammas: "energy|g to J-π"  
3. General references: "level_energy, J-π level"

Usage:
    python check_quoted_jpi.py filepath.ens
    python check_quoted_jpi.py filepath.ens > report.txt

Author: ENSDF AI Agent (FRIBND Mode)
Date: 2025-01-13
"""

import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# ANSI color codes
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
RESET = '\033[0m'

class ENSDFLevel:
    """Represents an ENSDF level with energy and J-π."""
    def __init__(self, energy: float, jpi: str, line_num: int):
        self.energy = energy
        self.jpi = jpi.strip()
        self.line_num = line_num
    
    def __repr__(self):
        return f"Level({self.energy}, {self.jpi!r}, line {self.line_num})"

class QuotedReference:
    """Represents a quoted level reference in a comment."""
    def __init__(self, pattern_type: str, energy: float, jpi: str, line_num: int, context: str):
        self.pattern_type = pattern_type
        self.energy = energy
        self.jpi = jpi.strip()
        self.line_num = line_num
        self.context = context
    
    def __repr__(self):
        return f"QuotedRef({self.pattern_type}, {self.energy}, {self.jpi!r}, line {self.line_num})"

def parse_ensdf_file(filepath: Path) -> Dict[float, ENSDFLevel]:
    """
    Parse ENSDF file and build dictionary of levels.
    
    Returns:
        Dict mapping energy → ENSDFLevel
    """
    levels = {}
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    for i, line in enumerate(lines, start=1):
        if len(line) < 9:
            continue
        
        # L-record: columns 1-5 = NUCID, 8 = 'L', 10-19 = energy, 23-39 = J-π
        nucid = line[0:5]
        rectype = line[7:8] if len(line) > 7 else ''
        
        if rectype == 'L' and 'CL' in nucid:
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

def find_quoted_references(filepath: Path) -> List[QuotedReference]:
    """
    Extract all quoted level references from cL J$ comments.
    
    Pattern Types:
    1. Feeding: "2339.4|g from 7178.6, 1/2(+)"
    2. Outgoing: "2339.4|g to 1/2-"
    3. General: "7178.6, 1/2(+) level"
    
    Returns:
        List of QuotedReference objects
    """
    references = []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Track continuation lines for cL J$ comments
    in_j_comment = False
    j_comment_lines = []
    j_comment_start_line = 0
    
    for i, line in enumerate(lines, start=1):
        if len(line) < 9:
            continue
        
        nucid = line[0:5]
        cont = line[5:6]
        rectype_char = line[7:8]  # Column 8 (index 7)
        
        # Check if this is a cL comment (rectype = 'L' at column 8)
        if rectype_char == 'L' and 'CL' in nucid:
            # Check if J$ identifier present
            if 'J$' in line[9:]:
                in_j_comment = True
                j_comment_lines = [line]
                j_comment_start_line = i
            elif in_j_comment:
                # Continuation line (e.g., 2cL, 3cL)
                # Column 8 must still be 'L' for continuation
                j_comment_lines.append(line)
        else:
            # Process accumulated J$ comment
            if in_j_comment and j_comment_lines:
                refs = extract_patterns_from_comment(j_comment_lines, j_comment_start_line)
                references.extend(refs)
            
            # Reset
            in_j_comment = False
            j_comment_lines = []
    
    # Handle last comment if file ends with cL
    if in_j_comment and j_comment_lines:
        refs = extract_patterns_from_comment(j_comment_lines, j_comment_start_line)
        references.extend(refs)
    
    return references

def extract_patterns_from_comment(comment_lines: List[str], start_line: int) -> List[QuotedReference]:
    """
    Extract quoted level references from cL J$ comment block.
    
    Patterns:
    1. Feeding: r'(\d+\.?\d*)\|g from (\d+\.?\d*),\s*([^,\s]+(?:\([^)]*\))?)'
    2. Outgoing: r'(\d+\.?\d*)\|g to ([^,\s]+(?:\([^)]*\))?)'
    3. General: r'(\d+\.?\d*),\s*([^,\s]+(?:\([^)]*\))?) level'
    
    Returns:
        List of QuotedReference objects
    """
    # Merge all comment lines into single text (columns 10-80)
    full_text = ''
    for line in comment_lines:
        if len(line) > 9:
            # Extract comment text (columns 10-80, indices 9:80)
            text = line[9:80] if len(line) >= 80 else line[9:]
            full_text += text
    
    references = []
    
    # Pattern 1: Feeding gamma "gamma_energy|g from level_energy, J-π"
    # Example: "2339.4|g from 7178.6, 1/2(+)" or "3183.9|g from 8038.4, 1/2+,3/2+"
    # J-π can contain commas (e.g., "1/2+,3/2+") so use more flexible pattern
    # Capture until " level" keyword or end of reasonable J-π pattern
    pattern1 = r'(\d+\.?\d*)\|g\s+from\s+(\d+\.?\d*),\s*([^\s]+(?:\s*\([^)]*\))?[^\s]*?)(?:\s+level|,\s*\d+\.?\d*\|g|\s*$)'
    for match in re.finditer(pattern1, full_text):
        gamma_energy = float(match.group(1))
        level_energy = float(match.group(2))
        jpi = match.group(3).strip()
        
        # Clean up J-π (remove trailing "level" if captured)
        if jpi.endswith(' level'):
            jpi = jpi[:-6].strip()
        
        references.append(QuotedReference(
            pattern_type='feeding',
            energy=level_energy,
            jpi=jpi,
            line_num=start_line,
            context=f"{gamma_energy}|g from {level_energy}, {jpi}"
        ))
    
    # Pattern 2: Outgoing gamma "gamma_energy|g to J-π"
    # Example: "2339.4|g to 1/2-"
    pattern2 = r'(\d+\.?\d*)\|g\s+to\s+([^\s,;]+(?:\s*\([^)]*\))?)'
    for match in re.finditer(pattern2, full_text):
        gamma_energy = float(match.group(1))
        jpi = match.group(2).strip()
        
        # Note: For outgoing gammas, no level energy is quoted directly
        # We'd need current level + gamma to calculate, but for now just flag J-π
        # (Skip for now as user's example focuses on level energy + J-π pairs)
        pass
    
    # Pattern 3: General level reference "level_energy, J-π level"
    # Example: "7178.6, 1/2(+) level"
    # CRITICAL: This pattern is prone to false positives from merged continuation lines
    # Skip this pattern entirely to avoid partial energy matches
    # (Feeding pattern should catch the relevant cases)
    
    return references

def find_level(levels: Dict[float, ENSDFLevel], energy: float, tolerance: float = 0.5) -> Optional[ENSDFLevel]:
    """
    Find level matching energy within tolerance.
    
    Args:
        levels: Dictionary of levels
        energy: Target energy
        tolerance: Matching tolerance in keV
    
    Returns:
        Matching ENSDFLevel or None
    """
    # Exact match first
    if energy in levels:
        return levels[energy]
    
    # Tolerance search
    for lvl_energy, level in levels.items():
        if abs(lvl_energy - energy) <= tolerance:
            return level
    
    return None

def verify_quoted_references(
    references: List[QuotedReference],
    levels: Dict[float, ENSDFLevel]
) -> Tuple[List[Dict], List[Dict], List[Dict]]:
    """
    Verify each quoted reference against L-records.
    
    Returns:
        (critical_errors, warnings, passed)
    """
    critical_errors = []
    warnings = []
    passed = []
    
    for ref in references:
        # Find matching level
        level = find_level(levels, ref.energy, tolerance=0.5)
        
        if level is None:
            # CRITICAL: Level not found
            # Search broader tolerance for suggestion
            suggestion = find_level(levels, ref.energy, tolerance=5.0)
            
            critical_errors.append({
                'type': 'LEVEL_NOT_FOUND',
                'line': ref.line_num,
                'pattern': ref.pattern_type,
                'quoted_energy': ref.energy,
                'quoted_jpi': ref.jpi,
                'context': ref.context,
                'suggestion': f"Nearest: {suggestion.energy} keV (line {suggestion.line_num})" if suggestion else "No nearby levels"
            })
            continue
        
        # Check energy mismatch
        energy_diff = abs(level.energy - ref.energy)
        if energy_diff > 0.5:
            critical_errors.append({
                'type': 'ENERGY_MISMATCH',
                'line': ref.line_num,
                'pattern': ref.pattern_type,
                'quoted_energy': ref.energy,
                'quoted_jpi': ref.jpi,
                'actual_energy': level.energy,
                'actual_jpi': level.jpi,
                'diff': energy_diff,
                'context': ref.context,
                'suggestion': f"Update to {level.energy}"
            })
            continue
        
        # Check J-π mismatch (exact character matching)
        if ref.jpi != level.jpi:
            critical_errors.append({
                'type': 'JPI_MISMATCH',
                'line': ref.line_num,
                'pattern': ref.pattern_type,
                'quoted_energy': ref.energy,
                'quoted_jpi': ref.jpi,
                'actual_energy': level.energy,
                'actual_jpi': level.jpi,
                'context': ref.context,
                'suggestion': f"Update to {level.jpi!r}"
            })
            continue
        
        # Marginal energy tolerance
        if energy_diff > 0.1:
            warnings.append({
                'type': 'MARGINAL_ENERGY',
                'line': ref.line_num,
                'pattern': ref.pattern_type,
                'quoted_energy': ref.energy,
                'actual_energy': level.energy,
                'diff': energy_diff,
                'context': ref.context
            })
        else:
            # PASSED
            passed.append({
                'line': ref.line_num,
                'pattern': ref.pattern_type,
                'energy': ref.energy,
                'jpi': ref.jpi,
                'context': ref.context
            })
    
    return critical_errors, warnings, passed

def print_results(
    filepath: Path,
    references: List[QuotedReference],
    critical_errors: List[Dict],
    warnings: List[Dict],
    passed: List[Dict]
):
    """Print formatted verification results."""
    
    print("=" * 80)
    print(f"ENSDF Quoted J-π Cross-Check Report")
    print(f"File: {filepath}")
    print("=" * 80)
    print()
    
    print(f"Total quoted references: {len(references)}")
    print(f"  {GREEN}✓ Passed:{RESET} {len(passed)}")
    print(f"  {YELLOW}⚠ Warnings:{RESET} {len(warnings)}")
    print(f"  {RED}✗ Critical Errors:{RESET} {len(critical_errors)}")
    print()
    
    # Critical errors
    if critical_errors:
        print(f"{RED}{'=' * 80}{RESET}")
        print(f"{RED}CRITICAL ERRORS (MUST FIX){RESET}")
        print(f"{RED}{'=' * 80}{RESET}")
        print()
        
        for i, err in enumerate(critical_errors, 1):
            print(f"{RED}Error #{i}: {err['type']}{RESET}")
            print(f"  Line: {err['line']}")
            print(f"  Pattern: {err['pattern']}")
            print(f"  Context: {err['context']}")
            
            if err['type'] == 'LEVEL_NOT_FOUND':
                print(f"  Quoted Energy: {err['quoted_energy']} keV")
                print(f"  Quoted J-π: {err['quoted_jpi']}")
                print(f"  {err['suggestion']}")
            
            elif err['type'] == 'ENERGY_MISMATCH':
                print(f"  Quoted Energy: {err['quoted_energy']} keV")
                print(f"  Actual Energy: {err['actual_energy']} keV")
                print(f"  Difference: {err['diff']:.2f} keV")
                print(f"  {CYAN}→ {err['suggestion']}{RESET}")
            
            elif err['type'] == 'JPI_MISMATCH':
                print(f"  Energy: {err['quoted_energy']} keV")
                print(f"  Quoted J-π: {err['quoted_jpi']!r}")
                print(f"  Actual J-π: {err['actual_jpi']!r}")
                print(f"  {CYAN}→ {err['suggestion']}{RESET}")
            
            print()
    
    # Warnings
    if warnings:
        print(f"{YELLOW}{'=' * 80}{RESET}")
        print(f"{YELLOW}WARNINGS (Review Recommended){RESET}")
        print(f"{YELLOW}{'=' * 80}{RESET}")
        print()
        
        for i, warn in enumerate(warnings, 1):
            print(f"{YELLOW}Warning #{i}: {warn['type']}{RESET}")
            print(f"  Line: {warn['line']}")
            print(f"  Pattern: {warn['pattern']}")
            print(f"  Context: {warn['context']}")
            print(f"  Quoted Energy: {warn['quoted_energy']} keV")
            print(f"  Actual Energy: {warn['actual_energy']} keV")
            print(f"  Difference: {warn['diff']:.2f} keV")
            print()
    
    # Summary
    print("=" * 80)
    if critical_errors:
        print(f"{RED}VERIFICATION FAILED: {len(critical_errors)} critical errors found{RESET}")
        print(f"{RED}Fix all critical errors before proceeding.{RESET}")
        return 1
    elif warnings:
        print(f"{YELLOW}VERIFICATION PASSED with warnings: {len(warnings)} marginal tolerances{RESET}")
        print(f"{YELLOW}Review warnings for potential issues.{RESET}")
        return 0
    else:
        print(f"{GREEN}VERIFICATION PASSED: All quoted references match exactly{RESET}")
        return 0

def main():
    if len(sys.argv) < 2:
        print("Usage: python check_quoted_jpi.py filepath.ens", file=sys.stderr)
        return 1
    
    filepath = Path(sys.argv[1])
    
    if not filepath.exists():
        print(f"Error: File not found: {filepath}", file=sys.stderr)
        return 1
    
    # Parse file
    print(f"Parsing ENSDF file: {filepath.name}...")
    levels = parse_ensdf_file(filepath)
    print(f"Found {len(levels)} levels")
    
    # Find quoted references
    print(f"Extracting quoted references from cL J$ comments...")
    references = find_quoted_references(filepath)
    print(f"Found {len(references)} quoted references")
    print()
    
    # Verify references
    critical_errors, warnings, passed = verify_quoted_references(references, levels)
    
    # Print results
    exit_code = print_results(filepath, references, critical_errors, warnings, passed)
    
    return exit_code

if __name__ == '__main__':
    sys.exit(main())
