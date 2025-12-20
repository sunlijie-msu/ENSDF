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
        print(f"Matched line {i+1}")
        # Clean up
        if len(line) >= 9 and line[7].lower() == 'c':
            prefix = line[:9]
            content = line[9:].strip()
            content = content.strip('. ')
            if not content:
                line = prefix.rstrip() + '\n'
            else:
                content = re.sub(r'\s\s+', ' ', content)
                line = prefix + content + '\n'
        else:
            line = line.strip() + '\n'

    new_lines.append(line)

final_lines = []
for line in new_lines:
    if len(line) >= 9 and line[7].lower() == 'c':
        if not line[9:].strip():
            continue
    final_lines.append(line)

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(final_lines)

print(f"Successfully processed file. Final lines: {len(final_lines)}")
