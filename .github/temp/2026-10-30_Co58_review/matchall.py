import re, glob, os
from collections import defaultdict

D = r"d:/X/ND/ENSDF/XUNDL/A58/Co58/new/"
MAP = {"58co_it_decay_8.853_h":"A","51v_10b_p2ng":"B","55mn_a_ng":"C","56fe_t_ng":"D",
 "56fe_3he_p":"E","56fe_3he_pg":"F","56fe_a_d":"G","57fe_p_g":"H","57fe_d_n_d_ng":"I",
 "57fe_3he_d":"J","58fe_p_n_p_ng":"K","58fe_3he_t":"L","58ni_d_2he":"M","58ni_t_3he":"N",
 "59co_n_2ng":"O","59co_p_d":"P","59co_d_t":"Q","59co_3he_a":"R","60ni_d_a_pol_d_a":"S"}

def eu(raw, de):
    raw = raw.strip(); de = de.strip()
    try: v = float(raw)
    except: return None, None
    if not de or de in ("GT","LT","LE","GE"): return v, None
    try: d = float(de)
    except: return v, None
    nd = len(raw.split(".")[1]) if "." in raw else 0
    return v, d * 10 ** (-nd)

def lines(p): return [l.ljust(80) for l in open(p, encoding="utf-8", errors="replace").read().split("\n")]

# ---- adopted levels with per-letter reported energies
AD = lines(D + "Co58_adopted.ens")
adt, cur = [], None
for i, l in enumerate(AD, 1):
    v, u = eu(l[9:19], l[19:21])
    if l[5] == " " and l[6] == " " and l[7] == "L" and v is not None:
        cur = dict(line=i, E=v, DE=u, J=l[22:39].strip(), x="", xl=None)
        adt.append(cur)
    elif cur and l[5] == "X" and l[7] == "L":
        if cur["xl"] is None: cur["xl"] = i
        cur["x"] += re.sub(r"^XREF(\+=|=)", "", l[9:80].strip())

def cites(letter):
    """list of (adopted_level, reported_energy, label) for a dataset letter"""
    out = []
    for v in adt:
        for m in re.finditer(r"([A-Za-z])(?:\(([^)]*)\))?", v["x"]):
            if m.group(1) != letter: continue
            arg = m.group(2); e = v["E"]
            if arg:
                num = re.match(r"[\d.]+", arg)
                if num: e = float(num.group(0))
            out.append((v, e, m.group(0)))
    return out

# ---- reported-energy per letter: what does the adopted actually claim?
print("### A) 60Ni(d,a) = letter S : region 2750-2920")
S = lines(D + "Co58_60ni_d_a_pol_d_a.ens")
print("  dataset S levels:")
for i, l in enumerate(S, 1):
    v, u = eu(l[9:19], l[19:21])
    if l[5] == " " and l[6] == " " and l[7] == "L" and v is not None and 2750 <= v <= 2920:
        print(f"    S:{i}  E={v:g} ± {u if u is not None else '?'} J={l[22:39].strip()!r}")
print("  adopted levels citing S in the same window:")
for v, e, lab in cites("S"):
    if 2750 <= v["E"] <= 2920:
        print(f"    adopted L{v['line']}/{v['xl']} E={v['E']:g} ± {v['DE'] if v['DE'] is not None else '?'} → S reported as {e:g}  [{lab}]  XREF={v['x']}")

# ---- global check for every dataset letter
print("\n### B) global: dataset level vs adopted citations (overlap = |dE| <= DE_ds+DE_ad, min 2 keV)")
for fn, letter in sorted(MAP.items(), key=lambda kv: kv[1]):
    DL = lines(D + "Co58_" + fn + ".ens")
    lv = []
    for i, l in enumerate(DL, 1):
        v, u = eu(l[9:19], l[19:21])
        if l[5] == " " and l[6] == " " and l[7] == "L" and v is not None:
            lv.append((i, v, u))
    cit = cites(letter)
    orphan = []
    for i, v, u in lv:
        ok = False
        for av, e, lab in cit:
            tol = (u or 0) + (av["DE"] or 0)
            if tol < 2: tol = 2
            if abs(v - e) <= tol: ok = True; break
        if not ok: orphan.append((i, v, u))
    print(f"  {letter} {fn:<22} dataset levels {len(lv):>3}  adopted citations {len(cit):>3}  dataset levels with NO adopted home: {len(orphan)}")
    for o in orphan[:8]:
        print(f"       orphan dataset level: line {o[0]} E={o[1]:g} ± {o[2] if o[2] is not None else '?'}")
