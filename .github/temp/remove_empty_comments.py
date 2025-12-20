import re
import os

file_path = r'd:\X\ND\ENSDF\A34\Cl34\new\Cl34_33s_3he_d.ens'

with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

final_lines = []

for line in lines:
    # Remove lines that are just the prefix and whitespace
    if re.match(r'^\s34CL\s+cL\s*$', line):
        continue
    final_lines.append(line)

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(final_lines)

print("Empty comment lines removed.")
