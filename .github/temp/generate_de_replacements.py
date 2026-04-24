#!/usr/bin/env python3
"""
Generate precise DE field replacements for integer-energy gamma rays.
For each target G-record with integer energy and blank DE field:
  - Replace DE field (columns 20-21) from "  " to "1 "
  - Preserve all other columns exactly
"""

import os

# Read the file
file_path = "A34/Cl34/new/Cl34_27al_12c_ang.ens"
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Target lines (0-indexed)
target_indices = [
    75, 78, 79, 81, 83, 85, 87, 88, 90, 91, 93, 95, 97, 103, 106, 108, 109, 110,
    112, 114, 115, 116, 118, 120, 122, 150, 154, 168, 174, 181, 183, 184, 193,
    197, 213, 217, 221, 225, 230, 234, 239
]

print(f"Total target G-records: {len(target_indices)}\n")

replacements = []

for idx in target_indices:
    line_num = idx + 1
    line = lines[idx].rstrip('\n')
    
    # Verify it's a G-record with integer energy
    if len(line) < 21:
        print(f"ERROR Line {line_num}: Line too short ({len(line)} chars)")
        continue
    
    if line[7] != 'G':
        print(f"ERROR Line {line_num}: Not a G-record (char at pos 8: '{line[7]}')")
        continue
    
    # Extract the energy field (columns 10-19, 0-indexed: 9-19)
    energy_str = line[9:19]
    energy_trimmed = energy_str.strip()
    
    # Check if it's an integer energy (no decimal point)
    if '.' not in energy_trimmed and energy_trimmed.isdigit():
        # Check if DE field (columns 20-21, 0-indexed: 19-21) is blank
        de_field = line[19:21]
        if de_field == '  ':
            # This is a target line
            before = line[:19]  # Everything before DE field
            after = line[21:]   # Everything after DE field
            
            old_line = line
            new_line = before + '1 ' + after
            
            # Verify length
            if len(new_line) == 80:
                replacements.append({
                    'line_num': line_num,
                    'energy': energy_trimmed,
                    'old': old_line,
                    'new': new_line
                })
                print(f"✓ Line {line_num}: Energy={energy_trimmed}")
            else:
                print(f"ERROR Line {line_num}: New line length is {len(new_line)}, not 80")

print(f"\nValid replacements: {len(replacements)}")
for r in replacements[:5]:
    print(f"\nLine {r['line_num']} (Energy {r['energy']}):")
    print(f"  Old: '{r['old']}'")
    print(f"  New: '{r['new']}'")
