import re, math
def L(p): return [l.rstrip("\n").ljust(80) for l in open(p, encoding="utf-8", errors="replace")]
DIR = r"XUNDL/A58/Ni58/new/"
C  = L(DIR + "Ni58_58ni_p_pP_pol_p_pP_p_pPg.ens")
AD = L(DIR + "Ni58_adopted.ens")

def parse_E(rec):
    e = rec[9:19].strip()
    d = rec[19:21].strip()
    if not e: return None, None
    m = re.match(r"^([0-9.]+)", e)
    if not m: return None, None
    E = float(m.group(1))
    dec = len(m.group(1).split(".")[1]) if "." in m.group(1) else 0
    s = int(d) * 10.0**-dec if d.isdigit() else 0.0
    return E, s

def parse_J(rec):
    # J starts col 23 normally; some records are shifted so col 22 also holds J chars
    a = rec[22:39].strip()
    b = rec[21:39].strip()
    if b and (b[0] in "0123456789(+" or b[0] == "-"):
        a = b
    return a

def jset(txt):
    """return set of (J, parity) ; empty set = unknown"""
    if not txt: return set()
    out = set()
    for tok in re.split(r"[,\s]+", txt.strip()):
        if not tok: continue
        nums = re.findall(r"\d+", tok)
        par = None
        if "+" in tok: par = "+"
        elif "-" in tok: par = "-"
        if not nums:
            out.add((None, par))
        for n in nums:
            out.add((int(n), par))
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

# ---- dataset C levels ----
ds = []
for l in C:
    if l[5] == " " and l[6] == " " and l[7] == "L":
        E, s = parse_E(l)
        if E is None: continue
        ds.append(dict(E=E, s=s, J=parse_J(l), L=l[55:64].strip(), S=l[64:74].strip()))

# ---- adopted levels + XREF ----
lv = [i for i, l in enumerate(AD, 1) if l[5] == " " and l[6] == " " and l[7] == "L"]
ad = []
for k, i in enumerate(lv):
    l = AD[i-1]
    E, s = parse_E(l)
    if E is None: continue
    end = lv[k+1] if k+1 < len(lv) else len(AD)+1
    xs = ""
    for n in range(i+1, end):
        if "XREF" in AD[n-1]:
            t = re.sub(r"^XREF[+=]?", "", AD[n-1][9:80].strip())
            xs += t
        if AD[n-1][7] == "G" and AD[n-1][5] == " ": break
    ad.append(dict(E=E, s=s, J=parse_J(l), X=xs))

def cclaim(x):
    """C citation on an adopted level: None if none, else parenthetical energy or '*' etc"""
    if not x or "C" not in x: return None
    m = re.search(r"C(?:\(([^)]*)\))?", x)
    if not m: return None
    return m.group(1) if m.group(1) else ""

nC = len(ds); nAd = len(ad)
ncit = sum(1 for a in ad if cclaim(a["X"]) is not None)
print(f"C levels: {nC}   adopted levels: {nAd}   adopted citing C: {ncit}")
print(f"C level E range: {ds[0]['E']} .. {ds[-1]['E']}")
print("sample J parse C:", [d['J'] for d in ds[:8]])
print("sample J parse ad:", [a['J'] for a in ad[:8]])
