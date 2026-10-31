import re
p = r"d:/X/ND/ENSDF/XUNDL/A58/Ni58/new/Ni58_adopted.ens"
L = open(p, encoding="utf-8", errors="replace").read().split("\n")

def g(l, a, b):
    return l.ljust(80)[a - 1:b]

def val(s):
    s = s.strip()
    if not s:
        return None
    m = re.match(r"^([\d.]+)E(\d+)$", s)
    if m:
        return float(m.group(1)) * 10 ** int(m.group(2))
    if re.match(r"^[\d.]+(\+X)?$", s):
        return float(s.replace("+X", ""))
    return None

levels = []
cur = None
for i, l in enumerate(L, 1):
    rt = g(l, 8, 8); c6 = g(l, 6, 6); c7 = g(l, 7, 7)
    if rt == "L" and c7 == " " and c6 in (" ", "X") and val(g(l, 10, 19)) is not None:
        cur = dict(line=i, Eraw=g(l, 10, 19).strip(), E=val(g(l, 10, 19)),
                   DE=g(l, 20, 21).strip(), J=g(l, 22, 39).strip(),
                   T=g(l, 40, 49).strip(), f77=g(l, 77, 77), q=g(l, 80, 80),
                   xref="", com=[])
        levels.append(cur)
    elif cur is not None and rt == "L" and c6 == "X":
        cur["xref"] = g(l, 10, 80).replace("XREF=", "").strip()
    elif cur is not None and c7 == "c" and rt == "L":
        cur["com"].append(g(l, 10, 80).rstrip())

blank = [v for v in levels if not v["J"]]
print("TOTAL LEVELS:", len(levels), " BLANK J:", len(blank))

print("\n=== all pairs with dE < 1.0 keV ===")
srt = sorted(levels, key=lambda v: v["E"])
for a, b in zip(srt, srt[1:]):
    if abs(b["E"] - a["E"]) < 1.0:
        print(f"  L{a['line']:>4} {a['Eraw']:<10} DE={a['DE']:<3} J={a['J']:<10} XREF={a['xref']:<22} || "
              f"L{b['line']:>4} {b['Eraw']:<10} DE={b['DE']:<3} J={b['J']:<10} XREF={b['xref']}")

print("\n=== BLANK-J LIST (sorted by energy) ===")
for v in blank:
    hedge = "HEDGE" if any(re.search(r"suggest", c) and c.startswith("J") for c in v["com"]) else ""
    res = "RES" if any(re.search(r"(giant|GQR|GDR|ISGDR|broad)", c) for c in v["com"]) else ""
    tagn = "BX" if v["Eraw"].endswith("+X") else ""
    print(f"L{v['line']:>4}  E={v['Eraw']:<10} DE={v['DE']:<3} T={v['T']:<8} flag={v['f77']}{v['q']:<2} "
          f"XREF={v['xref']:<26} {hedge:5} {res:3} {tagn}")
