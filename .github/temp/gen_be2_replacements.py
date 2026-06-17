"""Generate exact replacements for inserting B(E2) cG lines after existing cG comments."""
import re

ENSDF_FILE = r"d:\X\ND\ENSDF\XUNDL\2026MAAA_CT11001_141Sm.ens"

BE2_DATA = {
    "486.7":  ("0.46", "0.04", "0.04", False),
    "792.4":  ("0.30", "0.02", "0.02", False),
    "1044.0": ("0.22", "0.02", "0.02", False),
    "1239.5": ("0.09", "0.01", "0.01", False),
    "1468.0": ("0.02", None, None, True),
    "1205.2": ("0.05", None, None, True),
    "457.2":  ("0.48", "0.08", "0.07", False),
    "748.2":  ("0.47", "0.04", "0.04", False),
    "841.4":  ("0.42", "0.05", "0.05", False),
    "938.3":  ("0.35", "0.03", "0.03", False),
    "1040.2": ("0.26", "0.03", "0.02", False),
    "1164.1": ("0.17", None, None, True),
    "679.9":  ("0.25", "0.04", "0.03", False),
    "783.7":  ("0.27", "0.04", "0.03", False),
    "918.8":  ("0.26", "0.03", "0.03", False),
    "1108.5": ("0.24", "0.03", "0.03", False),
    "1328.4": ("0.20", None, None, True),
}

def make_be2(val, up, low, is_limit):
    if is_limit:
        return f"141SM cG $B(E2)|_=>{val} e{{+2}}b{{+2}} (2026MaAA).".ljust(80)
    elif up == low:
        digits = up.replace('0.', '').lstrip('0') or '0'
        return f"141SM cG $B(E2)|_={val} e{{+2}}b{{+2}} {{I{digits}}} (2026MaAA).".ljust(80)
    else:
        up_d = up.replace('0.', '').lstrip('0') or '0'
        low_d = low.replace('0.', '').lstrip('0') or '0'
        return f"141SM cG $B(E2)|_={val} e{{+2}}b{{+2}} {{I+{up_d}-{low_d}}} (2026MaAA).".ljust(80)

with open(ENSDF_FILE, 'r') as f:
    lines = f.readlines()

# For each target gamma, find G-record + existing cG lines
replacements = []

for eg in BE2_DATA:
    val, up, low, is_limit = BE2_DATA[eg]
    be2_line = make_be2(val, up, low, is_limit)
    
    # Find G-record
    for i, line in enumerate(lines):
        raw = line.rstrip('\n').rstrip('\r')
        if len(raw) < 37:
            continue
        if raw[7] != 'G' or raw[6] != ' ':
            continue
        e_field = raw[9:19].strip()
        if e_field != eg:
            continue
        
        # Found the G-record. Find all existing cG lines
        cg_start = i
        cg_end = i  # include G-record itself
        for j in range(i + 1, min(i + 15, len(lines))):
            check = lines[j].rstrip('\n').rstrip('\r')
            if len(check) >= 9 and check[6] == 'c' and check[7] == 'G':
                cg_end = j
            elif len(check) >= 9 and check[7] == 'c' and check[8] == 'G':
                # continuation like 2cG
                cg_end = j
            else:
                break
        
        # Build old_string (G-record + existing cG lines)
        old_lines = []
        for k in range(i, cg_end + 1):
            old_lines.append(lines[k].rstrip('\n').rstrip('\r'))
        old_str = '\n'.join(old_lines)
        
        # Build new_string (add B(E2) cG line after)
        new_lines = old_lines + [be2_line]
        new_str = '\n'.join(new_lines)
        
        print(f"EG={eg:>8s}: G at line {i+1}, cG lines {i+1}-{cg_end+1}")
        if cg_end > i:
            print(f"  Existing cG: {lines[cg_end].rstrip()}")
        print(f"  New B(E2):   {be2_line}")
        print()
        
        replacements.append({
            'eg': eg,
            'old': old_str,
            'new': new_str,
            'line': i + 1,
            'be2': be2_line,
        })
        break

print(f"Total: {len(replacements)} replacements")

# Write to JSON for use by multi_replace
import json
with open(r'd:\X\ND\ENSDF\.github\temp\be2_replacements.json', 'w') as f:
    json.dump(replacements, f, indent=2)
print("Saved to be2_replacements.json")
