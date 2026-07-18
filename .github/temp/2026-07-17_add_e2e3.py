"""Add E2 and E3 columns to revised Table IV, sourced from original file."""

with open('d:/X/ND/ENSDF/XUNDL/2026OSAA_CT11035_152Gd_Table_IV.md', 'r') as f:
    orig = f.readlines()
with open('d:/X/ND/ENSDF/XUNDL/2026OSAA_CT11035_152Gd_Table_IV_revised.md', 'r') as f:
    rev = f.readlines()

def parse_inner(line):
    """Return list of inner cell contents (pipe-delimited, stripped)."""
    parts = [p.strip() for p in line.split('|')]
    return parts[1:-1]  # strip leading/trailing empty

# Build lookup from original: (E, g1, g2) -> (E2, E3)
orig_lookup = {}
for l in orig:
    s = l.strip()
    if not s.startswith('| '): continue
    if '$' in s or '---' in s or ':' in s: continue
    inner = parse_inner(l)
    if len(inner) < 8: continue
    # Original: [E1, Eg1, Eg2, A0, A2, A4, E2, E3, J1, J2, J3, d1]
    key = (inner[0], inner[1], inner[2])
    e2 = inner[6] if len(inner) > 6 else ''
    e3 = inner[7] if len(inner) > 7 else ''
    orig_lookup[key] = (e2, e3)

print(f"Lookup entries built: {len(orig_lookup)}")

# Process revised file
output = []
data_count = 0
for l in rev:
    s = l.strip()
    
    # Header line
    if '$A_4$' in s and '$J_1$' in s and '$E_2$' not in s:
        # Insert E2/E3 before J1
        l = l.replace('| $J_1$', '| $E_2$ | $E_3$ | $J_1$')
        output.append(l)
        continue
    
    # Separator line
    if ':---' in s and 'E_2' not in s:
        # Check if it has 10 separators (for 10 columns)
        sep_count = s.count(':---')
        if sep_count == 10:
            l = l.replace('| :--- | :--- | :--- |', '| :--- | :--- | :--- | :--- | :--- |')
            # More precise: insert two :--- after the 6th one
            parts = l.split('|')
            # Insert at position 7 (0-indexed, after A4 separator)
            parts.insert(7, ' :--- ')
            parts.insert(8, ' :--- ')
            l = '|'.join(parts)
        output.append(l)
        continue
    
    # Data rows
    if s.startswith('| ') and not '$' in s and '---' not in s:
        inner = parse_inner(l)
        if len(inner) >= 3:
            key = (inner[0], inner[1], inner[2])
            if key in orig_lookup:
                e2, e3 = orig_lookup[key]
                # Insert E2, E3 after A4 (index 5, which is position 6 in inner list)
                # inner indices: 0=E, 1=g1, 2=g2, 3=A0, 4=A2, 5=A4, 6=J1, 7=J2, 8=J3, 9=d1
                inner.insert(6, e2)
                inner.insert(7, e3)
                # Rebuild line: pad each cell with space
                cells = [''] + [' ' + c + ' ' for c in inner] + ['']
                l = '|'.join(cells) + '\n'
                data_count += 1
            else:
                print(f"WARNING: Key not found in original: {key}")
        output.append(l)
        continue
    
    # Non-data lines (title, blank)
    output.append(l)

print(f"Data rows updated: {data_count}")

# Verify
test = ''.join(output)
lines = test.split('\n')
data_lines = [l for l in lines if l.strip().startswith('| ') and not '$' in l and '---' not in l]
print(f"Output data lines: {len(data_lines)}")

# Write back
with open('d:/X/ND/ENSDF/XUNDL/2026OSAA_CT11035_152Gd_Table_IV_revised.md', 'w') as f:
    f.write(''.join(output))

print("Done. Revised file updated with E2/E3 columns.")
