"""
Cross-check: source Markdown table vs target ENSDF for 141Sm.
Checks: levels, gammas, E, DE, Jpi, RI, DRI, M, Flag X, cG comments.
"""
import re, sys

# ====== PARSE SOURCE TABLE ======
src_text = open('XUNDL/2026MAAA_CT11001_141Sm_Table.md', 'r', encoding='utf-8').read()
src_rows = []
for line in src_text.split('\n'):
    if line.startswith('|') and 'E_x' not in line and '---' not in line and 'Excitation' not in line:
        parts = [c.strip() for c in line.split('|')[1:-1]]
        if len(parts) >= 8:
            src_rows.append(parts)

def pvu(s):
    """Parse 'val(unc)' -> (val_str, unc_str)"""
    if not s: return '', ''
    clean = s.replace('*','').replace('b','').replace('\u2217','').replace('\u2212','-')
    m = re.match(r'^([+-]?\d+\.?\d*)\s*(?:\((\d+)\))?\s*$', clean)
    if m: return m.group(1), m.group(2) or ''
    return s, ''

# Build source data: {ex_val: {'jpi':..., 'de':..., 'gammas': [(eg, eg_de, ri, ri_de, rdco, rado, pol, assign, star, b), ...]}}
src_levels = {}
for row in src_rows:
    ex_v, ex_d = pvu(row[0])
    jpi = row[1]
    eg_v, eg_d = pvu(row[2])
    has_star = '*' in row[2] or '\u2217' in row[2]
    ri_v, ri_d = pvu(row[3])
    has_b = 'b' in row[3]
    if '.' in ri_v and ri_v.split('.')[1] == '0': ri_v = ri_v.split('.')[0]
    
    if ex_v not in src_levels:
        src_levels[ex_v] = {'ex_de': ex_d, 'jpi': jpi, 'gammas': []}
    src_levels[ex_v]['gammas'].append({
        'eg': eg_v, 'eg_de': eg_d, 'ri': ri_v, 'ri_de': ri_d,
        'rdco': row[4], 'rado': row[5], 'pol': row[6],
        'assign': row[7], 'star': has_star, 'b': has_b
    })

# ====== PARSE TARGET ENSDF ======
ens_lines = open('XUNDL/2026MAAA_CT11001_141Sm.ens', 'r', encoding='utf-8').readlines()
ens_data = {}  # {level_e: {'jpi':..., 'ex_de':..., 'gammas': [...]}}
cur_ex = None
cur_gammas = []

def add_level():
    global cur_ex, cur_gammas
    if cur_ex is not None:
        ens_data[cur_ex] = gammas.copy() if gammas else []

gammas = {}
for i, line in enumerate(ens_lines):
    if len(line) < 9: continue
    col7, col8 = line[7], line[8] if len(line) > 8 else ' '
    if col7 == 'c': continue  # comment lines
    
    if col8 == 'L' and line[5] == ' ':
        add_level()
        ex_v = line[9:19].strip()
        jpi = line[22:39].strip()
        ex_de = line[19:21].strip()
        cur_ex = ex_v
        cur_jpi = jpi
        cur_ex_de = ex_de
        gammas = {'jpi': jpi, 'ex_de': ex_de, 'g_list': []}
    elif col8 == 'G' and line[5] == ' ':
        eg_v = line[9:19].strip()
        eg_de = line[19:21].strip()
        ri = line[22:29].strip()
        ri_de = line[29:31].strip()
        m = line[32:41].strip()
        flag = line[76] if len(line) > 76 else ' '
        gammas['g_list'].append({
            'eg': eg_v, 'eg_de': eg_de, 'ri': ri, 'ri_de': ri_de,
            'm': m, 'flag': flag
        })

add_level()  # final level

# Match cG comments to preceding gamma
cg_map = {}  # (level_e, gamma_idx) -> comment text
prev_gamma_key = None
for i, line in enumerate(ens_lines):
    if 'cG ' in line and line[7] == 'c':
        # Find preceding G record
        for j in range(i-1, -1, -1):
            if len(ens_lines[j]) >= 9 and ens_lines[j][7] == 'c': continue
            if len(ens_lines[j]) >= 9 and ens_lines[j][8] == 'G':
                # Extract gamma info
                ge = ens_lines[j][9:19].strip()
                # Find which level owns this G
                for k in range(j-1, -1, -1):
                    if len(ens_lines[k]) >= 9 and ens_lines[k][8] == 'L' and ens_lines[k][5] == ' ':
                        le = ens_lines[k][9:19].strip()
                        if le in ens_data:
                            glist = ens_data[le]
                            for gi, gg in enumerate(glist['g_list']):
                                if gg['eg'] == ge:
                                    prev_gamma_key = (le, gi)
                                    break
                        break
                break
        if prev_gamma_key:
            # Concatenate all following cG lines
            cmt = line[10:].strip()
            ii = i + 1
            while ii < len(ens_lines) and 'cG' in ens_lines[ii] and ens_lines[ii][7] == 'c':
                cmt += ' ' + ens_lines[ii][10:].strip()
                ii += 1
            if prev_gamma_key not in cg_map:
                cg_map[prev_gamma_key] = []
            cg_map[prev_gamma_key].append(cmt)

# ====== COMPARE ======
src_ex_list = sorted(src_levels.keys(), key=float)
ens_ex_list = sorted(ens_data.keys(), key=float)

mismatches = []

# Check target has L 0.0 and 175.9 (not in source)
for e in ['0.0', '175.9']:
    if e in ens_data and e not in src_levels:
        print(f'[INFO] Level {e} in ENSDF but not in source (pre-existing, expected)')

# Check each source level exists in target
for ex_v in src_ex_list:
    if ex_v not in ens_data:
        mismatches.append(f'[MISSING] Level E={ex_v} in source but NOT found in ENSDF')
        continue
    
    sl = src_levels[ex_v]
    tl = ens_data[ex_v]
    tg_list = tl['g_list']
    
    # Compare Jpi
    if sl['jpi'] != tl['jpi']:
        mismatches.append(f'Level {ex_v}: Jpi SRC="{sl["jpi"]}" ENS="{tl["jpi"]}"')
    
    # Match source gammas to target gammas by energy
    matched_src = set()
    matched_tg = set()
    
    for si, sg in enumerate(sl['gammas']):
        best = None
        best_diff = 999
        for ti, tg in enumerate(tg_list):
            if ti in matched_tg: continue
            diff = abs(float(sg['eg']) - float(tg['eg']))
            if diff < 0.3 and diff < best_diff:
                best = ti
                best_diff = diff
        
        if best is None:
            eg = sg['eg']
            mismatches.append(f'Level {ex_v} G {eg}: in source but NOT found in ENSDF')
            continue
        
        matched_src.add(si)
        matched_tg.add(best)
        tg = tg_list[best]
        
        # Compare fields
        # DE
        if sg['eg_de'] != tg['eg_de']:
            mismatches.append(f'Level {ex_v} G {sg["eg"]}: DE SRC="({sg["eg_de"]})" ENS="({tg["eg_de"]})"')
        
        # RI
        if sg['ri'] != tg['ri']:
            mismatches.append(f'Level {ex_v} G {sg["eg"]}: RI SRC="{sg["ri"]}" ENS="{tg["ri"]}"')
        
        # DRI
        if sg['ri_de'] != tg['ri_de']:
            mismatches.append(f'Level {ex_v} G {sg["eg"]}: DRI SRC="({sg["ri_de"]})" ENS="({tg["ri_de"]})"')
        
        # M field mapping
        assign = sg['assign']
        expected_m = ''
        if 'E2' in assign: expected_m = 'E2'
        elif 'E1' in assign: expected_m = 'E1'
        elif 'M1' in assign: expected_m = 'M1'
        if 'M1+E2' in assign: expected_m = 'M1+E2'
        if assign.startswith('('): expected_m = '(' + expected_m + ')' if expected_m else ''
        # ΔI=0 handling
        if 'Delta' in assign or '\\Delta' in assign:
            if 'E1' in assign: expected_m = 'E1'
            elif 'M1' in assign: expected_m = 'M1'
        if tg['m'] != expected_m:
            mismatches.append(f'Level {ex_v} G {sg["eg"]}: M SRC="{assign}"->"{expected_m}" ENS="{tg["m"]}"')
        
        # Flag X
        src_has_x = sg['star']
        ens_has_x = tg['flag'] == 'X'
        if src_has_x != ens_has_x:
            mismatches.append(f'Level {ex_v} G {sg["eg"]}: Flag X SRC={src_has_x} ENS={ens_has_x}')
    
    # Check for extra gammas in target
    for ti, tg in enumerate(tg_list):
        if ti not in matched_tg:
            mismatches.append(f'Level {ex_v} G {tg["eg"]}: in ENSDF but NOT in source (extra)')

# Check for extra levels in target (besides 0.0 and 175.9)
for ex_v in ens_ex_list:
    if ex_v not in ['0.0', '175.9'] and ex_v not in src_levels:
        mismatches.append(f'[EXTRA] Level E={ex_v} in ENSDF but not in source')

# Report
print('=' * 60)
print('DATA CROSS-CHECK REPORT: source (MD table) vs target (ENSDF)')
print(f'Source: {len(src_levels)} levels, {sum(len(v["gammas"]) for v in src_levels.values())} gammas')
print(f'Target: {len(ens_data)} levels, {sum(len(v["g_list"]) for v in ens_data.values())} gammas')
print('=' * 60)

if not mismatches:
    print('NO MISMATCHES FOUND — 100% consistency')
else:
    print(f'\n{len(mismatches)} MISMATCH(ES):')
    for m in mismatches:
        print(f'  {m}')

print()

# cG comment spot check: verify key entries
print('--- cG comment spot check (key transitions) ---')
for i, row in enumerate(src_rows):
    if 'Delta' in row[7] or '\\Delta' in row[7]:
        ex_v, _ = pvu(row[0])
        eg_v, _ = pvu(row[2])
        print(f'  ΔI=0 transition: L={ex_v} G={eg_v} assign="{row[7]}"')
