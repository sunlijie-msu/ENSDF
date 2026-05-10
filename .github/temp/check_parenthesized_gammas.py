#!/usr/bin/env python3
"""
Find all parenthesized gamma energies in markdown and check ENSDF for ? flag
"""

import re

# Read markdown
with open('XUNDL/2026BAAA_CR11022_209Po_original_Table_I.md', 'r', encoding='utf-8') as f:
    md_lines = f.readlines()

# Read ENSDF
with open('XUNDL/2026BAAA_CR11022_209Po.ens', 'r', encoding='utf-8') as f:
    ens_lines = f.readlines()

print("=" * 100)
print("PARENTHESIZED GAMMA ENERGIES IN MARKDOWN")
print("=" * 100)

# Find all parenthesized gamma energies in markdown
parenthesized_gammas = []

for line_num, line in enumerate(md_lines, 1):
    if not line.startswith('|'):
        continue
    if '---' in line or 'Eγ' in line:
        continue
    
    parts = [p.strip() for p in line.split('|')[1:-1]]
    if len(parts) < 2:
        continue
    
    eg_raw = parts[0]
    
    # Check if energy is in parentheses: (642), (584), etc.
    if eg_raw.startswith('(') and eg_raw.endswith(')'):
        # Extract numeric value
        num_match = re.match(r'\((\d+)\)', eg_raw)
        if num_match:
            eg_val = num_match.group(1)
            jpi_raw = parts[1] if len(parts) > 1 else ''
            ei_raw = parts[2] if len(parts) > 2 else ''
            
            # Extract E_i value
            ei_match = re.match(r'([\d.]+)\((\d+)\)', ei_raw)
            if ei_match:
                ei_val = ei_match.group(1)
                
                # Extract Jpi_i
                jpi_clean = jpi_raw.replace('$', '').strip()
                if ' \\to ' in jpi_clean:
                    jpi_i = jpi_clean.split(' \\to ')[0].strip()
                else:
                    jpi_i = jpi_clean
                
                parenthesized_gammas.append({
                    'Eg': eg_val,
                    'Eg_raw': eg_raw,
                    'E_i': ei_val,
                    'Jpi_i': jpi_i,
                    'md_line': line_num
                })

print(f"\nFound {len(parenthesized_gammas)} parenthesized gamma energies:\n")

for g in parenthesized_gammas:
    print(f"  Eγ={g['Eg_raw']:>8} keV at E_i={g['E_i']:>8} keV, Jπ_i={g['Jpi_i']}")
    print(f"     Markdown line {g['md_line']}")

# Now check ENSDF for these
print("\n" + "=" * 100)
print("CHECKING ENSDF FILE FOR THESE TRANSITIONS")
print("=" * 100)

for g in parenthesized_gammas:
    eg_float = float(g['Eg'])
    ei_float = float(g['E_i'])
    
    print(f"\nSearching ENSDF for Eγ={g['Eg']} keV in level E={g['E_i']} keV:")
    
    # Find the level first
    level_found = False
    level_line_num = None
    
    for line_idx, line in enumerate(ens_lines):
        if len(line) < 20:
            continue
        if '209PO' not in line[0:5]:
            continue
        if line[7] != 'L':
            continue
        
        e_str = line[9:19].strip()
        if e_str:
            try:
                if abs(float(e_str) - ei_float) < 0.1:
                    level_found = True
                    level_line_num = line_idx
                    print(f"  ✓ Level found at ENSDF line {line_idx + 1}: {line.rstrip()[:60]}")
                    break
            except:
                pass
    
    if not level_found:
        print(f"  ✗ Level E={g['E_i']} NOT found in ENSDF")
        continue
    
    # Now find the G-record for this gamma
    gamma_found = False
    for line_idx in range(level_line_num, min(level_line_num + 50, len(ens_lines))):
        line = ens_lines[line_idx]
        
        if len(line) < 20:
            continue
        if '209PO' not in line[0:5]:
            continue
        
        # Check if it's a new L-record (end of current level)
        if line[7] == 'L' and line_idx > level_line_num:
            break
        
        # Check if it's a G-record
        if line[7] == 'G':
            e_str = line[9:19].strip()
            if e_str:
                try:
                    if abs(float(e_str) - eg_float) < 0.1:
                        gamma_found = True
                        q_flag = line[79] if len(line) > 79 else ' '
                        print(f"  ✓ G-record found at ENSDF line {line_idx + 1}")
                        print(f"     {line.rstrip()}")
                        print(f"     Column 80 (Q flag): '{q_flag}'")
                        
                        if q_flag != '?':
                            print(f"     ⚠ NEEDS ? FLAG: Currently '{q_flag}' (should be '?')")
                        else:
                            print(f"     ✓ Already has ? flag")
                        break
                except:
                    pass
    
    if not gamma_found:
        print(f"  ✗ G-record Eγ={g['Eg']} NOT found in level")

print("\n" + "=" * 100)
print("END OF ANALYSIS")
print("=" * 100)
