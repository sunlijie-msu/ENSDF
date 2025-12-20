import re
import os

file_path = r'd:\X\ND\ENSDF\A34\Cl34\new\Cl34_33s_3he_d.ens'

if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    exit(1)

with open(file_path, 'r') as f:
    lines = f.readlines()

new_lines = []

# Regex for $E(p)(res)=...
# Matches $E(p)(res)= followed by digits/dots, and optionally a space and {I...}
ep_res_pattern = re.compile(r'\$E\(p\)\(res\)=[\d\.]+(\s+\{I[\+\-\d]+\})?')

# Regex for Resonance strength |w|g...
# Matches Resonance strength |w|g followed by <, >, or =, then digits/dots, 
# optionally meV, and optionally a space and {I?...} or {...}
w_g_pattern = re.compile(r'Resonance strength \|w\|g[<>=][\d\.]+(\s+meV)?(\s+\{I?[\+\-\d]+\})?')

for line in lines:
    # Only process comment lines (cL, cG, c, etc.)
    # Column 8 is 'c' or 'C'.
    if len(line) >= 8 and line[7].lower() == 'c':
        # Remove the patterns
        line = ep_res_pattern.sub('', line)
        line = w_g_pattern.sub('', line)
        
        # Clean up: collapse multiple spaces and remove leading/trailing dots/spaces in the content part
        prefix = line[:9]
        content = line[9:].strip()
        
        # Remove leading/trailing dots that might have been separators
        content = content.strip('. ')
        
        if not content:
            # If content is empty, we'll skip this line later
            line = prefix.rstrip() + '\n'
        else:
            # Collapse multiple spaces in content
            content = re.sub(r'\s\s+', ' ', content)
            line = prefix + content + '\n'

    new_lines.append(line)

final_lines = []
for line in new_lines:
    # Skip lines that are just the prefix (empty comments)
    if len(line) >= 8 and line[7].lower() == 'c':
        if not line[9:].strip():
            continue
    final_lines.append(line)

with open(file_path, 'w') as f:
    f.writelines(final_lines)

print("Successfully processed file.")
