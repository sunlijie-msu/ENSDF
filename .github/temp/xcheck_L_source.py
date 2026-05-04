"""
Comprehensive cross-check of L-transfer values in adopted J$ comments
against source reaction .ens files.
"""

ADOPTED_PATH = r'A34\Cl34\new\Cl34_adopted.ens'
THRESHOLD = 5200.0

# Map: reaction label → (file path, target Jpi, particle type description)
REACTION_FILES = {
    '36ar_d_a':   (r'A34\Cl34\new\Cl34_36ar_d_a_pol_d_a.ens', '0+',   '1+  (pn pair)'),
    '33s_3he_d':  (r'A34\Cl34\new\Cl34_33s_3he_d.ens',         '3/2+', '1/2+ (proton)'),
    '35cl_3he_a': (r'A34\Cl34\new\Cl34_35cl_3he_a.ens',        '3/2+', '1/2+ (proton pickup)'),
    '32s_3he_p':  (r'A34\Cl34\new\Cl34_32s_3he_p.ens',         '0+',   '1+  (pn pair)'),
    '32s_a_d':    (r'A34\Cl34\new\Cl34_32s_a_d.ens',           '0+',   '1+  (pn pair)'),
    '35cl_p_d':   (r'A34\Cl34\new\Cl34_35cl_p_d.ens',          '3/2+', '1/2+ (neutron pickup)'),
    '34s_3he_t':  (r'A34\Cl34\new\Cl34_34s_3he_t.ens',         '0+',   'charge-exchange'),
    '36ar_p_3he': (r'A34\Cl34\new\Cl34_36ar_p_3he.ens',        '0+',   '1+  (pn pair pickup)'),
}


def load_levels(filepath):
    """Load all L-records: {line, E, E_str, L_field}"""
    levels = []
    try:
        with open(filepath, 'r') as f:
            for i, line in enumerate(f, 1):
                raw = line.rstrip('\n')
                if len(raw) >= 9 and raw[7] == 'L' and raw[5] == ' ' and raw[6] == ' ':
                    e_str = raw[9:19].strip()
                    try:
                        E = float(e_str)
                    except ValueError:
                        E = None
                    L_field = raw[55:64].strip() if len(raw) >= 64 else ''
                    levels.append({'line': i, 'E': E, 'E_str': e_str, 'L': L_field, 'raw': raw})
    except FileNotFoundError:
        pass
    return levels


def find_best_match(levels, E_adopted, tol=60.0):
    """Find source level matching adopted energy within tolerance keV."""
    if E_adopted is None:
        return None
    best = None
    best_diff = tol
    for lvl in levels:
        if lvl['E'] is None:
            continue
        diff = abs(lvl['E'] - E_adopted)
        if diff < best_diff:
            best_diff = diff
            best = dict(lvl)
            best['diff'] = diff
    return best


# Load all source files
print("Loading source reaction files...")
source_data = {}
for key, (path, target_jpi, particle) in REACTION_FILES.items():
    levels = load_levels(path)
    source_data[key] = {'levels': levels, 'path': path, 'target_jpi': target_jpi, 'particle': particle}
    print(f"  {key}: {len(levels)} L-records in {path.split(chr(92))[-1]}")

print()

# Load adopted levels with J$ comments (using fixed logic)
with open(ADOPTED_PATH, 'r') as f:
    adopted_lines = f.readlines()

# Parse adopted levels
adopted_levels = []
current = None
in_J_block = False

for i, line in enumerate(adopted_lines, 1):
    raw = line.rstrip('\n')
    if len(raw) < 8:
        continue
    if raw[5] == ' ' and raw[6] == ' ' and raw[7] == 'L':
        if current is not None:
            adopted_levels.append(current)
        e_str = raw[9:19].strip()
        try:
            E = float(e_str)
        except ValueError:
            E = None
        current = {'E': E, 'line': i, 'raw': raw, 'J_text': '', 'J_lines': [], 'J_parts': []}
        in_J_block = False
        if E is None or E >= THRESHOLD:
            current = None
        continue
    if current is None:
        continue
    if len(raw) < 9:
        continue
    col6, col7, col8 = raw[5], raw[6], raw[7]
    if col6 == ' ' and col7 == 'c' and col8 == 'L':
        rest = raw[9:].strip()
        if rest.startswith('J$'):
            current['J_parts'] = [rest[2:]]
            current['J_lines'] = [(i, raw)]
            in_J_block = True
        else:
            in_J_block = False
    elif col6 in '23456789' and col7 == 'c' and col8 == 'L':
        if in_J_block:
            rest = raw[9:].strip()
            current['J_parts'].append(rest)
            current['J_lines'].append((i, raw))

if current is not None:
    adopted_levels.append(current)

for lvl in adopted_levels:
    lvl['J_text'] = ' '.join(lvl['J_parts'])

# Now systematically check each adopted level
print(f"Adopted levels below {THRESHOLD} keV: {len(adopted_levels)}")
with_J = [l for l in adopted_levels if l['J_text']]
print(f"Levels with J$ comments: {len(with_J)}")
print()

# Map reaction text patterns to source keys
REACTION_PATTERNS = [
    ('36Ar(d', '36ar_d_a'),
    ('pol d', '36ar_d_a'),
    ('33S(3He,d)', '33s_3he_d'),
    ('{+33}S({+3}He,d)', '33s_3he_d'),
    ('35Cl(3He', '35cl_3he_a'),
    ('{+35}Cl({+3}He,', '35cl_3he_a'),
    ('{+32}S({+3}He,p)', '32s_3he_p'),
    ('32S(3HE,P)', '32s_3he_p'),
    ('{+32}S(|a,d)', '32s_a_d'),
    ('{+35}Cl(p,d)', '35cl_p_d'),
    ('{+34}S({+3}He,t)', '34s_3he_t'),
    ('{+36}Ar(p', '36ar_p_3he'),
]

print("=" * 80)
print("CROSS-CHECK REPORT: Adopted J$ L-values vs Source Reaction Files")
print("=" * 80)

for lvl in with_J:
    E = lvl['E']
    J_text = lvl['J_text']
    
    # Identify which reactions are cited
    cited_reactions = set()
    for pattern, key in REACTION_PATTERNS:
        if pattern in J_text:
            cited_reactions.add(key)
    
    if not cited_reactions:
        continue
    
    print(f"\nLevel E={E} keV (adopted line {lvl['line']}):")
    for jline in lvl['J_lines']:
        print(f"  {jline[1]}")
    
    for key in sorted(cited_reactions):
        fpath, target_jpi, particle = REACTION_FILES[key]
        src_levels = source_data[key]['levels']
        
        # Try to match with different tolerances
        match = find_best_match(src_levels, E, tol=60.0)
        
        if match:
            print(f"  SOURCE [{key}]: Line {match['line']}, E={match['E']} (diff={match.get('diff',0):.1f} keV), L='{match['L']}'")
            print(f"  SOURCE raw: {match['raw']}")
        else:
            print(f"  SOURCE [{key}]: NO MATCH within 60 keV (adopted E={E})")
            # List nearby levels
            nearby = sorted(src_levels, key=lambda l: abs((l['E'] or 9999) - E))[:3]
            for nb in nearby:
                if nb['E'] is not None:
                    print(f"    Nearest: E={nb['E']} keV (diff={abs(nb['E']-E):.1f} keV)")
