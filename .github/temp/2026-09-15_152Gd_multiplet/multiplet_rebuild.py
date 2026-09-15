"""Rebuild 152Gd multiplet evidence from current Table II (source) and target .ens.

For every asterisk-marked row in Table II, list:
  - the target G-record(s) with the same Egamma and their col-77 flag
  - all source rows whose Egamma is within TOL keV (candidate unresolved multiplet partners)
  - all target G-records whose Egamma is within TOL keV (with parent level energy)
"""
import re
import sys
from collections import defaultdict

OUT = open(r"D:\X\ND\ENSDF\.github\temp\multiplet_rebuild.txt", "w", encoding="utf-8")
sys.stdout = OUT

AST = "\u2217"
TOL = 2.0

SRC = r"D:\X\ND\ENSDF\XUNDL\2026OSAA_CT11035_152Gd_Table_II.md"
ENS = r"D:\X\ND\ENSDF\XUNDL\2026OSAA_CT11035_152Gd.ens"


def num(txt):
    m = re.search(r"-?\d+(?:\.\d+)?", txt.replace("*", ""))
    return float(m.group(0)) if m else None


# ---------------- source ----------------
rows = []
for i, line in enumerate(open(SRC, encoding="utf-8").read().split("\n"), 1):
    if not line.startswith("|") or line.startswith("| :") or "E_i" in line:
        continue
    c = [x.strip() for x in line.strip("|").split("|")]
    if len(c) < 5:
        continue
    rows.append(dict(
        ln=i, ei=c[0], eg=c[1], ig=c[2], ef=c[3], jf=c[4],
        E=num(c[1]), I=num(c[2]), ast=AST in c[2]))

# ---------------- target ----------------
ens = [l.rstrip("\r") for l in open(ENS, encoding="ascii", errors="ignore")]
cur_level = None
trecs = []
for i, l in enumerate(ens, 1):
    if len(l) < 80:
        l = l.ljust(80)
    if l[5] != " ":
        continue
    if l[7] == "L" and l[6] == " ":
        cur_level = dict(ln=i, E=num(l[9:19]), DE=l[19:21], J=l[22:39].strip())
    elif l[7] == "G" and l[6] == " " and cur_level is not None:
        trecs.append(dict(ln=i, E=num(l[9:19]), DE=l[19:21], RI=l[22:29].strip(),
                          DRI=l[29:31].strip(), flag=l[76], q=l[79],
                          lvl=cur_level["E"], lvl_ln=cur_level["ln"], lvl_J=cur_level["J"]))

ast_rows = [r for r in rows if r["ast"]]
print(f"source rows={len(rows)}  asterisked={len(ast_rows)}  target G-records={len(trecs)}")
print(f"TOL={TOL} keV\n")

for k, r in enumerate(ast_rows, 1):
    tgt = [t for t in trecs if t["E"] is not None and abs(t["E"] - r["E"]) < 0.005]
    tgt_txt = " ; ".join(
        f"ens L{t['ln']} lvl={t['lvl']} E={t['E']:.2f}({t['DE']}) RI={t['RI']}({t['DRI']}) flag='{t['flag']}' q='{t['q']}'"
        for t in tgt) or "NO EXACT MATCH"
    print(f"[{k:2d}] src L{r['ln']}: Ei={r['ei']} Eg={r['eg']} Ig={r['ig']} Ef={r['ef']}")
    print(f"     target: {tgt_txt}")
    part = [q for q in rows if q is not r and q["E"] is not None
            and abs(q["E"] - r["E"]) <= TOL]
    for q in sorted(part, key=lambda z: abs(z["E"] - r["E"])):
        same_i = q["I"] is not None and r["I"] is not None and abs(q["I"] - r["I"]) < 1e-12
        sum_i = (q["I"] is not None and r["I"] is not None and abs(q["I"] + r["I"] - r["I"]) < 1e-12)
        print(f"       partner dE={q['E']-r['E']:+.2f} src L{q['ln']}: Ei={q['ei']} Eg={q['eg']} "
              f"Ig={q['ig']}{'*' if q['ast'] else ''} Ef={q['ef']} equalIg={'Y' if same_i else 'n'}")
    tp = [t for t in trecs if t["E"] is not None and 0 < abs(t["E"] - r["E"]) <= TOL]
    for t in sorted(tp, key=lambda z: abs(z["E"] - r["E"]))[:4]:
        print(f"       ens-partner dE={t['E']-r['E']:+.2f} L{t['ln']} lvl={t['lvl']} "
              f"E={t['E']:.4f}({t['DE']}) RI={t['RI']}({t['DRI']}) flag='{t['flag']}'")
    print()
