#!/usr/bin/env python3
"""
Check for feeding gamma energy references in cL J$ comments.
Pattern: "energy|g from initial_level, spin-parity"

Verifies:
1. Initial level energy = current level + gamma energy
2. Initial level exists with matching energy
3. Spin-parity matches
4. G-record exists with gamma energy at initial level
"""
import re
import sys

def parse_ensdf_file(filepath):
    """Parse ENSDF file and build level structure."""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    levels = {}  # key: line_num, value: {energy, J, G_records: [(energy, line_num)]}
    level_blocks = []
    current_block = {
        'L_line': None, 'L_num': None, 'L_energy': None, 'L_J': None,
        'cL_lines': [], 'G_records': []
    }
    
    for i, line in enumerate(lines, start=1):
        if len(line) < 9:
            continue
        
        nucid = line[0:5]
        cont = line[5] if len(line) > 5 else ' '
        cmt = line[6] if len(line) > 6 else ' '
        rec_type = line[7] if len(line) > 7 else ' '
        
        # Start new level block on L-record
        if rec_type == 'L' and cont == ' ' and cmt == ' ':
            if current_block['L_line'] is not None:
                level_blocks.append(current_block)
                if current_block['L_energy'] is not None:
                    levels[current_block['L_energy']] = {
                        'line_num': current_block['L_num'],
                        'J': current_block['L_J'],
                        'G_records': current_block['G_records']
                    }
            
            # Parse L-record energy
            try:
                energy_field = line[9:19].strip()
                L_energy = float(energy_field) if energy_field else None
            except ValueError:
                L_energy = None
            
            # Parse J-π (columns 23-39)
            J_field = line[22:39].strip() if len(line) > 39 else ''
            
            current_block = {
                'L_line': line, 'L_num': i, 'L_energy': L_energy, 'L_J': J_field,
                'cL_lines': [], 'G_records': []
            }
        
        # Collect cL comment lines
        elif rec_type == 'L' and (cmt.lower() == 'c' or (cont.isdigit() and cmt.lower() == 'c')):
            current_block['cL_lines'].append((i, line))
        
        # Collect G-records
        elif rec_type == 'G' and cont == ' ' and cmt == ' ':
            try:
                G_energy_field = line[9:19].strip()
                G_energy = float(G_energy_field) if G_energy_field else None
                if G_energy:
                    current_block['G_records'].append((G_energy, i))
            except ValueError:
                pass
    
    # Add last block
    if current_block['L_line'] is not None:
        level_blocks.append(current_block)
        if current_block['L_energy'] is not None:
            levels[current_block['L_energy']] = {
                'line_num': current_block['L_num'],
                'J': current_block['L_J'],
                'G_records': current_block['G_records']
            }
    
    return level_blocks, levels

def find_feeding_gamma_refs(level_blocks, levels):
    """Find feeding gamma references in cL J$ comments."""
    mismatches = []
    
    # Pattern: "3827.3|g from 8001.0, (7/2+)"
    # Also: "3827.3|g from 8001.0" without spin-parity
    pattern = r'(\d+\.?\d*)\|g\s+from\s+(\d+\.?\d*)[,\s]*([\(\[\w/\+\-:\)\]]*)'
    
    for block in level_blocks:
        current_level = block['L_energy']
        if current_level is None:
            continue
        
        # Search cL J$ comments
        for cL_num, cL_line in block['cL_lines']:
            if ' cL J$' not in cL_line:
                continue
            
            matches = re.finditer(pattern, cL_line)
            for match in matches:
                gamma_energy_str = match.group(1)
                initial_level_str = match.group(2)
                stated_J = match.group(3).strip() if match.group(3) else None
                
                gamma_energy = float(gamma_energy_str)
                stated_initial = float(initial_level_str)
                
                # Calculate expected initial level
                expected_initial = current_level + gamma_energy
                
                # Check if stated initial level matches calculation
                initial_diff = abs(expected_initial - stated_initial)
                if initial_diff > 0.5:  # Allow 0.5 keV tolerance
                    mismatches.append({
                        'type': 'energy_mismatch',
                        'current_level': current_level,
                        'current_line': block['L_num'],
                        'cL_line': cL_num,
                        'cL_text': cL_line.rstrip(),
                        'gamma_energy': gamma_energy,
                        'stated_initial': stated_initial,
                        'expected_initial': expected_initial,
                        'difference': initial_diff,
                        'stated_J': stated_J
                    })
                    continue
                
                # Find initial level in levels dict (with tolerance)
                found_level = None
                for level_E, level_info in levels.items():
                    if abs(level_E - stated_initial) <= 1.0:  # 1 keV tolerance
                        found_level = level_E
                        break
                
                if found_level is None:
                    mismatches.append({
                        'type': 'level_not_found',
                        'current_level': current_level,
                        'current_line': block['L_num'],
                        'cL_line': cL_num,
                        'cL_text': cL_line.rstrip(),
                        'gamma_energy': gamma_energy,
                        'stated_initial': stated_initial,
                        'stated_J': stated_J
                    })
                    continue
                
                # Check spin-parity if stated
                if stated_J:
                    actual_J = levels[found_level]['J']
                    # Clean up J-π values for comparison
                    stated_J_clean = stated_J.strip('(), ')
                    actual_J_clean = actual_J.strip()
                    
                    if stated_J_clean != actual_J_clean:
                        mismatches.append({
                            'type': 'J_mismatch',
                            'current_level': current_level,
                            'current_line': block['L_num'],
                            'cL_line': cL_num,
                            'cL_text': cL_line.rstrip(),
                            'gamma_energy': gamma_energy,
                            'stated_initial': stated_initial,
                            'stated_J': stated_J_clean,
                            'actual_J': actual_J_clean,
                            'initial_level_line': levels[found_level]['line_num']
                        })
                
                # Check if G-record exists at initial level
                G_records = levels[found_level]['G_records']
                found_G = False
                for G_E, G_line in G_records:
                    if abs(G_E - gamma_energy) <= 0.2:  # 0.2 keV tolerance
                        found_G = True
                        break
                
                if not found_G:
                    mismatches.append({
                        'type': 'G_not_found',
                        'current_level': current_level,
                        'current_line': block['L_num'],
                        'cL_line': cL_num,
                        'cL_text': cL_line.rstrip(),
                        'gamma_energy': gamma_energy,
                        'stated_initial': stated_initial,
                        'initial_level_line': levels[found_level]['line_num'],
                        'available_G': [G_E for G_E, _ in G_records]
                    })
    
    return mismatches

def main():
    if len(sys.argv) < 2:
        print("Usage: python check_feeding_gamma_refs.py <ensdf_file>")
        sys.exit(1)
    
    filepath = sys.argv[1]
    print(f"Analyzing file: {filepath}\n")
    
    level_blocks, levels = parse_ensdf_file(filepath)
    print(f"DEBUG: Found {len(level_blocks)} level blocks")
    print(f"DEBUG: Found {len(levels)} unique level energies\n")
    
    mismatches = find_feeding_gamma_refs(level_blocks, levels)
    
    if not mismatches:
        print("OK: No feeding gamma reference issues found!")
        return
    
    print(f"Found {len(mismatches)} issue(s):\n")
    
    for i, m in enumerate(mismatches, start=1):
        print(f"Issue #{i} - Type: {m['type']}")
        print(f"  Current level: {m['current_level']} keV (L-record line {m['current_line']})")
        print(f"  cL J$ comment: Line {m['cL_line']}")
        print(f"  Comment text: {m['cL_text'][6:]}")  # Skip NUCID+cont
        print(f"  Gamma energy: {m['gamma_energy']} keV")
        print(f"  Stated initial level: {m['stated_initial']} keV")
        
        if m['type'] == 'energy_mismatch':
            print(f"  ERROR: Expected initial = {m['expected_initial']:.1f} keV")
            print(f"  Difference: {m['difference']:.1f} keV")
        elif m['type'] == 'level_not_found':
            print(f"  ERROR: Initial level {m['stated_initial']} keV not found in file")
        elif m['type'] == 'J_mismatch':
            print(f"  ERROR: Stated J-π = '{m['stated_J']}' but actual = '{m['actual_J']}'")
            print(f"  Initial level at line {m['initial_level_line']}")
        elif m['type'] == 'G_not_found':
            print(f"  ERROR: No G-record with {m['gamma_energy']} keV at initial level")
            print(f"  Initial level at line {m['initial_level_line']}")
            print(f"  Available gammas: {m['available_G']}")
        
        print()

if __name__ == '__main__':
    main()
