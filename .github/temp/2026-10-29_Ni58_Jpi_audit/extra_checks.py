import re
p = r"d:/X/ND/ENSDF/XUNDL/A58/Ni58/new/Ni58_adopted.ens"
L = open(p, encoding="utf-8", errors="replace").read().split("\n")

def g(l, a, b):
    return l.ljust(80)[a - 1:b]

print("=== A. levels with J>6 and NO parentheses (firm) ===")
for i, l in enumerate(L, 1):
    if g(l, 8, 8) == "L" and g(l, 7, 7) == " " and g(l, 6, 6) in (" ", "X") and re.match(r"^[\d.]+", g(l, 10, 19).strip() or ""):
        J = g(l, 22, 39).strip()
        if not J or "(" in J:
            continue
        for tok in J.split(","):
            m = re.match(r"^(\d+)", tok.strip())
            if m and int(m.group(1)) > 6:
                print(f"  line{i:>5} E={g(l,10,19).strip():<10} J={J:<12} flag={g(l,77,77)}{g(l,78,79).strip()}")

print()
print("=== B. comment records with uppercase/lowercase anomaly in col 7 (record type) ===")
from collections import Counter
c = Counter()
for i, l in enumerate(L, 1):
    if len(l) > 8:
        c[g(l, 6, 8)] += 1
for k, v in sorted(c.items()):
    if "c" in k.lower() and v < 200:
        print(f"  {k!r:8} {v}")

print()
print("=== C. near-degenerate levels (dE < 6 keV) ===")
lv = []
for i, l in enumerate(L, 1):
    if g(l, 8, 8) == "L" and g(l, 7, 7) == " " and g(l, 6, 6) in (" ", "X") and re.match(r"^[\d.]+", g(l, 10, 19).strip() or ""):
        e = g(l, 10, 19).strip()
        if "E" in e or "+" in e:
            continue
        lv.append((float(e), i, g(l, 22, 39).strip(), g(l, 20, 21).strip(), g(l, 77, 80).strip()))
lv.sort()
for a, b in zip(lv, lv[1:]):
    if b[0] - a[0] < 6:
        print(f"  {a[0]:>9} L{a[1]} J={a[2]:<10} DE={a[3]:<3} flag={a[4]:<4} || {b[0]:>9} L{b[1]} J={b[2]:<10} DE={b[3]:<3} flag={b[4]}")

print()
print("=== D. 'I' flagged levels and any cL I definition ===")
for i, l in enumerate(L, 1):
    if g(l, 8, 8) == "L" and g(l, 7, 7) == " " and g(l, 6, 6) in (" ", "X") and "I" in (g(l, 77, 79)):
        print(f"  USED line{i:>5} E={g(l,10,19).strip():<10} J={g(l,22,39).strip():<12} flag={g(l,77,79)}")
for i, l in enumerate(L, 1):
    if g(l, 7, 7) in ("c", "C") and g(l, 8, 8) == "L" and ("J(I)" in l or "BAND(I)" in l):
        print("  DEF?", i, l[:70])
