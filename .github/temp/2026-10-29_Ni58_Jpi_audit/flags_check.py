import re
from collections import defaultdict, Counter

p = r"d:/X/ND/ENSDF/XUNDL/A58/Ni58/new/Ni58_adopted.ens"
L = open(p, encoding="utf-8", errors="replace").read().split("\n")

def g(l, a, b):
    return l.ljust(80)[a - 1:b]

def isnum(s):
    return bool(re.match(r"^[\d.]+", s.strip() or ""))

blocks = []
cur = None
for i, l in enumerate(L, 1):
    rt = g(l, 8, 8); c6 = g(l, 6, 6); c7 = g(l, 7, 7)
    if rt == "L" and c7 == " " and c6 in (" ", "X") and isnum(g(l, 10, 19)):
        cur = dict(line=i, E=g(l, 10, 19).strip(), J=g(l, 22, 39).strip(),
                   f77=g(l, 77, 77), ms=g(l, 78, 79).strip(), q=g(l, 80, 80),
                   xref="", com=[], flags="", l56=g(l, 56, 64).strip())
        blocks.append(cur)
    elif cur and rt == "L" and c6 == "X":
        cur["xref"] = g(l, 10, 80).replace("XREF=", "").strip()
    elif cur and rt == "L" and c6 == "F":
        cur["flags"] = g(l, 10, 80).strip()
    elif cur and c7 == "c" and rt == "L":
        cur["com"].append(g(l, 10, 80).rstrip())

# --- defined flags from header comments ---
defined = {}
for b in blocks[:40]:
    pass
for i, l in enumerate(L[:200], 1):
    if g(l, 7, 8) == "cL" or g(l, 6, 8) in ("2cL", "3cL", "4cL", "5cL", "6cL", "7cL"):
        t = g(l, 10, 80).rstrip()
        m = re.match(r"BAND\(([A-Za-z])\)\$", t) or re.match(r"SEQ\(([A-Za-z])\)\$", t)
        if m:
            defined[m.group(1)] = t.split("$", 1)[1]
        m2 = re.match(r"J\(([A-Za-z])\)\s*\$?", t)
        if m2:
            defined[m2.group(1)] = t

print("DEFINED FLAGS:", sorted(defined))
print()
used = Counter()
for b in blocks:
    for ch in (b["f77"] + b["ms"]).strip():
        if ch.strip():
            used[ch] += 1
print("USED FLAGS:", dict(sorted(used.items())))
print("UNDEFINED:", [k for k in used if k not in defined])
print()

print("=== levels with J but NO J-comment and NO flag and no L-transfer ===")
for b in blocks:
    if not b["J"]:
        continue
    hasJ = any(c.startswith("J$") or c.startswith("J ") or c.startswith("J(") for c in b["com"])
    fl = (b["f77"] + b["ms"]).strip()
    if not hasJ and not fl:
        print(f"  line{b['line']:>5} E={b['E']:<10} J={b['J']:<14} q={b['q']}")
print()

print("=== J-comment text vs J field (flag mismatch) ===")
for b in blocks:
    js = [c for c in b["com"] if c.startswith("J$") or c.startswith("J(") or c.startswith("J ")]
    if not js:
        continue
    txt = " ".join(js)
    # collect candidate J values in comment
    cands = re.findall(r"\(?\d+(?:/\d+)?[+\-]?\)?", txt)
    print(f"  line{b['line']:>5} E={b['E']:<9} J=[{b['J']}]  :: {txt[:110]}")
