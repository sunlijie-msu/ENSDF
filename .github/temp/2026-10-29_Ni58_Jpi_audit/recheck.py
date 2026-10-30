import re
p = r"d:/X/ND/ENSDF/XUNDL/A58/Ni58/new/Ni58_adopted.ens"
L = open(p, encoding="utf-8", errors="replace").read().split("\n")

def g(l, a, b):
    return l.ljust(80)[a - 1:b]

print("--- header footnote definitions J(..) and their delimiter ---")
for i, l in enumerate(L, 1):
    if g(l, 7, 8) in ("cL", "CL") and re.match(r"^J\([A-Za-z]\)", g(l, 10, 80)):
        t = g(l, 10, 80)
        print(f"  L{i}: has_$={'$' in t[:8]!s:5} {t[:52]!r}")

print("\n--- level records 3451.0 / 5394.3 / 5359.6 / 4574.3 flags (cols 77-80) ---")
for i, l in enumerate(L, 1):
    if g(l, 8, 8) == "L" and g(l, 7, 7) == " " and g(l, 6, 6) in (" ", "X") and g(l, 10, 19).strip() in ("3451.0", "5394.3", "5359.6", "4574.3"):
        print(f"  L{i}: cols77-80={g(l,77,80)!r} full={l[:80]!r}")

print("\n--- count of ' cL J' records lacking '$' ---")
n = 0
for l in L:
    if g(l, 6, 8) == " cL" and g(l, 10, 10) == "J" and g(l, 11, 11) != "$":
        n += 1
print("  total:", n)
