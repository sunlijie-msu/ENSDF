import re
from collections import Counter
p = r"d:/X/ND/ENSDF/XUNDL/A58/Ni58/new/Ni58_adopted.ens"
L = open(p, encoding="utf-8", errors="replace").read().split("\n")

def g(l, a, b):
    return l.ljust(80)[a - 1:b]

cur = None
stats = Counter()
noJ = []
for i, l in enumerate(L, 1):
    if g(l, 8, 8) == "L" and g(l, 7, 7) == " " and g(l, 6, 6) in (" ", "X") and re.match(r"^[\d.]+", g(l, 10, 19).strip() or ""):
        J = g(l, 22, 39).strip()
        stats["levels"] += 1
        if not J:
            stats["noJ"] += 1
            noJ.append((i, g(l, 10, 19).strip()))
        else:
            stats["J"] += 1
            if "(" in J: stats["paren"] += 1
            else: stats["firm"] += 1
            if "+" in J or "-" in J: stats["with_parity"] += 1
            if re.fullmatch(r"[\d./]+", J): stats["spin_only"] += 1
print(dict(stats))
print("blank-J levels:", len(noJ))
