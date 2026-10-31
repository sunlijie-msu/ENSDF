import re, math
from collections import Counter, defaultdict

P = r"d:/X/ND/ENSDF/XUNDL/A58/Fe58/new/Fe58_adopted.ens"
L = open(P, encoding="utf-8", errors="replace").read().split("\n")

def g(l, a, b):
    return l.ljust(80)[a-1:b]

def val(s):
    s = s.strip()
    if not s: return None
    m = re.match(r"^([\d.]+)E(\d+)$", s)
    if m: return float(m.group(1)) * 10 ** int(m.group(2))
    try: return float(s)
    except ValueError: return None

print("total lines:", len(L))

# ---------- 1. record inventory ----------
inv = Counter()
for l in L:
    inv[g(l, 6, 8)] += 1
print("\nrecord-type inventory (cols6-8):")
for k, v in sorted(inv.items()):
    print(f"   {k!r:8} {v}")

# ---------- 2. length check ----------
print("\nlength != 80 (non-empty):")
bad = [(i, len(l)) for i, l in enumerate(L, 1) if l.strip() and len(l.rstrip()) != 80]
print("  ", bad[:10], "count", len(bad))

# ---------- 3. Q record ----------
print("\nQ record fields:")
for i, l in enumerate(L, 1):
    if g(l, 8, 8) == "Q":
        for a, b in [(10,19),(20,21),(22,29),(30,31),(32,39),(40,41),(42,49),(50,51),(52,59),(60,61),(62,73),(74,80)]:
            print(f"   {a:>2}-{b:<2} [{g(l,a,b)}]")

# ---------- 4. levels & gammas ----------
levels, gammas = [], []
cur = None
for i, l in enumerate(L, 1):
    rt = g(l, 8, 8); c6 = g(l, 6, 6); c7 = g(l, 7, 7)
    if rt == "L" and c7 == " " and c6 in (" ", "X") and val(g(l, 10, 19)) is not None:
        cur = dict(line=i, Eraw=g(l, 10, 19).strip(), E=val(g(l, 10, 19)),
                   DE=val(g(l, 20, 21)), J=g(l, 22, 39).strip(), T=g(l, 40, 49).strip(),
                   xref="", com=[], gams=[], jcol=None, flag=(g(l,77,79)).strip(), q=g(l,80,80))
        j = 21
        while j < 39 and l.ljust(80)[j] == " ": j += 1
        cur["jcol"] = j + 1
        levels.append(cur)
    elif cur and rt == "L" and c6 == "X":
        cur["xref"] = g(l, 10, 80).replace("XREF=", "").strip()
    elif cur and c7 == "c" and rt == "L":
        cur["com"].append((i, g(l, 10, 80).rstrip()))
    elif rt == "G" and c7 == " " and c6 == " " and cur and val(g(l, 10, 19)) is not None:
        gg = dict(line=i, E=val(g(l, 10, 19)), DE=val(g(l, 20, 21)),
                  RI=g(l, 22, 29), DRI=g(l, 29, 31), Mraw=g(l, 31, 45), q=g(l, 80, 80), owner=cur, FL=None)
        gi = 21
        while gi < 29 and l.ljust(80)[gi] == " ": gi += 1
        gg["ricol"] = gi + 1
        cur["gams"].append(gg); gammas.append(gg)
    elif rt == "G" and c6.upper() == "F" and gammas and "FL=" in l:
        gammas[-1]["FL"] = l.split("FL=")[1].strip()

print(f"\nlevels: {len(levels)}   gammas: {len(gammas)}")

print("\n=== A. J-field not starting at column 23 ===")
cnt = Counter()
for v in levels:
    if v["J"] and v["jcol"] != 23:
        cnt[v["jcol"]] += 1
        print(f"  L{v['line']:>5} col{v['jcol']}  J={v['J']!r:<14} E={v['Eraw']}")
print("  distribution:", dict(cnt))

print("\n=== B. gamma RI field start column (expect 23 when RI present) ===")
cnt = Counter()
ex = defaultdict(list)
for gg in gammas:
    if gg["RI"].strip():
        cnt[gg["ricol"]] += 1
        if gg["ricol"] != 23 and len(ex[gg["ricol"]]) < 4:
            ex[gg["ricol"]].append((gg["line"], gg["RI"]))
print("  distribution:", dict(cnt))
for k, v in ex.items():
    print(f"   col {k}: {v}")

print("\n=== C. ENERGY CONSERVATION: Egamma > Elevel ===")
for v in levels:
    for gg in v["gams"]:
        if gg["E"] is not None and v["E"] is not None and gg["E"] > v["E"] + 0.001:
            print(f"  L{v['line']:>5} level {v['Eraw']} ({v['J']}) : gamma {gg['E']} (line {gg['line']}) exceeds level by {gg['E']-v['E']:.3f}")

print("\n=== D. gamma ordering inside level (descending/out of order) ===")
for v in levels:
    es = [(gg["E"], gg["line"]) for gg in v["gams"] if gg["E"] is not None]
    for (e1, l1), (e2, l2) in zip(es, es[1:]):
        if e2 < e1 - 0.001:
            print(f"  L{v['line']:>5} E={v['Eraw']}: gamma {e1} (line {l1}) followed by smaller {e2} (line {l2})")

print("\n=== E. duplicate comment identifiers in one L block ===")
for v in levels:
    ids = []
    for i, c in v["com"]:
        m = re.match(r"^([A-Za-z]{1,3}(?:\([A-Za-z]\))?)\$", c)
        ids.append(m.group(1) if m else "general")
    c2 = Counter(x for x in ids if x != "general")
    for k, n in c2.items():
        if n > 1:
            print(f"  L{v['line']:>5} E={v['Eraw']}: identifier {k}$ appears {n} times")

print("\n=== F. comment identifiers without '$' (col10 SYM, no $ in first 10 chars) ===")
n = 0
for i, l in enumerate(L, 1):
    c7 = g(l, 7, 7); rt = g(l, 8, 8); c6 = g(l, 6, 6)
    if c7 != "c": continue
    t = g(l, 10, 80)
    m = re.match(r"^([A-Za-z]{1,4}(?:_?\([A-Za-z]\))?)\s+(\S)", t)
    if m and "$" not in t[:len(m.group(1)) + 2] and m.group(2) not in ("$",):
        # possible identifier followed by spaces then text
        if re.match(r"^[A-Za-z]{1,3}(\([A-Za-z]\))?\s{2,}\S", t) or re.match(r"^[A-Za-z]{1,3}\s{2,}\S", t):
            n += 1
            if n <= 25:
                print(f"  line {i}: {t[:60]!r}")
print("  total:", n)
