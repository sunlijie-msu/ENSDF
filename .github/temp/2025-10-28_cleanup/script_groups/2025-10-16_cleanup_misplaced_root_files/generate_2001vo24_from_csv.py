#!/usr/bin/env python3
"""
Generate NEW 2001VO24.ens from CSV source with CORRECT ENSDF formatting.

CSV Structure: Rows=Exf values, Columns=Exi values, Cells=RI
L-records (energy levels): 0, 1219, 1763, 1763, 2646, 2694, 3003, 3163, 3918, 3943, 3968, 4059, 4113, 4173, 4178, 4624, 4770, 4839, 4881, 5216, 5586, 5599, 5646, 5654, 5724, 6181
Exi values from CSV: 5645, 7179, 7547, 7838, 8207, 8216, 8381, 8484, 8893, 8907, 9081

G-Record Format (EXACT columns):
Cols 1-5:   NUCID (" 35Cl")
Cols 6-9:   " G " with continuation
Cols 10-19: Egamma energy (LEFT-JUSTIFIED)
Cols 20-21: DE (energy uncertainty - BLANK for RI data)
Col 22:     Space
Cols 23-29: RI value (LEFT-JUSTIFIED)
Cols 30-80: Rest (blank for minimal data)
"""

import csv

def parse_csv():
    """Parse CSV and extract all transitions"""
    with open("A35/Cl35/raw/2001VO24.csv", "r") as f:
        reader = csv.reader(f)
        lines = list(reader)
    
    # CSV Structure:
    # Line 0: ,Ep,,832,1212,1510,... (header with Ep)
    # Line 1: Empty
    # Line 2: ,Exi,5645,7179,7547,7838,8207,8216,8381,8484,8893,8907,9081,  (Exi values)
    # Line 3+: Exf,0,,38,,21,78,... (Exf rows with RI values)
    
    exi_row = lines[2]  # ["", "Exi", "5645", "7179", "7547", ...]
    exi_values = [float(x) for x in exi_row[2:] if x]  # Skip empty and "Exi"
    
    transitions = []  # List of (Exi, Exf, RI, Egamma)
    
    for row_idx in range(3, len(lines)):  # Start from data rows
        row = lines[row_idx]
        if not row or len(row) < 3:  # Need at least ["Exf", value, ...]
            continue
        
        # Extract Exf value - it's in column [1], column [0] is the "Exf" label
        exf_str = row[1].strip()
        if not exf_str:
            continue
        
        try:
            exf = float(exf_str)
        except:
            continue
        
        # Parse RI values across Exi columns (columns 2+ contain RI values for each Exi)
        for exi_idx, exi in enumerate(exi_values):
            col_idx = exi_idx + 2  # Column index in CSV (column 0=label, column 1=Exf, columns 2+=RI values)
            if col_idx < len(row) and row[col_idx].strip():
                try:
                    ri = float(row[col_idx])
                    egamma = exi - exf
                    if egamma > 0:  # Only positive energies
                        transitions.append((exi, exf, ri, egamma))
                except:
                    pass
    
    return sorted(transitions, key=lambda x: (x[0], x[3]))  # Sort by Exi, then Egamma

def generate_ens_file(transitions):
    """Generate NEW ENS file with CORRECT ENSDF formatting"""
    
    lines = []
    
    # Header
    lines.append(" 35CL    2001Vo24                      2001Vo24                                 ")
    lines.append(" 35CL cL S$LABEL=E{-p}(lab) (keV)                                               ")
    lines.append(" 35CL PN                                                                     7  ")
    
    # Group transitions by Exi (energy level)
    levels_dict = {}
    for exi, exf, ri, egamma in transitions:
        if exi not in levels_dict:
            levels_dict[exi] = []
        levels_dict[exi].append((egamma, ri, exf))
    
    # Sort by Exi
    sorted_exi = sorted(levels_dict.keys())
    
    for exi in sorted_exi:
        # Add L-record for this level
        line_l = " 35CL  L {:<9}                                                                    ".format(
            "{:.1f}".format(exi) if exi % 1 != 0 else str(int(exi))
        )
        # Trim/pad to exactly 80 chars
        line_l = (line_l[:80] if len(line_l) > 80 else line_l).ljust(80)
        lines.append(line_l)
        
        # Sort gamma rays for this level by ascending energy
        gammas = sorted(levels_dict[exi], key=lambda x: x[0])
        
        # Add G-records for this level
        for egamma, ri, exf in gammas:
            # Format: " 35CL  G 2642        80                                                           "
            # Cols: 1-5=NUCID, 6=blank, 7-9=" G ", 10-19=Egamma (LEFT-JUSTIFIED), 20-21=blank, 22=space, 23-29=RI left-justified, 30-80=blank
            
            energy_str = "{:.1f}".format(egamma) if egamma % 1 != 0 else str(int(egamma))
            ri_str = "{:.1f}".format(ri) if ri % 1 != 0 else str(int(ri))
            
            # Build G-record with exact column positioning
            nucid = " 35CL"           # Cols 1-5
            blank1 = " "              # Col 6
            g_type = "G"              # Col 7
            blank2 = "  "             # Cols 8-9
            energy_field = energy_str.ljust(10)  # LEFT-JUSTIFIED in 10-char field (cols 10-19)
            de_field = "  "           # Cols 20-21 blank
            space1 = " "              # Col 22
            ri_field = ri_str.ljust(7)  # LEFT-justified in 7-char field (cols 23-29)
            rest = " " * (80 - 29)    # Rest of line to 80 chars (cols 30-80)
            
            line_g = nucid + blank1 + g_type + blank2 + energy_field + de_field + space1 + ri_field + rest
            line_g = (line_g[:80] if len(line_g) > 80 else line_g).ljust(80)
            lines.append(line_g)
    
    # Write file - CRITICAL: Do NOT rstrip() - ENSDF requires exactly 80 characters!
    with open("A35/Cl35/new/2001VO24.ens", "w") as f:
        for line in lines:
            # Ensure exactly 80 characters per ENSDF standard
            line_80 = (line[:80] if len(line) >= 80 else line.ljust(80))
            f.write(line_80 + "\n")
    
    return len(lines), len([l for l in lines if " L " in l[5:10]]), len([l for l in lines if " G " in l[5:10]])

if __name__ == "__main__":
    print("Parsing CSV...")
    transitions = parse_csv()
    print(f"✓ Extracted {len(transitions)} transitions from CSV")
    
    print("\nGenerating NEW ENS file...")
    total, num_l, num_g = generate_ens_file(transitions)
    
    print(f"✓ Generated A35/Cl35/new/2001VO24.ens")
    print(f"  Total lines: {total}")
    print(f"  L-records: {num_l}")
    print(f"  G-records: {num_g}")
    print(f"\nNEXT: Validate with column_calibrate.py, check_gamma_ordering.py, ensdf_1line_ruler.py")
