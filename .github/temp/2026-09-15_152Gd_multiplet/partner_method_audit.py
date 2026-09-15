"""Partner-search audit: how the 53 asterisked rows pair, and the method's caveats."""
import io
import re

TOL = 1.0
SRC = r"D:\X\ND\ENSDF\XUNDL\2026OSAA_CT11035_152Gd_Table_II.md"
rows = []
for i, l in enumerate(io.open(SRC, encoding="utf-8").read().split("\n"), 1):
    l = l.rstrip("\r")
    if not l.startswith("|") or l.startswith("| :") or "E_i" in l:
        continue
    c = [x.strip() for x in l.strip("|").split("|")]
    if len(c) < 5:
        continue
    rows.append(dict(ln=i, ei=c[0], eg=c[1], ig=c[2],
                     E=float(re.match(r"-?\d+(?:\.\d+)?", c[1]).group(0)), ast="*" in c[2]))

ast = sorted([r for r in rows if r["ast"]], key=lambda z: (z["E"], z["ln"]))
dist, same_lvl, at_edge = {}, 0, 0
for r in ast:
    p = [q for q in rows if q is not r and abs(q["E"] - r["E"]) <= TOL]
    d = sorted(abs(q["E"] - r["E"]) for q in p)
    dist[len(p)] = dist.get(len(p), 0) + 1
    same_lvl += sum(1 for q in p if q["ei"] == r["ei"])
    if d and d[0] > TOL - 0.05:
        at_edge += 1
        print("edge case: {} vs {}".format(r["eg"], min(p, key=lambda q: abs(q["E"] - r["E"]))["eg"]))
print("partners per asterisked record:", sorted(dist.items()))
print("pairs sharing the same parent level:", same_lvl)
print("records whose nearest partner sits within 0.05 keV of the window edge:", at_edge)
near = max((min(abs(q["E"] - r["E"]) for q in rows if q is not r and abs(q["E"] - r["E"]) <= TOL),
            r["eg"]) for r in ast)
print("largest distance to a nearest partner: {:.2f} keV (row {})".format(near[0], near[1]))
print("largest distance over all listed pairs: {:.2f} keV".format(
    max(abs(q["E"] - r["E"]) for r in ast for q in rows if q is not r and abs(q["E"] - r["E"]) <= TOL)))
