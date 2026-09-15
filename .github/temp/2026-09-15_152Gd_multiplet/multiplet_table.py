"""Build the 152Gd multiplet classification table from Table II (source) + target .ens.

Grouping: single-linkage clusters of source rows whose Egamma differ by <= TOL keV
(TOL=1.0 is the operational "unresolvable multiplet" cut-off: every asterisked row's
nearest neighbour lies within 1.0 keV, and no further partners appear between 1 and 5 keV).

Writes a machine-generated evidence table to .github/temp/multiplet_groups.txt
"""
import re
import sys
from collections import defaultdict

AST = "\u2217"
TOL = 1.0
SRC = r"D:\X\ND\ENSDF\XUNDL\2026OSAA_CT11035_152Gd_Table_II.md"
OLD = r"D:\X\ND\ENSDF\XUNDL\2026OSAA_CT11035_152Gd_old_Table_I.md"
ENS = r"D:\X\ND\ENSDF\XUNDL\2026OSAA_CT11035_152Gd.ens"
OUT = open(r"D:\X\ND\ENSDF\.github\temp\multiplet_groups.txt", "w", encoding="utf-8")


def num(t):
    m = re.search(r"-?\d+(?:\.\d+)?", t.replace(AST, ""))
    return float(m.group(0)) if m else None


def parse_5col(path):
    rows = []
    for i, line in enumerate(open(path, encoding="utf-8").read().split("\n"), 1):
        if not line.startswith("|") or line.startswith("| :") or "E_i" in line:
            continue
        c = [x.strip() for x in line.strip("|").split("|")]
        if len(c) < 5:
            continue
        rows.append(dict(ln=i, ei=c[0], eg=c[1], ig=c[2], ef=c[3], jf=c[4],
                         E=num(c[1]), I=num(c[2]), ast=AST in c[2]))
    return rows


def parse_10col(path):
    rows = []
    for i, line in enumerate(open(path, encoding="utf-8").read().split("\n"), 1):
        if not line.startswith("|") or line.startswith("| :") or "E_i$" in line:
            continue
        c = [x.strip() for x in line.strip("|").split("|")]
        if len(c) < 8:
            continue
        rows.append(dict(ln=i, ei=c[0], ji=c[1], eg=c[2], ig=c[3], ef=c[4], jf=c[5],
                         E=num(c[2]), I=num(c[3]), ast=AST in c[3], ast_e=AST in c[2]))
    return rows


src = parse_5col(SRC)
old = parse_10col(OLD)
ast_new = sorted((r["ei"], r["eg"]) for r in src if r["ast"])
ast_old = sorted((r["ei"], r["eg"]) for r in old if r["ast"])
print(f"Table II rows={len(src)} asterisked={len(ast_new)}", file=OUT)
print(f"Table I  rows={len(old)} asterisked={len(ast_old)}", file=OUT)
print(f"asterisk key sets identical: {ast_new == ast_old}", file=OUT)
print(f"Table I rows with asterisk in BOTH Eg and Ig: "
      f"{sum(1 for r in old if r['ast'] and r['ast_e'])}", file=OUT)

# target G-records
ens = [l.rstrip("\r") for l in open(ENS, encoding="ascii", errors="ignore")]
lvl = None
tg = []
for i, l in enumerate(ens, 1):
    if len(l) < 80 or l[5] != " ":
        continue
    if l[7] == "L" and l[6] == " ":
        lvl = (i, num(l[9:19]))
    elif l[7] == "G" and l[6] == " " and lvl:
        tg.append(dict(ln=i, E=num(l[9:19]), RI=l[22:29].strip(), DRI=l[29:31].strip(),
                       flag=l[76], lvl=lvl[1], lvl_ln=lvl[0]))
print(f"target L-records/G-records: {sum(1 for l in ens if len(l)>=8 and l[5]==' ' and l[6]==' ' and l[7]=='L')}"
      f"/{len(tg)}", file=OUT)

# single-linkage grouping over the source table, sorted by Egamma
idx = sorted([r for r in src if r["E"] is not None], key=lambda r: r["E"])
groups, cur = [], [idx[0]]
for prev, r in zip(idx, idx[1:]):
    if r["E"] - prev["E"] <= TOL:
        cur.append(r)
    else:
        groups.append(cur)
        cur = [r]
groups.append(cur)

ast_groups = [g for g in groups if any(r["ast"] for r in g)]
print(f"\ntotal energy clusters={len(groups)}  clusters containing an asterisked row={len(ast_groups)}", file=OUT)

n_exact = n_near = 0
for g in sorted(ast_groups, key=lambda g: g[0]["E"]):
    print("\n" + "-" * 78, file=OUT)
    for r in g:
        flag = ""
        t = [x for x in tg if x["E"] is not None and abs(x["E"] - r["E"]) < 0.005
             and abs(x["lvl"] - num(r["ei"])) < 0.02]
        if t:
            flag = f" > ens L{t[0]['ln']} col77='{t[0]['flag']}'"
        print(f"  {'AST' if r['ast'] else '   '} src L{r['ln']:3d} Ei={r['ei']:14s} "
              f"Eg={r['eg']:16s} Ig={r['ig']:16s} Ef={r['ef']:12s}{flag}", file=OUT)
    igs = [r["ig"].replace(AST, "").strip() for r in g]
    asts = [r for r in g if r["ast"]]
    for a in asts:
        partners = [r for r in g if r is not a]
        if not partners:
            kind = "singleton"
        elif any(abs(r["E"] - a["E"]) < 0.005 for r in partners):
            kind = "same-Eg placement"
            n_exact += 1
        else:
            kind = "near-degenerate partner"
            n_near += 1
        eq = [r for r in partners if r["I"] is not None and a["I"] is not None
              and abs(r["I"] - a["I"]) < 1e-12]
        print(f"    -> ASTEROID Eg={a['eg']} Ig={a['ig']} : {kind}, "
              f"partners={len(partners)}, Ig equal to partner={bool(eq)}", file=OUT)

print(f"\nasterisked rows: same-Eg placement={n_exact} near-degenerate={n_near}", file=OUT)
OUT.close()
print("done")
