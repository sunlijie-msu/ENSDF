"""Generate and apply cL comments for S34_32s_t_p.ens."""
import re

# ====== PARSE .old ======
with open(r'A34\S34\old\S34_32s_t_p.old', 'r') as f:
    lines = f.readlines()

text_rows = []
for line in lines:
    if len(line) < 8: continue
    if line[5] == '2' and line[6] == 't':
        text_rows.append(line[8:].rstrip('\n'))

data_start = 5
per_level = {}
current_ekev = None
prev_l = None

for t in text_rows[data_start:]:
    leading = len(t) - len(t.lstrip())
    text_clean = t.strip()
    if not text_clean:
        continue
    
    is_energy_row = (leading <= 4)
    tokens = text_clean.split()
    
    if is_energy_row and len(tokens) >= 4:
        e_str = tokens[0].replace(',', '.')
        try:
            e_mev = float(e_str)
            e_kev = int(round(e_mev * 1000))
        except ValueError:
            continue
        current_ekev = e_kev
        l_val = tokens[1]
        config = tokens[2]
        sii = tokens[3]
        siip = tokens[4] if len(tokens) > 4 else ''
        prev_l = l_val
    elif not is_energy_row and len(tokens) >= 3:
        # Check if first token is L value (integer or (int))
        t0 = tokens[0].strip('()')
        if t0.isdigit():
            l_val = tokens[0]
            config = tokens[1]
            sii = tokens[2]
            siip = tokens[3] if len(tokens) > 3 else ''
            prev_l = l_val
        else:
            # No L value, inherit from previous
            l_val = prev_l if prev_l else ''
            config = tokens[0]
            sii = tokens[1]
            siip = tokens[2] if len(tokens) > 2 else ''
    else:
        continue
    
    if current_ekev is None:
        continue
    
    if current_ekev not in per_level:
        per_level[current_ekev] = []
    per_level[current_ekev].append((l_val, config, sii, siip))

# ====== READ .ens ======
with open(r'A34\S34\new\S34_32s_t_p.ens', 'r') as f:
    ens_lines = f.readlines()

# Get L-record energies and line indices
ens_levels = {}
for i, line in enumerate(ens_lines):
    if len(line) >= 10 and line[7] == 'L' and line[8] == ' ':
        e_str = line[9:19].strip()
        if e_str:
            try:
                e_int = int(round(float(e_str)))
                ens_levels[e_int] = i
            except ValueError:
                pass

# ====== MATCH ======
def match_energy(old_ekev):
    best = None
    best_diff = 999
    for ens_e in ens_levels:
        d = abs(old_ekev - ens_e)
        if d < best_diff:
            best_diff = d
            best = ens_e
    if best_diff <= 10:
        return best, best_diff
    return None, best_diff

# ====== BUILD COMMENT TEXT ======
def build_comment(rows):
    """Build cL comment block from configuration rows."""
    lines = []
    parts = []
    for lv, cfg, sii, siip in rows:
        if siip:
            part = f"{cfg} (I,I)={sii}, (I,I')={siip}"
        else:
            part = f"{cfg} (I,I)={sii}"
        parts.append(part)
    
    # Join with semicolons
    header = "$|s{-rel}/|s{-DW} from DWBA (1978Cr01):"
    
    # Build lines, max ~70 chars per cL line (accounting for " 34S  cL " prefix = 9 chars)
    # cL lines: " 34S  cL " = 9 chars, plus text
    # 2cL lines: " 34S 2cL " = 9 chars
    
    if len(parts) == 1:
        line1 = f"{header} {parts[0]}."
        lines.append(line1)
    else:
        # Multiple configs per level
        line1 = header
        lines.append(line1)
        for j, p in enumerate(parts):
            is_last = (j == len(parts) - 1)
            if is_last:
                lines.append(f"{p}.")
            else:
                lines.append(f"{p};")
    
    return lines

# ====== GENERATE EDITS ======
# For each matched level, we need to add cL comments after the L-record
# The cL comments go AFTER the L-record and BEFORE any existing cL comments,
# or after continuation records (2 L, F L) and before cL comments.

# Strategy: find the line index of each L-record, then insert new cL lines
# after that L-record but before any existing cL comments or before the B-record

print("=== Planned edits ===")
matches_info = []
for old_ekev in sorted(per_level.keys()):
    ens_e, diff = match_energy(old_ekev)
    if ens_e is None:
        print(f"  NO MATCH: {old_ekev} keV (best diff={diff})")
        continue
    
    rows = per_level[old_ekev]
    comment_lines = build_comment(rows)
    
    # Find insertion point: after the L-record but before any existing cL or B/G records
    l_idx = ens_levels[ens_e]
    
    # Check what comes after the L-record
    # We insert BEFORE the first non-continuation-of-L record
    # i.e., after any 2L, FL records but before cL, B, G, or next L
    
    insert_after = l_idx  # default: insert right after L
    for k in range(l_idx + 1, min(l_idx + 10, len(ens_lines))):
        line = ens_lines[k]
        if len(line) < 8: break
        # If continuation of L (2 L or F L), skip
        if line[7] == 'L' and line[6] != ' ':
            insert_after = k
            continue
        # If cL comment, skip (we want to insert before existing cL)
        if line[7] == 'c' and line[6] in (' ', 'L') and len(line) > 10 and 'cL' in line[6:9]:
            # Actually, we insert BEFORE existing cL
            # But wait: the existing cL in .ens is GLOBAL (before first L), not per-level
            # For per-level, we add new cL after L, before B or G
            pass
        # Stop at B, G, next L, or comment
        if line[7] in ('B', 'G', 'L', 'c') or (line[6] == ' ' and line[7] == 'c'):
            break
        insert_after = k
    
    # Actually, looking at .ens structure: L-records are followed by nothing or by cL comments
    # For levels with existing cL (e.g., 4888 has " 34S  cL $Doublet..."), we insert after L but before cL
    # For levels without cL, we insert after L before next L
    
    # Simple approach: insert right after the L-record line (after any 2L/FL continuations)
    # Existing cL lines (like for 4888, 5679, 7112) will come after our new cL
    
    # Find last continuation-of-L line
    while insert_after + 1 < len(ens_lines):
        next_line = ens_lines[insert_after + 1]
        if len(next_line) >= 8 and next_line[7] == 'L' and next_line[6] != ' ':
            insert_after += 1
        else:
            break
    
    print(f"  {old_ekev}->{ens_e} keV (d={diff}): insert after line {insert_after+1}, {len(rows)} configs")
    for cl in comment_lines:
        print(f"    {cl}")
    matches_info.append({
        'old_ekev': old_ekev,
        'ens_e': ens_e,
        'insert_after': insert_after,
        'comment_lines': comment_lines,
        'rows': rows
    })

print(f"\nTotal: {len(matches_info)} levels to edit")
