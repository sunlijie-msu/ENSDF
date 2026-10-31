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

res = []
stats = Counter()
staruse = Counter()
for E, s, xs, ln in ads:
    for lab, mod in toks(xs):
        if "*" in mod: staruse[(lab, mod)] += 1

for lab, P in PK.items():
    if not P: continue
    claim = defaultdict(list)
    mine = []
    for E, s, xs, ln in ads:
        for L_, mod in toks(xs):
            if L_ != lab: continue
            num = re.search(r"\(([0-9.]+)", mod)
            if num:
                stated = float(num.group(1))
                i = min(range(len(P)), key=lambda k: abs(P[k][0]-stated))
                if abs(P[i][0]-stated) > 2.0:
                    stats["PHANTOM-ENERGY"] += 1
                    res.append(("PHANTOM-ENERGY", lab, E, mod, stated, P[i][0], ln))
                    continue
            else:
                i = min(range(len(P)), key=lambda k: abs(P[k][0]-E))
            claim[i].append((E, mod, ln))
            mine.append((E, mod, ln, i))
    for E, mod, ln, i in mine:
        d = abs(P[i][0]-E)
        W = max(20.0, 2.0*P[i][1])
        starred = "*" in mod
        if d > W:
            stats["FABRICATED-LEVEL"] += 1
            res.append(("FABRICATED-LEVEL", lab, E, mod, P[i][0], d, ln))
        elif len(claim[i]) > 1 and not starred:
            stats["SHARED-NO-STAR"] += 1
            res.append(("SHARED-NO-STAR", lab, E, mod, P[i][0], d, ln))
        if "*" in mod and staruse[(lab, mod)] < 2:
            stats["STAR-ONCE"] += 1
            res.append(("STAR-ONCE", lab, E, mod, P[i][0], d, ln))
        if re.search(r"\([0-9]", mod):
            free = [k for k in range(len(P)) if k not in claim or claim[k] == []]
            free = [k for k in range(len(P)) if not claim[k]]
            if free:
                alt = min(free, key=lambda k: abs(P[k][0]-E))
                if abs(P[alt][0]-E) < d - 1.0:
                    stats["SWAPPED"] += 1
                    res.append(("SWAPPED", lab, E, mod, P[i][0], P[alt][0], ln))

print("flagged:", sum(stats.values()), dict(stats))
seen = set()
for kind, lab, E, mod, a, b, ln in sorted(res, key=lambda x: (x[0], x[1], x[2])):
    key = (kind, lab, round(E, 1))
    if key in seen: continue
    seen.add(key)
    print(f"  {kind:<17} {lab}  adopted {E:>8}  {mod or '(plain)':<11} level {a}  -> {b}")
