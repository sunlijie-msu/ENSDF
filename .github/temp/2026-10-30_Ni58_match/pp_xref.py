import re, io, sys
from collections import Counter, defaultdict
def L(p): return [l.rstrip("\n").ljust(80) for l in open(p, encoding="utf-8", errors="replace")]
DIR = r"XUNDL/A58/Ni58/new/"
C  = L(DIR + "Ni58_58ni_p_pP_pol_p_pP_p_pPg.ens")
AD = L(DIR + "Ni58_adopted.ens")

def parse_E(rec):
    e = rec[9:19].strip(); d = rec[19:21].strip()
    m = re.match(r"^([0-9.]+)", e)
    if not m: return None, None, 0
    E = float(m.group(1)); dec = len(m.group(1).split(".")[1]) if "." in m.group(1) else 0
    return E, (int(d)*10.0**-dec if d.isdigit() else None), dec

def parse_J(rec):
    a = rec[22:39].strip(); b = rec[21:39].strip()
    if b and (b[0].isdigit() or b[0] in "(+-"): a = b
    return a

def jset(t):
    if not t: return set()
    out = set()
    for tok in re.split(r"[,\s]+", t.strip()):
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

def f(E, s, dec):
    if E is None: return "-"
    if s is None: return f"{E:g}"
    return f"{int(round(E))}({int(round(s))})" if dec == 0 else f"{E:.{dec}f}({int(round(s*10**dec))})"

ds = []
for l in C:
    if l[5] == " " and l[6] == " " and l[7] == "L":
        E, s, dec = parse_E(l)
        if E is not None: ds.append(dict(E=E, s=s, dec=dec, J=parse_J(l), T=f(E, s, dec)))

def tokens(xs):
    """split XREF content into (letter, modifier) pairs"""
    out = []
    i = 0
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

def ctoken(xs):
    """exact C token including modifier, as written; None if absent"""
    for lab, mod in tokens(xs):
        if lab == "C":
            return "C" + mod
    return None

lv = [i for i, l in enumerate(AD, 1) if l[5] == " " and l[6] == " " and l[7] == "L"]
ad = []
lowc = 0
for k, i in enumerate(lv):
    l = AD[i-1]; E, s, dec = parse_E(l)
    if E is None: continue
    end = lv[k+1] if k+1 < len(lv) else len(AD)+1
    xs = ""
    for n in range(i+1, end):
        if "XREF" in AD[n-1]: xs += re.sub(r"^XREF[+=]?", "", AD[n-1][9:80].strip())
        if AD[n-1][7] == "G" and AD[n-1][5] == " ": break
    if any(lab == "c" for lab, mod in tokens(xs)): lowc += 1
    ad.append(dict(E=E, s=s, dec=dec, J=parse_J(l), X=xs, T=f(E, s, dec)))

print("adopted levels:", len(ad), " with lowercase c token:", lowc)
rows = []
used = Counter()
for a in ad:
    tok = ctoken(a["X"])
    if tok is None: continue
    mm = re.search(r"\(([^)]*)\)", tok)
    mod = mm.group(1) if mm else ""
    num = re.match(r"^([0-9.]+)", mod)
    target = float(num.group(1)) if num else a["E"]
    near = [d for d in ds if abs(d["E"]-target) <= 50.0]
    rep = sorted(near if near else ds, key=lambda d: (abs(d["E"]-target), used[(d["E"], d["s"])] > 0))[0]
    used[(rep["E"], rep["s"])] += 1
    rows.append((a, rep, tok, mod, target))
shared = Counter((r[1]["E"], r[1]["s"]) for r in rows)

out = []
for a, rep, tok, mod, target in rows:
    dE = abs(rep["E"]-a["E"])
    jc = jcmp(a["J"], rep["J"])
    stated_missing = ("." in mod or mod[:1].isdigit()) and abs(rep["E"]-target) > 2.0
    sh = shared[(rep["E"], rep["s"])] > 1
    if jc == "J!": v = "**J≠**"
    elif stated_missing: v = "**stated E not a peak**"
    elif dE > 50: v = "**Δ>50**"
    elif sh and "*" not in tok: v = "**shared, no `*`**"
    elif sh: v = "shared `*`"
    elif dE > 5: v = "loose"
    else: v = "match"
    out.append((a["E"], f"| {a['T']} | {a['J'] or '-'} | `{tok}` | {rep['T']} | {rep['J'] or '-'} | {dE:g} | {jc} | {v} |"))

path = r".github/temp/2026-10-30_Ni58_match/pp_xref.md"
fh = io.open(path, "w", encoding="utf-8")
fh.write("| adopted E(σ) | adopted Jπ | XREF token for C | (p,p′) peak E(σ) | (p,p′) Jπ | Δ (keV) | J | check |\n")
fh.write("|---|---|---|---|---|---|---|---|\n")
for _, line in sorted(out): fh.write(line + "\n")
fh.close()
print("rows:", len(out))
print("verdict counts:", Counter(l.split("|")[-2].strip() for _, l in out).most_common())
print("wrote", path)
