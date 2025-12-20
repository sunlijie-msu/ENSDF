import re
import os

file_path = r'd:\X\ND\ENSDF\A34\Cl34\new\Cl34_33s_3he_d.ens'

with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

final_lines = []

for line in lines:
    # Skip empty lines (completely empty or just whitespace)
    if not line.strip():
        continue
        
    # Check if it's a comment line
    if len(line) >= 8 and line[7].lower() == 'c':
        # Extract content after column 9
        content = line[9:].strip('. ')
        if not content:
            continue # Skip empty comments
            
        # Fix prefix
        # Standard prefix: " 34CL" (5) + CONT (1) + " " (1) + "c" (1) + ID (1) = 9 chars
        # Or " 34CL cL"
        prefix = line[:9]
        # Normalize prefix: remove extra spaces, ensure it starts with a space
        prefix = ' ' + prefix.strip()
        # Ensure it's 9 chars
        if 'cL' in prefix:
            # Handle " 34CL cL"
            prefix = " 34CL  cL" # 5 + 1 + 1 + 1 + 1 = 9? No.
            # 1 (space) + 4 (34CL) + 2 (spaces) + 1 (c) + 1 (L) = 9
            prefix = " 34CL  cL"
        elif '2cL' in prefix:
            prefix = " 34CL2 cL"
        elif ' c ' in prefix:
            prefix = " 34CL   c"
            
        # Actually, let's just use the original prefix but fix the leading space and length
        prefix = line[:9]
        if not prefix.startswith(' '):
            prefix = ' ' + prefix.lstrip()
        
        # If it's something like "  34CL2cL", fix it to " 34CL2cL"
        if prefix.startswith('  '):
            prefix = prefix[1:]
            
        # Ensure it's exactly 9 chars
        if len(prefix) < 9:
            prefix = prefix.ljust(9)
        elif len(prefix) > 9:
            prefix = prefix[:9]
            
        final_lines.append(prefix + content + '\n')
    else:
        final_lines.append(line)

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(final_lines)

print("Final cleanup complete.")
