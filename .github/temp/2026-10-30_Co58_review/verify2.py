import re
D = r"d:/X/ND/ENSDF/XUNDL/A58/Co58/new/"
def lines(p): return [l.ljust(80) for l in open(p, encoding="utf-8", errors="replace").read().split("\n")]
AD = lines(D + "Co58_adopted.ens")
adt = []; cur = None
for i, l in enumerate(AD, 1):
    try: e = float(l[9:19])
    except: e = None
    if l[5] == " " and l[6] == " " and l[7] == "L" and e is not None:
        cur = dict(line=i, E=e, DE=l[19:21].strip(), J=l[22:39].strip(), x="", xl=None)
        adt.append(cur)
    elif cur and l[5] == "X" and l[7] == "L":
        if cur["xl"] is None: cur["xl"] = i
        cur["x"] += re.sub(r"^XREF(\+=|=)", "", l[9:80].strip())

print("adopted g.s. level:", "L%d:%d" % (adt[0]["line"], adt[0]["xl"]), "E=", adt[0]["E"], "XREF=", adt[0]["x"])
miss = [c for c in "ABCDEFGHIJKLMNOPQRS" if c not in amd] if False else []
for c in "ABCDEFGHIJKLMNOPQRS":
    if c not in adt[0]["x"]:
        print("   missing letter on g.s.:", c)

CASES = [("Co58_56fe_a_d.ens", 18, "G"), ("Co58_58fe_3he_t.ens", 13, "L"),
         ("Co58_58ni_d_2he.ens", 20, "M"), ("Co58_58ni_d_2he.ens", 46, "M"),
         ("Co58_60ni_d_a_pol_d_a.ens", 76, "S"), ("Co58_59co_3he_a.ens", 34, "R")]
for fn, ln, letter in CASES:
    d = lines(D + fn)[ln - 1]
    try: de = float(d[9:19])
    except: de = None
    print(f"\n=== {fn}:{ln}  E={de} DE={d[19:21].strip()!r} J={d[22:39].strip()!r}")
    print("    ", d.rstrip())
    cands = [v for v in adt if abs(v["E"] - de) <= 25]
    for v in cands:
        has = letter in re.sub(r"\([^)]*\)", "", v["x"])
        print(f"    adopted L{v['line']}:{v['xl']} E={v['E']} DE={v['DE']!r} gap={de-v['E']:+.1f} [{'HAS ' if has else 'no '}{letter}] XREF={v['x']}")
    if not cands:
        n = min(adt, key=lambda v: abs(v["E"] - de))
        print(f"    adopted nearest L{n['line']} E={n['E']} gap={de-n['E']:+.1f} XREF={n['x']}")
# how many levels does each dataset list at 0.0?
for fn in ["Co58_56fe_a_d.ens", "Co58_58fe_3he_t.ens", "Co58_58ni_d_2he.ens"]:
    L = lines(D + fn)
    hits = [(i, l[9:19].strip()) for i, l in enumerate(L, 1) if l[5] == " " and l[6] == " " and l[7] == "L" and l[9:19].strip() in ("0.0", "0")]
    print(fn, "zero-energy level records:", hits)
