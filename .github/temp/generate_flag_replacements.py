"""
Generate FLAG expansion replacement pairs for Cl34_adopted.ens
Read-only analysis - outputs JSON of (old_string, new_string) pairs
"""
import re
import json

def pad80(s):
    return s.ljust(80)

J_LINE   = pad80(" 34CL cL J$From {+33}S(p,p):resonances based R-matrix analysis (1989Va15)") + "\n"
assert len(J_LINE.rstrip('\n')) == 80, f"J_LINE length {len(J_LINE.rstrip())} != 80"

with open('A34/Cl34/new/Cl34_adopted.ens', 'r', encoding='latin-1') as f:
    content = f.read()
    lines = content.splitlines(keepends=True)

replacements = []  # list of (old_string, new_string, description)

# =========================================================================
# FLAG=b L-record expansion
# Strategy:
#   Case A (no following cL comment): replace [XREF]\n[FLAG=b]\n with [XREF]\n[J$]\n
#   Case B (has cL E$, no T$): replace [FLAG=b]\n[E$block]\n with [E$block]\n[J$]\n
#   Case C (has cL E$, has T$): replace [FLAG=b]\n[E$block]\n[T$] with [E$block]\n[J$]\n[T$]
#   Case D (has other cL, no E$): inspect individually
# =========================================================================
def find_parent_data_line(lines, idx, record_type):
    """Find the parent data record line (L or G) for a FLAG= continuation"""
    for j in range(idx-1, max(idx-20, -1), -1):
        nl = lines[j]
        if len(nl) > 7 and nl[5] == ' ' and nl[6] == ' ' and nl[7] == record_type and nl[0:5].strip():
            return j  # 0-indexed
    return None

def build_context(lines, parent_idx, flag_idx):
    """Build old_string from parent data record through FLAG= line (inclusive)"""
    if parent_idx is None:
        return lines[flag_idx-1] + lines[flag_idx]
    return ''.join(lines[parent_idx:flag_idx+1])

print("=== FLAG=b replacement generation ===")
flag_b_lines = []
for i, line in enumerate(lines):
    if line.startswith(' 34CLF L FLAG=b'):
        flag_b_lines.append(i)

print(f"Total FLAG=b: {len(flag_b_lines)}")

case_counts = {'A': 0, 'B': 0, 'C': 0, 'D': 0}

for idx in flag_b_lines:
    flag_line = lines[idx]
    # Find all following cL comment lines until we hit a G-record or next L-record
    following_cL = []
    following_end = idx + 1
    for j in range(idx + 1, min(idx + 15, len(lines))):
        nl = lines[j]
        if len(nl) < 8:
            following_end = j
            break  # blank line
        # Check if it's a data L or G record (col6=' ', col7=' ', col8='L' or 'G')
        is_data_record = (nl[5] == ' ' and nl[6] == ' ' and nl[7] in ('L', 'G') and nl[0:5].strip())
        if is_data_record:
            following_end = j
            break
        following_cL.append((j, nl))
        following_end = j + 1

    has_E = any('cL E$' in l[1] for l in following_cL)
    has_T = any('cL T$' in l[1] for l in following_cL)
    has_J = any('cL J$' in l[1] for l in following_cL)
    
    if has_J:
        # Already expanded - skip
        continue
    
    # Determine the preceding context line (XREF line)
    prev_line = lines[idx - 1] if idx > 0 else ''
    
    if not has_E and not has_T and not following_cL:
        # Case A: no following cL comments
        case_counts['A'] += 1
        # Use full context from parent L-record through FLAG=b for uniqueness
        parent_idx = find_parent_data_line(lines, idx, 'L')
        old_str = build_context(lines, parent_idx, idx)
        # Replace FLAG line with J$ (keeping all parent lines before it)
        if parent_idx is not None:
            new_str = ''.join(lines[parent_idx:idx]) + J_LINE
        else:
            new_str = lines[idx-1] + J_LINE
        replacements.append({
            'case': 'flag_b_A',
            'line': idx + 1,
            'old': old_str,
            'new': new_str,
            'desc': f'FLAG=b case A (no comment) at line {idx+1}'
        })
    
    elif has_E and not has_T:
        # Case B: has E$ only
        case_counts['B'] += 1
        # Collect the E$ block
        e_lines = []
        other_after_e = []
        in_e_block = False
        for j, nl in following_cL:
            if 'cL E$' in nl:
                in_e_block = True
                e_lines.append(nl)
            elif in_e_block and ('cL2' in nl or '2cL' in nl or '3cL' in nl):
                e_lines.append(nl)
            elif in_e_block:
                in_e_block = False
                other_after_e.append(nl)
            else:
                other_after_e.append(nl)
        
        old_str = flag_line + ''.join(e_lines) + ''.join(other_after_e)
        new_str = ''.join(e_lines) + J_LINE + ''.join(other_after_e)
        replacements.append({
            'case': 'flag_b_B',
            'line': idx + 1,
            'old': old_str,
            'new': new_str,
            'desc': f'FLAG=b case B (has E$, no T$) at line {idx+1}'
        })
    
    elif has_E and has_T:
        # Case C: has E$ and T$
        case_counts['C'] += 1
        # Build: E$block + J$ + T$
        e_lines = []
        t_lines = []
        other_before_t = []
        phase = 'before_e'
        for j, nl in following_cL:
            if 'cL E$' in nl:
                phase = 'in_e'
                e_lines.append(nl)
            elif phase == 'in_e' and (nl.startswith(' 34CL2cL') or nl.startswith(' 34CL3cL')):
                e_lines.append(nl)
            elif 'cL T$' in nl:
                phase = 'in_t'
                t_lines.append(nl)
            elif phase == 'in_t' and (nl.startswith(' 34CL2cL') or nl.startswith(' 34CL3cL')):
                t_lines.append(nl)
            elif phase == 'in_e':
                phase = 'between'
                other_before_t.append(nl)
            else:
                other_before_t.append(nl)
        
        old_str = flag_line + ''.join(e_lines) + ''.join(other_before_t) + ''.join(t_lines)
        new_str = ''.join(e_lines) + ''.join(other_before_t) + J_LINE + ''.join(t_lines)
        replacements.append({
            'case': 'flag_b_C',
            'line': idx + 1,
            'old': old_str,
            'new': new_str,
            'desc': f'FLAG=b case C (has E$ and T$) at line {idx+1}'
        })
    
    else:
        # Case D: other
        case_counts['D'] += 1
        print(f"  Case D (other) at line {idx+1}: {[l[1][:50] for l in following_cL]}")
        old_str = prev_line + flag_line
        new_str = prev_line + J_LINE
        replacements.append({
            'case': 'flag_b_D',
            'line': idx + 1,
            'old': old_str,
            'new': new_str,
            'desc': f'FLAG=b case D (other) at line {idx+1}'
        })

print(f"Cases: {case_counts}")
print()

# =========================================================================
# FLAG=a L-record: just delete (all have detailed cL E$ already)
# =========================================================================
print("=== FLAG=a deletion ===")
flag_a_lines = []
for i, line in enumerate(lines):
    if line.startswith(' 34CLF L FLAG=a'):
        flag_a_lines.append(i)

for idx in flag_a_lines:
    flag_line = lines[idx]
    prev_line = lines[idx - 1] if idx > 0 else ''
    # Just delete the FLAG=a line
    old_str = prev_line + flag_line
    new_str = prev_line
    replacements.append({
        'case': 'flag_a_delete',
        'line': idx + 1,
        'old': old_str,
        'new': new_str,
        'desc': f'FLAG=a delete at line {idx+1}'
    })
    print(f"  Line {idx+1}: delete FLAG=a")

print()

# =========================================================================
# FLAG=AB G-records: add cG E$ and cG RI$ comments
# Strategy: Replace [FLAG=AB line] with cG E$ + cG RI$ 
# But for some, existing cG E,RI$ comment is already there
# =========================================================================
E_LINE_A  = pad80(" 34CL cG E$From {+32}S({+3}He,p|g)") + "\n"
RI_LINE_B = pad80(" 34CL cG RI$From {+32}S({+3}He,p|g)") + "\n"
assert len(E_LINE_A.rstrip('\n')) == 80 and len(RI_LINE_B.rstrip('\n')) == 80

print("=== FLAG=AB/A/B G-record expansion ===")

for i, line in enumerate(lines):
    m = re.match(r' 34CLF G FLAG=(A|B|AB)\s*$', line.rstrip())
    if not m:
        continue
    flags = m.group(1)
    
    # Check if this line is a "double" entry (FLAG=A followed immediately by FLAG=B)
    next_line = lines[i+1] if i+1 < len(lines) else ''
    prev_is_flagA = (i > 0 and re.match(r' 34CLF G FLAG=A\s*$', lines[i-1].rstrip()))
    
    # Check if there's already a cG E$ or cG RI$ or E,RI$ comment in the following cG block
    following_cG = []
    for j in range(i+1, min(i+15, len(lines))):
        nl = lines[j]
        if len(nl) < 8:
            break
        is_data = (nl[5] == ' ' and nl[6] == ' ' and nl[7] in ('L', 'G', 'B', 'E', 'D') and nl[0:5].strip())
        is_cont_type = nl[5] in ('F', 'S', 'B', 'X', '2', '3', '4', '5', '6', '7', '8', '9')
        if is_data:
            break
        following_cG.append(nl)
    
    has_E = any('cG E$' in l or 'E,RI$' in l or 'E,MR$' in l for l in following_cG)
    has_RI = any('cG RI$' in l or 'E,RI$' in l or ',RI$' in l for l in following_cG)
    
    # Determine what to add
    add_E = ('A' in flags) and not has_E
    add_RI = ('B' in flags) and not has_RI
    
    if not add_E and not add_RI:
        print(f"  Line {i+1}: FLAG={flags} - already has E$={has_E} RI$={has_RI} - SKIP (delete only)")
        parent_idx = find_parent_data_line(lines, i, 'G')
        old_str = build_context(lines, parent_idx, i)
        if parent_idx is not None:
            new_str = ''.join(lines[parent_idx:i])
        else:
            new_str = prev_line
        replacements.append({
            'case': f'flag_{flags}_delete_only',
            'line': i + 1,
            'old': old_str,
            'new': new_str,
            'desc': f'FLAG={flags} G-record (delete only, comment exists) at line {i+1}'
        })
    else:
        # Build new content to replace FLAG= line with
        new_content = ''
        if add_E:
            new_content += E_LINE_A
        if add_RI:
            new_content += RI_LINE_B
        parent_idx = find_parent_data_line(lines, i, 'G')
        old_str = build_context(lines, parent_idx, i)
        if parent_idx is not None:
            new_str = ''.join(lines[parent_idx:i]) + new_content
        else:
            new_str = prev_line + new_content
        replacements.append({
            'case': f'flag_{flags}_expand',
            'line': i + 1,
            'old': old_str,
            'new': new_str,
            'desc': f'FLAG={flags} G-record expand at line {i+1}'
        })
        print(f"  Line {i+1}: FLAG={flags} -> add E$={add_E}, RI$={add_RI}")

print()

# =========================================================================
# FLAG=C G-records: add cG E$ from (12C,pn/an)
# =========================================================================
E_LINE_C = pad80(" 34CL cG E$From {+24}Mg({+12}C,pn|g), {+27}Al({+12}C,|an|g).") + "\n"
assert len(E_LINE_C.rstrip('\n')) == 80

print("=== FLAG=C G-record expansion ===")
for i, line in enumerate(lines):
    if not line.startswith(' 34CLF G FLAG=C'):
        continue
    # Check for existing cG E$
    following_cG = []
    for j in range(i+1, min(i+15, len(lines))):
        nl = lines[j]
        if len(nl) < 8:
            break
        is_data = (nl[5] == ' ' and nl[6] == ' ' and nl[7] in ('L', 'G', 'B', 'E', 'D') and nl[0:5].strip())
        if is_data:
            break
        following_cG.append(nl)
    has_E = any('cG E$' in l for l in following_cG)
    
    parent_idx = find_parent_data_line(lines, i, 'G')
    old_str = build_context(lines, parent_idx, i)
    if has_E:
        print(f"  Line {i+1}: FLAG=C - already has E$ - delete only")
        new_str = ''.join(lines[parent_idx:i]) if parent_idx is not None else lines[i-1]
        replacements.append({
            'case': 'flag_C_delete_only',
            'line': i + 1,
            'old': old_str,
            'new': new_str,
            'desc': f'FLAG=C delete (E$ already present) at line {i+1}'
        })
    else:
        print(f"  Line {i+1}: FLAG=C - add E$")
        if parent_idx is not None:
            new_str = ''.join(lines[parent_idx:i]) + E_LINE_C
        else:
            new_str = lines[i-1] + E_LINE_C
        replacements.append({
            'case': 'flag_C_expand',
            'line': i + 1,
            'old': old_str,
            'new': new_str,
            'desc': f'FLAG=C expand (add E$) at line {i+1}'
        })

print()

# =========================================================================
# Verify: check for duplicate old_strings
# =========================================================================
old_strings = [r['old'] for r in replacements]
duplicates = [s for s in set(old_strings) if old_strings.count(s) > 1]
if duplicates:
    print(f"WARNING: {len(duplicates)} duplicate old_strings found!")
    for d in duplicates[:5]:
        print(f"  {repr(d[:80])}")
else:
    print("OK: All old_strings are unique.")

print(f"\nTotal replacements to make: {len(replacements)}")

# Save the replacements to a file for review
with open('.github/temp/flag_expansion_replacements.json', 'w', encoding='utf-8') as f:
    json.dump(replacements, f, indent=2, ensure_ascii=False)

print(f"Saved {len(replacements)} replacements to .github/temp/flag_expansion_replacements.json")
