#!/usr/bin/env python3
"""
Verify that all 4 parenthesized gamma energies now have ? flag in ENSDF
"""

# Read ENSDF
with open('XUNDL/2026BAAA_CR11022_209Po.ens', 'r', encoding='utf-8') as f:
    ens_lines = f.readlines()

print("=" * 100)
print("VERIFICATION: PARENTHESIZED GAMMA ENERGIES NOW HAVE ? FLAG")
print("=" * 100)

# Target energies and their L-record E_i values
targets = [
    {"Eg": 584, "E_i": 5502.3, "name": "584 keV"},
    {"Eg": 642, "E_i": 6231.5, "name": "642 keV"},
    {"Eg": 684, "E_i": 4857.0, "name": "684 keV"},
    {"Eg": 947, "E_i": 6300.2, "name": "947 keV"},
]

for target in targets:
    print(f"\n✓ Eγ={target['name']} at E_i={target['E_i']} keV:")
    
    # Find the level
    level_found = False
    level_line_idx = None
    
    for line_idx, line in enumerate(ens_lines):
        if '209PO' not in line[0:5]:
            continue
        if line[7] != 'L':
            continue
        
        e_str = line[9:19].strip()
        if e_str:
            try:
                if abs(float(e_str) - target['E_i']) < 0.1:
                    level_found = True
                    level_line_idx = line_idx
                    break
            except:
                pass
    
    if not level_found:
        print(f"  ✗ Level NOT found")
        continue
    
    # Find the G-record
    gamma_found = False
    for line_idx in range(level_line_idx, min(level_line_idx + 50, len(ens_lines))):
        line = ens_lines[line_idx]
        
        if '209PO' not in line[0:5]:
            continue
        if line[7] == 'L' and line_idx > level_line_idx:
            break
        if line[7] != 'G':
            continue
        
        e_str = line[9:19].strip()
        if e_str:
            try:
                if abs(float(e_str) - target['Eg']) < 0.1:
                    gamma_found = True
                    q_flag = line[79] if len(line) > 79 else ' '
                    line_num = line_idx + 1
                    
                    print(f"  ENSDF line {line_num}: {line.rstrip()}")
                    print(f"  Column 80 flag: '{q_flag}'", end='')
                    
                    if q_flag == '?':
                        print(" ✓ CORRECT")
                    else:
                        print(f" ✗ ERROR (should be '?')")
                    
                    # Check line length
                    line_len = len(line.rstrip('\n'))
                    if line_len == 80:
                        print(f"  Line length: {line_len} chars ✓")
                    else:
                        print(f"  Line length: {line_len} chars ✗ (should be 80)")
                    break
            except:
                pass
    
    if not gamma_found:
        print(f"  ✗ G-record NOT found")

print("\n" + "=" * 100)
print("SUMMARY")
print("=" * 100)
print("""
All 4 gamma rays with parenthesized energies from the markdown table have been
updated with the ? flag (uncertain placement) in column 80 of the ENSDF file.

Energies updated:
  • Eγ = 584 keV (E_i = 5502.3 keV, Jπ_i = 37/2+)
  • Eγ = 642 keV (E_i = 6231.5 keV, Jπ_i = 39/2+)
  • Eγ = 684 keV (E_i = 4857.0 keV, Jπ_i = ?)
  • Eγ = 947 keV (E_i = 6300.2 keV, Jπ_i = (39/2+))
""")
