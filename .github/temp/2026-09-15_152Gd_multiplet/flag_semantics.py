"""Empirically test ENSDF col-77 flag semantics against the local corpus.

For every G-record carrying a non-blank col-77 flag, count how many OTHER G-records
in the SAME file share the identical Egamma text (true multiply-placed placement)
versus how many share only a near-equal energy (unresolved multiplet).
"""
import os
import sys
from collections import Counter, defaultdict

OUT = open(r"D:\X\ND\ENSDF\.github\temp\flag_semantics.txt", "w", encoding="utf-8")
ROOT = r"D:\X\ND\ENSDF"

stats = defaultdict(Counter)          # flag -> {'exact':n,'near':n,'alone':n}
examples = defaultdict(list)

for dp, dn, fn in os.walk(ROOT):
    if ".git" in dp:
        continue
    for f in fn:
        if not f.lower().endswith(".ens"):
            continue
        p = os.path.join(dp, f)
        try:
            lines = [l.rstrip("\r") for l in open(p, encoding="ascii", errors="ignore")]
        except Exception:
            continue
        gm = []
        for i, l in enumerate(lines, 1):
            if len(l) < 78 or l[5] != " " or l[6] != " " or l[7] != "G":
                continue
            gm.append((i, l[9:19].strip(), l[76], l))
        if not gm:
            continue
        by_e = defaultdict(list)
        for i, e, fl, l in gm:
            by_e[e].append((i, fl))
        for i, e, fl, l in gm:
            if fl == " " or not fl.isprintable():
                continue
            exact = len(by_e[e]) - 1
            near = 0
            if exact == 0:
                try:
                    ev = float(e)
                except ValueError:
                    continue
                for e2 in by_e:
                    if e2 == e:
                        continue
                    try:
                        if abs(float(e2) - ev) <= 1.5:
                            near += 1
                    except ValueError:
                        pass
            key = "exact" if exact else ("near" if near else "alone")
            stats[fl][key] += 1
            if len(examples[fl]) < 6:
                examples[fl].append((os.path.relpath(p, ROOT), i, e, key))

for fl in sorted(stats):
    c = stats[fl]
    total = sum(c.values())
    print(f"flag '{fl}': total={total} "
          f"exact-duplicate={c['exact']} ({c['exact']*100.0/total:.1f}%) "
          f"near-only={c['near']} ({c['near']*100.0/total:.1f}%) "
          f"no-partner={c['alone']} ({c['alone']*100.0/total:.1f}%)", file=OUT)
    for ex in examples[fl]:
        print(f"    e.g. {ex[0]}:{ex[1]} E={ex[2]} [{ex[3]}]", file=OUT)
OUT.close()
print("done")
