"""Probe: match Table VI energies to placed G-records in the .ens to infer RI normalization."""
import json, os, re

ENS = r"d:\X\ND\ENSDF\XUNDL\2026OSAA_CT11035_152Gd.ens"
HERE = os.path.dirname(os.path.abspath(__file__))
rows = json.load(open(os.path.join(HERE, 'table_vi_rows.json')))

gs = []          # placed G records only (those preceded by an L record)
seen_L = False
eline = 0
for ln, line in enumerate(open(ENS, encoding='utf-8'), 1):
    s = line.rstrip('\n')
    if len(s) < 21:
        continue
    typ = s[7] if len(s) > 7 else ' '
    if typ == 'L':
        seen_L = True
    if typ == 'G' and seen_L:
        e = s[9:19].strip()
        ri = s[22:29].strip()
        gs.append((ln, e, ri))
    if typ == 'E':
        eline = ln
print("placed G records:", len(gs))
print("G records with E-notation in RI:", [(a, b, c) for a, b, c in gs if 'E' in c][:10])

def f(x):
    try:
        return float(x)
    except Exception:
        return None

pairs = []
for r in rows:
    ev = f(r['e'])
    best = min(gs, key=lambda g: abs((f(g[1]) or 1e9) - ev))
    d = abs((f(best[1]) or 1e9) - ev)
    if d <= 0.10:
        pairs.append((d, r['e'], r['e_dec'], r['ri'], r['dri'], best[1], best[2], best[0]))
pairs.sort()
print("candidate matches (|dE|<=0.10 keV):", len(pairs))
for p in pairs[:40]:
    d, te, td, tri, tdri, ge, gri, gln = p
    ratio = ''
    if tri and gri:
        try:
            ratio = "ratio=%.3f" % (float(tri) / float(gri))
        except Exception:
            ratio = 'n/a'
    print("dE=%.3f tableE=%s(%s dgts) tableI=%s(%s) ensE=%s ensI=%s line=%d %s" % (d, te, td, tri, tdri, ge, gri, gln, ratio))
