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

def show(fn, lo, hi, letter):
    print(f"\n=== {fn} levels in [{lo},{hi}] ; letter={letter}")
    for i, l in enumerate(lines(D + fn), 1):
        try: e = float(l[9:19])
        except: continue
        if l[5] == " " and l[6] == " " and l[7] == "L" and lo <= e <= hi:
            print(f"   dataset line {i}: E={e} DE={l[19:21].strip()!r} J={l[22:39].strip()!r}  |{l.rstrip()}")
    for v in adt:
        if lo - 5 <= v["E"] <= hi + 5:
            has = letter in re.sub(r"\([^)]*\)", "", v["x"])
            print(f"   adopted L{v['line']}/{v['xl']}: E={v['E']} DE={v['DE']!r} [{'HAS' if has else 'no'} {letter}] XREF={v['x']}")

show("Co58_58ni_d_2he.ens", 3350, 3450, "M")
show("Co58_60ni_d_a_pol_d_a.ens", 2790, 2900, "S")
show("Co58_59co_3he_a.ens", 2200, 2280, "R")
show("Co58_58ni_d_2he.ens", 0, 1, "M")
