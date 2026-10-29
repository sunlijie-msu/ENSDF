"""Ni58 adopted: Jpi audit v2 (robust field parsing).
Checks:
 1) gamma multipolarity vs adopted Jpi (Delta-J, Delta-parity)
 2) gamma placements (Ritz) and residuals
 3) J$ comments / block text vs L-record J field
"""
import re, math
from collections import Counter

PATH = r"d:\X\ND\ENSDF\XUNDL\A58\Ni58\new\Ni58_adopted.ens"
lines = open(PATH, encoding="utf-8", errors="replace").read().split("\n")

def get(l, a, b):
    return l.ljust(80)[a-1:b]

def fnum(s):
    s = s.strip()
    if not s: return None
    m = re.match(r"^([\d.]+)E(\d+)$", s)
    if m: return float(m.group(1)) * 10**int(m.group(2))
    try: return float(s)
    except ValueError: return None

MTOK = ['M1+E2','M1(+E2)','(M1+E2)','(M1(+E2))','E1+M2','E1(+M2)','(E1+M2)','(E1(+M2))',
        'E2+M1','E2(+M1)','[M1]','[E1]','[E2]','[M2]','[M1,E2]','(M1)','(E1)','(E2)','(M2)','(Q)','(D)',
        'D+Q','D(+Q)','M1','E1','E2','E3','M2','M3','E4','M4','E0','D','Q']

def parse_M(line):
    sub = get(line, 31, 45)
    start = None
    for k, ch in enumerate(sub):
        if ch in "([EMDQ":
            start = k
            break
    if start is None:
        return ""
    sub = sub[start:]
    best = None
    for t in sorted(MTOK, key=len, reverse=True):
        if sub.startswith(t):
            return t
    return ""

def parse_M_old(sub):
    best = None
    for i in range(len(sub)):
        for t in MTOK:
            if sub.startswith(t, i):
                if best is None or i < best[0] or (i == best[0] and len(t) > len(best[1])):
                    best = (i, t)
        if best and best[0] == i:
            break
    return best[1] if best else ""

levels = []
gammas = []
cur = None
pending = []
for i, l in enumerate(lines, 1):
    rt = get(l, 8, 8); cont = get(l, 6, 6); c7 = get(l, 7, 7)
    if rt == "L" and c7 == " " and cont in (" ", "X"):
        Eraw = get(l, 10, 19).strip()
        if Eraw and (Eraw[0].isdigit() or Eraw[0] == "."):
            lv = dict(line=i, Eraw=Eraw, E=fnum(Eraw), DE=fnum(get(l, 20, 21)),
                      Jraw=get(l, 22, 39).strip(),
                      T=get(l, 40, 49).strip(), DT=get(l, 50, 55).rstrip(),
                      Lf=get(l, 56, 64).strip(), c77=get(l, 77, 77),
                      ms=get(l, 78, 79).strip(), q=get(l, 80, 80))
            levels.append(lv); cur = lv
        continue
    if rt == "G" and c7 == " " and cont == " " and cur is not None:
        M = parse_M(l)
        g = dict(line=i, owner=cur, E=fnum(get(l, 10, 19)), DE=fnum(get(l, 20, 21)),
                 RI=get(l, 22, 29).strip(), DRI=get(l, 29, 31).strip(),
                 M=M, MR=get(l, 41, 49).strip(), CC=get(l, 55, 62).strip(),
                 FL=None, q=get(l, 80, 80), c77=get(l, 77, 77))
        gammas.append(g); pending.append(g)
    elif rt == "G" and cont.upper() == "F":
        if pending and "FL=" in l:
            pending[-1]["FL"] = l.split("FL=")[1].strip()

print("real levels:", len(levels), " gammas:", len(gammas))

# ---------------- J parsing ----------------
def parse_J(raw):
    if not raw: return []
    out = []
    for p in raw.split(","):
        p = p.strip()
        if not p: continue
        b = p.strip("()")
        m = re.match(r"^(\d+(?:/\d+)?)\s*([+\-]?)", b)
        if not m:
            out.append((None, None)); continue
        js, par = m.group(1), m.group(2)
        J = (float(js.split("/")[0]) / float(js.split("/")[1])) if "/" in js else float(js)
        out.append((J, par or None))
    return out

for lv in levels:
    lv["Jlist"] = parse_J(lv["Jraw"])

# ---------------- placement ----------------
bylist = levels
def placer(g):
    lvl = g["owner"]
    if g["FL"]:
        for L in levels:
            if L["Eraw"] == g["FL"].strip():
                return L
    if g["E"] is None or lvl["E"] is None: return None
    best = None
    for L in levels:
        if L is lvl or L["E"] is None or L["E"] >= lvl["E"] - 1e-9: continue
        resid = lvl["E"] - g["E"] - L["E"]
        tol = 1.2 + 3 * math.sqrt(sum((x or 0)**2 for x in (lvl["DE"], g["DE"], L["DE"])))
        if abs(resid) <= tol and (best is None or abs(resid) < abs(best[0])):
            best = (resid, L)
    return best[1] if best else None

def rules(M):
    m = M.strip("[]")
    if not m:
        return None
    if m.strip("()") in ("D", "Q", "D+Q", "D(+Q)"):
        g0 = m.strip("()")
        lim = 1 if g0 == "D" else 2
        return [({0, 1} if lim == 1 else {0, 1, 2}, None)]
    m = m.strip("()")
    out = []
    for c in re.findall(r"[EM]\d", m):
        out.append(c)
    res = []
    for c in out:
        if c == "E0": res.append(({0}, "no"))
        elif c == "E1": res.append(({0,1}, "yes"))
        elif c == "M1": res.append(({0,1}, "no"))
        elif c == "E2": res.append(({0,1,2}, "no"))
        elif c == "M2": res.append(({1,2}, "yes"))
        elif c == "E3": res.append(({2,3}, "yes"))
        elif c == "M3": res.append(({2,3}, "no"))
        elif c == "E4": res.append(({3,4}, "no"))
        elif c == "M4": res.append(({3,4}, "yes"))
    return res or None

print("\n=== A. MULTIPOLARITY vs ADOPTED Jpi ===")
nA = 0
for g in gammas:
    tgt = placer(g)
    g["tgt"] = tgt
    if tgt is None: continue
    rs = rules(g["M"])
    if not rs: continue
    L1, L2 = g["owner"]["Jlist"], tgt["Jlist"]
    if not L1 or not L2: continue
    ok = False
    for (j1, p1) in L1:
        for (j2, p2) in L2:
            if j1 is None or j2 is None: continue
            dJ = abs(j1 - j2)
            dpi = None
            if p1 and p2: dpi = "no" if p1 == p2 else "yes"
            for (djs, dpr) in rs:
                if round(dJ) in djs and (dpi is None or dpr is None or dpi == dpr):
                    if j1 == 0 and j2 == 0 and dJ == 0 and g["M"].strip("[]") in ("E2","M2","E1","M1"):
                        continue
                    ok = True
    if not ok:
        nA += 1
        print(f"  line{g['line']:>5} gE={g['E']:<10} M={g['M']:<10} : {g['owner']['Eraw']} {g['owner']['Jraw']} -> {tgt['Eraw']} {tgt['Jraw']}")
print("total:", nA)

print("\n=== B. UNPLACED GAMMAS ===")
nB = 0
for g in gammas:
    if g["E"] is None: continue
    if g["tgt"] is None:
        nB += 1
        print(f"  line{g['line']:>5} gE={g['E']:<10} RI={g['RI']:<8} M={g['M']:<10} owner={g['owner']['Eraw']} {g['owner']['Jraw']} FL={g['FL']}")
print("total:", nB)

print("\n=== C. PLACEMENT RESIDUALS > 1.0 keV ===")
for g in gammas:
    if g["tgt"] is None or g["E"] is None: continue
    lvl = g["owner"]; t = g["tgt"]
    resid = lvl["E"] - g["E"] - t["E"]
    if abs(resid) > 1.0:
        print(f"  line{g['line']:>5} gE={g['E']:<10} {lvl['Eraw']}({lvl['DE']}) -> {t['Eraw']}({t['DE']}) resid={resid:+.2f} M={g['M']}")

print("\n=== D. LEVELS WITH NO J ===")
for lv in levels:
    if not lv["Jraw"]:
        print(f"  line{lv['line']:>5} E={lv['Eraw']:<10} DE={lv['DE']} T={lv['T']} L={lv['Lf']} ms={lv['ms']} q={lv['q']}")
