import re
p = r"d:/X/ND/ENSDF/XUNDL/A58/Ni58/new/Ni58_adopted.ens"
L = open(p, encoding="utf-8", errors="replace").read().split("\n")

def g(l, a, b):
    return l.ljust(80)[a - 1:b]

defined = {}
for i, l in enumerate(L, 1):
    r78 = g(l, 7, 8)
    if r78 != "cL" and r78 != "c ":
        tag = "MALFORMED(" + r78 + ")"
    else:
        tag = None
    t = g(l, 10, 80)
    for m in re.finditer(r"([A-Za-z]{1,4})\(([A-Za-z])\)\s*\$?", t):
        sym, fl = m.group(1), m.group(2)
        if sym in ("BAND", "SEQ", "J", "E", "T", "M", "RI", "MR"):
            defined.setdefault(fl, []).append((i, m.group(0).rstrip(), tag))

print("DEFINED FLAGS:")
for k in sorted(defined):
    print(f"  {k:2}: {defined[k]}")

used = {}
for i, l in enumerate(L, 1):
    if g(l, 8, 8) in ("L", "G") and g(l, 7, 7) == " " and g(l, 6, 6) in (" ", "X") and re.match(r"^[\d.]+", g(l, 10, 19).strip() or ""):
        f = (g(l, 78, 79).strip() or g(l, 77, 77).strip())
        if f and f not in ("*", "@", "&"):
            used.setdefault(f, 0)
            used[f] += 1

print("\nUSED but NOT DEFINED:", [k for k in sorted(used) if k not in defined])
print("DEFINED but NOT USED:", [k for k in sorted(defined) if k not in used])
