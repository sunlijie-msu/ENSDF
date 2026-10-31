import re, math
from collections import Counter, defaultdict
def L(p): return [l.rstrip("\n").ljust(80) for l in open(p, encoding="utf-8", errors="replace")]
DIR = r"XUNDL/A58/Ni58/new/"
C  = L(DIR + "Ni58_58ni_p_pP_pol_p_pP_p_pPg.ens")
AD = L(DIR + "Ni58_adopted.ens")

def parse_E(rec):
    e = rec[9:19].strip(); d = rec[19:21].strip()
    if not e: return None, None, 0
    m = re.match(r"^([0-9.]+)", e)
    if not m: return None, None, 0
    E = float(m.group(1))
    dec = len(m.group(1).split(".")[1]) if "." in m.group(1) else 0
    s = int(d) * 10.0**-dec if d.isdigit() else None
    return E, s, dec

def parse_J(rec):
    a = rec[22:39].strip(); b = rec[21:39].strip()
    if b and (b[0].isdigit() or b[0] in "(+-"): a = b
    return a

def jset(txt):
    if not txt: return set()
    out = set()
    for tok in re.split(r"[,\s]+", txt.strip()):
        if not tok: continue
        par = "+" if "+" in tok else ("-" if "-" in tok else None)
        nums = re.findall(r"\d+", tok)
        if not nums: out.add((None, par))
        for n in nums: out.add((int(n), par))
    return out

def jcmp(a, b):
    sa, sb = jset(a), jset(b)
    if not sa or not sb: return "?"
    for ja, pa in sa:
        for jb, pb in sb:
            if ja is not None and jb is not None and ja != jb: continue
            if pa is not None and pb is not None and pa != pb: continue
            return "ok"
    return "J!"

def fmt(E, s, dec):
    if E is None: return "-"
    if s is None: return f"{E:g}"
    if dec == 0: return f"{int(round(E))}({int(round(s))})"
    return f"{E:.{dec}f}({int(round(s*10**dec))})"

ds = []
for l in C:
    if l[5] == " " and l[6] == " " and l[7] == "L":
        E, s, dec = parse_E(l)
        if E is not None: ds.append(dict(E=E, s=s, dec=dec, J=parse_J(l), T=fmt(E, s, dec)))
lv = [i for i, l in enumerate(AD, 1) if l[5] == " " and l[6] == " " and l[7] == "L"]
ad = []
for k, i in enumerate(lv):
    l = AD[i-1]; E, s, dec = parse_E(l)
    if E is None: continue
    end = lv[k+1] if k+1 < len(lv) else len(AD)+1
    xs = ""
    for n in range(i+1, end):
        if "XREF" in AD[n-1]: xs += re.sub(r"^XREF[+=]?", "", AD[n-1][9:80].strip())
        if AD[n-1][7] == "G" and AD[n-1][5] == " ": break
    ad.append(dict(E=E, s=s, dec=dec, J=parse_J(l), X=xs, T=fmt(E, s, dec)))

def cclaim(x):
    if not x: return None
    m = re.search(r"C(?:\(([^)]*)\))?", x)
    if not m: return None
    return m.group(1) if m.group(1) else ""

rows = []
used = Counter()
WIN = 50.0
for a in ad:
    cl = cclaim(a["X"])
    if cl is None: continue
    m = re.match(r"^([0-9.]+)", cl)
    target = float(m.group(1)) if m else a["E"]
    near = [d for d in ds if abs(d["E"]-target) <= WIN]
    pool = near if near else ds
    rep = sorted(pool, key=lambda d: (abs(d["E"]-target),
                                      used[(d["E"], d["s"])] > 0,
                                      jcmp(a["J"], d["J"]) == "J!"))[0]
    used[(rep["E"], rep["s"])] += 1
    rows.append((a, rep, cl))
byc = Counter((r[1]["E"], r[1]["s"]) for r in rows)

out = []
for a, rep, cl in rows:
    dE = abs(rep["E"]-a["E"])
    jc = jcmp(a["J"], rep["J"])
    shared = byc[(rep["E"], rep["s"])] > 1
    star = "*" in cl
    if jc == "J!": v = "**J conflict**"
    elif dE > WIN: v = "**far (>50 keV)**"
    elif shared and not star: v = "**shared, no `*`**"
    elif shared: v = "shared `*`"
    elif dE > 5: v = "loose"
    else: v = "ok"
    out.append(f"| {a['T']} | {a['J'] or '-'} | {rep['T']} | {rep['J'] or '-'} | {dE:g} | {jc} | {v} |")
order = sorted(range(len(rows)), key=lambda i: rows[i][0]["E"])
print("| adopted E(σ) | J(π) | (p,p′) peak E(σ) | J(π) | Δ (keV) | J | verdict |")
print("|---|---|---|---|---|---|---|")
for i in order: print(out[i])
print()
for d in ds:
    if used[(d["E"], d["s"])] == 0:
        near = sorted(ad, key=lambda a: abs(a["E"]-d["E"]))[0]
        dE = abs(near["E"]-d["E"]); jc = jcmp(near["J"], d["J"])
        cited = "C" in near["X"]
        out.append(f"| {near['T']} (no C) | {near['J'] or '-'} | {d['T']} | {d['J'] or '-'} | {dE:g} | {jc} | **peak not cited** |")
        print(f"| {near['T']} (no C) | {near['J'] or '-'} | {d['T']} | {d['J'] or '-'} | {dE:g} | {jc} | **peak not cited** |")
print("\nrows:", len(rows), " uncited peaks:", sum(1 for d in ds if used[(d['E'], d['s'])] == 0))
print("\n--- check adopted 10720 / 10744 and C peaks 10720 / 10744 ---")
for a in ad:
    if 10700 <= a["E"] <= 10760: print(f"  ad {a['T']:<12} J={a['J']:<8} XREF={a['X']}")
for d in ds:
    if 10700 <= d["E"] <= 10760: print(f"  C  {d['T']:<12} J={d['J']}")
print("\n--- C peaks 9193 / 10119 ---")
for d in ds:
    if d["E"] in (9193.0, 10119.0): print(f"  C  {d['T']:<12} J={d['J']}")
for a in ad:
    if a["E"] in (9191.5, 10120.0): print(f"  ad {a['T']:<12} J={a['J']:<8} XREF={a['X']}")
