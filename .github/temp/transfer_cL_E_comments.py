"""
Transfer cL E$ comments from 1977DA02_1983WA27.adp to Cl34_33s_p_g.ens.
Insert right after the matching L record, before any existing cL/cG lines.
"""

ADP_FILE = r'd:\X\ND\ENSDF\A34\Cl34\raw\1977DA02_1983WA27.adp'
ENS_FILE = r'd:\X\ND\ENSDF\A34\Cl34\new\Cl34_33s_p_g.ens'

def pad80(s):
    s = s.rstrip()
    if len(s) > 80:
        raise ValueError(f"Line exceeds 80 chars: [{s}]")
    return s.ljust(80)

def is_L_record(line):
    """True if this is an L-record (data record, not comment)."""
    return (len(line) >= 8 and
            line[5] == ' ' and  # CONT blank = first record
            line[6] == ' ' and  # col 7 blank
            line[7] == 'L')     # TYPE = L

def is_cL_E(line):
    """True if this is a cL E$ comment line (first record or continuation)."""
    if len(line) < 11:
        return False
    # First record: cols 7='c', cols 8='L', cols 10='E', cols 11='$'
    if line[6] == 'c' and line[7] == 'L' and line[9:11] == 'E$':
        return True
    return False

def is_cL_cont(line):
    """True if this is a continuation of a cL line (e.g., 2cL, 3cL)."""
    if len(line) < 8:
        return False
    return (line[5] in '23456789' and line[6] == 'c' and line[7] == 'L')

def get_L_energy(line):
    """Extract numeric energy string from cols 10-19 of L record."""
    return line[9:19].strip()

# ─────────────────────────────────────────────────────────
# Step 1: Parse adp - collect (energy_str, [cL_E lines]) blocks
# ─────────────────────────────────────────────────────────
with open(ADP_FILE, encoding='utf-8') as f:
    adp_lines = f.readlines()

adp_blocks = []  # list of (energy_str, [raw_cL_E_lines])
current_L_energy = None
i = 0
while i < len(adp_lines):
    line = adp_lines[i].rstrip('\n')
    if is_L_record(line):
        current_L_energy = get_L_energy(line)
        # Look ahead for immediately following cL E$ lines
        j = i + 1
        cL_E_lines = []
        if j < len(adp_lines) and is_cL_E(adp_lines[j].rstrip('\n')):
            cL_E_lines.append(adp_lines[j].rstrip('\n'))
            j += 1
            # Collect continuation lines (2cL, 3cL) immediately following
            while j < len(adp_lines) and is_cL_cont(adp_lines[j].rstrip('\n')):
                cL_E_lines.append(adp_lines[j].rstrip('\n'))
                j += 1
        if cL_E_lines:
            adp_blocks.append((current_L_energy, cL_E_lines))
    i += 1

print(f"Parsed {len(adp_blocks)} cL E$ blocks from adp:")
for energy, lines in adp_blocks:
    print(f"  L {energy!r:12s} → {len(lines)} line(s): [{lines[0].rstrip()[:60]}...]")

# ─────────────────────────────────────────────────────────
# Step 2: Parse ens - collect L record positions and what follows
# ─────────────────────────────────────────────────────────
with open(ENS_FILE, encoding='utf-8') as f:
    ens_lines = f.readlines()

# Build dict: energy_str -> line_index of L record in ens (0-based)
ens_L_positions = {}
for idx, line in enumerate(ens_lines):
    raw = line.rstrip('\n')
    if is_L_record(raw):
        energy = get_L_energy(raw)
        ens_L_positions[energy] = idx

def find_ens_L(adp_energy):
    """Find matching L record in ens by energy. Try exact first, then ±1 decimal digit."""
    if adp_energy in ens_L_positions:
        return ens_L_positions[adp_energy]
    # Fuzzy: compare as float with tolerance 0.2 keV
    try:
        adp_val = float(adp_energy)
    except ValueError:
        return None
    best_idx = None
    best_diff = 0.25
    for ens_energy, idx in ens_L_positions.items():
        try:
            ens_val = float(ens_energy)
        except ValueError:
            continue
        diff = abs(adp_val - ens_val)
        if diff < best_diff:
            best_diff = diff
            best_idx = idx
    return best_idx

def ens_already_has_cL_E(L_idx):
    """Check if the L record at L_idx already has a cL E$ as its first following comment."""
    j = L_idx + 1
    while j < len(ens_lines):
        raw = ens_lines[j].rstrip('\n')
        if is_L_record(raw):
            break  # hit next L record
        if is_cL_E(raw):
            return True
        # If first non-empty thing after L is NOT cL E$ (e.g. it's a G record or cL T$), stop
        if raw.strip():
            return False
        j += 1
    return False

# ─────────────────────────────────────────────────────────
# Step 3: Determine what needs to be inserted
# ─────────────────────────────────────────────────────────
insertions = []  # list of (insert_after_line_idx, [padded_lines_to_insert])

for adp_energy, cL_lines in adp_blocks:
    L_idx = find_ens_L(adp_energy)
    if L_idx is None:
        print(f"  WARNING: No matching L record in ens for adp energy {adp_energy!r}")
        continue
    ens_energy = get_L_energy(ens_lines[L_idx].rstrip('\n'))
    if ens_already_has_cL_E(L_idx):
        print(f"  SKIP  L {adp_energy!r:12s} (ens L {ens_energy!r}) already has cL E$")
        continue
    # Pad all lines to 80
    padded = []
    for cl in cL_lines:
        padded.append(pad80(cl) + '\n')
    # Insert AFTER L record (= insert before line L_idx+1)
    # But we want to insert BEFORE existing cL lines that follow the L record
    # Find the right insert position: right after the L record line
    insert_pos = L_idx + 1
    insertions.append((insert_pos, padded, adp_energy, ens_energy))

# Sort insertions in reverse order of line index so we can insert without shifting positions
insertions.sort(key=lambda x: x[0], reverse=True)

print(f"\n{len(insertions)} insertions to perform:")
for pos, lines, ae, ee in reversed(insertions):
    print(f"  Insert after ens line {pos} (L {ee!r}, adp energy {ae!r}): {len(lines)} line(s)")

# ─────────────────────────────────────────────────────────
# Step 4: Apply insertions
# ─────────────────────────────────────────────────────────
modified = list(ens_lines)
for insert_pos, padded_lines, ae, ee in insertions:
    modified[insert_pos:insert_pos] = padded_lines

# Write back
with open(ENS_FILE, 'w', encoding='utf-8') as f:
    f.writelines(modified)

print(f"\nDone. Inserted {sum(len(p) for _, p, _, _ in insertions)} lines total.")
print(f"ENS file updated: {ENS_FILE}")
