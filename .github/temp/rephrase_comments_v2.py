import re
import os

file_path = r'd:\X\ND\ENSDF\A34\Cl34\new\Cl34_33s_3he_d.ens'

with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

new_lines = []

# Task 2: Remove specific comment lines
# We do this first to avoid processing them
lines = [l for l in lines if not l.startswith(' 34CL cL from adopted value of E{-x}=')]

for i in range(len(lines)):
    line = lines[i]
    
    # Task 1: Remove Flag E (Column 77)
    if line.startswith(' 34CL  L'):
        if len(line) >= 77 and line[76] == 'E':
            line_list = list(line)
            line_list[76] = ' '
            line = "".join(line_list)
            
    # Task 3: Rephrase cL comments
    # Case 1: Single line "Value for L=3 is 0.020 {I1}"
    if 'Value for L=' in line and ' is ' in line:
        match = re.search(r'Value for L=([\d\+]+) is ([\d\.\s\{I\+\-\}]+)', line)
        if match:
            l_val = match.group(1)
            s_val = match.group(2).strip()
            replacement = f'C{{+2}}S={s_val} for L={l_val}'
            line = line.replace(match.group(0), replacement)
            
    # Case 2: Multi-line "For L=2, value is" followed by value on next line
    if 'For L=2, value is' in line:
        # Check next line
        if i + 1 < len(lines) and ' 34CL2cL ' in lines[i+1]:
            val_line = lines[i+1]
            val_match = re.search(r' 34CL2cL ([\d\.\s\{I\+\-\}]+)', val_line)
            if val_match:
                s_val = val_match.group(1).strip()
                # Rephrase line i
                line = line.replace('For L=2, value is', f'C{{+2}}S={s_val} for L=2')
                # Clear line i+1 (we'll skip it)
                lines[i+1] = "" 
        else:
            line = line.replace('For L=2, value is', 'C{+2}S= for L=2')

    # Case 3: Multi-line "Value for L=2 is " followed by value on next line
    if 'Value for L=2 is' in line:
        if i + 1 < len(lines) and ' 34CL2cL ' in lines[i+1]:
            val_line = lines[i+1]
            val_match = re.search(r' 34CL2cL ([\d\.\s\{I\+\-\}]+)', val_line)
            if val_match:
                s_val = val_match.group(1).strip()
                line = line.replace('Value for L=2 is', f'C{{+2}}S={s_val} for L=2')
                lines[i+1] = ""
        else:
            line = line.replace('Value for L=2 is', 'C{+2}S= for L=2')

    if line:
        new_lines.append(line)

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Processing complete.")
