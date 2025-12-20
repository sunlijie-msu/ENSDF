import re
import os

file_path = r'd:\X\ND\ENSDF\A34\Cl34\new\Cl34_33s_3he_d.ens'

with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Fix joined lines
# Pattern: "for L=... 34CL"
content = re.sub(r'(for L=[\d\+]+)\s+(34CL)', r'\1\n\2', content)

# Fix "C{+2}S= for L=2 34CL2cL"
content = re.sub(r'(C\{+2\}S=\s+for L=2)\s+(34CL2cL)', r'\1\n\2', content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Joined lines fixed.")
