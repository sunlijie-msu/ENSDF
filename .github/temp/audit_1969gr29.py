"""
Audit script: check which 1969Gr29 RI comments exist vs. missing in Cl34_33s_p_g.ens.
CORRECTED PARSER: uses line[6] to distinguish data records from cG comment lines.
"""
from pathlib import Path

src_path = Path(r'd:/X/ND/ENSDF/A34/Cl34/raw/1969GR29.ens')
tgt_path = Path(r'd:/X/ND/ENSDF/A34/Cl34/new/Cl34_33s_p_g.ens')

level_map = {
    146.0: 146.4,   461.0: 461.2,   666.0: 665.3,
    1229.0: 1230.33, 1886.0: 1887.29, 2158.0: 2157.9,
    2376.0: 2375.7,  2581.0: 2580.3,  3545.0: 3545.08,
    3598.0: 3600.28, 3982.0: 3983.0,  6166.0: 6169.0,
    6179.0: 6181.27, 6204.0: 6207.1,  6271.0: 6273.3,
    6318.0: 6322.0,  6369.0: 6370.2
}

# -- Parse SOURCE file --
src_lines = src_path.read_text('utf-8').splitlines()
src_data = {}
cur_level = None
for line in src_lines:
    if len(line) < 9:
        continue
    # col6=line[5] blank = primary record; col7=line[6]; col8=line[7]
    if line[5] == ' ' and line[6] == ' ' and line[7] == 'L':
        try:
            cur_level = float(line[9:19].strip())
        except ValueError:
            cur_level = None
    elif line[5] == ' ' and line[6] == ' ' and line[7] == 'G' and cur_level in level_map:
        parts = line[9:].split()
        if parts:
            try:
                src_data.setdefault(cur_level, []).append({
                    'g':   float(parts[0]),
                    'ri':  parts[1] if len(parts) > 1 else '',
                    'dri': parts[2] if len(parts) > 2 else '',
                })
            except ValueError:
                pass

# -- Parse TARGET file (correctly separating data records from cG comments) --
tgt_lines = tgt_path.read_text('utf-8').splitlines()
tgt_levels = []
cur_tgt = None
last_g = None
for i, line in enumerate(tgt_lines, 1):
    if len(line) < 9:
        continue
    col6 = line[5]   # column 6: continuation marker
    col7 = line[6]   # column 7: 'c' for comment, ' ' for data
    col8 = line[7]   # column 8: record type

    if col7 == ' ' and col8 == 'L':
        # Primary L-record
        try:
            cur_tgt = {'lv': float(line[9:19].strip()), 'g': []}
            tgt_levels.append(cur_tgt)
            last_g = None
        except ValueError:
            pass
    elif col7 == ' ' and col8 == 'G' and cur_tgt is not None:
        # Primary G-record (data line)
        try:
            last_g = {'g': float(line[9:19].strip()), 'ln': i, 'cmt': ''}
            cur_tgt['g'].append(last_g)
        except ValueError:
            pass
    elif col7 == 'c' and col8 == 'G' and last_g is not None:
        # Primary cG comment (col6 is blank)
        last_g['cmt'] += ' ' + line.rstrip()
    elif col6.isdigit() and col7 == 'c' and col8 == 'G' and last_g is not None:
        # Continuation cG comment (2cG, 3cG ...)
        last_g['cmt'] += ' ' + line.rstrip()

# -- Compare --
# DEBUG: inspect one level to verify parser correctness
print("=== DEBUG PARSER CHECK ===")
for lv in tgt_levels:
    if abs(lv['lv'] - 461.2) < 0.5:
        print(f"Found level {lv['lv']}, has {len(lv['g'])} G records")
        for g in lv['g']:
            print(f"  G={g['g']} ln={g['ln']} cmt={repr(g['cmt'][:80])}")
        break
print("=== END DEBUG ===\n")

TOL = 3.0
ok = miss = no_match = 0

for sl, gammas in sorted(src_data.items()):
    alv = min(tgt_levels, key=lambda x: abs(x['lv'] - level_map[sl]))
    print(f"--- Src L={sl} -> Adp L={alv['lv']} ---")
    for sg in gammas:
        candidates = [g for g in alv['g'] if abs(g['g'] - sg['g']) <= TOL]
        if not candidates:
            print(f"  NO_MATCH: G={sg['g']} {sg['ri']} {sg['dri']}")
            no_match += 1
            continue
        best = min(candidates, key=lambda g: abs(g['g'] - sg['g']))
        d = abs(best['g'] - sg['g'])
        has = '1969Gr29' in best['cmt']
        tag = 'OK  ' if has else 'MISS'
        print(f"  {tag}: G={sg['g']} ri={sg['ri']} {sg['dri']} -> adp={best['g']}(d={d:.1f}) L{best['ln']}")
        if has:
            ok += 1
        else:
            miss += 1
    print()

print(f"TOTAL: OK={ok}  MISS={miss}  NO_MATCH(no adopted G within {TOL} keV)={no_match}")
