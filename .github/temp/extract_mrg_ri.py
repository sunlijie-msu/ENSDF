from pathlib import Path
from collections import OrderedDict

lines = Path('A35/P35/raw/35.mrg').read_text(encoding='utf-8').splitlines()

# Verified column layout (ENSDF 1-based cols within embedded G-record):
#   col 1-5:  NUCID (' 35P ')
#   col 6:    continuation (' ' for primary record)
#   col 8:    'G'
#   col 10-19: E
#   col 20-21: DE
#   col 22:   readability space (ENSDF standard) — may be absent in some source files
#   col 23-29: RI
#   col 30-31: DRI
#
# The ENSDF record starts at col1_pos = ln.find('35P   G ') - 1  (the space at NUCID col 1)

def parse_g_record(ln):
    """If ln is a primary G-record for dataset A, K, or L, return (ds, ri, dri). Else None."""
    if '35P   G ' not in ln:
        return None
    col1_pos = ln.find('35P   G ') - 1
    if col1_pos < 0:
        return None
    e = ln[col1_pos:]          # e[N-1] = ENSDF col N (1-based)
    if len(e) < 9:
        return None
    if e[7] != 'G':            # col 8 must be 'G'
        return None
    if e[5] != ' ':            # col 6 must be blank (primary record, not continuation)
        return None
    # Identify dataset
    if '--->A  A ' in ln:
        ds = 'A'
    elif '--->K  ' in ln:
        ds = 'K'
    elif '--->L  ' in ln:
        ds = 'L'
    else:
        return None
    # Extract RI: col 22 is normally a readability space; if it is not, RI starts at col 22
    col22 = e[21] if len(e) > 21 else ' '
    if col22 == ' ':
        ri_raw = e[22:29].strip() if len(e) >= 29 else ''
    else:
        ri_raw = e[21:28].strip() if len(e) >= 28 else ''
    dri_raw = e[29:31].strip() if len(e) >= 31 else ''
    return ds, ri_raw or None, dri_raw or None


rows = []
cur_gE = None

for ln in lines:
    # GAMMA header line → set current adopted gamma energy
    if ' GAMMA' in ln and '------' in ln and '35P   G ' in ln:
        col1_pos = ln.find('35P   G ') - 1
        cur_gE = ln[col1_pos + 9 : col1_pos + 19].strip()  # cols 10-19
        continue
    # LEVEL separator → reset
    if ' LEVEL' in ln and '******' in ln:
        cur_gE = None
        continue
    # Dataset G-record
    result = parse_g_record(ln)
    if result and cur_gE:
        ds, ri, dri = result
        rows.append({'gE': cur_gE, 'ds': ds, 'ri': ri, 'dri': dri})

# Build table keyed by adopted gE
table = OrderedDict()
for r in rows:
    if r['gE'] not in table:
        table[r['gE']] = {'A': None, 'K': None, 'L': None}
    val = f"{r['ri']}({r['dri']})" if r['ri'] and r['dri'] else (r['ri'] or None)
    table[r['gE']][r['ds']] = val

# ── Final table ──
print(f"{'gE (adopted)':>12} | {'A: 35Si β-':>14} | {'K: Pb(215 MeV)':>14} | {'L: Pb(230 MeV)':>14}")
print('-' * 65)
for gE, vals in table.items():
    a = vals['A'] or '-'
    k = vals['K'] or '-'
    l = vals['L'] or '-'
    # Only print rows where at least one of A, K, L has data
    if a != '-' or k != '-' or l != '-':
        print(f"{gE:>12} | {a:>14} | {k:>14} | {l:>14}")
print(f"\nTotal rows with A/K/L data: {sum(1 for v in table.values() if any(v[d] for d in 'AKL'))}")
