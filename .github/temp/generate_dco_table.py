#!/usr/bin/env python3
"""
Complete DCO and POL analysis for all 209Po gamma transitions.
Generates updated markdown table with two new columns.
"""

import re
from typing import Optional, Tuple, List

def extract_j_value(jpi_str: str) -> Optional[float]:
    """Extract J value from J-pi string"""
    jpi_clean = jpi_str.strip().replace('$', '').replace('(', '').replace(')', '').replace(' ', '')
    match = re.match(r'(\d+)/(\d+)', jpi_clean)
    if match:
        num, denom = int(match.group(1)), int(match.group(2))
        return num / denom
    return None

def calc_delta_j(jpi_i: str, jpi_f: str) -> Optional[float]:
    """Calculate spin change |J_i - J_f|"""
    ji = extract_j_value(jpi_i)
    jf = extract_j_value(jpi_f)
    if ji is not None and jf is not None:
        return abs(ji - jf)
    return None

def extract_rdco_and_gate(rdco_str: str) -> Tuple[Optional[float], Optional[str]]:
    """Extract R_DCO value and gate type"""
    if '–' in rdco_str or not rdco_str.strip():
        return None, None
    match = re.search(r'([\d.]+)', rdco_str)
    if match:
        value = float(match.group(1))
        gate = 'd' if '[d]' in rdco_str else ('q' if '[q]' in rdco_str else None)
        return value, gate
    return None, None

def extract_pol(pol_str: str) -> Optional[float]:
    """Extract POL value"""
    if '–' in pol_str or not pol_str.strip():
        return None
    match = re.search(r'(-?[\d.]+)', pol_str)
    if match:
        return float(match.group(1))
    return None

def classify_dco(rdco_val: Optional[float], gate: Optional[str], dj: Optional[float], 
                 ji: Optional[float], jf: Optional[float]) -> str:
    """
    Classify as D, Q, ΔJ=0, or Mixed based on DCO decision rules.
    
    From 2026BaAA comment:
    - R_DCO(Q)≈1.0 for stretched quadrupole (ΔJ=2) or unstretched dipole (ΔJ=0)
    - R_DCO(Q)≈0.76 for stretched dipole (ΔJ=1)
    - R_DCO(D)≈1.0 for stretched dipole (ΔJ=1)
    - R_DCO(D)≈1.33 for stretched quadrupole (ΔJ=2) or unstretched dipole (ΔJ=0)
    """
    if rdco_val is None:
        return "–"
    
    # Special case: J_i = J_f means ΔJ = 0
    if ji is not None and jf is not None and abs(ji - jf) < 0.01:
        return "ΔJ=0"
    
    if gate == 'q':  # Gate on stretched quadrupole
        # R_DCO(Q)≈1.0 → Q or ΔJ=0; R_DCO(Q)≈0.76 → D
        if 0.90 <= rdco_val <= 1.10:  # ~1.0
            return "Q"  # Could be Q or ΔJ=0; check ΔJ to refine
        elif 0.68 <= rdco_val <= 0.84:  # ~0.76
            return "D"
        else:
            return "Mixed"
    elif gate == 'd':  # Gate on stretched dipole
        # R_DCO(D)≈1.0 → D; R_DCO(D)≈1.33 → Q or ΔJ=0
        if 0.90 <= rdco_val <= 1.10:  # ~1.0
            return "D"
        elif 1.20 <= rdco_val <= 1.50:  # ~1.33
            return "Q"  # Could be Q or ΔJ=0; check ΔJ to refine
        else:
            return "Mixed"
    
    return "Mixed"

def assign_multipolarity(dco_class: str, pol_val: Optional[float], dj: Optional[float]) -> str:
    """Assign multipolarity based on DCO and POL"""
    if dco_class == "–":
        return "–"
    
    if pol_val is None:
        # No POL - assign D, Q, or D+Q/Q+O based on ΔJ
        if dco_class == "D":
            return "D"
        elif dco_class == "Q":
            return "Q"
        elif dco_class == "ΔJ=0":
            return "D"
        elif dco_class == "Mixed":
            if dj is None:
                return "D+Q"
            elif dj < 1.5:
                return "D+Q"
            else:
                return "Q+O"
        return dco_class
    
    is_electric = pol_val > 0
    
    if dco_class == "D":
        return "E1" if is_electric else "M1"
    elif dco_class == "Q":
        return "E2" if is_electric else "M2"
    elif dco_class == "ΔJ=0":
        return "E1" if is_electric else "M1"
    elif dco_class == "Mixed":
        if dj is None or dj < 1.5:
            return "E1+M2" if is_electric else "M1+E2"
        else:
            return "E2+M3" if is_electric else "M2+E3"
    
    return "–"

def parse_and_analyze_table(markdown_content: str) -> str:
    """Parse table and generate updated version with DCO and POL columns"""
    lines = markdown_content.split('\n')
    
    # Find table start
    table_start = None
    for i, line in enumerate(lines):
        if '| $E_{\\gamma}$' in line:
            table_start = i
            break
    
    if table_start is None:
        return markdown_content
    
    # Header row + separator
    header_line = lines[table_start]
    separator_line = lines[table_start + 1]
    
    # Update headers to add two new columns
    new_header = header_line.replace('| Multipolarity |', '| Multipolarity | DCO Classification | Assigned Multipolarity |')
    # Update separator: change 7 columns to 9 columns
    new_separator = '| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |'
    
    # Process data rows
    updated_lines = lines[:table_start] + [new_header, new_separator]
    
    for i in range(table_start + 2, len(lines)):
        line = lines[i].strip()
        if not line or not line.startswith('|'):
            updated_lines.append(lines[i])
            continue
        
        # Parse row - split by | and filter empty strings
        parts = [p.strip() for p in line.split('|')]
        parts = [p for p in parts if p]  # Remove empty parts
        
        if len(parts) < 7:
            updated_lines.append(lines[i])
            continue
        
        eg = parts[0]
        jpis = parts[1]
        ei = parts[2]
        igamma = parts[3]
        rdco_str = parts[4]
        pol_str = parts[5]
        mult_orig = parts[6]  # Original author multipolarity
        
        # Extract J values
        if '\\to' in jpis:
            ji_str, jf_str = jpis.split('\\to')
        else:
            ji_str = jf_str = jpis
        
        ji = extract_j_value(ji_str)
        jf = extract_j_value(jf_str)
        dj = calc_delta_j(ji_str, jf_str)
        rdco_val, gate = extract_rdco_and_gate(rdco_str)
        pol_val = extract_pol(pol_str)
        
        # Classify and assign
        dco_class = classify_dco(rdco_val, gate, dj, ji, jf)
        mult_assigned = assign_multipolarity(dco_class, pol_val, dj)
        
        # Rebuild row with new columns AFTER original multipolarity
        new_row = f"| {eg} | {jpis} | {ei} | {igamma} | {rdco_str} | {pol_str} | {mult_orig} | {dco_class} | {mult_assigned} |"
        updated_lines.append(new_row)
    
    return '\n'.join(updated_lines)

# Read the markdown file
with open(r'd:\X\ND\ENSDF\XUNDL\2026BAAA_CR11022_209Po_original_Table_I.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Process
updated_content = parse_and_analyze_table(content)

# Write back
with open(r'd:\X\ND\ENSDF\.github\temp\updated_table.md', 'w', encoding='utf-8') as f:
    f.write(updated_content)

print("Updated table written to .github/temp/updated_table.md")
print("\nSample rows (first 10 data rows):")
for i, line in enumerate(updated_content.split('\n')[3:13]):  # Skip header + separator, show first 10 data rows
    if line.startswith('|'):
        print(line)
