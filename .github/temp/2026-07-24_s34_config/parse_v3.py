"""Build cL comments for S34_32s_t_p.ens - final version with correct fixed-width parse."""
import re

with open(r'A34\S34\old\S34_32s_t_p.old', 'r') as f:
    lines = f.readlines()

# Collect 2t records
text_rows = []
for line in lines:
    if len(line) < 8: continue
    if line[5] == '2' and line[6] == 't':
        text = line[8:].rstrip('\n')
        text_rows.append(text)

# Skip header rows (rows 0-4)
data_start = 5

# Fixed-width column positions in the text after col8:
# Using the raw text to determine widths:
# "  0.00       0       (d{-3/2}){+2}           100       100       "
#  ^0      ^10     ^18                         ^48       ^60
# Let me figure out exact positions from the raw data
# Print one row to determine widths
for i, t in enumerate(text_rows[data_start:data_start+5]):
    print(f"[{i}]'{t}'")
    for pos in [0, 10, 18, 48, 60, 72]:
        print(f"  pos {pos}: '{t[pos:pos+1] if pos < len(t) else 'END'}'")

# Try: E=cols 0-9, L=cols 10-17, Config=cols 18-47, (I,I)=cols 48-59, (I,I')=cols 60-71
print("\n=== Fixed-width parse V2 ===")
per_level = {}
current_ekev = None

for t in text_rows[data_start:]:
    e_str = t[0:10].strip()
    l_str = t[10:18].strip()
    config_str = t[18:48].strip()
    sii_str = t[48:60].strip() if len(t) > 48 else ''
    siip_str = t[60:72].strip() if len(t) > 60 else ''
    
    # Handle comma decimal in energy only
    if e_str:
        e_str_clean = e_str.replace(',', '.')
        try:
            e_mev = float(e_str_clean)
            e_kev = int(round(e_mev * 1000))
            current_ekev = e_kev
        except ValueError:
            if e_str_clean:
                print(f"  BAD ENERGY: '{e_str}' -> '{e_str_clean}'")
            continue
    
    if current_ekev is None:
        continue
    
    if current_ekev not in per_level:
        per_level[current_ekev] = []
    
    per_level[current_ekev].append((l_str, config_str, sii_str, siip_str))

print("\n=== Results ===")
for e_kev in sorted(per_level.keys()):
    rows = per_level[e_kev]
    print(f"E={e_kev} keV:")
    for lv, cfg, sii, siip in rows:
        print(f"  L={lv}  cfg=[{cfg}]  (I,I)={sii}  (I,I')={siip}")
