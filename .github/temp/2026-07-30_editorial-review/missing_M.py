#!/usr/bin/env python3
"""Identify G-records with empty M field where both parent + target Jpi known."""
import re

fp = r"d:\X\ND\ENSDF\XUNDL\A58\Fe58\old\Fe58_adopted.ens"
levels = {}; gammas = []; parent = None
with open(fp) as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    ln = i+1
    if len(line) < 10: continue
    c6,c7,c8 = line[5],line[6],line[7]
    if c6!=' ' or c7!=' ': continue
    if not line[:5].strip(): continue
    if c8 == 'L':
        e = line[9:19].strip()
        if e and e[0] in '0123456789.-':
            try: float(e)
            except: continue
            jpi = line[22:39].strip() if len(line)>39 else ''
            levels[e] = {'energy': float(e), 'jpi': jpi, 'line': ln}
            parent = e
    elif c8 == 'G':
        if parent:
            e = line[9:19].strip()
            if e:
                try: float(e)
                except: continue
                m = line[31:40].strip() if len(line)>40 else ''
                gammas.append({'estr': e, 'e': float(e), 'm': m, 'parent': parent, 'line': ln})

def find_target(pe, ge):
    exp = float(pe) - ge
    best, bd = None, 999
    for ek, lv in levels.items():
        d = abs(float(ek) - exp)
        if d < bd: bd, best = d, (ek, lv)
    if best and bd < 2.0:
        return best[0], best[1]['jpi']
    return None, None

def parse_j(j):
    if not j or j in ('','(',')'): return None,None
    j = j.strip()
    pi = None
    if j.endswith('+'): pi = '+'; j = j[:-1]
    elif j.endswith('-'): pi = '-'; j = j[:-1]
    j = j.strip('()')
    try:
        if '/' in j: s = float(j.split('/')[0])/float(j.split('/')[1])
        else: s = float(j)
    except: return None,None
    return s, pi

count = 0
print("Gammas with EMPTY M field but KNOWN Jpi on both parent and target:")
print("="*80)
for g in gammas:
    if g['m']: continue
    pj = levels.get(g['parent'], {}).get('jpi', '')
    te, tj = find_target(g['parent'], g['e'])
    if not pj or not tj: continue
    ps, pp = parse_j(pj)
    ts, tp = parse_j(tj)
    if ps is None or ts is None: continue
    if pp is None or tp is None: continue
    dj = abs(ps - ts)
    dp = (pp != tp)
    count += 1
    exp_m = []
    if dj <= 1:
        exp_m.append('E1(+M2)' if dp else 'M1(+E2)')
    elif dj == 2:
        exp_m.append('M2(+E3)' if dp else 'E2(+M3)')
    else:
        exp_m.append(f'O/H(ΔJ={int(dj)})')
    if count <= 50:
        print(f"L{g['line']}: G {g['estr']} parent={g['parent']}({pj}) target={te}({tj})  DJ={int(dj):.0f} dpi={dp}  expected: {','.join(exp_m)}")

print(f"\nTotal: {count} gammas with empty M where both Jpi known")
print(f"Of 250 empty-M gammas, {count} have Jpi known on both sides")
