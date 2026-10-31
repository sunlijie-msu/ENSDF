import re
from collections import Counter, defaultdict
BASE = r"XUNDL/A58/Ni58/new/"
MAP = {
 "A":"Ni58_ec_decay_3.204_s.ens","B":"Ni58_58ni_n_nP_n_nPg.ens","C":"Ni58_58ni_p_pP_pol_p_pP_p_pPg.ens",
 "D":"Ni58_58ni_a_aP.ens","E":"Ni58_58ni_g_gP_pol_g_gP.ens","F":"Ni58_58ni_e_eP.ens","G":"Ni58_60ni_p_t.ens",
 "H":"Ni58_58ni_3he_3heP.ens","I":"Ni58_58ni_d_dP.ens","J":"Ni58_coulex.ens","K":"Ni58_54fe_6li_d.ens",
 "L":"Ni58_54fe_7li_t.ens","M":"Ni58_54fe_12c_8be.ens","N":"Ni58_54fe_16o_12c.ens","O":"Ni58_56fe_3he_n.ens",
 "P":"Ni58_56fe_a_2ng.ens","Q":"Ni58_58ni_18o_18oP.ens","R":"Ni58_45sc_16o_p2ng.ens","S":"Ni58_48ti_12c_2ng.ens",
 "T":"Ni58_28si_36ar_a2pg.ens","U":"Ni58_40ca_24mg_a2pg.ens","V":"Ni58_58ni_16o_16oP.ens",
 "W":"Ni58_59zn_ecp_decay_178.6_ms.ens","X":"Ni58_58ni_6li_6liP.ens","Y":"Ni58_59cu_p_decay_mixed.ens",
 "Z":"Ni58_ni_k-_xg.ens","#":"Ni58_9be_74kr_58nig.ens","j":"Ni58_4he_58ni_4heP_58ni_4he.ens"}

def L(p): return [x.rstrip("\n").ljust(80) for x in open(BASE+p, encoding="utf-8", errors="replace")]

def parse(rec):
    e = rec[9:19].strip(); d = rec[19:21].strip()
    m = re.match(r"^([0-9.]+)(?:E([+-]?\d+))?$", e.replace(" ", ""))
    if not m: return None, 0.0
    mant, exp = m.group(1), int(m.group(2)) if m.group(2) else 0
    E = float(mant)*10.0**exp
    dec = exp - (len(mant.split(".")[1]) if "." in mant else 0)
    return E, (int(d)*10.0**dec if d.isdigit() else 0.0)

PK = {}
for k, v in MAP.items():
    rows = []
    for i, l in enumerate(L(v), 1):
        if l[5] == " " and l[6] == " " and l[7] == "L":
            E, s = parse(l)
            if E is not None: rows.append((E, s, i))
    PK[k] = sorted(rows)

AD = [x.rstrip("\n").ljust(80) for x in open(BASE+"Ni58_adopted.ens", encoding="utf-8", errors="replace")]
lv = [i for i, l in enumerate(AD, 1) if l[5] == " " and l[6] == " " and l[7] == "L"]
ads = []
for k, i in enumerate(lv):
    E, s = parse(AD[i-1])
    if E is None: continue
    end = lv[k+1] if k+1 < len(lv) else len(AD)+1
    xs = ""
    for n in range(i+1, end):
        if "XREF" in AD[n-1]: xs += re.sub(r"^XREF[+=]?", "", AD[n-1][9:80].strip())
        if AD[n-1][7] == "G" and AD[n-1][5] == " ": break
    ads.append((E, s, xs, i))

def toks(xs):
    out = []; i = 0
    KEY = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz#")
    while i < len(xs):
        c = xs[i]
        if c in KEY:
            lab = c; i += 1; mod = ""
            if i < len(xs) and xs[i] == "(":
                j = xs.find(")", i)
                if j < 0: break
                mod = xs[i:j+1]; i = j + 1
            out.append((lab, mod))
        else: i += 1
    return out

find = []
stats = Counter()
for lab in MAP:
    P = PK[lab]
    if not P: continue
    claim = {}            # peak index -> [(adopted E, tok)]
    order = []
    for E, s, xs, ln in ads:
        for L_, mod in toks(xs):
            if L_ != lab: continue
            order.append((E, s, mod, ln))
    # pass 1: numeric parentheticals claim their stated peak
    for E, s, mod, ln in order:
        num = re.search(r"\(([0-9.]+)", mod)
        if not num: continue
        stated = float(num.group(1))
        best = min(range(len(P)), key=lambda i: abs(P[i][0]-stated))
        if abs(P[best][0]-stated) > 2.0:
            find.append(("PHANTOM-ENERGY", lab, E, mod, None, P[best][0], ln)); stats["PHANTOM-ENERGY"] += 1
        else:
            claim.setdefault(best, []).append((E, mod, ln))
    # pass 2: bare / starred tokens take nearest FREE peak within window
    for E, s, mod, ln in order:
        if re.search(r"\([0-9]", mod): continue
        W = 20.0
        free = [i for i in range(len(P)) if i not in claim]
        if not free:
            find.append(("NO-FREE-LEVEL", lab, E, mod, None, None, ln)); stats["NO-FREE-LEVEL"] += 1; continue
        best = min(free, key=lambda i: abs(P[i][0]-E))
        if abs(P[best][0]-E) > W:
            find.append(("NO-LEVEL-IN-WINDOW", lab, E, mod, None, P[best][0], ln)); stats["NO-LEVEL-IN-WINDOW"] += 1
        else:
            claim.setdefault(best, []).append((E, mod, ln))
    # shared without star
    for i, lst in claim.items():
        if len(lst) > 1 and any("*" not in m for _, m, _ in lst):
            for E, mod, ln in lst:
                if "*" not in mod:
                    find.append(("SHARED-NO-STAR", lab, E, mod, P[i][0], P[i][0], ln)); stats["SHARED-NO-STAR"] += 1
    # swapped parenthetical: a free peak closer to the adopted level exists
    for E, s, mod, ln in order:
        if not re.search(r"\([0-9]", mod): continue
        mine = [i for i, lst in claim.items() if any(x[0] == E and x[1] == mod for x in lst)]
        if not mine: continue
        d_mine = abs(P[mine[0]][0]-E)
        free = [i for i in range(len(P)) if i not in claim]
        if not free: continue
        alt = min(free, key=lambda i: abs(P[i][0]-E))
        if abs(P[alt][0]-E) < d_mine - 1.0:
            find.append(("SWAPPED", lab, E, mod, P[mine[0]][0], P[alt][0], ln)); stats["SWAPPED"] += 1
    # orphans: unclaimed dataset peak with a citing adopted level nearby
    for i in range(len(P)):
        if i in claim: continue
        cand = [(abs(E-P[i][0]), E, mod, ln) for E, s, mod, ln in order]
        if not cand: continue
        d, E, mod, ln = min(cand)
        if d <= 20.0 and d < 20.0:
            find.append(("ORPHAN-PEAK", lab, E, mod, P[i][0], P[i][0], ln)); stats["ORPHAN-PEAK"] += 1

print("checks flagged:", sum(stats.values()), dict(stats))
seen = set()
for kind, lab, E, mod, a, b, ln in find:
    key = (kind, lab, round(E, 1))
    if key in seen: continue
    seen.add(key)
    extra = "" if a is None or b is None else f" cited {a:g} / better {b:g}"
    print(f"  {kind:<18} {lab}  adopted {E:>8}  token {mod or '(plain)':<10}{extra}")
