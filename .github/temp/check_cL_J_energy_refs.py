#!/usr/bin/env python3
"""
Check for mismatches between energy references in cL J$ comments and actual G-records.
"""
import re
import sys

def parse_ensdf_file(filepath):
    """Parse ENSDF file and find energy reference mismatches."""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    mismatches = []
    level_blocks = []
    current_block = {'L_line': None, 'L_num': None, 'cL_lines': [], 'G_records': []}
    
    for i, line in enumerate(lines, start=1):
        if len(line) < 9:
            continue
            
        nucid = line[0:5]
        cont = line[5] if len(line) > 5 else ' '  # Column 6
        cmt = line[6] if len(line) > 6 else ' '   # Column 7
        rec_type = line[7] if len(line) > 7 else ' '  # Column 8
        
        # Start new level block on L-record
        if rec_type == 'L' and cont == ' ' and cmt == ' ':
            if current_block['L_line'] is not None:
                level_blocks.append(current_block)
            current_block = {'L_line': line, 'L_num': i, 'cL_lines': [], 'G_records': []}
        
        # Collect cL comment lines (cmt='c' or cont is digit for 2cL, 3cL, etc.)
        elif rec_type == 'L' and (cmt.lower() == 'c' or (cont.isdigit() and cmt.lower() == 'c')):
            current_block['cL_lines'].append((i, line))
        
        # Collect G-records
        elif rec_type == 'G' and cont == ' ' and cmt == ' ':
            current_block['G_records'].append((i, line))
    
    # Add last block
    if current_block['L_line'] is not None:
        level_blocks.append(current_block)
    
    # Now check for energy mismatches in cL J$ comments
    print(f"DEBUG: Found {len(level_blocks)} level blocks")
    cl_j_count = 0
    energy_ref_count = 0
    
    for block in level_blocks:
        # Find cL J$ comments
        for cL_num, cL_line in block['cL_lines']:
            if ' cL J$' in cL_line:
                cl_j_count += 1
                # Look for pattern like "6141.9|g (M1+E2) to 1/2+" or "2180|g E2 to 5/2+"
                # Pattern: number followed by |g with optional space and multipolarity
                pattern = r'(\d+\.?\d*)\|g\s*(?:\(([^)]+)\)|([A-Z][A-Z0-9+]+))?\s+to\s+'
                matches = re.finditer(pattern, cL_line)
                
                for match in matches:
                    energy_str = match.group(1)
                    energy_in_comment = float(energy_str)
                    energy_ref_count += 1
                    print(f"DEBUG: Found energy reference {energy_in_comment} at line {cL_num}")
                    
                    # Search for matching G-record in this level block
                    best_match = None
                    min_diff = 10.0  # Maximum acceptable difference
                    
                    for G_num, G_line in block['G_records']:
                        # Parse G-record energy (columns 10-19)
                        try:
                            G_energy_field = G_line[9:19].strip()
                            if G_energy_field:
                                G_energy = float(G_energy_field)
                                diff = abs(G_energy - energy_in_comment)
                                if diff < min_diff:
                                    min_diff = diff
                                    best_match = (G_num, G_line, G_energy)
                        except ValueError:
                            continue
                    
                    # Report if mismatch found
                    if best_match and min_diff > 0.01:  # Allow 0.01 keV tolerance
                        G_num, G_line, G_energy = best_match
                        mismatches.append({
                            'level_line': block['L_num'],
                            'cL_line': cL_num,
                            'cL_text': cL_line.rstrip(),
                            'comment_energy': energy_in_comment,
                            'G_line': G_num,
                            'G_text': G_line.rstrip(),
                            'G_energy': G_energy,
                            'difference': min_diff
                        })
    
    print(f"DEBUG: Found {cl_j_count} cL J$ lines")
    print(f"DEBUG: Found {energy_ref_count} energy references")
    return mismatches

def main():
    if len(sys.argv) < 2:
        print("Usage: python check_cL_J_energy_refs.py <ensdf_file>")
        sys.exit(1)
    
    filepath = sys.argv[1]
    print(f"Analyzing file: {filepath}")
    mismatches = parse_ensdf_file(filepath)
    print(f"Analysis complete. Found {len(mismatches)} mismatch(es).")
    
    if not mismatches:
        print("OK: No mismatches found! All energy references match corresponding G-records.")
        return
    
    print(f"Found {len(mismatches)} mismatch(es):\n")
    
    for i, m in enumerate(mismatches, start=1):
        print(f"Mismatch #{i}:")
        print(f"  Level L-record: Line {m['level_line']}")
        print(f"  cL J$ comment: Line {m['cL_line']}")
        print(f"    Comment energy: {m['comment_energy']} keV")
        print(f"    Text: {m['cL_text'][6:]}")  # Skip NUCID+cont
        print(f"  G-record: Line {m['G_line']}")
        print(f"    Actual energy: {m['G_energy']} keV")
        print(f"    Text: {m['G_text']}")
        print(f"  Difference: {m['difference']:.2f} keV")
        print()

if __name__ == '__main__':
    main()
