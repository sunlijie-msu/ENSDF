import re
from itertools import combinations

p = r"d:/X/ND/ENSDF/XUNDL/A58/Ni58/new/Ni58_adopted.ens"
L = open(p, encoding="utf-8", errors="replace").read().split("\n")

def g(l, a, b):
    return l.ljust(80)[a - 1:b]

def isnum(s):
    return bool(re.match(r"^[\d.]+$", s.strip() or ""))

levels = []
cur = None
for i, l in enumerate(L, 1):
    rt = g(l, 8, 8); c6 = g(l, 6, 6); c7 = g(l, 7, 7)
    if rt == "L" and c7 == " " and c6 in (" ", "X") and isnum(g(l, 10, 19)):
        cur = dict(line=i, Eraw=g(l, 10, 19).strip(), E=float(g(l, 10, 19)),
                   DE=g(l, 20, 21).strip(), J=g(l, 22, 39).strip(),
                   T=g(l, 40, 49).strip(), DT=g(l, 50, 55).rstrip(),
                   f77=g(l, 77, 77), f78=g(l, 78, 79).strip(), q=g(l, 80, 80),
                   xref="", com=[], flaglines=[])
        levels.append(cur)
    elif cur is not None and rt == "L" and c6 == "X":
        cur["xref"] = g(l, 10, 80).replace("XREF=", "").strip()
    elif cur is not None and rt == "L" and c6 == "F" and "FLAG=" in l:
        cur["flaglines"].append(g(l, 10, 80).strip())
    elif cur is not None and c7 == "c" and rt == "L":
        cur["com"].append(g(l, 10, 80).rstrip())

def xset(x):
    s = set()
    for tok in x.split("(")[0:1]:
        pass
    # letters outside parentheses
    outside = re.sub(r"\([^)]*\)", "", x)
    for ch in outside:
        if ch.isalpha():
            s.add(ch)
    return s

print("=== A. level pairs with |dE| <= 6 keV (shared dataset letters) ===")
for a, b in combinations(levels, 2):
    if abs(a["E"] - b["E"]) > 6:
        continue
    shared = xset(a["xref"]) & xset(b["xref"])
    flag = "SHARED-DATA" if shared else ""
    print(f"  L{a['line']:>4} {a['Eraw']:>9}({a['DE'] or '-'}) J={a['J'] or '[':9} XREF={a['xref']:<28} || "
          f"L{b['line']:>4} {b['Eraw']:>9}({b['DE'] or '-'}) J={b['J'] or '[':9} XREF={b['xref']:<28} "
          f"shared={''.join(sorted(shared)) or '-'} {flag}")

print("\n=== B. levels with BLANK J ===")
n = 0
for v in levels:
    if v["J"]:
        continue
    n += 1
    jc = [c for c in v["com"] if c.startswith("J") or "$" in c[:4]]
    print(f"{n:>3}. L{v['line']:>4} E={v['Eraw']:<10} DE={v['DE']:<3} T={v['T']:<9} DT={v['DT']:<7} "
          f"flag77={v['f77']} flag78={v['f78']:<3} q={v['q']} XREF={v['xref']:<30} FLAG= {v['flaglines']}")
    for c in v["com"]:
        print(f"       | {c}")
print("total blank J:", n)
