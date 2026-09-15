"""Cross-check Table VI intensities against the previous evaluation's unplaced-gamma block (.old)."""
import json, os, re

OLD = r"d:\X\ND\ENSDF\XUNDL\152GD_152TB_EC_DECAY_17.5_H.old"
HERE = os.path.dirname(os.path.abspath(__file__))
rows = json.load(open(os.path.join(HERE, 'table_vi_rows.json')))

old = []
seen_L = False
for ln, line in enumerate(open(OLD, encoding='utf-8', errors='replace'), 1):
    s = line.rstrip('\n')
    if len(s) < 21:
        continue
    typ = s[7] if (len(s) > 7 and s[6] != 'c') else ' '
    if typ == 'L':
        if not seen_L:
            print("first L record in .old: line %d |%s|" % (ln, s))
        seen_L = True
    if typ == 'G' and not seen_L:
        old.append((ln, s[9:19].strip(), s[19:21].strip(), s[22:29].strip(), s[29:31].strip(), s))
print(".old unplaced G records:", len(old))
print(".old first/last energy:", old[0][1], old[-1][1])

def f(x):
    try:
        return float(x)
    except Exception:
        return None

matched = 0
for ln, oe, ode, ori, odri, raw in old:
    ov = f(oe)
    if ov is None:
        continue
    best = min(rows, key=lambda r: abs(float(r['e']) - ov))
    d = abs(float(best['e']) - ov)
    if d <= 0.15:
        matched += 1
        ratio = ''
        if ori and best['ri']:
            try:
                ratio = "ratio_table/old=%.3f" % (float(best['ri']) / float(ori))
            except Exception:
                ratio = ''
        print("dE=%.3f old=%s(%s) I=%s(%s) | table=%s I=%s(%s) %s" % (d, oe, ode, ori, odri, best['e'], best['ri'], best['dri'], ratio))
print("matched within 0.15 keV:", matched)
