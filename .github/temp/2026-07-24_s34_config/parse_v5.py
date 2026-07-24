"""Final robust parser using leading-space + regex approach."""
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

for t in text_rows[data_start:]:
    leading = len(t) - len(t.lstrip())
    text_clean = t.strip()
    if not text_clean:
        continue
    
    # Determine row type by leading whitespace
    # Energy rows: leading <= 4 spaces before the number
    # Continuation rows: leading >= 10 spaces
    is_energy_row = (leading <= 4)
    
    # Parse tokens
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
    elif not is_energy_row and len(tokens) >= 3:
        # Continuation: L, config, sii[, siip]
        # L is always a digit or digit in parens like (4)
        l_val = tokens[0]
        config = tokens[1]
        sii = tokens[2]
        siip = tokens[3] if len(tokens) > 3 else ''
    else:
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
