"""Re-derive 152Gd multiplet groupings from current Table II (2026OSAA).

Footnote: Asterisk (*) = "Multiplet gamma with unresolvable intensity.
Total multiplet intensity is given for each gamma."

That means: for each member of an unresolved multiplet the SAME (total)
intensity value is reported, i.e. the intensity is NOT divided between
placements -> ENSDF column-77 flag '&'.
"""
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
SRC = r"D:\X\ND\ENSDF\XUNDL\2026OSAA_CT11035_152Gd_Table_II.md"
AST = "\u2217"  # ASTERISK OPERATOR used by the source


def num(s):
    if s is None:
        return None
    m = re.match(r"^\s*([0-9]+(?:\.[0-9]*)?)", s)
    return float(m.group(1)) if m else None


rows = []
for i, line in enumerate(open(SRC, encoding="utf-8").read().split("\n"), 1):
    if not line.startswith("|"):
        continue
    c = [x.strip() for x in line.strip("|").split("|")]
    if len(c) != 5 or c[0].startswith(":"):
        continue
    rows.append(
        {
            "line": i,
            "Ei": c[0],
            "Eg": c[1],
            "Ig": c[2],
            "Ef": c[3],
            "Jp": c[4],
            "eg": num(c[1]),
            "ast": AST in c[2],
            "ig_clean": c[2].replace(AST, "").strip(),
        }
    )

ast = [r for r in rows if r["ast"]]
print("Table rows:", len(rows), "| asterisk rows:", len(ast))

# ---- 1. For each asterisk row, nearest neighbours at several tolerances ----
print("\n=== Asterisk rows: nearest E-gamma neighbour & I-gamma relation ===")
for tol in (0.1, 0.2, 0.3, 0.5):
    eq = ne = none = 0
    for r in ast:
        cand = [
            o
            for o in rows
            if o["line"] != r["line"]
            and o["eg"] is not None
            and abs(o["eg"] - r["eg"]) <= tol
        ]
        if not cand:
            none += 1
            continue
        # prefer identical I-gamma text
        if any(o["ig_clean"] == r["ig_clean"] for o in cand):
            eq += 1
        else:
            ne += 1
    print(
        f"  tol={tol:<4} neighbours w/ SAME I-gamma: {eq:2d}   "
        f"neighbours w/ DIFFERENT I-gamma: {ne:2d}   no neighbour: {none:2d}"
    )

# ---- 2. Multplet groups: identical I-gamma text + unresolvable dE ----
print("\n=== Candidate unresolved multiplets (same I-gamma, |dE|<0.5 keV) ===")


def compatible(a, b, tol=0.5):
    return a["eg"] is not None and b["eg"] is not None and abs(a["eg"] - b["eg"]) <= tol


candidates = [r for r in rows if r["eg"] is not None]
groups = []
for r in ast:
    placed = False
    for g in groups:
        if r["ig_clean"] == g[0]["ig_clean"] and any(compatible(r, m) for m in g):
            g.append(r)
            placed = True
            break
    if not placed:
        groups.append([r])

# attach every other table row that shares the I-gamma and is energy-coincident
for g in groups:
    for o in candidates:
        if o in g or o["line"] == g[0]["line"]:
            continue
        if o["ig_clean"] == g[0]["ig_clean"] and any(compatible(o, m) for m in g):
            g.append(o)
for g in groups:
    g.sort(key=lambda m: m["line"])

print(f"groups containing asterisk rows: {len(groups)}")
for gi, g in enumerate(groups, 1):
    dE = max(m["eg"] for m in g) - min(m["eg"] for m in g)
    print(
        f"\n[{gi}] I-gamma={g[0]['ig_clean']:<12} members={len(g)}  span={dE:.2f} keV"
    )
    for m in g:
        print(
            f"    L{m['line']:>4} Ei={m['Ei']:<14} Eg={m['Eg']:<14} "
            f"Ig={m['Ig']:<14} Ef={m['Ef']:<14} ast={'Y' if m['ast'] else 'n'}"
        )

# ---- 3. Every row that shares an energy with an asterisk row (pair check) ----
print("\n=== All rows within 0.5 keV of an asterisk row (incl. non-asterisk) ===")
seen = set()
for r in ast:
    for o in rows:
        if o["line"] == r["line"] or o["eg"] is None or r["eg"] is None:
            continue
        if abs(o["eg"] - r["eg"]) <= 0.5:
            key = (min(r["line"], o["line"]), max(r["line"], o["line"]))
            if key in seen:
                continue
            seen.add(key)
            same = "SAME" if o["ig_clean"] == r["ig_clean"] else "diff"
            print(
                f"  L{r['line']:>4} {r['Eg']:<13} Ig={r['ig_clean']:<13}ast  <->  "
                f"L{o['line']:>4} {o['Eg']:<13} Ig={o['ig_clean']:<13}"
                f"{'ast' if o['ast'] else '   '}  dE={abs(o['eg']-r['eg']):.2f}  Ig:{same}"
            )
