"""
Verify every cL E$ block from adp is also present in ens.
"""
import re

ADP_FILE = r'd:\X\ND\ENSDF\A34\Cl34\raw\1977DA02_1983WA27.adp'
ENS_FILE = r'd:\X\ND\ENSDF\A34\Cl34\new\Cl34_33s_p_g.ens'

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
    best_diff = 2.0  # wider tolerance for verification
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
    """Scan all comment/record lines under this L until next L record."""
    j = L_idx + 1
    while j < len(ens_lines):
        raw = ens_lines[j].rstrip('\n')
        if is_L_record(raw):
            return False
        if is_cL_E(raw):
            return True
        j += 1
    return False

print("Completeness check: adp cL E$ blocks vs ens")
missing = []
for adp_energy, cL_lines in adp_blocks:
    L_idx = find_ens_L(adp_energy)
    if L_idx is None:
        ens_energy = 'NOT IN ENS'
        has_cL = False
        missing.append((adp_energy, ens_energy, 'NOT IN ENS'))
        continue
    ens_energy = get_L_energy(ens_lines[L_idx].rstrip('\n'))
    has_cL = ens_has_cL_E_after_L(L_idx)
    if not has_cL:
        missing.append((adp_energy, ens_energy, 'MISSING cL E$'))

if missing:
    print("PROBLEMS FOUND:")
    for ae, ee, msg in missing:
        print(f"  adp L {ae} -> ens L {ee}: {msg}")
else:
    print("ALL PASS: Every adp cL E$ block has a matching entry in ens.")

print(f"\nTotal adp cL E$ blocks: {len(adp_blocks)}")
print(f"Missing count: {len(missing)}")
