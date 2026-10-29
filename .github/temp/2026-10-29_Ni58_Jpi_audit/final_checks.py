p = r"d:/X/ND/ENSDF/XUNDL/A58/Ni58/new/Ni58_adopted.ens"
L = open(p, encoding="utf-8", errors="replace").read().split("\n")

def g(l, a, b):
    return l.ljust(80)[a - 1:b]

print("=== CL (uppercase C) records ===")
for i, l in enumerate(L, 1):
    if g(l, 7, 8) == "CL":
        print(i, repr(l))

print("\n=== cL J without '$' delimiter ===")
n = 0
for i, l in enumerate(L, 1):
    if g(l, 6, 8) == " cL" and g(l, 10, 10) == "J" and g(l, 11, 11) != "$":
        n += 1
        if n <= 4:
            print("  ", i, repr(l[:66]))
print("  total:", n)

print("\n=== selected level records (raw) ===")
for idx in [709, 719, 1217, 1219, 1465, 1473, 1475, 1513, 1516, 1739, 1742, 570]:
    print(f"L{idx+1:>5}", repr(L[idx][:80]))
