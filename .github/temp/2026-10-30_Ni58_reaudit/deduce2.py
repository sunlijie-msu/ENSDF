import re, math
from fractions import Fraction

p = r"d:/X/ND/ENSDF/XUNDL/A58/Ni58/new/Ni58_adopted.ens"
L = open(p, encoding="utf-8", errors="replace").read().split("\n")

def g(l, a, b):
    return l.ljust(80)[a - 1:b]

def val(s):
    s = s.strip()
    if not s: return None
    m = re.match(r"^([\d.]+)E(\d+)$", s)
    if m: return float(m.group(1)) * 10 ** int(m.group(2))
    if re.match(r"^[\d.]+(\+X)?$", s): return float(s.replace("+X", ""))
    return None

levels, gammas = [], []
cur = None
for i, l in enumerate(L, 1):
    rt = g(l, 8, 8); c6 = g(l, 6, 6); c7 = g(l, 7, 7)
    if rt == "L" and c7 == " " and c6 in (" ", "X") and val(g(l, 10, 19)) is not None:
        cur = dict(line=i, Eraw=g(l, 10, 19).strip(), E=val(g(l, 10, 19)),
                   DE=val(g(l, 20, 21)), J=g(l, 22, 39).strip(),
                   T=g(l, 40, 49).strip(), xref="", com=[], gams=[])
        levels.append(cur)
    elif cur and rt == "L" and c6 == "X":
        cur["xref"] = g(l, 10, 80).replace("XREF=", "").strip()
    elif cur and c7 == "c" and rt == "L":
        cur["com"].append(g(l, 10, 80).rstrip())
    elif rt == "G" and c7 == " " and c6 == " " and cur and val(g(l, 10, 19)) is not None:
        gg = dict(line=i, E=val(g(l, 10, 19)), DE=val(g(l, 20, 21)),
                  RI=g(l, 22, 29).strip(), M="", FL=None, q=g(l, 80, 80), owner=cur)
        sub = g(l, 31, 45); st = None
        for k, ch in enumerate(sub):
            if ch in "([EMDQ": st = k; break
        if st is not None:
            s2 = sub[st:]
            for t in ['M1+E2', 'M1(+E2)', '(M1+E2)', '(M1(+E2))', 'E1+M2', 'E1(+M2)',
                      '(E1+M2)', '(E1(+M2))', 'E2+M1', 'E2(+M1)', '[M1,E2]', '[M1]',
                      '[E1]', '[E2]', '[M2]', '(M1)', '(E1)', '(E2)', '(M2)', '(Q)', '(D)',
                      'D+Q', 'D(+Q)', 'M1', 'E1', 'E2', 'E3', 'M2', 'M3', 'E4', 'M4',
                      'E0', 'D', 'Q']:
                if s2.startswith(t): gg["M"] = t; break
        cur["gams"].append(gg); gammas.append(gg)
    elif rt == "G" and c6.upper() == "F" and gammas and "FL=" in l:
        gammas[-1]["FL"] = l.split("FL=")[1].strip()

def parse_J(raw):
    out = []
    if not raw: return out
    for tok in raw.split(","):
        b = tok.strip().strip("()")
        m = re.match(r"^(\d+(?:/\d+)?)\s*([+\-]?)", b)
        if not m: continue
        js, par = m.group(1), m.group(2)
        J = float(Fraction(js)) if "/" in js else float(js)
        out.append((J, par or None))
    return out

for v in levels:
    v["Jlist"] = parse_J(v["J"])

def placer(gg):
    if gg["FL"]:
        for v in levels:
            if v["Eraw"] == gg["FL"].strip(): return v
    o = gg["owner"]
    if gg["E"] is None or o["E"] is None: return None
    best = None
    for v in levels:
        if v is o or v["E"] is None or v["E"] >= o["E"] - 1e-9: continue
        r = o["E"] - gg["E"] - v["E"]
        tol = 1.2 + 3 * math.sqrt(sum((x or 0) ** 2 for x in (o["DE"], gg["DE"], v["DE"])))
        if abs(r) <= tol and (best is None or abs(r) < abs(best[0])): best = (r, v)
    return best[1] if best else None

for gg in gammas:
    gg["tgt"] = placer(gg)

def mult_set(M):
    """return list of (dJ_set, dpi) ; None if unusable (bracketed) ; 'UNK' if blank"""
    m = M.strip()
    if not m: return "UNK"
    if m.startswith("["): return None
    core = m.strip("()")
    if core == "D": return [({0, 1}, None)]
    if core == "Q": return [({0, 1, 2}, None)]
    if core in ("D+Q", "D(+Q)"): return [({0, 1}, None)]
    if core == "E0": return [({0}, "no")]
    parts = re.findall(r"[EM][0-4]", core)
    out = []
    for c in parts:
        out.append({"E1": ({0, 1}, "yes"), "M1": ({0, 1}, "no"), "E2": ({0, 1, 2}, "no"),
                    "M2": ({1, 2}, "yes"), "E3": ({2, 3}, "yes"), "M3": ({2, 3}, "no"),
                    "E0": ({0}, "no")}[c])
    return out or None

def unk_decay(jf, pf):
    s = set()
    for d in (-1, 0, 1):
        if jf + d >= 0 and not (jf == 0 and d == 0):
            s.add((jf + d, "+")); s.add((jf + d, "-"))
    for d in (-2, 2):
        if jf + d >= 0:
            if pf: s.add((jf + d, pf))
            else: s.add((jf + d, "+")); s.add((jf + d, "-"))
    return s

def unk_feed(ji, pi):
    s = set()
    for d in (-1, 0, 1):
        if ji + d >= 0 and not (ji == 0 and d == 0):
            s.add((ji + d, "+")); s.add((ji + d, "-"))
    for d in (-2, 2):
        if ji + d >= 0:
            if pi: s.add((ji + d, pi))
            else: s.add((ji + d, "+")); s.add((ji + d, "-"))
    return s

GRID = [i / 2 for i in range(0, 33)]

def run(use_unknown):
    res = {}
    for v in levels:
        if v["J"]: continue
        cand = set((j, pa) for j in GRID for pa in ("+", "-"))
        used = []
        deex = [gg for gg in v["gams"] if gg["tgt"] is not None]
        feed = [gg for gg in gammas if gg["tgt"] is v and gg["owner"] is not v]
        for gg in deex:
            ms = mult_set(gg["M"])
            tgt = gg["tgt"]
            if ms is None or not tgt["Jlist"]: continue
            allowed = set()
            if ms == "UNK":
                if not use_unknown: continue
                for (jf, pf) in tgt["Jlist"]:
                    allowed |= unk_decay(jf, pf)
                used.append(f"{gg['E']:g}(?)->{tgt['Eraw']}[{tgt['J']}]")
            else:
                for (djs, dpi) in ms:
                    for (jf, pf) in tgt["Jlist"]:
                        for d in djs:
                            ji = jf + d
                            if ji < 0 or (jf == 0 and ji == 0): continue
                            pi = None
                            if dpi and pf:
                                pi = pf if dpi == "no" else ("-" if pf == "+" else "+")
                            if pi is None:
                                allowed.add((ji, "+")); allowed.add((ji, "-"))
                            else:
                                allowed.add((ji, pi))
                used.append(f"{gg['E']:g}({gg['M']})->{tgt['Eraw']}[{tgt['J']}]")
            cand &= allowed
        for gg in feed:
            ms = mult_set(gg["M"])
            ji_list = gg["owner"]["Jlist"]
            if ms is None or not ji_list: continue
            allowed = set()
            if ms == "UNK":
                if not use_unknown: continue
                for (ji, pi) in ji_list:
                    allowed |= unk_feed(ji, pi)
                used.append(f"fed {gg['E']:g}(?) from {gg['owner']['Eraw']}[{gg['owner']['J']}]")
            else:
                for (djs, dpi) in ms:
                    for (ji, pi) in ji_list:
                        for d in djs:
                            jf = ji + d
                            if jf < 0 or (ji == 0 and jf == 0): continue
                            pf = None
                            if dpi and pi:
                                pf = pi if dpi == "no" else ("-" if pi == "+" else "+")
                            if pf is None:
                                allowed.add((jf, "+")); allowed.add((jf, "-"))
                            else:
                                allowed.add((jf, pf))
                used.append(f"fed {gg['E']:g}({gg['M']}) from {gg['owner']['Eraw']}[{gg['owner']['J']}]")
            cand &= allowed
        res[v["line"]] = (v, cand, used)
    return res

def fmt(cand):
    d = {}
    for (j, pa) in cand:
        d.setdefault(j, set()).add(pa)
    out = []
    for j in sorted(d):
        ps = d[j]
        out.append(f"{j:g}" + ("+/-" if len(ps) == 2 else list(ps)[0]))
    return ", ".join(out)

for label, use in (("STRICT (measured M only)", False), ("WITH D-or-E2 ASSUMPTION for blank M", True)):
    print("\n" + "=" * 20, label)
    r = run(use)
    for ln, (v, cand, used) in sorted(r.items(), key=lambda kv: (len(kv[1][1]), kv[0])):
        n = len(cand)
        if 0 < n <= 3 and used:
            print(f"\nL{ln} E={v['Eraw']} DE={v['DE']} T={v['T']} XREF={v['xref']}")
            for u in used: print("    ", u)
            for c in v["com"]: print("     com:", c)
            print("    =>", fmt(cand))
    from collections import Counter
    print("counts:", sorted(Counter(len(c) for v, c, u in r.values()).items()))
