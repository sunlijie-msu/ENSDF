"""Build cL comments for S34_32s_t_p.ens from parsed .old table."""
import re

# -- Parsed data from .old (fixed: no comma-replacement for configs) --
with open(r'A34\S34\old\S34_32s_t_p.old', 'r') as f:
    lines = f.readlines()

text_rows = []
for line in lines:
    if len(line) < 8: continue
    if line[5] == '2' and line[6] == 't':
        text = line[8:].rstrip('\n')
        text_rows.append(text)

data_start = 5
per_level = {}  # energy_keV -> [(L, config, sii, siip), ...]
current_ekev = None

for t in text_rows[data_start:]:
    # Replace comma decimal ONLY in numeric fields, not in config names
    # Strategy: parse the row, identify position of config vs numbers
    
    # Fixed-width parsing approach for robustness
    # The text after col8 has approximate widths:
    # E: 1-10, L: 11-16, Config: 17-48, (I,I): 49-60, (I,I'): 61-72
    if len(t) < 10:
        continue
    
    e_str = t[0:10].strip().replace(',', '.')
    l_str = t[10:18].strip()
    config_str = t[18:48].strip()
    sii_str = t[48:60].strip() if len(t) > 48 else ''
    siip_str = t[60:72].strip() if len(t) > 60 else ''
    
    if e_str:
        try:
            e_mev = float(e_str)
            e_kev = int(round(e_mev * 1000))
            current_ekev = e_kev
        except ValueError:
            continue
    
    if current_ekev is None:
        continue
    
    if current_ekev not in per_level:
        per_level[current_ekev] = []
    
    l_val = l_str if l_str else ''
    sii = sii_str if sii_str else ''
    siip = siip_str if siip_str else ''
    per_level[current_ekev].append((l_val, config_str, sii, siip))

# Print parsed data
print("=== Per-level data (fixed-width parse) ===")
for e_kev in sorted(per_level.keys()):
    rows = per_level[e_kev]
    print(f"E={e_kev} keV:")
    for lv, cfg, sii, siip in rows:
        siip_str = f"  (I,I')={siip}" if siip else ""
        print(f"  L={lv}: [{cfg}]  (I,I)={sii}{siip_str}")

# -- Read .ens and match --
with open(r'A34\S34\new\S34_32s_t_p.ens', 'r') as f:
    ens_lines = f.readlines()

# Extract L-record energies (rounded to keV int)
ens_levels = {}  # energy_int -> line_index
for i, line in enumerate(ens_lines):
    if len(line) >= 10 and line[7] == 'L' and line[8] == ' ':
        e_str = line[9:19].strip()
        if e_str:
            try:
                e_float = float(e_str)
                e_int = int(round(e_float))
                ens_levels[e_int] = i
            except ValueError:
                pass

print("\n=== .ens L-record energies ===")
for e in sorted(ens_levels.keys()):
    print(f"  {e} keV at line {ens_levels[e]+1}")

# Match
print("\n=== Matching ===")
matches = []
for old_ekev in sorted(per_level.keys()):
    best_match = None
    best_diff = 999
    for ens_ekev in ens_levels.keys():
        diff = abs(old_ekev - ens_ekev)
        if diff < best_diff:
            best_diff = diff
            best_match = ens_ekev
    if best_diff <= 10:
        matches.append((best_match, old_ekev, best_diff, per_level[old_ekev]))
        print(f"  {old_ekev} -> {best_match} keV (diff={best_diff}) OK")
    else:
        print(f"  {old_ekev} -> NO MATCH (best={best_match}, diff={best_diff})")

print(f"\nTotal matched: {len(matches)} levels")
