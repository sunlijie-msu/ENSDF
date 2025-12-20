import re
import os

file_path = r'd:\X\ND\ENSDF\A34\Cl34\new\Cl34_33s_3he_d.ens'

with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

new_lines = []

for i in range(len(lines)):
    line = lines[i]
    
    # Fix indentation for lines starting with 34CL
    if line.startswith('34CL'):
        line = ' ' + line
        
    # Fix multi-line rephrasing for L=2
    if 'C{+2}S= for L=2' in line:
        # Check next line
        if i + 1 < len(lines):
            next_line = lines[i+1]
            # Fix indentation of next line if needed
            if next_line.startswith('34CL'):
                next_line = ' ' + next_line
            
            match = re.search(r' 34CL2cL ([\d\.\s\{I\+\-\}]+)', next_line)
            if match:
                s_val = match.group(1).strip()
                line = line.replace('C{+2}S= for L=2', f'C{{+2}}S={s_val} for L=2')
                # Mark next line for removal
                lines[i+1] = ""
    
    if line:
        new_lines.append(line)

# Final pass to ensure 80 columns for L-records
final_lines = []
for line in new_lines:
    if line.startswith(' 34CL  L'):
        # Pad with spaces to 80 chars (excluding newline)
        content = line.rstrip('\n\r')
        if len(content) < 80:
            content = content.ljust(80)
        elif len(content) > 80:
            content = content[:80]
        line = content + '\n'
    final_lines.append(line)

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(final_lines)

print("Final fixes complete.")
