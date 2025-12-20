import re
import os

file_path = r'd:\X\ND\ENSDF\A34\Cl34\new\Cl34_33s_3he_d.ens'

with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

final_lines = []

for line in lines:
    # Fix broken words from previous failed attempts
    line = line.replace('34CL2cL able 2 of 2014Pa44.', ' 34CL2cL Table 2 of 2014Pa44.')
    line = line.replace('34CL2cL of 2014Pa44.', ' 34CL2cL Table 2 of 2014Pa44.')
    
    # Fix prefix (ensure leading space)
    if line.startswith('34CL'):
        line = ' ' + line
        
    # Remove empty or near-empty comment lines
    if len(line) >= 8 and line[7].lower() == 'c':
        content = line[9:].strip('. ')
        if not content:
            continue
            
    final_lines.append(line)

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(final_lines)

print("Cleanup complete.")
