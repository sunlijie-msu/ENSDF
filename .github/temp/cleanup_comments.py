import re
import os

file_path = r'd:\X\ND\ENSDF\A34\Cl34\new\Cl34_33s_3he_d.ens'

with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

final_lines = []

for line in lines:
    # Check if it's a comment line (even if prefix is slightly broken)
    # We look for 'cL', 'c ', '2cL', etc. in the first few columns.
    # Standard ENSDF: NUCID (1-5), CONT (6), BLANK (7), TYPE (8), BLANK (9)
    # For comments: TYPE is 'c' or 'C'.
    
    is_comment = False
    if len(line) >= 8 and line[7].lower() == 'c':
        is_comment = True
    elif 'cL' in line[:10] or ' c ' in line[:10]:
        is_comment = True
        
    if is_comment:
        # Extract content
        # Try to find where the content starts. Usually column 10.
        content = line[9:].strip('. ')
        if not content:
            continue # Skip empty comments
        
        # Fix prefix if needed
        # Standard prefix for 34CL: " 34CL  " (5 chars) + " " (col 6) + " " (col 7) + "c" (col 8) + "L" (col 9)
        # Or " 34CL cL"
        prefix = line[:9]
        if not prefix.startswith(' '):
            prefix = ' ' + prefix.lstrip()
        
        # Ensure prefix is 9 chars
        if len(prefix) < 9:
            prefix = prefix.ljust(9)
        elif len(prefix) > 9:
            prefix = prefix[:9]
            
        final_lines.append(prefix + content + '\n')
    else:
        final_lines.append(line)

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(final_lines)

print("Cleanup complete.")
