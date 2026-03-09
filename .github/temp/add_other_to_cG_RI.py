"""
For every 'cG RI$from 1977Da02' or 'cG RI$from 1983Wa27' with no 'Other:'
in the adp, look up the OTHER dataset's gamma intensity in the mrg
and append '. Other: value (dataset).' to the comment line.

MRG format (0-indexed):
  Dataset lines: chars 22-34 = dataset tag (e.g. '1977DA02--->A')
  ENSDF G record starts at char 40
    E  : chars 49-58 (cols 10-19)
    RI : chars 62-68 (cols 23-29)
    DRI: chars 69-70 (cols 30-31)
"""

ADP_FILE = r'd:\X\ND\ENSDF\A34\Cl34\raw\1977DA02_1983WA27.adp'
MRG_FILE = r'd:\X\ND\ENSDF\A34\Cl34\raw\1977DA02_1983WA27.mrg'

TOLERANCE = 2.0  # keV

# ── 1. Parse mrg ─────────────────────────────────────────────────────────────
# Build: mrg_gammas[ adopted_gamma_E_str ] = { 'A': (ri, dri), 'B': (ri, dri) }
# We keep a list of entries per bucket in case of energy collisions.
# Structure: mrg_gamma_list = [ (adopted_E_float, {'A': (ri,dri), 'B': (ri,dri)}) ]

# Verified mrg absolute column positions (NUCID starts at pos 39 in mrg lines):
#   RI  : mrg positions 60-67 (8 chars = cols 22-29 relative to NUCID start)
#   DRI : mrg positions 68-69 (2 chars = cols 30-31 relative to NUCID start)
#   E   : mrg positions 48-57 (10 chars = cols 10-19 relative to NUCID start)
# NUCID leading space is at pos 39; '34CL' is at positions 40-43.

def parse_mrg_dataset_line(line):
    """Return (dataset_letter, ri, dri) or None if not a dataset gamma line."""
    # Must have dataset tag at pos 22 and ' 34CL  G' at pos 39 (NUCID leading space)
    if len(line) < 72:
        return None
    tag = line[22:35]
    if '--->A' in tag:
        letter = 'A'
    elif '--->B' in tag:
        letter = 'B'
    else:
        return None
    # Check for G record: NUCID starts at pos 39 (' '), type 'G' at pos 46
    if len(line) < 47 or line[46] != 'G':
        return None
    # Also confirm it's a G record, not L
    if line[39:47] != ' 34CL  G':
        return None
    # Extract RI and DRI (verified positions from column debug)
    ri  = line[60:68].strip()
    dri = line[68:70].strip()
    return letter, ri, dri

def parse_mrg_gamma_header(line):
    """Return adopted gamma energy as float, or None."""
    if not line.startswith(' GAMMA-'):
        return None
    # NUCID starts at pos 39; E field at pos 48-57
    idx = line.find(' 34CL  G')
    if idx < 0:
        return None
    # E field: offset 9 from NUCID start
    e_start = idx + 9
    e_str = line[e_start : e_start + 10].strip()
    try:
        return float(e_str)
    except ValueError:
        return None

mrg_lines = open(MRG_FILE, encoding='utf-8').readlines()

# Parse in one pass
mrg_gamma_list = []  # list of (adopted_E_float, {dataset_letter: (ri, dri)})
current_gamma_E = None
current_datasets = {}

for raw in mrg_lines:
    line = raw.rstrip('\n')
    if line.startswith(' GAMMA-'):
        # save prev gamma if any
        if current_gamma_E is not None and current_datasets:
            mrg_gamma_list.append((current_gamma_E, dict(current_datasets)))
        e = parse_mrg_gamma_header(line)
        current_gamma_E = e
        current_datasets = {}
    elif line.startswith(' LEVEL') or line.startswith('-----'):
        # possibly save
        if current_gamma_E is not None and current_datasets:
            mrg_gamma_list.append((current_gamma_E, dict(current_datasets)))
        current_gamma_E = None
        current_datasets = {}
    else:
        result = parse_mrg_dataset_line(line)
        if result and current_gamma_E is not None:
            letter, ri, dri = result
            current_datasets[letter] = (ri, dri)

# last entry
if current_gamma_E is not None and current_datasets:
    mrg_gamma_list.append((current_gamma_E, dict(current_datasets)))

print(f"Parsed {len(mrg_gamma_list)} gamma entries from mrg")

def find_mrg_gamma(adp_e_float):
    """Return the mrg entry (adopted_E, datasets_dict) closest to adp_e_float within TOLERANCE."""
    best = None
    best_diff = TOLERANCE
    for (mrg_e, ds) in mrg_gamma_list:
        diff = abs(adp_e_float - mrg_e)
        if diff < best_diff:
            best_diff = diff
            best = (mrg_e, ds)
    return best  # None if no match within tolerance

def format_other(ri, dri, dataset_name):
    """Format the 'Other: ...' string."""
    if not ri:
        return None  # no RI data, skip
    if dri == 'LT':
        return f'. Other: <{ri} ({dataset_name}).'
    elif dri == 'GT':
        return f'. Other: >{ri} ({dataset_name}).'
    elif dri:
        # integer uncertainty
        return f'. Other: {ri} {{I{dri}}} ({dataset_name}).'
    else:
        return f'. Other: {ri} ({dataset_name}).'

# ── 2. Process adp ───────────────────────────────────────────────────────────
adp_lines = open(ADP_FILE, encoding='utf-8').readlines()

def is_G_record(line):
    return len(line) >= 8 and line[5] == ' ' and line[6] == ' ' and line[7] == 'G'

def get_G_energy(line):
    return line[9:19].strip()

changes = []  # list of (line_idx_0based, old_line, new_line)

prev_G_energy = None
prev_G_line_idx = None

for i, raw in enumerate(adp_lines):
    line = raw.rstrip('\n')
    
    if is_G_record(line):
        prev_G_energy = get_G_energy(line)
        prev_G_line_idx = i
        continue
    
    # Check for plain 'cG RI$from' without 'Other'
    if ('cG RI$from 1977Da02' in line or 'cG RI$from 1983Wa27' in line) and 'Other' not in line:
        if prev_G_energy is None:
            print(f"  WARN: No preceding G record at line {i+1}")
            continue
        
        # Determine source and other dataset
        if 'from 1977Da02' in line:
            source_letter = 'A'
            other_letter  = 'B'
            other_name    = '1983Wa27'
        else:
            source_letter = 'B'
            other_letter  = 'A'
            other_name    = '1977Da02'
        
        try:
            adp_e = float(prev_G_energy)
        except ValueError:
            print(f"  WARN: Non-numeric G energy '{prev_G_energy}' at adp line {i+1}")
            continue
        
        mrg_entry = find_mrg_gamma(adp_e)
        if mrg_entry is None:
            # No mrg entry within tolerance → no other data → skip
            continue
        
        mrg_e, ds = mrg_entry
        if other_letter not in ds:
            # Other dataset not measured → no Other: to add
            continue
        
        ri, dri = ds[other_letter]
        other_str = format_other(ri, dri, other_name)
        if other_str is None:
            continue
        
        # Build new comment line: base + other_str, padded to 80
        content = line.rstrip()
        new_content = content + other_str
        if len(new_content) > 80:
            print(f"  WARN: Line too long ({len(new_content)}) at adp line {i+1}: {new_content}")
            # Still apply but note it
        new_line = new_content.ljust(80)[:80] + '\n'
        
        changes.append((i, raw, new_line))
        diff = abs(adp_e - mrg_e)
        print(f"  L{i+1} G{adp_e}: +{other_str.strip()} [mrg adopted E={mrg_e}, diff={diff:.2f}]")

print(f"\nTotal changes to apply: {len(changes)}")

# ── 3. Apply changes ──────────────────────────────────────────────────────────
for (idx, old, new) in changes:
    adp_lines[idx] = new

with open(ADP_FILE, 'w', encoding='utf-8') as f:
    f.writelines(adp_lines)

print("Done.")
