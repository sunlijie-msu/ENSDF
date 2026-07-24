"""Cross-check S34_32s_t_p.old vs S34_32s_t_p.ens: config + N factors."""
import re

# ====== PARSE .old text table ======
with open(r'A34\S34\old\S34_32s_t_p.old', 'r') as f:
    old_lines = f.readlines()

text_rows = []
for line in old_lines:
    if len(line) < 8: continue
    if line[5] == '2' and line[6] == 't':
        text_rows.append(line[8:].rstrip('\n'))

data_start = 5
per_level_old = {}
current_ekev = None
prev_l = None

for t in text_rows[data_start:]:
    leading = len(t) - len(t.lstrip())
    text_clean = t.strip()
    if not text_clean: continue
    
    is_energy_row = (leading <= 4)
    tokens = text_clean.split()
    
    if is_energy_row and len(tokens) >= 4:
        e_str = tokens[0].replace(',', '.')
        try:
            e_mev = float(e_str)
            e_kev = int(round(e_mev * 1000))
        except ValueError: continue
        current_ekev = e_kev
        l_val = tokens[1]
        config = tokens[2]
        sii = tokens[3]
        siip = tokens[4] if len(tokens) > 4 else ''
        prev_l = l_val
    elif not is_energy_row and len(tokens) >= 3:
        t0 = tokens[0].strip('()')
        if t0.isdigit():
            l_val = tokens[0]
            config = tokens[1]
            sii = tokens[2]
            siip = tokens[3] if len(tokens) > 3 else ''
            prev_l = l_val
        else:
            l_val = prev_l if prev_l else ''
            config = tokens[0]
            sii = tokens[1]
            siip = tokens[2] if len(tokens) > 2 else ''
    else: continue
    
    if current_ekev is None: continue
    
    if current_ekev not in per_level_old:
        per_level_old[current_ekev] = []
    per_level_old[current_ekev].append((l_val, config, sii, siip))

# ====== PARSE .ens cL comments ======
with open(r'A34\S34\new\S34_32s_t_p.ens', 'r') as f:
    ens_lines = f.readlines()

# Find L-records and their associated cL comments
per_level_ens = {}  # e_kev -> [(config_str, N_val1, N_val2), ...]
current_l_ekev = None

for i, line in enumerate(ens_lines):
    if len(line) < 10: continue
    
    # Detect L-record
    if line[7] == 'L' and line[8] == ' ':
        e_str = line[9:19].strip()
        if e_str:
            try:
                current_l_ekev = int(round(float(e_str)))
            except ValueError:
                current_l_ekev = None
        continue
    
    # Detect cL comment with N= pattern
    if current_l_ekev is not None and line[7] == 'c' and 'N=' in line:
        # Parse compact format: $cfg. N=v1, v2. cfg. N=v1.
        # Can span multiple cL/2cL lines
        # We need to collect ALL cL lines for this level
        
        # Actually simpler: start collecting when we see a cL with N= after an L-record
        # But we need to handle continuation (2cL, 3cL)
        # For simplicity, collect the full text block
        
        # Let me use a different approach: find cL blocks by scanning forward
        pass

# Better approach: scan for cL blocks associated with preceding L-records
# Build mapping: L-record index -> list of cL lines with N=
l_to_cl = {}
current_l_idx = None
for i, line in enumerate(ens_lines):
    if len(line) < 10: continue
    
    # L-record: col8='L', col9=' ', and NOT a comment (col7 != 'c')
    if line[7] == 'L' and line[8] == ' ' and line[6] != 'c':
        current_l_idx = i
        continue
    
    # cL with N=
    if current_l_idx is not None and 'N=' in line:
        # Check if this is a cL comment (col7='c')
        if len(line) > 7 and line[6] == 'c':
            if current_l_idx not in l_to_cl:
                l_to_cl[current_l_idx] = []
            l_to_cl[current_l_idx].append(line.rstrip())

# Now parse the collected cL text for each level
for l_idx, cl_lines in l_to_cl.items():
    # Get the L-record energy
    l_line = ens_lines[l_idx]
    e_str = l_line[9:19].strip()
    if not e_str: continue
    try:
        e_kev = int(round(float(e_str)))
    except ValueError: continue
    
    # Join all cL lines, extract text after cL/2cL prefix
    full_text = ""
    for cl in cl_lines:
        # Extract text after the cL/2cL/3cL identifier
        # Format: " 34S  cL $text..." or " 34S 2cL $text..."
        # The prefix is always 9 chars: " 34S  cL " or " 34S 2cL "
        if len(cl) >= 10:
            full_text += cl[9:].strip() + " "
    
    full_text = full_text.strip()
    
    # Parse compact format: $(cfg1). N=v1, v2. (cfg2) N=v3, v4. ...
    # Split by "$" to get blocks
    # Each $ starts a new section: $(cfg). N=v1, v2. cfg. N=v3.
    
    # Remove leading $
    if full_text.startswith('$'):
        full_text = full_text[1:]
    
    # Split into entries by pattern: "cfg. N=v1, v2." or "cfg. N=v1."
    # Entries are separated by ". " but config names may contain periods? No.
    # Pattern: config_string. N=num, num. or config_string. N=num.
    
    entries = []
    # Find all patterns: (config). N=(numbers).
    pattern = r'([^.$]+?)\.\s*N=([\d.]+)(?:,\s*([\d.]+))?\.'
    for m in re.finditer(pattern, full_text):
        cfg = m.group(1).strip()
        n1 = m.group(2)
        n2 = m.group(3) if m.group(3) else ''
        entries.append((cfg, n1, n2))
    
    if entries:
        per_level_ens[e_kev] = entries

print(f"Old levels with config: {len(per_level_old)}")
print(f"Ens levels with config: {len(per_level_ens)}")

# ====== MATCH AND COMPARE ======
print("\n========== CROSS-CHECK REPORT ==========\n")

# Match old energies to ens energies (within ±10 keV)
def match_e(old_e):
    best, best_d = None, 999
    for e in per_level_ens:
        d = abs(old_e - e)
        if d < best_d: best, best_d = e, d
    return (best, best_d) if best_d <= 10 else (None, best_d)

errors = 0
warnings = 0
matched_count = 0

for old_ekev in sorted(per_level_old.keys()):
    ens_e, diff = match_e(old_ekev)
    old_rows = per_level_old[old_ekev]
    
    if ens_e is None:
        print(f"E={old_ekev} keV: NO MATCH in .ens (best diff={diff} keV)")
        print(f"  Old configs: {len(old_rows)}")
        errors += 1
        continue
    
    ens_rows = per_level_ens.get(ens_e, [])
    matched_count += 1
    
    if len(old_rows) != len(ens_rows):
        print(f"E={old_ekev}->{ens_e} keV: COUNT MISMATCH old={len(old_rows)} ens={len(ens_rows)}")
        errors += 1
    
    # Compare entry by entry
    for j, (old_l, old_cfg, old_sii, old_siip) in enumerate(old_rows):
        if j >= len(ens_rows):
            print(f"  [{j}] OLD ONLY: L={old_l} {old_cfg} (I,I)={old_sii}, (I,I')={old_siip}")
            errors += 1
            continue
        
        ens_cfg, ens_n1, ens_n2 = ens_rows[j]
        
        # Compare config name
        cfg_match = (old_cfg == ens_cfg)
        
        # Compare N values
        n1_match = (old_sii == ens_n1)
        n2_match = True
        if old_siip or ens_n2:
            n2_match = (old_siip == ens_n2)
        
        if not (cfg_match and n1_match and n2_match):
            print(f"E={old_ekev}->{ens_e} keV [{j}]: MISMATCH")
            if not cfg_match:
                print(f"  CONFIG: old=[{old_cfg}] vs ens=[{ens_cfg}]")
            if not n1_match:
                print(f"  N1: old={old_sii} vs ens={ens_n1}")
            if not n2_match:
                print(f"  N2: old=[{old_siip}] vs ens=[{ens_n2}]")
            errors += 1
    
    # Check for extra ens entries
    for j in range(len(old_rows), len(ens_rows)):
        ens_cfg, ens_n1, ens_n2 = ens_rows[j]
        print(f"  [{j}] ENS ONLY: {ens_cfg} N={ens_n1}, {ens_n2}")
        errors += 1

# Check for ens-only levels
for ens_ekev in sorted(per_level_ens.keys()):
    found = False
    for old_ekev in per_level_old:
        if abs(old_ekev - ens_ekev) <= 10:
            found = True
            break
    if not found:
        print(f"E={ens_ekev} keV: ENS ONLY (no old match)")
        errors += 1

print(f"\n========== SUMMARY ==========")
print(f"Matched levels: {matched_count}")
print(f"Old-only levels: {len(per_level_old) - matched_count}")
print(f"Ens-only levels: {len(per_level_ens) - matched_count}")
print(f"Errors: {errors}")
print(f"Warnings: {warnings}")
