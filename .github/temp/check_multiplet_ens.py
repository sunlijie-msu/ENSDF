"""Check which of the 53 asterisk-marked 152Gd gammas are multiply placed
in the target ENSDF file (same/ near-equal E-gamma in 2+ level blocks).
"""
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
SRC = r"D:\X\ND\ENSDF\XUNDL\2026OSAA_CT11035_152Gd_Table_II.md"
ENS = r"D:\X\ND\ENSDF\XUNDL\2026OSAA_CT11035_152Gd.ens"
AST = "\u2217"


def num(s):
    m = re.match(r"^\s*([0-9]+(?:\.[0-9]*)?)", s or "")
    return float(m.group(1)) if m else None


src_rows = []
for i, l in enumerate(open(SRC, encoding="utf-8").read().split("\n"), 1):
    if not l.startswith("|"):
        continue
    c = [x.strip() for x in l.strip("|").split("|")]
    if len(c) != 5 or c[0].startswith(":"):
        continue
    src_rows.append(
        dict(line=i, Ei=c[0], Eg=c[1], Ig=c[2], Ef=c[3], eg=num(c[1]), ast=AST in c[2])
    )
ast = [r for r in src_rows if r["ast"]]

# --- parse target: level blocks, G records ---
raw = open(ENS, encoding="ascii").read().split("\n")
grecs = []
cur_level = None
for i, l in enumerate(raw, 1):
    if len(l) < 9:
        continue
    if l[6] != " ":
        continue  # continuation record (col6 non-blank) or comment (col7 flag)
    if l[7] == "L":
        cur_level = float(l[9:19]) if l[9:19].strip() else None
        continue
    if l[7] == "G":
        eg = num(l[9:19])
        grecs.append(
            dict(
                line=i,
                level=cur_level,
                eg=eg,
                ig=l[22:29].strip(),
                flag=l[76] if len(l) > 76 else "",
            )
        )

print(f"target L blocks/G recs: {len(grecs)} G records")
print(f"\n{'srcLine':>7} {'Eg(src)':>10} {'Ig(src)':>14} | placements in .ens (level, Eg, Ig, flag)")

mult_placed = 0
for r in ast:
    hits = [g for g in grecs if g["eg"] is not None and abs(g["eg"] - r["eg"]) < 1e-9]
    near = [
        g
        for g in grecs
        if g["eg"] is not None and 1e-9 < abs(g["eg"] - r["eg"]) <= 1.0
    ]
    if len(hits) > 1:
        mult_placed += 1
    desc = "; ".join(
        f"L{g['level']} Eg={g['eg']} Ig={g['ig']} flag='{g['flag']}'@{g['line']}"
        for g in hits
    )
    ndesc = "; ".join(f"L{g['level']} Eg={g['eg']} Ig={g['ig']}" for g in near)
    print(f"{r['line']:>7} {r['Eg']:>10} {r['Ig']:>14} | n={len(hits)} {desc}")
    if ndesc:
        print(f"{'':>7} {'':>10} {'':>14} |   near(<=1keV): {ndesc}")

print(f"\nasterisk gammas with >1 exact placement in target: {mult_placed}/{len(ast)}")

# energy level list of target levels that host these gammas
print("\n=== target blocks hosting asterisk gammas (level -> n asterisk gammas) ===")
from collections import Counter

cnt = Counter()
for r in ast:
    for g in grecs:
        if g["eg"] is not None and abs(g["eg"] - r["eg"]) < 1e-9:
            cnt[g["level"]] += 1
for lv, n in sorted(cnt.items()):
    print(f"  L {lv}: {n}")
