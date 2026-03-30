"""
Fix remaining 12 FLAG=B lines that failed to apply due to ordering.
Reads the current (modified) file and applies targeted replacements.
"""
import os

BASE = 'd:\\X\\ND\\ENSDF'
ENS_FILE = os.path.join(BASE, 'A34', 'Cl34', 'new', 'Cl34_adopted.ens')

with open(ENS_FILE, 'r') as f:
    file_lines = f.readlines()
    content = ''.join(file_lines)

# Build exact lines from file by searching
def find_line(content_lines, substr, start=0):
    for i in range(start, len(content_lines)):
        if substr in content_lines[i]:
            return i
    return -1

def pad80(s):
    """Pad or truncate to exactly 80 chars (no newline)."""
    return s.ljust(80)

# RI$ line to add (padded to 80 + newline)
RI_LINE = pad80(' 34CL cG RI$From {+32}S({+3}He,p|g)') + '\n'
FLAG_B_LINE = pad80(' 34CLF G FLAG=B') + '\n'

print(f'RI line ({len(RI_LINE.rstrip())} chars): {repr(RI_LINE.rstrip())}')
print(f'FLAG=B line ({len(FLAG_B_LINE.rstrip())} chars): {repr(FLAG_B_LINE.rstrip())}')

# Define replacements for each remaining FLAG=B instance
# Format: (context_line_content, action, g_energy)
# action: 'delete' or 'expand'
# For uniqueness, use the G data line before (if needed) or E$ line

replacements_spec = [
    # (unique_prefix_substr_in_file, action, label)
    # G 1740.2: FLAG=B between G data and B cont — delete only
    ('G 1740.2    16 72.8   16 D+Q', 'delete_G+FLAG', 'G 1740.2'),
    # G 271: E$+FLAG=B followed by next G record — expand (add RI$)
    ('G 271         1.5     LT [M1,E2]', 'expand_G+E+FLAG', 'G 271'),
    # G 927.6: E$+FLAG=B followed by existing RI$ — delete only
    ('G 927.6       8.61    31 D(+Q)', 'delete_G+E+FLAG', 'G 927.6'),
    # G 1492.6: E$+FLAG=B followed by next G record — expand
    ('G 1492.6      0.76    LT [M1,E2]', 'expand_G+E+FLAG', 'G 1492.6'),
    # G 1697.6: E$+FLAG=B followed by existing RI$ — delete only
    ('G 1697.6    4 100.0   5 M1+E2', 'delete_G+E+FLAG', 'G 1697.6'),
    # G 2011.4: E$+FLAG=B followed by existing RI$ — delete only
    ('G 2011.4      15      5 D+Q', 'delete_G+E+FLAG', 'G 2011.4'),
    # G 2157.8: E$+FLAG=B followed by existing RI$ — delete only
    ('G 2157.8      23.5    5 [E2]', 'delete_G+E+FLAG', 'G 2157.8'),
    # G 1145.4: E$+FLAG=B followed by B cont + RI$ — delete only
    ('G 1145.4      0.85    26 [E2]', 'delete_G+E+FLAG', 'G 1145.4'),
    # G 1710.4: E$+FLAG=B followed by next G record — expand
    ('G 1710.4      2       LT [M3]', 'expand_G+E+FLAG', 'G 1710.4'),
    # G 1914.4: E$+FLAG=B followed by next G record — expand
    ('G 1914.4      4       LT [M3]', 'expand_G+E+FLAG', 'G 1914.4'),
    # G 2230.1: E$+FLAG=B followed by B cont + RI$ — delete only
    ('G 2230.1    4 100.00  20 M1+E2', 'delete_G+E+FLAG', 'G 2230.1'),
    # G 2375.6: E$+FLAG=B followed by blank — expand
    ('G 2375.6      2       LT [E4]', 'expand_G+E+FLAG', 'G 2375.6'),
]

# E$ line added by flag_A_expand ops (common to all)
E_FROM_LINE = pad80(' 34CL cG E$From {+32}S({+3}He,p|g)') + '\n'

applied_count = 0
errors = []

for (search_str, action, label) in replacements_spec:
    # Find the G data line
    g_idx = find_line(file_lines, search_str)
    if g_idx < 0:
        errors.append(f'NOT FOUND: G line for {label} (search: {search_str})')
        continue

    g_line = file_lines[g_idx]

    if action == 'delete_G+FLAG':
        # Old: G_data + FLAG=B, New: G_data (FLAG=B deleted)
        # Find FLAG=B right after G data
        flag_idx = g_idx + 1
        while flag_idx < len(file_lines) and 'FLAG=' not in file_lines[flag_idx] and file_lines[flag_idx].strip() == '':
            flag_idx += 1
        if 'FLAG=B' not in file_lines[flag_idx]:
            errors.append(f'Expected FLAG=B at {flag_idx+1} for {label}, got: {repr(file_lines[flag_idx].rstrip())}')
            continue
        old = g_line + file_lines[flag_idx]
        new = g_line
        print(f'{label} ({action}): delete FLAG=B at line {flag_idx+1}')

    elif action == 'delete_E+FLAG':
        # Old: E$_line + FLAG=B, New: E$_line (FLAG=B deleted)
        # E$ line is right before FLAG=B (may have been added by expand op or already existed)
        flag_idx = find_line(file_lines, 'FLAG=B', g_idx)
        if flag_idx < 0:
            errors.append(f'No FLAG=B found after G line for {label}')
            continue
        e_idx = flag_idx - 1
        e_line = file_lines[e_idx]
        if 'cG E$' not in e_line:
            errors.append(f'Expected cG E$ at line {e_idx+1} for {label}, got: {repr(e_line.rstrip())}')
            continue
        old = e_line + file_lines[flag_idx]
        new = e_line
        print(f'{label} ({action}): delete FLAG=B at line {flag_idx+1}')

    elif action == 'delete_G+E+FLAG':
        # Old: G_data + E$_line + FLAG=B, New: G_data + E$_line (FLAG=B deleted)
        e_idx = g_idx + 1
        e_line = file_lines[e_idx]
        if 'cG E$' not in e_line:
            errors.append(f'Expected cG E$ at line {e_idx+1} for {label}, got: {repr(e_line.rstrip())}')
            continue
        flag_idx = e_idx + 1
        if 'FLAG=B' not in file_lines[flag_idx]:
            errors.append(f'Expected FLAG=B at line {flag_idx+1} for {label}, got: {repr(file_lines[flag_idx].rstrip())}')
            continue
        old = g_line + e_line + file_lines[flag_idx]
        new = g_line + e_line
        print(f'{label} ({action}): delete FLAG=B at line {flag_idx+1}')

    elif action == 'expand_G+E+FLAG':
        # Old: G_data + E$_line + FLAG=B, New: G_data + E$_line + RI$_line
        # E$ immediately follows G data, FLAG=B follows E$
        e_idx = g_idx + 1
        if 'cG E$' not in file_lines[e_idx]:
            errors.append(f'Expected cG E$ at line {e_idx+1} for {label}, got: {repr(file_lines[e_idx].rstrip())}')
            continue
        flag_idx = e_idx + 1
        if 'FLAG=B' not in file_lines[flag_idx]:
            errors.append(f'Expected FLAG=B at line {flag_idx+1} for {label}, got: {repr(file_lines[flag_idx].rstrip())}')
            continue
        old = g_line + file_lines[e_idx] + file_lines[flag_idx]
        new = g_line + file_lines[e_idx] + RI_LINE
        print(f'{label} ({action}): replace FLAG=B with RI$ at line {flag_idx+1}')

    # Verify uniqueness
    count = content.count(old)
    if count != 1:
        errors.append(f'{label}: old string found {count} times (expected 1)')
        print(f'  ERROR: old string found {count} times!')
        print(f'  old: {repr(old[:100])}')
        continue

    # Apply replacement
    content = content.replace(old, new, 1)
    file_lines = content.splitlines(keepends=True)  # update lines
    applied_count += 1
    print(f'  -> Applied successfully ({applied_count} total)')

print()
print(f'Applied: {applied_count}/12')
if errors:
    print('ERRORS:')
    for e in errors:
        print(f'  {e}')
else:
    print('No errors.')

# Check remaining FLAG= lines
remaining = [l.strip() for l in content.splitlines() if 'FLAG=' in l]
print(f'Remaining FLAG= lines: {len(remaining)}')
for r in remaining[:10]:
    print(f'  {r}')

# Write file
with open(ENS_FILE, 'w') as f:
    f.write(content)
print('File written.')
