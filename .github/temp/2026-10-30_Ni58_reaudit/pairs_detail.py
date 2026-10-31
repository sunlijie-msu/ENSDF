import re
p = r"d:/X/ND/ENSDF/XUNDL/A58/Ni58/new/Ni58_adopted.ens"
L = open(p, encoding="utf-8", errors="replace").read().split("\n")

def g(l, a, b):
    return l.ljust(80)[a - 1:b]

print("=== column of flag characters on L records (sample) ===")
from collections import Counter
c = Counter()
for l in L:
    if g(l, 8, 8) == "L" and g(l, 7, 7) == " " and g(l, 6, 6) in (" ", "X"):
        for col in (77, 78, 79, 80):
            ch = g(l, col, col)
            if ch.strip():
                c[(col, ch)] += 1
for k in sorted(c):
    print("  col", k[0], repr(k[1]), c[k])

print("\n=== full records + comments for the contested pairs ===")
targets = ["9870", "11080", "9631.4", "9632", "15241.8", "15241.9", "10209", "10214", "11158", "11165"]
for i, l in enumerate(L, 1):
    if g(l, 8, 8) == "L" and g(l, 7, 7) == " " and g(l, 6, 6) in (" ", "X") and g(l, 10, 19).strip() in targets:
        print(f"--- L{i}: {l[:80]}")
        # print following lines until next level
        j = i
        while j < len(L):
            nl = L[j]
            if g(nl, 8, 8) == "L" and g(nl, 7, 7) == " " and g(nl, 6, 6) in (" ", "X") and re.match(r"^[\d.]+", g(nl, 10, 19).strip() or ""):
                break
            print("      " + nl[:80].rstrip())
            j += 1
