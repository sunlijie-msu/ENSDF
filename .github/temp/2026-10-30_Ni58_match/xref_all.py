import re, glob, os
from collections import Counter, defaultdict

BASE = r"XUNDL/A58/Ni58/new"
MAP = {
    "A": "Ni58_ec_decay_3.204_s.ens",
    "B": "Ni58_58ni_n_nP_n_nPg.ens",
    "C": "Ni58_58ni_p_pP_pol_p_pP_p_pPg.ens",
    "D": "Ni58_58ni_a_aP.ens",
    "E": "Ni58_58ni_g_gP_pol_g_gP.ens",
    "F": "Ni58_58ni_e_eP.ens",
    "G": "Ni58_60ni_p_t.ens",
    "H": "Ni58_58ni_3he_3heP.ens",
    "I": "Ni58_58ni_d_dP.ens",
    "J": "Ni58_coulex.ens",
    "K": "Ni58_54fe_6li_d.ens",
    "L": "Ni58_54fe_7li_t.ens",
    "M": "Ni58_54fe_12c_8be.ens",
    "N": "Ni58_54fe_16o_12c.ens",
    "O": "Ni58_56fe_3he_n.ens",
    "P": "Ni58_56fe_a_2ng.ens",
    "Q": "Ni58_58ni_18o_18oP.ens",
    "R": "Ni58_45sc_16o_p2ng.ens",
    "S": "Ni58_48ti_12c_2ng.ens",
    "T": "Ni58_28si_36ar_a2pg.ens",
    "U": "Ni58_40ca_24mg_a2pg.ens",
    "V": "Ni58_58ni_16o_16oP.ens",
    "W": "Ni58_59zn_ecp_decay_178.6_ms.ens",
    "X": "Ni58_58ni_6li_6liP.ens",
    "Y": "Ni58_59cu_p_decay_mixed.ens",
    "Z": "Ni58_ni_k-_xg.ens",
    "#": "Ni58_9be_74kr_58nig.ens",
    "j": "Ni58_4he_58ni_4heP_58ni_4he.ens",
}

def L(p): return [x.rstrip("\n").ljust(80) for x in open(p, encoding="utf-8", errors="replace")]

def parse_E(rec):
    e = rec[9:19].strip(); d = rec[19:21].strip()
    m = re.match(r"^([0-9.]+)(?:E([+-]?\d+))?$", e.replace(" ", ""))
    if not m: return None, None
    mant = m.group(1); exp = int(m.group(2)) if m.group(2) else 0
    E = float(mant) * 10.0**exp
    dec = exp - (len(mant.split(".")[1]) if "." in mant else 0)
    return E, (int(d) * 10.0**dec if d.isdigit() else None)

def peaks(path):
    out = []
    for l in L(path):
        if l[5] == " " and l[6] == " " and l[7] == "L":
            E, s = parse_E(l)
            if E is not None: out.append((E, s if s is not None else 0.0))
    return sorted(out)

def tokens(xs):
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
        else:
            i += 1
    return out

AD = L(os.path.join(BASE, "Ni58_adopted.ens"))
PK = {k: peaks(os.path.join(BASE, v)) for k, v in MAP.items()}
for k, v in sorted(PK.items()):
    print(f"  {k}: {len(v):>4} levels   {v[0][0]:>8} .. {v[-1][0]:<9} {MAP[k]}")

lv = [i for i, l in enumerate(AD, 1) if l[5] == " " and l[6] == " " and l[7] == "L"]
ads = []
for k, i in enumerate(lv):
    l = AD[i-1]; E, s = parse_E(l)
    if E is None: continue
    s = s if s is not None else 0.0
    end = lv[k+1] if k+1 < len(lv) else len(AD)+1
    xs = ""
    for n in range(i+1, end):
        if "XREF" in AD[n-1]: xs += re.sub(r"^XREF[+=]?", "", AD[n-1][9:80].strip())
        if AD[n-1][7] == "G" and AD[n-1][5] == " ": break
    ads.append((E, s, xs, i))

# explicit energies claimed per letter, to detect "shadow" citations
explicit = defaultdict(lambda: defaultdict(list))   # letter -> peakE -> [adopted E]
for E, s, xs, i in ads:
    for lab, mod in tokens(xs):
        m = re.search(r"\(([0-9.]+)", mod)
        if m: explicit[lab][round(float(m.group(1)), 1)].append(E)

cases = []
ntok = 0
for E, s, xs, i in ads:
    for lab, mod in tokens(xs):
        if lab not in PK: continue
        ntok += 1
        P = PK[lab]
        if not P: continue
        num = re.search(r"\(([0-9.]+)", mod)
        if num:
            stated = float(num.group(1))
            best = min(P, key=lambda p: abs(p[0]-stated))
            if abs(best[0]-stated) > 2.0:
                cases.append((lab, E, mod, stated, best[0], abs(best[0]-stated), "PHANTOM-ENERGY", i))
        else:
            best = min(P, key=lambda p: abs(p[0]-E))
            d = abs(best[0]-E)
            tol = max(10.0, 2.0 * (s**2 + best[1]**2) ** 0.5)
            if d > tol:
                cases.append((lab, E, mod, None, best[0], d, "NO-LEVEL", i, tol))
            elif d > 2.0 and explicit[lab].get(round(best[0], 1)):
                others = [x for x in explicit[lab][round(best[0], 1)] if x != E]
                if others and "*" not in mod:
                    cases.append((lab, E, mod, None, best[0], d, "SHADOW", i, tol))

print("\nXREF tokens checked against dataset level lists:", ntok)
print("total token checks flagged:", len(cases))
print(Counter(c[6] for c in cases).most_common())
print(Counter(c[0] for c in cases).most_common())
for kind in ("PHANTOM-ENERGY", "NO-LEVEL", "SHADOW"):
    sel = sorted([c for c in cases if c[6] == kind], key=lambda c: -c[5])
    print("\n==== %s (%d) ====" % (kind, len(sel)))
    for lab, E, mod, stated, pk, d, k, i, tol in sel:
        print(f"  adopted {E:>9}  token {lab}{mod:<8} nearest {lab} level {pk:>8}   d={d:6.1f}  tol={tol:6.1f}")
