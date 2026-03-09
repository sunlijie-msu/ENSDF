"""Final verification: check if each Other: RI value exists anywhere in mrg data."""

import re

ADP_FILE = r'd:\X\ND\ENSDF\A34\Cl34\raw\1977DA02_1983WA27.adp'
MRG_FILE = r'd:\X\ND\ENSDF\A34\Cl34\raw\1977DA02_1983WA27.mrg'

def extract_other_numeric(cg_line):
    """Extract numeric part from Other: VALUE, e.g., extract '3.1' from '<3.1'."""
    match = re.search(r'\. Other:\s*([<>]?)(\d+\.?\d*)', cg_line)
    if match:
        prefix = match.group(1)  # '<' or '>' or ''
        val = match.group(2)
        return (prefix + val).strip()
    return None

def get_all_mrg_ri_values():
    """Get all RI values from mrg."""
    mrg_lines = open(MRG_FILE, encoding='utf-8').readlines()
    ri_values = set()
    
    for ml in mrg_lines:
        l = ml.rstrip()
        if ' 34CL  G' in l and len(l) > 67:
            ri = l[60:68].strip()
            if ri and not ri.startswith('*'):
                ri_values.add(ri)
    
    return ri_values

adp_lines = open(ADP_FILE, encoding='utf-8').readlines()
mrg_ri_set = get_all_mrg_ri_values()

print(f"MRG RI values available: {len(mrg_ri_set)}")
print(f"Sample: {sorted(list(mrg_ri_set))[:15]}\n")

# Check adp lines
other_lines = []
for i, line in enumerate(adp_lines):
    if 'Other' in line and ('from 1977Da02' in line or 'from 1983Wa27' in line):
        # Get preceding L
        l_energy = None
        for j in range(i-1, max(i-20, -1), -1):
            if '34CL  L' in adp_lines[j]:
                try:
                    l_energy = float(adp_lines[j][9:19].strip())
                    break
                except:
                    pass
        if l_energy is not None and l_energy <= 6136:
            other_lines.append((i+1, l_energy, line))

print(f"Checking {len(other_lines)} Other: lines (L <= 6136)\n")

not_found = []
for (lnum, le, cg_line) in other_lines:
    val = extract_other_numeric(cg_line)
    if val is None:
        print(f"SKIP L{lnum}: Could not parse")
        continue
    
    # check if val is in mrg_ri_set (exact match)
    if val in mrg_ri_set:
        pass  # OK
    else:
        # maybe it's a float/int mismatch, try normalizing
        found = False
        for mrg_val in mrg_ri_set:
            try:
                if abs(float(val) - float(mrg_val)) < 0.01:
                    found = True
                    break
            except:
                pass
        if not found:
            not_found.append((lnum, val, cg_line.rstrip()))
            print(f"NOT FOUND L{lnum}: '{val}' {cg_line.rstrip()}")

print(f"\n{'='*70}")
if not not_found:
    print(f"SUCCESS: All {len(other_lines)} values found in mrg or close match ✓")
else:
    print(f"SUSPICIOUS: {len(not_found)} values not found in mrg")
    for ln, v, line in not_found:
        print(f"  L{ln}: '{v}'")
