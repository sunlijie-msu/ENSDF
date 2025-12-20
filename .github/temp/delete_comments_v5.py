import re
import os

file_path = r'd:\X\ND\ENSDF\A34\Cl34\new\Cl34_33s_3he_d.ens'

with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

# Regex for $E(p)(res)=...
ep_res_pattern = re.compile(r'\$E\(p\)\(res\)\s*=\s*[\d\.]+(\s+\{I[\+\-\d]+\})?')
# Regex for Resonance strength |w|g...
w_g_pattern = re.compile(r'Resonance\s+strength\s+\|w\|g\s*[<>=]\s*[\d\.]+(\s+meV)?(\s+\{I?[\+\-\d]+\})?')

new_lines = []

for line in lines:
    if len(line) >= 8 and line[7].lower() == 'c':
        # It's a comment line
        original_line = line
        
        # 1. Remove the patterns
        line = ep_res_pattern.sub('', line)
        line = w_g_pattern.sub('', line)
        
        if line != original_line:
            # 2. Clean up the content part
            # We assume the header is the first 9 characters (or up to where 'c' is)
            # Let's find the 'c' or 'C' at index 7.
            header = line[:9]
            content = line[9:]
            
            # Remove leading/trailing dots and spaces from content
            content = content.strip()
            content = content.strip('. ')
            
            if not content:
                line = "" # Mark for removal
            else:
                # Collapse multiple spaces
                content = re.sub(r'\s\s+', ' ', content)
                line = header + content + '\n'
    
    if line:
        new_lines.append(line)

# Final pass to remove empty comments
final_lines = []
for line in new_lines:
    if len(line) >= 8 and line[7].lower() == 'c':
        if not line[9:].strip('. '):
            continue
    final_lines.append(line)

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(final_lines)

print("Cleanup complete.")
