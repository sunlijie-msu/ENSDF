"""Ni58 adopted: Jpi audit. Mechanical checks:
1) gamma multipolarity vs Delta-J / Delta-parity implied by adopted level Jpi.
2) gamma placement (Ritz) consistency.
3) comment J$ / block text vs L-record J field.
Output to stdout only.
"""
import re, math, sys

PATH = r"d:\X\ND\ENSDF\XUNDL\A58\Ni58\new\Ni58_adopted.ens"

lines = []
with open(PATH, encoding="utf-8", errors="replace") as f:
    for ln in f:
        lines.append(ln.rstrip("\n"))

def get(l, a, b):  # 1-based inclusive columns
    s = l.ljust(80)
    return s[a-1:b]

def num(s):
    s = s.strip()
    if not s:
        return None
    try:
        return float(s)
    except ValueError:
        return None

# ---------- parse J field ----------
JTOK = re.compile(r"^\(?(\d+(?:/\d+)?)([+\-]?)\)?$")

def parse_J(field):
    """return (list_of_(J, parity_or_None, tentative), raw)"""
    raw = field.strip()
    if not raw:
        return [], raw
    out = []
    # handle range A:B with optional parity
    if ":" in raw:
        return [], raw  # ranges not expected in this file
    parts = raw.split(",")
    for p in parts:
        p = p.strip()
        tent = p.startswith("(") and p.endswith(")")
        body = p.strip("()")
        m = re.match(r"^(\d+(?:/\d+)?)\s*([+\-]?)$", body)
        if not m:
            out.append((None, None, True))
            continue
        js, par = m.group(1), m.group(2)
        if "/" in js:
            a, b = js.split("/")
            J = float(a) / float(b)
        else:
            J = float(js)
        out.append((J, par if par else None, tent))
    return out, raw

def mult_rules(m):
    """return set of (dJ_allowed set, dpi: 'yes'|'no'|None)"""
    m = m.strip()
    if not m:
        return None
    m0 = m.strip("()[]")
    rules = []
    comps = [c for c in re.split(r"[+]", m0) if c and c not in ("", )]
    order = {"E1": 1, "M1": 1, "E2": 2, "M2": 2, "E3": 3, "M3": 3, "E0": 0, "M0": 0}
    for c in comps:
        c = c.strip("()[]")
        c = re.sub(r"\(.*\)", "", c)
        if c in order:
            o = order[c]
            rules.append((o, c))
    if not rules:
        if m0.startswith("E0"):
            rules = [(0, "E0")]
        elif m0 in ("D", "D+Q", "D(+Q)", "Q"):
            return ("generic", m0)
        else:
            return ("unknown", m0)
    # convert to dJ/dpi constraints
    allowed = []
    for c in comps:
        c = c.strip("()[]")
        c = re.sub(r"\(.*\)", "", c)
        if c == "E1":
            allowed.append(({0, 1}, "yes"))
        elif c == "M1":
            allowed.append(({0, 1}, "no"))
        elif c == "E2":
            allowed.append(({0, 1, 2}, "no"))
        elif c == "M2":
            allowed.append(({1, 2}, "yes"))
        elif c == "E3":
            allowed.append(({2, 3}, "yes"))
        elif c == "M3":
            allowed.append(({2, 3}, "no"))
        elif c == "E0":
            allowed.append(({0}, "no"))
        elif c == "M0":
            allowed.append(({0}, "no"))
    return ("strict", allowed, m0)

levels = []   # dict: line, E, DE, Jraw, Jlist, T, flags
gammas = []   # dict: line, lvl_index, E, DE, RI, DRI, M, MR, FL, flag
cur = None
for i, l in enumerate(lines, 1):
    if len(l) < 8:
        continue
    rt = get(l, 8, 8)
    cont = get(l, 6, 6)
    if rt == "L" and cont in (" ", "X") and get(l, 7, 7) == " ":
        E = num(get(l, 10, 19).replace("E", "E"))
        rawE = get(l, 10, 19).strip()
        m = re.match(r"^([\d.]+)E(\d+)$", rawE)
        if m:
            E = float(m.group(1)) * 10 ** int(m.group(2))
        DE = num(get(l, 20, 21))
        Jf = get(l, 23, 39)
        Jl, Jraw = parse_J(Jf)
        cur = dict(line=i, E=E, DE=DE, Jraw=Jraw, Jlist=Jl,
                   T=get(l, 40, 49).strip(), DT=get(l, 50, 55).rstrip(),
                   Lf=get(l, 56, 64).strip(), c77=get(l, 77, 77),
                   ms=get(l, 78, 79).strip(), q=get(l, 80, 80), raw=l)
        levels.append(cur)
    elif rt == "G" and cont == " " and get(l, 7, 7) == " " and cur is not None:
        E = num(get(l, 10, 19))
        g = dict(line=i, E=E, DE=num(get(l, 20, 21)), RI=get(l, 23, 29).strip(),
                 DRI=get(l, 30, 31).strip(), M=get(l, 33, 41).strip(),
                 MR=get(l, 42, 49).strip(), DMR=get(l, 50, 55).rstrip(),
                 CC=get(l, 56, 62).strip(), TI=get(l, 65, 74).strip(),
                 FL="",
                 flag=(get(l, 77, 77) + get(l, 78, 79) + get(l, 80, 80)).strip(), raw=l)
        gammas.append(g)
    elif rt == "G" and cont.upper() == "F" and gammas and "FL=" in l:
        gammas[-1]["FL"] = l[9:].strip()

print("levels:", len(levels), "gammas:", len(gammas))

# index levels by energy for placement
def place(g, lvl):
    if g["FL"] and g["FL"].startswith("FL="):
        tgt = g["FL"][3:].strip()
        for L in levels:
            if L["raw"][9:19].strip() == tgt:
                return L
    best = None
    for L in levels:
        if L["E"] is None or lvl["E"] is None:
            continue
        if L is lvl:
            continue
        if L["E"] >= lvl["E"]:
            continue
        resid = lvl["E"] - g["E"] - L["E"]
        tol = 1.0 + 3 * math.sqrt(sum((x or 0) ** 2 for x in (lvl["DE"], g["DE"], L["DE"])))
        if abs(resid) <= tol:
            if best is None or abs(resid) < abs(best[0]):
                best = (resid, L)
    return best[1] if best else None

# ---------- check 1 & 2 ----------
viol, unplaced = [], []
for g in gammas:
    lvl = None
    # gammas belong to the most recent level; track by scanning
    pass

# rebuild with explicit owner
owner = {}
gi = 0
cur = None
for i, l in enumerate(lines, 1):
    rt = get(l, 8, 8); cont = get(l, 6, 6)
    if rt == "L" and cont in (" ", "X") and get(l, 7, 7) == " ":
        cur = i
    elif rt == "G" and cont == " " and get(l, 7, 7) == " " and cur:
        owner[i] = cur
lvl_by_line = {L["line"]: L for L in levels}

for g in gammas:
    lvl = lvl_by_line.get(owner.get(g["line"]))
    if lvl is None:
        continue
    tgt = place(g, lvl)
    if tgt is None:
        unplaced.append((g, lvl))
        continue
    g["tgt"] = tgt
    L1, L2 = lvl["Jlist"], tgt["Jlist"]
    if not L1 or not L2:
        continue
    rule = mult_rules(g["M"])
    if rule is None:
        continue
    ok_any = False
    detail = []
    for (j1, p1, _t1) in L1:
        for (j2, p2, _t2) in L2:
            if j1 is None or j2 is None:
                continue
            dJ = abs(j1 - j2)
            if p1 and p2:
                dpi = "no" if p1 == p2 else "yes"
            else:
                dpi = None
            if rule[0] == "strict":
                for (djset, dpi_req) in rule[1]:
                    if round(dJ) in djset and (dpi is None or dpi == dpi_req):
                        if not (j1 == 0 and j2 == 0 and round(dJ) == 0 and dpi_req is None):
                            ok_any = True
                    else:
                        detail.append((j1, p1, j2, p2, dJ, dpi, djset, dpi_req))
            elif rule[0] == "generic":
                lim = 1 if "D" in rule[1] else 2
                if dJ <= lim:
                    ok_any = True
            else:
                ok_any = True
    if not ok_any:
        viol.append((g, lvl, tgt, rule))

print("\n=== A. MULTIPOLARITY vs ADOPTED Jpi VIOLATIONS ===")
for g, lvl, tgt, rule in viol:
    print(f"L{g['line']:>5} E={g['E']} M={g['M']!r} MR={g['MR']!r} : level {lvl['E']} {lvl['Jraw']} -> {tgt['E']} {tgt['Jraw']}")

print("\n=== B. UNPLACED GAMMAS (no level within tolerance) ===")
for g, lvl in unplaced:
    print(f"L{g['line']:>5} gamE={g['E']} RI={g['RI']} M={g['M']!r} owner={lvl['E']} {lvl['Jraw']}")

print("\n=== C. GAMMA PLACEMENT RESIDUALS (|resid|>0.6 keV, placed) ===")
for g in gammas:
    if "tgt" not in g:
        continue
    lvl = lvl_by_line.get(owner.get(g["line"]))
    resid = lvl["E"] - g["E"] - g["tgt"]["E"]
    if abs(resid) > 0.6:
        print(f"L{g['line']:>5} gamE={g['E']} : {lvl['E']}({lvl['DE']}) -> {g['tgt']['E']}({g['tgt']['DE']}) resid={resid:+.2f} M={g['M']!r}")

# ---------- check 3: comments ----------
print("\n=== D. cL J$ COMMENTS ===")
cur = None
for i, l in enumerate(lines, 1):
    if get(l, 8, 8) == "L" and get(l, 6, 6) in (" ", "X") and get(l, 7, 7) == " ":
        cur = l
    if get(l, 7, 7) == "c" and get(l, 8, 8) == "L":
        txt = l[9:].rstrip()
        if txt.startswith("J$") or txt.startswith("J ") or txt.startswith("J(") or txt.startswith("BAND") or txt.startswith("SEQ"):
            print(f"line{i:>5} [level {cur[9:19].strip():>9} J={cur[22:39].strip():<12}] {txt}")
