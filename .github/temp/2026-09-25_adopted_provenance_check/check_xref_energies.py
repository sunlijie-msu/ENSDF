"""Check every parenthetical XREF energy in the adopted dataset against the level
energies actually present in the referenced dataset.

XREF notation:  X(1234?)  ->  dataset X has a level at 1234 keV (here questionable).
The quoted energy must be traceable to a level of that dataset.

Usage: python check_xref_energies.py [--fix-list]
"""
import glob
import os
import re
import sys

ADOPTED = r'A34/S34/new/S34_adopted.ens'
NEW = r'A34/S34/new'
TOL = 1.0          # keV, accepted difference between quoted and dataset level
PLAIN_MIN = 2.0    # keV, offset above which a plain letter is worth reporting


def norm(s):
    s = s.lower()
    s = s.replace("'", 'p').replace('+', 'p').replace(',', ' ').replace('(', ' ')
    s = s.replace(')', ' ').replace(':', ' ').replace('=', ' ').replace('-', ' ')
    return re.sub(r'[^a-z0-9.]+', ' ', s)


def levels_of(path):
    out = []
    for l in open(path, encoding='utf-8', newline='').read().split('\r\n'):
        if len(l) >= 20 and l[7] == 'L' and l[5:7] == '  ' and l[6] != 'c':
            try:
                out.append((float(l[9:19]), l[9:19].strip()))
            except ValueError:
                pass
    return out


# --- tag -> file mapping -------------------------------------------------
tagmap = {}
for l in open(ADOPTED, encoding='utf-8', newline='').read().split('\r\n'):
    if len(l) > 9 and l[7] == 'X' and l[5:7] == '  ':
        tagmap[l[8]] = l[9:].strip()

files = [f for f in sorted(glob.glob(os.path.join(NEW, '*.ens')))
         if os.path.basename(f) != 'S34_adopted.ens']
titles = {}
for f in files:
    head = open(f, encoding='utf-8', newline='').read().split('\r\n')[0]
    titles[f] = norm(head[9:42]) if len(head) > 42 else norm(head[9:])

mapping, lvl_cache = {}, {}
for tag, desc in tagmap.items():
    nd = norm(desc).strip()
    best = None
    for f in files:
        if titles[f].strip() == nd:
            best = f
            break
    if best is None:                                  # fallback: token overlap
        toks = [t for t in nd.split() if t]
        bs = 0.0
        for f in files:
            score = sum(1 for t in toks if t in titles[f]) / len(toks)
            if score > bs:
                best, bs = f, score
    mapping[tag] = best
    if best:
        lvl_cache[tag] = levels_of(best)

print('tag -> dataset')
for tag in sorted(mapping):
    print(f"   {tag}  {tagmap[tag][:34]:<34} -> {os.path.basename(mapping[tag] or 'NONE')}")
print()

pat = re.compile(r'([A-Za-z])\((\d+(?:\.\d+)?)([*?]?)\)')
lines = open(ADOPTED, encoding='utf-8', newline='').read().split('\r\n')
stale = []
for i, l in enumerate(lines):
    if len(l) > 9 and l[5] == 'X' and l[7] == 'L':
        for tag, e, mod in pat.findall(l):
            lv = lvl_cache.get(tag)
            if not lv:
                continue
            quoted = float(e)
            near = min(lv, key=lambda x: abs(x[0] - quoted))
            d = abs(near[0] - quoted)
            # a quote is traceable only if it equals the dataset level rounded
            # to the precision of the quote itself
            dec = len(e.split('.')[1]) if '.' in e else 0
            tol = 0.5 * 10 ** (-dec) - 1e-9
            if d > tol:
                stale.append((i + 1, l[9:].strip(), tag, e, mod, near[1], d, os.path.basename(mapping[tag])))
print('STALE parentheticals (quoted value not traceable to a dataset level):', len(stale))
for s in stale:
    print(f"   XREF line {s[0]:>5}  [{s[2]}({s[3]}{s[4]})]  -> dataset level {s[5]} (dE={s[6]:.3f})  in {s[7]}")
    print(f"        {s[1]}")
print()
print('--- proposed replacements ---')
for s in stale:
    print(f"   line {s[0]:>5}: {s[2]}({s[3]}{s[4]})  ->  {s[2]}({s[5]}{s[4]})")

# --- reverse check: plain letters that arguably need a parenthetical --------
if '--plain' in sys.argv:
    print()
    print('--- plain letters whose dataset level lies outside the adopted DE range ---')
    for i, l in enumerate(lines):
        if not (len(l) > 9 and l[5] == 'X' and l[7] == 'L'):
            continue
        prev = lines[i - 1]
        try:
            ae = float(prev[9:19])
        except ValueError:
            continue
        dec = len(prev[9:19].split('.')[1].strip()) if '.' in prev[9:19] else 0
        mde = re.match(r'\s*(\d+)', prev[19:21])
        ade = int(mde.group(1)) * 10 ** (-dec) if mde else 0.0
        body = l[9:].strip()[5:]                      # drop 'XREF='
        for m in re.finditer(r'([A-Za-z])(\([^)]*\))?', body):
            tag, par = m.group(1), m.group(2)
            if not lvl_cache.get(tag):
                continue
            if par and not par.startswith('('):
                continue
            near = min(lvl_cache[tag], key=lambda x: abs(x[0] - ae))
            d = abs(near[0] - ae)
            # practice in this evaluation: a plain letter tolerates a few tenths of
            # keV; only clearly larger offsets are worth a parenthetical energy
            if d > max(ade, PLAIN_MIN) + 1e-9 and tag in ('A', 'B', 'C'):
                print(f"   line {i+1:>5}  adopted {prev[9:19].strip()}({prev[19:21].strip()}) "
                      f"{prev[22:39].strip():<12} {tag} plain -> dataset {near[1]} (dE={d:.3f})")

if '--tags' in sys.argv:
    print()
    print('--- dataset levels 3800-5500 keV for tags A, B, C ---')
    for tag in ('A', 'B', 'C'):
        print(f"  {tag} = {tagmap[tag]}  ({os.path.basename(mapping[tag])})")
        for e, raw in lvl_cache[tag]:
            if 3800 <= e <= 5500:
                print(f"        {raw}")
    print()
    print('--- every XREF that references tag A, B or C ---')
    for i, l in enumerate(lines):
        if len(l) > 9 and l[5] == 'X' and l[7] == 'L':
            letters = re.findall(r'([A-Za-z])(?:\([^)]*\))?', l[9:])
            if {'A', 'B', 'C'} & set(letters):
                print(f"   line {i+1:>5}  adopted L {lines[i-1][9:19].strip():<10} {lines[i-1][22:39].strip():<14} {l[9:].strip()}")
