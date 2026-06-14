"""
15% random spot check: trace 15 random transitions from source to target.
"""
import re, random, json

random.seed(20260614)  # reproducible

def pvu(s):
    if not s: return '', ''
    clean = s.replace('*','').replace('b','').replace('\u2217','').replace('\u2212','-')
    m = re.match(r'^([+-]?\d+\.?\d*)\s*(?:\((\d+)\))?\s*$', clean)
    if m: return m.group(1), m.group(2) or ''
    return s, ''

# Parse source
src_text = open('XUNDL/2026MAAA_CT11001_141Sm_Table.md', 'r', encoding='utf-8').read()
src_rows = []
for line in src_text.split('\n'):
    if line.startswith('|') and 'E_x' not in line and '---' not in line and 'Excitation' not in line:
        parts = [c.strip() for c in line.split('|')[1:-1]]
        if len(parts) >= 8: src_rows.append(parts)

# Parse target
lines = open('XUNDL/2026MAAA_CT11001_141Sm.ens', 'r', encoding='utf-8').readlines()
ens_levels = {}
cur_ex = None; cur_glist = []; cur_jpi = ''
for line in lines:
    if len(line) < 10 or line[6] == 'c': continue
    if line[7] == 'L' and line[6] == ' ':
        if cur_ex is not None: ens_levels[cur_ex] = {'jpi': cur_jpi, 'g_list': cur_glist}
        cur_ex = line[9:19].strip(); cur_jpi = line[22:39].strip(); cur_glist = []
    elif line[7] == 'G' and line[6] == ' ' and cur_ex is not None:
        eg = line[9:19].strip(); eg_d = line[19:21].strip()
        ri = line[22:29].strip(); ri_d = line[29:31].strip()
        m = line[32:41].strip(); flag = line[76] if len(line) > 76 else ' '
        cur_glist.append((eg, eg_d, ri, ri_d, m, flag))
if cur_ex is not None: ens_levels[cur_ex] = {'jpi': cur_jpi, 'g_list': cur_glist}

# Select 15 random source gamma rows
indices = sorted(random.sample(range(len(src_rows)), 15))

print('=' * 70)
print(f'15% SPOT CHECK (seed=20260614): {len(indices)} of {len(src_rows)} transitions')
print('=' * 70)

errors = 0
for idx in indices:
    row = src_rows[idx]
    ex_v, ex_d = pvu(row[0])
    jpi_src = row[1]
    eg_v, eg_d = pvu(row[2])
    ri_v, ri_d = pvu(row[3])
    if '.' in ri_v and ri_v.split('.')[1] == '0': ri_v = ri_v.split('.')[0]
    has_star = '*' in row[2] or '\u2217' in row[2]
    assign = row[7]
    
    if ex_v not in ens_levels:
        print(f'FAIL: [{idx}] L {ex_v} not found in ENSDF')
        errors += 1; continue
    
    tl = ens_levels[ex_v]
    # Find matching gamma
    match = [tg for tg in tl['g_list'] if abs(float(tg[0]) - float(eg_v)) < 0.3]
    if not match:
        print(f'FAIL: [{idx}] L{ex_v} G{eg_v} not found in ENSDF')
        errors += 1; continue
    
    tg = match[0]  # best match
    ok = True
    
    # Check each field
    checks = []
    # E
    if tg[0] != eg_v: checks.append(f'EG: src={eg_v} ens={tg[0]}')
    # DE
    if tg[1] != eg_d: checks.append(f'DE: src=({eg_d}) ens=({tg[1]})')
    # RI
    if tg[2] != ri_v: checks.append(f'RI: src={ri_v} ens={tg[2]}')
    # DRI
    if tg[3] != ri_d: checks.append(f'DRI: src=({ri_d}) ens=({tg[3]})')
    # Flag X
    if has_star and tg[5] != 'X': checks.append('X flag missing')
    if not has_star and tg[5] == 'X': checks.append('Unexpected X flag')
    
    if checks:
        print(f'FAIL: [{idx}] L{ex_v} G{eg_v}: {"; ".join(checks)}')
        errors += 1
    else:
        print(f'OK:   [{idx}] L{ex_v} G{eg_v} RI={ri_v}({ri_d}) M={tg[4]} star={has_star}')

print(f'\n{len(indices)} checked, {errors} errors')
if errors == 0: print('PASS: All 15 random spot checks verified')
else: print(f'FAIL: {errors} error(s) found')
