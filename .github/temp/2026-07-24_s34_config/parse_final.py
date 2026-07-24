"""Final parser using whitespace-split approach."""
import re

with open(r'A34\S34\old\S34_32s_t_p.old', 'r') as f:
    lines = f.readlines()

text_rows = []
for line in lines:
    if len(line) < 8: continue
    if line[5] == '2' and line[6] == 't':
        text = line[8:].rstrip('\n')
        text_rows.append(text)

data_start = 5

per_level = {}
current_ekev = None

def is_number_like(s):
    """Check if string looks like a number (may have comma as decimal)."""
    s = s.replace(',', '.')
    try:
        float(s)
        return True
    except ValueError:
        return False

for t in text_rows[data_start:]:
    tokens = t.split()
    if not tokens:
        continue
    
    # Check if first token is a number (energy)
    if is_number_like(tokens[0]) and len(tokens) >= 4:
        # New energy row
        e_str = tokens[0].replace(',', '.')
        e_mev = float(e_str)
        e_kev = int(round(e_mev * 1000))
        current_ekev = e_kev
        l_val = tokens[1]
        config = tokens[2]
        sii = tokens[3] if len(tokens) > 3 else ''
        siip = tokens[4] if len(tokens) > 4 else ''
    elif len(tokens) >= 3:
        # Continuation row: L, config, sii, [siip]
        # First token could be L value (integer)
        if tokens[0].isdigit() or (tokens[0].startswith('(') and any(c.isdigit() for c in tokens[0])):
            l_val = tokens[0]
            config = tokens[1]
            sii = tokens[2] if len(tokens) > 2 else ''
            siip = tokens[3] if len(tokens) > 3 else ''
        else:
            # Might be: config, sii, siip (L implied same as previous in same group)
            # But looking at data, this doesn't happen - L is always present
            print(f"  SKIP unexpected: {tokens}")
            continue
    else:
        print(f"  SKIP short: {tokens}")
        continue
    
    if current_ekev is None:
        continue
    
    if current_ekev not in per_level:
        per_level[current_ekev] = []
    per_level[current_ekev].append((l_val, config, sii, siip))

print("=== Results ===")
for e_kev in sorted(per_level.keys()):
    rows = per_level[e_kev]
    print(f"E={e_kev} keV:")
    for lv, cfg, sii, siip in rows:
        print(f"  L={lv}  [{cfg}]  (I,I)={sii}  (I,I')={siip}")
