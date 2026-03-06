"""
Find all bare cL $E(p)(lab)= lines in 1983Wa27 blocks, verify uniqueness,
build replacement pairs, and execute replacements.
"""

filepath = r'd:\X\ND\ENSDF\A34\Cl34\new\Cl34_33s_p_g.ens'
with open(filepath) as f:
    lines = f.readlines()

DOLLAR = chr(36)  # '$' — avoid PowerShell interpolation issues

def is_L_record(l):
    return l[0:5] == ' 34CL' and l[5] == ' ' and l[6] == ' ' and l[7] == 'L'

def is_cL_record(l):
    return l[0:5] == ' 34CL' and l[6] == 'c' and l[7] == 'L'

def is_proper_ep_bare(l):
    """cL record, content = $E(p)(lab)=..., no existing attribution (19xx or 20xx)."""
    if not is_cL_record(l):
        return False
    # col 9 (0-indexed) must be '$', col 10 must start 'E(p)(lab)='
    if l[9] != DOLLAR:
        return False
    if l[10:20] != 'E(p)(lab)=':
        return False
    if '(19' in l or '(20' in l:
        return False
    return True

# Build level blocks
blocks = []
i = 0
while i < len(lines):
    l = lines[i]
    if is_L_record(l):
        start = i
        j = i + 1
        while j < len(lines):
            if is_L_record(lines[j]):
                break
            j += 1
        blocks.append((start + 1, lines[start:j]))
        i = j
    else:
        i += 1

print(f'Total level blocks: {len(blocks)}')

# Find targets
targets = []
for start_ln, blines in blocks:
    has_wa27 = any('1983Wa27' in l for l in blines)
    if not has_wa27:
        continue
    for i, l in enumerate(blines):
        if is_proper_ep_bare(l):
            lineno = start_ln + i
            stripped = l.rstrip()
            targets.append((lineno, stripped))

print(f'Target bare E(p)(lab)= lines in 1983Wa27 blocks: {len(targets)}')
print()

# Verify uniqueness and build replacements
replacements = []
all_ok = True
for lineno, old_stripped in targets:
    count = sum(1 for l in lines if l.rstrip() == old_stripped)
    if count != 1:
        print(f'ERROR L{lineno}: count={count} [{old_stripped}]')
        all_ok = False
        continue
    new_stripped = old_stripped.rstrip() + ' (1983Wa27)'
    if len(new_stripped) > 80:
        print(f'WARNING L{lineno}: exceeds 80 chars ({len(new_stripped)}): {new_stripped}')
        all_ok = False
        continue
    new_line = new_stripped.ljust(80)
    replacements.append((lineno, old_stripped, new_line))
    print(f'L{lineno}: [{old_stripped}]')
    print(f'      -> [{new_line}]')
    print()

print()
print(f'Replacements to execute: {len(replacements)}')
print(f'All OK: {all_ok}')

# Write pairs to JSON for reference
import json, os
out_path = r'd:\X\ND\ENSDF\.github\temp\wa27_ep_pairs.json'
with open(out_path, 'w') as f:
    json.dump([{'lineno': ln, 'old': o, 'new': n} for ln, o, n in replacements], f, indent=2)
print(f'Pairs written to {out_path}')
