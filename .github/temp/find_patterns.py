import re
import os

file_path = r'd:\X\ND\ENSDF\A34\Cl34\new\Cl34_33s_3he_d.ens'

with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if '$E(p)(res)' in line:
        print(f"Line {i+1}: {line.strip()}")
    if 'Resonance strength |w|g' in line:
        print(f"Line {i+1}: {line.strip()}")
