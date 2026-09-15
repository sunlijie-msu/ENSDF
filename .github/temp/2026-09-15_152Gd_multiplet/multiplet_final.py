"""Final 152Gd multiplet evidence for the report.

Source of truth: 2026OSAA_CT11035_152Gd_Table_II.md (authors' update, footnote line 758)
                 and 2026OSAA_CT11035_152Gd_Table_II.csv (machine-readable, '*' appended to Ig)
Target:          2026OSAA_CT11035_152Gd.ens
"""
import re

AST = "\u2217"
TOL = 1.0
SRC_MD = r"D:\X\ND\ENSDF\XUNDL\2026OSAA_CT11035_152Gd_Table_II.md"
SRC_CSV = r"D:\X\ND\ENSDF\XUNDL\2026OSAA_CT11035_152Gd_Table_II.csv"
ENS = r"D:\X\ND\ENSDF\XUNDL\2026OSAA_CT11035_152Gd.ens"
OUT = open(r"D:\X\ND\ENSDF\.github\temp\multiplet_final.txt", "w", encoding="utf-8")


def p(*a):
    print(*a, file=OUT)


def num(txt):
    m = re.search(r"-?\d+(?:\.\d+)?", txt.replace(AST, ""))
    return float(m.group(0)) if m else None


# ---- source rows (Table II md) ----
rows = []
for i, line in enumerate(open(SRC_MD, encoding="utf-8").read().split("\n"), 1):
    if not line.startswith("|") or line.startswith("| :") or "E_i" in line:
        continue
    c = [x.strip() for x in line.strip("|").split("|")]
    if len(c) < 5:
        continue
    rows.append(dict(ln=i, ei=c[0], eg=c[1], ig=c[2], ef=c[3], jf=c[4],
                     E=num(c[1]), I=num(c[2]), ast=AST in c[2]))

# ---- source rows (csv) ----
csv_rows = []
for i, line in enumerate(open(SRC_CSV, encoding="utf-8-sig").read().split("\n"), 1):
    if not line.strip() or line.startswith("Ei,"):
        continue
    c = line.split(",")
    csv_rows.append(dict(ln=i, ei=c[0], eg=c[1], ig=c[2],
                         E=num(c[1]), I=num(c[2]), ast="*" in c[2]))

# ---- target ----
ens = [l.rstrip("\r") for l in open(ENS, encoding="ascii", errors="ignore")]
cur = None
trecs = []
for i, l in enumerate(ens, 1):
    l = l.ljust(80)
    if l[5] != " ":
        continue
    if l[6] == " " and l[7] == "L":
        cur = dict(ln=i, E=num(l[9:19]), J=l[22:39].strip())
    elif l[6] == " " and l[7] == "G" and cur:
        trecs.append(dict(ln=i, E=num(l[9:19]), RI=l[22:29].strip(), flag=l[76],
                          lvl=cur["E"], lvl_ln=cur["ln"]))

ast = [r for r in rows if r["ast"]]
p(f"src md rows={len(rows)} asterisked={len(ast)}   csv rows={len(csv_rows)} asterisked={sum(1 for r in csv_rows if r['ast'])}")
p(f"target L={sum(1 for i,l in enumerate(ens,1) if len(l.ljust(80))==80 and l.ljust(80)[5]==' ' and l.ljust(80)[7]=='L' and l.ljust(80)[6]==' ')} G={len(trecs)}")

key_md = sorted((r["ei"], r["eg"]) for r in ast)
key_csv = sorted((r["ei"], r["eg"]) for r in csv_rows if r["ast"])
p(f"md-vs-csv asterisk row set identical: {key_md == key_csv}")

p("")
p("=== per-asterisk evidence ===")
p("idx|srcLine|Ei|Eg|Ig|Ef|ensLine|ensFlag|class|partners")
nb = {}
for k, r in enumerate(sorted(ast, key=lambda z: z["E"]), 1):
    tgt = [t for t in trecs if abs(t["E"] - r["E"]) < 0.005]
    tl = ";".join(f"{t['ln']}:{t['flag']}" for t in tgt) or "NONE"
    part = [q for q in rows if q is not r and abs(q["E"] - r["E"]) <= TOL]
    exact = [q for q in part if abs(q["E"] - r["E"]) < 0.005]
    cls = "same-Eg" if exact else ("near" if part else "NONE")
    txt = []
    for q in sorted(part, key=lambda z: abs(z["E"] - r["E"])):
        eq = "eq" if abs(q["I"] - r["I"]) < 1e-12 else "NE"
        txt.append(f"{q['E']:.2f}{'*' if q['ast'] else ''}({q['E']-r['E']:+.2f},Ig={q['I']},{eq},L{q['ln']})")
    allnear = [q for q in rows if q is not r and abs(q["E"] - r["E"]) < 3.0]
    d = min((abs(q["E"] - r["E"]) for q in allnear), default=None)
    nb[r["ln"]] = d
    p(f"{k}|{r['ln']}|{r['ei']}|{r['eg']}|{r['ig']}|{r['ef']}|{tl}|{cls}|{' || '.join(txt)}")

p("")
p(f"class counts: same-Eg={sum(1 for r in ast if any(q is not r and abs(q['E']-r['E'])<0.005 for q in rows))}  "
  f"near={sum(1 for r in ast if not any(q is not r and abs(q['E']-r['E'])<0.005 for q in rows) and any(q is not r and abs(q['E']-r['E'])<=TOL for q in rows))}")
p(f"target col77 among asterisked rows: *={sum(1 for t in trecs if t['flag']=='*')} @={sum(1 for t in trecs if t['flag']=='@')} &={sum(1 for t in trecs if t['flag']=='&')}")

# base rate: how many of ALL 751 rows have a partner within 1.0 keV (different parent level)?
def has_partner(r, pool):
    return any(q is not r and abs(q["E"] - r["E"]) <= TOL for q in pool)

allrows = rows
n_with = sum(1 for r in allrows if has_partner(r, allrows))
n_ast_with = sum(1 for r in ast if has_partner(r, allrows))
p("")
p(f"base rate: rows with >=1 partner within +/-{TOL} keV (any row): {n_with}/{len(allrows)} = {100*n_with/len(allrows):.1f}%")
p(f"asterisked rows with >=1 partner within +/-{TOL} keV: {n_ast_with}/{len(ast)}")

OUT.close()
print("done")
