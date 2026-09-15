"""Generate the markdown evidence table (53 rows) for the multiplet report."""
import re

AST = "\u2217"
TOL = 1.0
SRC_MD = r"D:\X\ND\ENSDF\XUNDL\2026OSAA_CT11035_152Gd_Table_II.md"
ENS = r"D:\X\ND\ENSDF\XUNDL\2026OSAA_CT11035_152Gd.ens"
OUT = r"D:\X\ND\ENSDF\.github\temp\multiplet_table_rows.md"


def num(txt):
    m = re.search(r"-?\d+(?:\.\d+)?", txt.replace(AST, ""))
    return float(m.group(0)) if m else None


rows = []
for i, line in enumerate(open(SRC_MD, encoding="utf-8").read().split("\n"), 1):
    if not line.startswith("|") or line.startswith("| :") or "E_i" in line:
        continue
    c = [x.strip() for x in line.strip("|").split("|")]
    if len(c) < 5:
        continue
    rows.append(dict(ln=i, ei=c[0], eg=c[1], ig=c[2], ef=c[3], jf=c[4],
                     E=num(c[1]), I=num(c[2]), ast=AST in c[2]))

ens = [l.rstrip("\r") for l in open(ENS, encoding="ascii", errors="ignore")]
cur = None
trecs = []
for i, l in enumerate(ens, 1):
    l = l.ljust(80)
    if l[5] != " ":
        continue
    if l[6] == " " and l[7] == "L":
        cur = dict(ln=i, E=num(l[9:19]))
    elif l[6] == " " and l[7] == "G" and cur:
        trecs.append(dict(ln=i, E=num(l[9:19]), RI=num(l[22:29]), flag=l[76], lvl=cur["E"]))

ast = sorted([r for r in rows if r["ast"]], key=lambda z: z["E"])
lines, unresolved = [], []
for k, r in enumerate(ast, 1):
    cand = [t for t in trecs if abs(t["E"] - r["E"]) < 0.005 and t["RI"] is not None
            and abs(t["RI"] - r["I"]) < 1e-9]
    if len(cand) != 1:
        flags = {t["flag"] for t in cand}
        unresolved.append((r["ln"], r["eg"], r["ig"], [(t["ln"], t["E"], t["RI"], t["flag"]) for t in cand]))
        if cand and len(flags) == 1:
            tln, tflag = "/".join(str(t["ln"]) for t in cand), cand[0]["flag"]
        else:
            tln, tflag = "?", "?"
    else:
        tln, tflag = cand[0]["ln"], cand[0]["flag"]
    part = [q for q in rows if q is not r and abs(q["E"] - r["E"]) <= TOL]
    exact = [q for q in part if abs(q["E"] - r["E"]) < 0.005]
    cls = "same $E_\\gamma$" if exact else "near-degenerate"
    ps = []
    for q in sorted(part, key=lambda z: abs(z["E"] - r["E"])):
        eq = "=" if abs(q["I"] - r["I"]) < 1e-12 else "&#8800;"
        ps.append(f"{q['E']:.2f}{AST if q['ast'] else ''} (&#916;{q['E']-r['E']:+.2f}, $I_\\gamma$ {eq} {q['I']})")
    lines.append("| {} | {} | {} | {} | {} | {} | {} | `{}` | {} | {} |".format(
        k, r["ln"], r["ei"], r["eg"], r["ig"], r["ef"], tln, tflag, cls, "<br>".join(ps)))

open(OUT, "w", encoding="utf-8").write("\n".join(lines) + "\n")
with open(OUT.replace(".md", "_notes.txt"), "w", encoding="utf-8") as fh:
    fh.write("rows written: {}\n".format(len(lines)))
    fh.write("ambiguous target matches: {}\n".format(len(unresolved)))
    for u in unresolved:
        fh.write("   {}\n".format(u))
    fh.write("flag tally: {}\n".format({f: sum(1 for x in lines if "`{}`".format(f) in x)
                                        for f in ["*", "@", "&", " "]}))
print("rows written:", len(lines))
