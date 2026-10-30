import re
p = r"d:/X/ND/ENSDF/XUNDL/A58/Ni58/new/Ni58_adopted.ens"
L = open(p, encoding="utf-8", errors="replace").read().split("\n")

def g(l, a, b):
    return l.ljust(80)[a - 1:b]

defined = {}   # flag -> (line, identifier)
for i, l in enumerate(L, 1):
    r78 = g(l, 7, 8)
    if r78.lower() != "cL":
        continue
    t = g(l, 10, 80)
    for m in re.finditer(r"\b([A-Za-z]{1,4})\(([A-Za-z])\)\s*\$", t):
        defined.setdefault(m.group(2), []).append((i, m.group(0)))

print("flags defined via SYM(FLAG)$ on cL records:")
for k in sorted(defined):
    print(f"  {k}: {defined[k]}")

# used flags on L records
used = {}
for i, l in enumerate(L, 1):
    if g(l, 8, 8) == "L" and g(l, 7, 7) == " " and g(l, 6, 6) in (" ", "X") and re.match(r"^[\d.]+", g(l, 10, 19).strip() or ""):
        f = (g(l, 78, 79).strip() or g(l, 77, 77).strip())
        if f:
            used.setdefault(f, []).append(i)

print("\nflags used on L records and where (line, E, J):")
for k in sorted(used):
    ex = []
    for ln in used[k][:2]:
        l = L[ln - 1]
        ex.append(f"L{ln} E={g(l,10,19).strip()} J={g(l,22,39).strip()}")
    print(f"  {k} ({len(used[k])}x): {ex}")

print("\nCL uppercase records in other workspace files (sample scan):")
import glob, os
for f in ["A36/A36_30September2026.ens", "A60/A60_13NDS.ens", "A34/A34_30September2026.ens", "A35/A35_2026Su18.ens"]:
    if not os.path.exists(f):
        continue
    n = sum(1 for l in open(f, encoding="utf-8", errors="replace") if l.ljust(80)[6:8] == "CL")
    print(f"  {f}: {n}")
