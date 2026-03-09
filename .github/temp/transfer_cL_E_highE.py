"""
Insert remaining cL E$ blocks (high-energy levels) from adp into ens.
Uses 2.0 keV tolerance for energy matching. Skips if already has cL E$.
"""
import re

ADP_FILE = r'd:\X\ND\ENSDF\A34\Cl34\raw\1977DA02_1983WA27.adp'
ENS_FILE = r'd:\X\ND\ENSDF\A34\Cl34\new\Cl34_33s_p_g.ens'

TOLERANCE_KEV = 2.0

def is_L_record(line):
    return (len(line) >= 8 and line[5] == ' ' and line[6] == ' ' and line[7] == 'L')

def is_cL_E(line):
    return (len(line) >= 11 and line[6] == 'c' and line[7] == 'L' and line[9:11] == 'E$')

def is_cL_cont(line):
    return (len(line) >= 8 and line[5] in '23456789' and line[6] == 'c' and line[7] == 'L')

def get_L_energy(line):
    return line[9:19].strip()

# Parse adp
with open(ADP_FILE, encoding='utf-8') as f:
    adp_lines = f.readlines()

adp_blocks = []
i = 0
while i < len(adp_lines):
    line = adp_lines[i].rstrip('\n')
    if is_L_record(line):
        energy = get_L_energy(line)
        j = i + 1
        cL_E_lines = []
        if j < len(adp_lines) and is_cL_E(adp_lines[j].rstrip('\n')):
            cL_E_lines.append(adp_lines[j].rstrip('\n'))
            j += 1
            while j < len(adp_lines) and is_cL_cont(adp_lines[j].rstrip('\n')):
                cL_E_lines.append(adp_lines[j].rstrip('\n'))
                j += 1
        if cL_E_lines:
            adp_blocks.append((energy, cL_E_lines))
    i += 1

print(f"Total adp cL E$ blocks: {len(adp_blocks)}")

# Parse ens
with open(ENS_FILE, encoding='utf-8') as f:
    ens_lines = f.readlines()

ens_L_positions = {}
for idx, line in enumerate(ens_lines):
    raw = line.rstrip('\n')
    if is_L_record(raw):
        energy = get_L_energy(raw)
        ens_L_positions[energy] = idx

def find_ens_L(adp_energy):
    if adp_energy in ens_L_positions:
        return ens_L_positions[adp_energy]
    try:
        adp_val = float(adp_energy)
    except ValueError:
        return None
    best_idx = None
    best_diff = TOLERANCE_KEV
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

def ens_has_cL_E_after_L(L_idx):
    j = L_idx + 1
    while j < len(ens_lines):
        raw = ens_lines[j].rstrip('\n')
        if is_L_record(raw):
            return False
        if is_cL_E(raw):
            return True
        if raw.strip():
            j += 1
            continue
        break
    return False

# Find blocks to insert (only those not already present)
insertions = []  # (L_idx_in_ens, adp_energy, ens_energy, cL_E_lines)
skipped = []
not_found = []

for adp_energy, cL_lines in adp_blocks:
    L_idx = find_ens_L(adp_energy)
    if L_idx is None:
        not_found.append(adp_energy)
        continue
    ens_energy = get_L_energy(ens_lines[L_idx].rstrip('\n'))
    if ens_has_cL_E_after_L(L_idx):
        skipped.append((adp_energy, ens_energy))
        continue
    insertions.append((L_idx, adp_energy, ens_energy, cL_lines))

print(f"Already present (skip): {len(skipped)}")
print(f"Not in ens: {len(not_found)}")
print(f"To insert: {len(insertions)}")
for L_idx, ae, ee, lines in sorted(insertions, key=lambda x: x[0]):
    diff = abs(float(ae) - float(ee))
    print(f"  adp L {ae:12s} -> ens L {ee:12s} (diff={diff:.2f}): {len(lines)} lines")

# Apply insertions in reverse order to preserve positions
insertions_sorted = sorted(insertions, key=lambda x: x[0], reverse=True)

with open(ENS_FILE, encoding='utf-8') as f:
    content = f.readlines()

total_lines_inserted = 0
for L_idx, adp_energy, ens_energy, cL_lines in insertions_sorted:
    # Insert right after the L record
    insert_pos = L_idx + 1
    padded = [line.ljust(80)[:80] + '\n' for line in cL_lines]
    content[insert_pos:insert_pos] = padded
    total_lines_inserted += len(padded)
    print(f"  Inserted {len(padded)} line(s) after L {ens_energy} (adp: {adp_energy})")

with open(ENS_FILE, 'w', encoding='utf-8') as f:
    f.writelines(content)

print(f"\nDone. {len(insertions)} blocks, {total_lines_inserted} lines inserted.")
if not_found:
    print(f"Not found in ens: {not_found}")
