#!/usr/bin/env python3
"""
Verify gamma energy citations in cL J$ comments against actual G-record values.
Identifies mismatches between quoted energies in comments and G-record energies.
"""

import re
import sys
from pathlib import Path

def extract_gamma_energies_from_comment(comment_text):
    """Extract all gamma energies from a comment line with |g notation."""
    # Pattern: number with decimal point followed by |g
    # Examples: 2339.4|g, 1184.6|g, 4886.4|g
    pattern = r'(\d+\.\d+)\|g'
    matches = re.findall(pattern, comment_text)
    return [float(energy) for energy in matches]

def find_g_record_energy(file_lines, approx_energy, tolerance=5.0):
    """
    Find G-record with energy close to the quoted value.
    Returns (line_number, exact_energy, line_text) or (None, None, None).
    """
    # Pattern: " 35CL  G EEEE.E" with various column alignments
    # Energy field is in columns 10-19 (1-indexed), so Python index 9-19
    g_record_pattern = r'^\s*35CL\s+G\s+(\d+\.?\d*)'
    
    for line_num, line in enumerate(file_lines, start=1):
        match = re.match(g_record_pattern, line)
        if match:
            g_energy = float(match.group(1))
            # Check if this energy is close to what we're looking for
            if abs(g_energy - approx_energy) < tolerance:
                return line_num, g_energy, line.rstrip()
    
    return None, None, None

def main():
    if len(sys.argv) < 2:
        print("Usage: python verify_cL_J_gamma_citations.py <path_to_Cl35_adopted.ens>")
        sys.exit(1)
    
    file_path = Path(sys.argv[1])
    if not file_path.exists():
        print(f"Error: File not found: {file_path}")
        sys.exit(1)
    
    # Read entire file
    with open(file_path, 'r', encoding='utf-8') as f:
        file_lines = f.readlines()
    
    # Pattern for cL J$ comments (can span multiple continuation lines)
    cl_j_pattern = r'^\s*35CL\s*\dcL\s+J\$.*\|g'
    cl_j_simple = r'^\s*35CL\s+cL\s+J\$.*\|g'
    
    mismatches = []
    matches = []
    not_found = []
    
    print("=" * 80)
    print("Gamma Energy Citation Verification Report")
    print("=" * 80)
    print()
    
    # Scan for cL J$ comments
    for line_num, line in enumerate(file_lines, start=1):
        if re.match(cl_j_simple, line) or re.match(cl_j_pattern, line):
            # Extract gamma energies from comment
            energies = extract_gamma_energies_from_comment(line)
            
            if energies:
                print(f"Line {line_num}: {line.rstrip()}")
                
                # Check each quoted energy
                for quoted_energy in energies:
                    g_line_num, g_energy, g_line = find_g_record_energy(file_lines, quoted_energy)
                    
                    if g_line_num is None:
                        not_found.append({
                            'comment_line': line_num,
                            'quoted_energy': quoted_energy,
                            'comment_text': line.rstrip()
                        })
                        print(f"  [!]  {quoted_energy}|g -> NOT FOUND in G-records")
                    elif abs(g_energy - quoted_energy) > 0.01:  # Allow 0.01 keV rounding tolerance
                        mismatches.append({
                            'comment_line': line_num,
                            'quoted_energy': quoted_energy,
                            'actual_energy': g_energy,
                            'g_line_num': g_line_num,
                            'comment_text': line.rstrip(),
                            'g_record_text': g_line
                        })
                        print(f"  [X] {quoted_energy}|g -> MISMATCH! G-record shows {g_energy} (line {g_line_num})")
                    else:
                        matches.append({
                            'comment_line': line_num,
                            'energy': quoted_energy,
                            'g_line_num': g_line_num
                        })
                        print(f"  [OK] {quoted_energy}|g -> G-record matches {g_energy} (line {g_line_num})")
                print()
    
    # Summary Report
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total matches: {len(matches)}")
    print(f"Total mismatches: {len(mismatches)}")
    print(f"Total not found (primary gammas from other datasets): {len(not_found)}")
    print()
    
    if mismatches:
        print("=" * 80)
        print("MISMATCHES REQUIRING CORRECTION")
        print("=" * 80)
        for i, mm in enumerate(mismatches, start=1):
            print(f"{i}. Line {mm['comment_line']}: {mm['quoted_energy']}|g → should be {mm['actual_energy']}|g")
            print(f"   Comment: {mm['comment_text']}")
            print(f"   G-record (line {mm['g_line_num']}): {mm['g_record_text']}")
            print()
    
    # Exit code: 0 if all OK, 1 if mismatches found
    sys.exit(1 if mismatches else 0)

if __name__ == '__main__':
    main()
