"""
Cross-check: source Markdown table vs target ENSDF for 141Sm.
"""
import re

def pvu(s):
    if not s: return '', ''
    clean = s.replace('*','').replace('b','').replace('\u2217','').replace('\u2212','-')
    m = re.match(r'^([+-]?\d+\.?\d*)\s*(?:\((\d+)\))?\s*$', clean)
    if m: return m.group(1), m.group(2) or ''
    return s, ''

# ===== PARSE SOURCE =====
src_text = open('XUNDL/2026MAAA_CT11001_141Sm_Table.md', 'r', encoding='utf-8').read()
src_rows = []
for line in src_text.split('\n'):
    if line.startswith('|') and 'E_x' not in line and '---' not in line and 'Excitation' not in line:
        parts = [c.strip() for c in line.split('|')[1:-1]]
        if len(parts) >= 8: src_rows.append(parts)

src_levels = {}
for row in src_rows:
    ex_v, ex_d = pvu(row[0])
    if ex_v not in src_levels:
        src_levels[ex_v] = {'ex_de': ex_d, 'jpi': row[1], 'gammas': []}
    eg_v, eg_d = pvu(row[2])
    ri_v, ri_d = pvu(row[3])
    if '.' in ri_v and ri_v.split('.')[1] == '0': ri_v = ri_v.split('.')[0]
    src_levels[ex_v]['gammas'].append({
        'eg': eg_v, 'eg_de': eg_d, 'ri': ri_v, 'ri_de': ri_d,
        'rdco': row[4], 'rado': row[5], 'pol': row[6], 'assign': row[7],
        'star': '*' in row[2] or '\u2217' in row[2], 'b': 'b' in row[3]
    })

# ===== PARSE TARGET ENSDF =====
lines = open('XUNDL/2026MAAA_CT11001_141Sm.ens', 'r', encoding='utf-8').readlines()
ens_levels = {}  # {ex_val: {'jpi':..., 'g_list': [(eg, eg_de, ri, ri_de, m, flag), ...]}}
cur_ex = None
cur_glist = []
cur_jpi = ''

def flush_level():
    global cur_ex, cur_glist, cur_jpi
    if cur_ex is not None:
        ens_levels[cur_ex] = {'jpi': cur_jpi, 'g_list': cur_glist}
    cur_glist = []

for line in lines:
    if len(line) < 10 or line[6] == 'c': continue  # skip comments
    if line[7] == 'L' and line[6] == ' ':
        flush_level()
        cur_ex = line[9:19].strip()
        cur_jpi = line[22:39].strip()
    elif line[7] == 'G' and line[6] == ' ' and cur_ex is not None:
        eg = line[9:19].strip()
        eg_d = line[19:21].strip()
        ri = line[22:29].strip()
        ri_d = line[29:31].strip()
        m = line[32:41].strip()
        flag = line[76] if len(line) > 76 else ' '
        cur_glist.append((eg, eg_d, ri, ri_d, m, flag))
flush_level()

# ===== COMPARE =====
def expected_m(assign):
    a = assign.strip()
    if 'Delta' in a or '\\Delta' in a:
        m = 'E1' if 'E1' in a else 'M1' if 'M1' in a else ''
        if '(' in a: m = '(' + m + ')'
        return m
    d = {'E2':'E2','E1':'E1','M1':'M1','Mixed M1+E2':'M1+E2',
         '(E2)':'(E2)','(E1)':'(E1)','(M1)':'(M1)','(Mixed M1+E2)':'(M1+E2)'}
    return d.get(a, '')

mismatches = []
src_ex_l = sorted(src_levels.keys(), key=float)

for ex_v in src_ex_l:
    sl = src_levels[ex_v]
    if ex_v not in ens_levels:
        mismatches.append(f'[MISSING LEVEL] E={ex_v}')
        continue
    tl = ens_levels[ex_v]
    
    # Jpi
    sj = sl['jpi'].replace('\u2212','-')
    tj = tl['jpi'].replace('\u2212','-')
    if sj != tj:
        mismatches.append(f'L{ex_v}: Jpi SRC="{sj}" ENS="{tj}"')
    
    # Match gammas
    matched_s = set()
    matched_t = set()
    for si, sg in enumerate(sl['gammas']):
        best = None
        bd = 999
        for ti, tg in enumerate(tl['g_list']):
            if ti in matched_t: continue
            diff = abs(float(sg['eg']) - float(tg[0]))
            if diff < 0.3 and diff < bd:
                best = ti; bd = diff
        if best is None:
            mismatches.append(f'L{ex_v} G{sg["eg"]}: MISSING in ENSDF')
            continue
        matched_s.add(si); matched_t.add(best)
        tg = tl['g_list'][best]
        
        # DE
        if sg['eg_de'] != tg[1]:
            mismatches.append(f'L{ex_v} G{sg["eg"]}: DE SRC=({sg["eg_de"]}) ENS=({tg[1]})')
        # RI
        if sg['ri'] != tg[2]:
            mismatches.append(f'L{ex_v} G{sg["eg"]}: RI SRC="{sg["ri"]}" ENS="{tg[2]}"')
        # DRI
        if sg['ri_de'] != tg[3]:
            mismatches.append(f'L{ex_v} G{sg["eg"]}: DRI SRC=({sg["ri_de"]}) ENS=({tg[3]})')
        # M
        em = expected_m(sg['assign'])
        if em != tg[4]:
            mismatches.append(f'L{ex_v} G{sg["eg"]}: M SRC="{sg["assign"]}"->"{em}" ENS="{tg[4]}"')
        # Flag X
        sx = 'X' if sg['star'] else ' '
        if sx != tg[5]:
            mismatches.append(f'L{ex_v} G{sg["eg"]}: Flag SRC={repr(sx)} ENS={repr(tg[5])}')
    
    for ti, tg in enumerate(tl['g_list']):
        if ti not in matched_t:
            mismatches.append(f'L{ex_v} G{tg[0]}: EXTRA in ENSDF (not in source)')

# Cross-check extras (known pre-existing levels)
for ex_v in sorted(ens_levels.keys(), key=float):
    if ex_v not in src_levels and ex_v not in ['0.0', '175.9']:
        mismatches.append(f'[EXTRA LEVEL] E={ex_v} in ENSDF only')

print('=' * 65)
print('CROSS-CHECK REPORT: source (MD table) vs target (ENSDF)')
print(f'Source: {len(src_levels)} levels, {sum(len(v["gammas"]) for v in src_levels.values())} gammas')
print(f'Target: {len(ens_levels)} levels, {sum(len(v["g_list"]) for v in ens_levels.values())} gammas')
print('=' * 65)

if not mismatches:
    print('NO MISMATCHES — 100% consistency.')
else:
    print(f'\n{len(mismatches)} MISMATCH(ES):')
    for m in mismatches:
        print(f'  {m}')

# Identify ΔI=0 transitions and their comments
print('\n--- ΔI=0 transition check ---')
for row in src_rows:
    if 'Delta' in row[7] or '\\Delta' in row[7]:
        ex_v, _ = pvu(row[0])
        eg_v, _ = pvu(row[2])
        print(f'  L={ex_v} G={eg_v} assign="{row[7]}" -> ENSDF M field should have |DJ=0 in cG')
