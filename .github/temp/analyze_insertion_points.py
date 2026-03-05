#!/usr/bin/env python3
"""
Script to add 1983Wa27 |w|g comment lines to Cl34_33s_p_g.ens
"""

import re

# Resonance strength data: Ep -> (|w|g value, {In} notation)
data_map = {
    447: ("0.4", "1"),
    507.6: ("0.7", "2"),
    546: ("0.7", "3"),
    639: ("0.1", "0"),
    662: ("0.4", "2"),
    683: ("0.4", "2"),
    731.4: ("0.5", "2"),
    777: ("0.5", "2"),
    822: ("0.8", "2"),
    914: ("0.4", "2"),
    976: ("1.0", "3"),  # near 974.61
    1023: ("0.7", "2"),
    1029: ("1.1", "3"),
    1057: ("1.8", "5"),
    1097: ("1.4", "3"),
    1118.5: ("1.2", "3"),
    1158: ("0.4", "2"),
    1165: ("3.3", "7"),
    1215: ("2.2", "9"),
    1264.4: ("2.7", "6"),
    1347.3: ("0.9", "3"),
    1386: ("0.6", "3"),
    1448: ("1.4", "4"),
    1477: ("0.7", "3"),
    1528: ("0.4", "1"),
    1629.4: ("1.0", "4"),
    1644: ("0.7", "3"),
    1698: ("0.2", "1"),
    1706: ("4.8", "10"),
    1738: ("0.4", "1"),
    1762: ("2.1", "5"),
    1752: ("4.7", "20"),
    1780.7: ("0.4", "2"),
    1798.1: ("2.9", "10"),
    1812.3: ("2.4", "6"),
    1843: ("0.8", "3"),
    1997: ("1.7", "4"),
}

with open(r'd:\X\ND\ENSDF\A34\Cl34\new\Cl34_33s_p_g.ens', 'r') as f:
    lines = f.readlines()

output_lines = []
i = 0
entries_added = 0
entries_skipped = 0

while i < len(lines):
    output_lines.append(lines[i])
    
    # Check if this line contains E(p)(lab)=
    if 'E(p)(lab)=' in lines[i]:
        # Extract all E(p)(lab) values from this line and the next line(s)
        current_text = lines[i]
        j = i + 1
        
        # Continue reading multiline comments (lines starting with " 34CLncL" or similar)
        while j < len(lines) and (lines[j].startswith(' 34CL') and ('cL' in lines[j]) and not lines[j].lstrip().startswith('L')):
            current_text += " " + lines[j].strip()
            j += 1
        
        # Find all E(p)(lab) values in this block
        ep_values = re.findall(r'E\(p\)\(lab\)=([\d.]+)', current_text)
        
        # Check if any match our data map
        for ep_str in ep_values:
            ep_float = float(ep_str)
            
            # Check for exact match or close match (within 1%)
            for ep_target in data_map.keys():
                if abs(ep_float - ep_target) < max(0.1, ep_target * 0.01):
                    # Found a match!
                    wg_val, unc_int = data_map[ep_target]
                    
                    # Check if 1983Wa27 |w|g already exists in this comment block
                    if '1983Wa27' not in current_text:
                        # Need to add it
                        # Find the position to insert: after the current comment block
                        # We'll append it to output_lines after the current block finishes
                        
                        cL_line = f" 34CL  cL $ |w|g={wg_val} {{I{unc_int}}} (1983Wa27)"
                        # Mark for insertion after current block
                        # We'll do this after copying all lines up to j-1
                        
                        print(f"Found E(p)(lab)={ep_target}: will add |w|g={wg_val} {{I{unc_int}}}")
                        entries_added += 1
    i += 1

# This script shows what WOULD be added; actual insertion is manual
print()
print(f"Total entries found: {entries_added}")
