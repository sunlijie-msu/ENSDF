import re
D = r"d:/X/ND/ENSDF/XUNDL/A58/Co58/new/"

def lines(p):
    return [l.ljust(80) for l in open(p, encoding="utf-8", errors="replace").read().split("\n")]

AD = lines(D + "Co58_adopted.ens")
# adopted levels with merged xref
adt = []
cur = None
for i, l in enumerate(AD, 1):
    try: e = float(l[9:19])
    except: e = None
    if l[5] == " " and l[6] == " " and l[7] == "L" and e is not None:
        cur = dict(line=i, E=e, DE=l[19:21].strip(), J=l[22:39].strip(), x="", xline=None)
        adt.append(cur)
    elif cur and l[5] == "X" and l[7] == "L":
        if cur["xline"] is None: cur["xline"] = i
        cur["x"] += re.sub(r"^XREF(\+=|=)", "", l[9:80].strip())

CASES = [("Co58_56fe_a_d.ens", 31, "G"), ("Co58_56fe_a_d.ens", 35, "G"),
         ("Co58_56fe_a_d.ens", 47, "G"), ("Co58_56fe_3he_p.ens", 63, "E"),
         ("Co58_58fe_p_n_p_ng.ens", 94, "K"), ("Co58_58fe_p_n_p_ng.ens", 101, "K")]

for fn, ln, letter in CASES:
    DL = lines(D + fn)
    d = DL[ln - 1]
    de = float(d[9:19].strip()); dde = d[19:21].strip(); dj = d[22:39].strip()
    print(f"\n=== dataset {fn}:{ln}  E={de} DE={dde!r} J={dj!r}")
    print(f"    {d.rstrip()}")
    cands = [v for v in adt if abs(v["E"] - de) <= 40]
    for v in cands:
        has = letter in re.sub(r"\([^)]*\)", "", v["x"])
        flag = "HAS " + letter if has else "no " + letter
        print(f"    adopted L{v['line']}:{v['xline']} E={v['E']} DE={v['DE']!r} J={v['J']!r}  [{flag}]  XREF={v['x']}  gap={de-v['E']:+.1f} keV")
    if not cands:
        near = min(adt, key=lambda v: abs(v["E"] - de))
        print(f"    adopted nearest: L{near['line']} E={near['E']} DE={near['DE']!r} gap={de-near['E']:+.1f} keV XREF={near['x']}")
