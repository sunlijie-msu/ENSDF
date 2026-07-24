"""Parse S34_32s_t_p.old 2t-table and match to .ens L-records."""
import re, json

with open(r'A34\S34\old\S34_32s_t_p.old', 'r') as f:
    lines = f.readlines()

# Collect all 2t records (col6='2', col7='t')
# ENSDF 1-based: col6 = index5, col7 = index6
text_rows = []
for line in lines:
    if len(line) < 8: continue
    if line[5] == '2' and line[6] == 't':
        text = line[8:].rstrip('\n')
        text_rows.append(text)

# Skip header rows (rows 0-4: blank, title, blank, column headers, blank)
# Data rows start at row 5 (0-indexed)
data_start = 5

per_level = {}
current_ekev = None

for t in text_rows[data_start:]:
    t_clean = t.replace(',', '.')
    
    # New energy row: starts with number
    m = re.match(r'\s*([\d.]+)\s+(\d+)\s+(\S+(?:\s+\S+)*?)\s+([\d.]+)\s*([\d.]*)\s*$', t_clean)
    if m:
        e_mev = float(m.group(1))
        e_kev = int(round(e_mev * 1000))
        current_ekev = e_kev
        l_val = m.group(2)
        config = m.group(3)
        sii = m.group(4)
        siip = m.group(5) if m.lastindex and m.lastindex >= 5 else ''
        if e_kev not in per_level:
            per_level[e_kev] = []
        per_level[e_kev].append((l_val, config, sii, siip))
        continue
    
    # Continuation row
    m2 = re.match(r'\s+(\d+)\s+(\S+(?:\s+\S+)*?)\s+([\d.]+)\s*([\d.]*)\s*$', t_clean)
    if m2 and current_ekev is not None:
        l_val = m2.group(1)
        config = m2.group(2)
        sii = m2.group(3)
        siip = m2.group(4) if m2.lastindex and m2.lastindex >= 4 else ''
        per_level[current_ekev].append((l_val, config, sii, siip))
        continue

print("=== Parsed per-level data ===")
for e_kev in sorted(per_level.keys()):
    rows = per_level[e_kev]
    print(f"E={e_kev} keV ({len(rows)} configs):")
    for lv, cfg, sii, siip in rows:
        siip_str = f"  (I,I')={siip}" if siip else ""
        print(f"  L={lv}: {cfg}  (I,I)={sii}{siip_str}")
