"""Level-energy offset statistics: source Table II Ei vs target .ens L-record."""
import re
from collections import Counter

AST = "\u2217"
SRC = r"D:\X\ND\ENSDF\XUNDL\2026OSAA_CT11035_152Gd_Table_II.md"
ENS = r"D:\X\ND\ENSDF\XUNDL\2026OSAA_CT11035_152Gd.ens"
OUT = open(r"D:\X\ND\ENSDF\.github\temp\level_offsets.txt", "w", encoding="utf-8")


def num(txt):
    m = re.search(r"-?\d+(?:\.\d+)?", txt.replace(AST, ""))
    return float(m.group(0)) if m else None


src_levels = []
for i, line in enumerate(open(SRC, encoding="utf-8").read().split("\n"), 1):
    if not line.startswith("|") or line.startswith("| :") or "E_i" in line:
        continue
    c = [x.strip() for x in line.strip("|").split("|")]
    if len(c) < 5:
        continue
    e = num(c[0])
    if e is not None and (not src_levels or src_levels[-1][0] != e):
        src_levels.append((e, c[0], i))

ens = [l.rstrip("\r") for l in open(ENS, encoding="ascii", errors="ignore")]
tlev = []
for i, l in enumerate(ens, 1):
    l = l.ljust(80)
    if l[5] == " " and l[6] == " " and l[7] == "L":
        tlev.append((num(l[9:19]), i))

print(f"source levels={len(src_levels)} target L-records={len(tlev)}", file=OUT)
d = Counter()
for e, txt, ln in src_levels:
    if e == 0:
        continue
    best = min(tlev, key=lambda t: abs(t[0] - e))
    off = round(best[0] - e, 2)
    d[off] += 1
print("offset histogram (target - source, keV):", file=OUT)
for k in sorted(d):
    print(f"   {k:+.2f}: {d[k]}", file=OUT)
big = []
for e, txt, ln in src_levels:
    if e == 0:
        continue
    best = min(tlev, key=lambda t: abs(t[0] - e))
    if abs(best[0] - e) > 0.05:
        big.append((e, txt, ln, best[0], best[1]))
print(f"\nlevels with |offset| > 0.05 keV: {len(big)}", file=OUT)
for b in big:
    print(f"   source Ei={b[1]} (Table II line {b[2]}) -> target {b[3]} (ens line {b[4]})", file=OUT)

# 3271.97 block content check
print("\n--- target block for L 3271.73 ---", file=OUT)


def num_any(t):
    return num(t)


sr = [r for r in open(SRC, encoding="utf-8").read().split("\n")
      if r.startswith("| 3271.97")]
print("source level 3271.97 rows:", file=OUT)
for r in sr:
    print("   ", r, file=OUT)
for i, l in enumerate(ens, 1):
    if l.ljust(80)[5] == " " and l.ljust(80)[6] == " " and l.ljust(80)[7] == "L" \
            and abs((num(l[9:19]) or -1) - 3271.73) < 0.005:
        print(f"target L at line {i}, gammas:", file=OUT)
        for j in range(i, min(i + 10, len(ens))):
            w = ens[j].ljust(80)
            if w[5] == " " and w[6] == " " and w[7] == "G":
                print("   ", j + 1, repr(ens[j][:80]), file=OUT)
            if w[5] == " " and w[6] == " " and w[7] == "L":
                break
OUT.close()
print("done")
