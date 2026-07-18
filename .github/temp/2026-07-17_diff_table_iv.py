import re

# Read both files
with open('d:/X/ND/ENSDF/XUNDL/2026OSAA_CT11035_152Gd_Table_IV.md', 'r') as f:
    orig = f.read()
with open('d:/X/ND/ENSDF/XUNDL/2026OSAA_CT11035_152Gd_Table_IV_revised.md', 'r') as f:
    rev = f.read()

def parse_table(text):
    rows = []
    for line in text.split('\n'):
        line = line.strip()
        if line.startswith('|') and line.endswith('|') and not line.startswith('| $') and not line.startswith('| :'):
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 3:
                rows.append(parts[1:-1])
    return rows

orig_rows = parse_table(orig)
rev_rows = parse_table(rev)

print(f"Orig rows: {len(orig_rows)}, Rev rows: {len(rev_rows)}")

# Original: E1, Eg1, Eg2, A0, A2, A4, E2, E3, J1, J2, J3, d1
# Revised:  Ei, Eg1, Eg2, A0, A2, A4, J1, J2, J3, d1

# Compare ignoring E2, E3
diffs = []
for i in range(min(len(orig_rows), len(rev_rows))):
    o = orig_rows[i]
    r = rev_rows[i]
    changes = {}
    # E1 vs Ei (both col 0)
    if o[0] != r[0]:
        changes['E_level'] = (o[0], r[0])
    if o[1] != r[1]:
        changes['Eg1'] = (o[1], r[1])
    if o[2] != r[2]:
        changes['Eg2'] = (o[2], r[2])
    if o[3] != r[3]:
        changes['A0'] = (o[3], r[3])
    if o[4] != r[4]:
        changes['A2'] = (o[4], r[4])
    if o[5] != r[5]:
        changes['A4'] = (o[5], r[5])
    if o[8] != r[6]:
        changes['J1'] = (o[8], r[6])
    if o[9] != r[7]:
        changes['J2'] = (o[9], r[7])
    if o[10] != r[8]:
        changes['J3'] = (o[10], r[8])
    if o[11] != r[9]:
        changes['d1'] = (o[11], r[9])
    if changes:
        key = f"E={o[0]} g1={o[1]} g2={o[2]}"
        diffs.append((i, key, changes))

print(f"\n{len(diffs)} rows changed (excluding E2/E3)\n")
for idx, key, changes in diffs:
    print(f"Row {idx+1}: {key}")
    for col, (old, new) in sorted(changes.items()):
        print(f"  {col}: '{old}' -> '{new}'")
    print()

print("=== Summary ===")
col_changes = {}
for _, _, changes in diffs:
    for col in changes:
        col_changes[col] = col_changes.get(col, 0) + 1
for col, count in sorted(col_changes.items(), key=lambda x: -x[1]):
    print(f"  {col}: {count}")
