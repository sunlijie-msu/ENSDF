"""
Print exact old/new pairs for all 35 replacements.
Used to construct multi_replace_string_in_file tool calls.
Does NOT modify the .ens file.
"""
import json
import sys

with open(r'd:\X\ND\ENSDF\.github\temp\replacements.json', 'r', encoding='ascii') as f:
    reps = json.load(f)

content = open(r'd:\X\ND\ENSDF\A34\Cl34\new\Cl34_33s_p_g.ens', 'rb').read().decode('ascii')

# Verify all found
all_ok = all(r['old'] in content for r in reps)
print(f'All {len(reps)} old strings found: {all_ok}')
print()

# Print each as labeled sections
for i, r in enumerate(reps):
    old = r['old']
    new = r['new']
    old_lines = old.split('\r\n')
    print(f'=== REP {i:02d} (old lines: {len(old_lines)}) ===')
    for j, line in enumerate(old_lines):
        stripped = line.rstrip()
        trailing = len(line) - len(stripped)
        print(f'  OLD L{j}: {repr(stripped)} + {trailing} spaces')
    print(f'  NEW: {repr(new)}')
    print()
