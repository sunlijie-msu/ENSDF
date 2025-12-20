import re
import os

file_path = r'd:\X\ND\ENSDF\A34\Cl34\new\Cl34_33s_3he_d.ens'

if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    exit(1)

with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

new_lines = []

# More flexible regex
ep_res_pattern = re.compile(r'\$E\(p\)\(res\)\s*=\s*[\d\.]+(\s+\{I[\+\-\d]+\})?')
w_g_pattern = re.compile(r'Resonance\s+strength\s+\|w\|g\s*[<>=]\s*[\d\.]+(\s+meV)?(\s+\{I?[\+\-\d]+\})?')

print(f"Processing {len(lines)} lines...")

for i, line in enumerate(lines):
    original_line = line
    
    # Remove the patterns
    line = ep_res_pattern.sub('', line)
    line = w_g_pattern.sub('', line)
    
    if line != original_line:
        # Clean up
        if len(line) >= 9 and line[7].lower() == 'c':
            prefix = line[:9]
            content = line[9:].strip()
            # Remove leading/trailing dots and spaces
            content = content.strip('. ')
            if not content:
                line = "" # Mark for removal
            else:
                # Collapse multiple spaces
                content = re.sub(r'\s\s+', ' ', content)
                line = prefix + content + '\n'
        else:
            # For non-comment lines (shouldn't happen with these patterns but just in case)
            line = line.strip() + '\n'
    
    if line:
        new_lines.append(line)

# Final pass to remove any remaining empty comment lines or lines that are just prefix
final_lines = []
for line in new_lines:
    if len(line) >= 9 and line[7].lower() == 'c':
        content = line[9:].strip('. ')
        if not content:
            continue
    final_lines.append(line)

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(final_lines)

print(f"Successfully processed file. Final lines: {len(final_lines)}")
