"""
Remove all inserted 'cL E$from 1983Wa27' lines that appear AFTER L 6136.2.
Preserves all pre-existing cL E$ blocks (which are multi-line, not single 'from 1983Wa27').
"""

ENS_FILE = r'd:\X\ND\ENSDF\A34\Cl34\new\Cl34_33s_p_g.ens'

TARGET_CONTENT = ' 34CL cL E$from 1983Wa27'  # 25 chars → padded to 80 in file

def is_L_record(line):
    return len(line) >= 8 and line[5] == ' ' and line[6] == ' ' and line[7] == 'L'

def get_L_energy(line):
    return line[9:19].strip()

with open(ENS_FILE, encoding='utf-8') as f:
    lines = f.readlines()

# Find L 6136.2 position
boundary_idx = None
for idx, line in enumerate(lines):
    raw = line.rstrip('\n')
    if is_L_record(raw) and get_L_energy(raw) == '6136.2':
        boundary_idx = idx
        break

if boundary_idx is None:
    print("ERROR: L 6136.2 not found!")
    exit(1)

print(f"L 6136.2 found at line {boundary_idx + 1} (1-based)")

# Identify lines to remove: single 'cL E$from 1983Wa27' lines after boundary
to_remove = set()
for idx in range(boundary_idx + 1, len(lines)):
    raw = lines[idx].rstrip('\n').rstrip()
    if raw == TARGET_CONTENT:
        to_remove.add(idx)

print(f"Lines to remove: {len(to_remove)}")
for idx in sorted(to_remove):
    print(f"  Line {idx + 1}: {lines[idx].rstrip()}")

# Apply removal
new_lines = [line for idx, line in enumerate(lines) if idx not in to_remove]

with open(ENS_FILE, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print(f"\nDone. Removed {len(to_remove)} lines.")
