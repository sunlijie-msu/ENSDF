"""Analyze FLAG= instances in Cl34_adopted.ens - READ ONLY"""
import re
from collections import Counter

with open('A34/Cl34/new/Cl34_adopted.ens', 'r', encoding='latin-1') as f:
    lines = f.readlines()

results = []
i = 0
while i < len(lines):
    line = lines[i]
    m = re.match(r'( 34CL)F (G|L) FLAG=(.+)\s*$', line)
    if m:
        flag_type = m.group(2)  # G or L
        flags = m.group(3).strip()
        line_no = i + 1
        # Find parent record (look backward)
        parent = None
        for j in range(i-1, max(i-20, -1), -1):
            pl = lines[j]
            if len(pl) < 8:
                continue
            col6 = pl[5]   # col 6, 0-indexed as [5]
            col8 = pl[7]   # col 8, 0-indexed as [7]
            # Data record: col6=' ', col8='L' or 'G', not a continuation marker
            if col6 == ' ' and col8 == flag_type and col6 not in ('F','B','S','X'):
                parent = (j+1, pl.rstrip())
                break
        # Find following cL/cG comment lines within same block
        following = []
        for j in range(i+1, min(i+30, len(lines))):
            nl = lines[j]
            if len(nl) < 8:
                following.append(nl.rstrip())
                continue
            col6 = nl[5]
            col8 = nl[7]
            # Stop if we hit a new data record (L or G) with col6=' '
            if col6 == ' ' and col8 in ('L', 'G') and nl[0:5].strip():
                break
            following.append(nl.rstrip())
        results.append({
            'line': line_no, 'type': flag_type, 'flags': flags,
            'parent': parent, 'following': following
        })
    i += 1

# Summary
flag_counts = Counter(r['flags'] for r in results)
print('=== FLAG COUNTS ===')
for f, n in sorted(flag_counts.items()):
    print(f'  FLAG={f}: {n} entries')

# FLAG=a (L-records)
print('\n=== FLAG=a (L-records) ===')
for r in results:
    if r['flags'] == 'a' and r['type'] == 'L':
        has_E = any('cL E$' in fc or ' cL2' in fc for fc in r['following'])
        print(f'  Line {r["line"]}: parent line {r["parent"][0] if r["parent"] else "?"}, has_cL_E$={has_E}')
        if r['parent']:
            print(f'    Parent: {r["parent"][1][:40]}')

# FLAG=A/B/AB (G-records)
print('\n=== FLAG=A/B/AB G-records ===')
for r in results:
    if r['type'] == 'G' and r['flags'] in ('A','B','AB'):
        has_E = any(('cG E$' in fc or 'E,RI$' in fc or ('cG' in fc and 'E,' in fc and '$' in fc)) for fc in r['following'])
        has_RI = any(('cG RI$' in fc or 'E,RI$' in fc or (',RI$' in fc)) for fc in r['following'])
        parent_brief = r['parent'][1][9:25].strip() if r['parent'] else '?'
        print(f'  Line {r["line"]}: FLAG={r["flags"]}, G~"{parent_brief}", has_E$={has_E}, has_RI$={has_RI}')

# FLAG=C (G-records)
print('\n=== FLAG=C (G-records): 4 entries ===')
for r in results:
    if r['type'] == 'G' and r['flags'] == 'C':
        has_E = any('cG E$' in fc for fc in r['following'])
        parent_brief = r['parent'][1][9:25].strip() if r['parent'] else '?'
        print(f'  Line {r["line"]}: FLAG=C, G~"{parent_brief}", has_cG_E$={has_E}')

# FLAG=b (L-records)
b_records = [r for r in results if r['flags'] == 'b' and r['type'] == 'L']
print(f'\n=== FLAG=b L-records: {len(b_records)} total ===')
has_J_count = 0
no_J_count = 0
for r in b_records:
    has_J = any('cL J$' in fc for fc in r['following'])
    has_E = any('cL E$' in fc for fc in r['following'])
    has_T = any('cL T$' in fc for fc in r['following'])
    if has_J:
        has_J_count += 1
    else:
        no_J_count += 1

print(f'  Already have cL J$: {has_J_count}')
print(f'  Need cL J$ added: {no_J_count}')

# Show all FLAG=b with no J$
print('\n  FLAG=b L-records WITHOUT existing cL J$ (first 30):')
shown = 0
for r in b_records:
    has_J = any('cL J$' in fc for fc in r['following'])
    has_E = any('cL E$' in fc for fc in r['following'])
    has_T = any('cL T$' in fc for fc in r['following'])
    if not has_J and shown < 30:
        parent_E = r['parent'][1][9:25].strip() if r['parent'] else '?'
        print(f'    Line {r["line"]}: L~"{parent_E}", has_E$={has_E}, has_T$={has_T}')
        shown += 1

# Show FLAG=b WITH existing J$
print('\n  FLAG=b L-records WITH existing cL J$:')
for r in b_records:
    has_J = any('cL J$' in fc for fc in r['following'])
    if has_J:
        parent_E = r['parent'][1][9:25].strip() if r['parent'] else '?'
        j_lines = [fc for fc in r['following'] if 'cL J$' in fc]
        print(f'    Line {r["line"]}: L~"{parent_E}", J$: {j_lines[0][:60] if j_lines else "?"}')
