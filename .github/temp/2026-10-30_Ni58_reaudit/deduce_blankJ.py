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

# ---------- parse levels and gammas ----------
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
        # multipolarity: first token of '([EMDQ' in cols 31-45
        sub = g(l, 31, 45)
        st = None
        for k, ch in enumerate(sub):
            if ch in "([EMDQ":
                st = k; break
        if st is not None:
            sub2 = sub[st:]
            for t in ['M1+E2', 'M1(+E2)', '(M1+E2)', '(M1(+E2))', 'E1+M2', 'E1(+M2)',
                      '(E1+M2)', '(E1(+M2))', 'E2+M1', 'E2(+M1)', '[M1,E2]', '[M1]', '[E1]',
                      '[E2]', '[M2]', '(M1)', '(E1)', '(E2)', '(M2)', '(Q)', '(D)', 'D+Q',
                      'D(+Q)', 'M1', 'E1', 'E2', 'E3', 'M2', 'M3', 'E4', 'M4', 'E0', 'D', 'Q']:
                if sub2.startswith(t):
                    gg["M"] = t; break
        cur["gams"].append(gg); gammas.append(gg)
    elif rt == "G" and c6.upper() == "F" and gammas and "FL=" in l:
        gammas[-1]["FL"] = l.split("FL=")[1].strip()

def parse_J(raw):
    if not raw: return []
    out = []
    for tok in raw.split(","):
        tok = tok.strip()
        b = tok.strip("()")
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
            if v["Eraw"] == gg["FL"].strip():
                return v
    owner = gg["owner"]
    if gg["E"] is None or owner["E"] is None: return None
    best = None
    for v in levels:
        if v is owner or v["E"] is None or v["E"] >= owner["E"] - 1e-9: continue
        r = owner["E"] - gg["E"] - v["E"]
        tol = 1.2 + 3 * math.sqrt(sum((x or 0) ** 2 for x in (owner["DE"], gg["DE"], v["DE"])))
        if abs(r) <= tol and (best is None or abs(r) < abs(best[0])):
            best = (r, v)
    return best[1] if best else None

for gg in gammas:
    gg["tgt"] = placer(gg)

# ---------- constraint engine ----------
def mconstraint(M):
    m = M.strip()
    if not m or m.startswith("["):        # bracketed -> circular, skip
        return None
    core = m.strip("()")
    if core == "D":      return [({0, 1}, None)]
    if core == "Q":      return [({0, 1, 2}, None)]
    if core == "D+Q" or core == "D(+Q)": return [({0, 1}, None)]
    if "E0" in core and not re.search(r"[EM][12-4]", core):
        return [({0}, "no")]
    parts = re.findall(r"[EM][0-4]", core)
    res = []
    for c in parts:
        if c == "E1": res.append(({0, 1}, "yes"))
        elif c == "M1": res.append(({0, 1}, "no"))
        elif c == "E2": res.append(({0, 1, 2}, "no"))
        elif c == "M2": res.append(({1, 2}, "yes"))
        elif c == "E3": res.append(({2, 3}, "yes"))
        elif c == "M3": res.append(({2, 3}, "no"))
        elif c == "E0": res.append(({0}, "no"))
    return res or None

def allow(baselist, djs, dpi_req):
    out = set()
    for (j, par) in baselist:
        if j is None: continue
        for d in djs:
            cand = j + d if d >= 0 else j - d
            if cand < 0: continue
            # J=0 -> J=0 only via monopole; dipole/quadrupole 0->0 forbidden
            out.add((cand, par))
    return out

blank = [v for v in levels if not v["J"]]
print("blank-J levels:", len(blank))

# candidate spin grid 0..14
GRID = [i / 2 for i in range(0, 29)]
PAR = ["+", "-", None]

results = []
for v in blank:
    deex = [gg for gg in v["gams"] if gg.get("tgt") is not None]
    feed = [gg for gg in gammas if gg.get("tgt") is v and gg["owner"] is not v]

    cand = set((j, p) for j in GRID for p in PAR)
    reasons = []

    for gg in deex:
        tgt = gg["tgt"]
        c = mconstraint(gg["M"])
        if not c: continue
        base = tgt["Jlist"]
        if not base: continue
        allowed = set()
        for (djs, dpi) in c:
            for (jf, pf) in base:
                for d in djs:
                    ji = jf + d
                    if ji < 0: continue
                    if jf == 0 and ji == 0:      # 0->0 forbidden for E1,M1,E2,M2
                        continue
                    pi = None
                    if dpi and pf:
                        pi = pf if dpi == "no" else ("-" if pf == "+" else "+")
                    allowed.add((ji, pi))
        cand &= allowed
        reasons.append(f"{gg['E']}|g({gg['M']})->{tgt['Eraw']}[{tgt['J']}]")

    for gg in feed:
        c = mconstraint(gg["M"])
        if not c: continue
        base = gg["owner"]["Jlist"]
        if not base: continue
        allowed = set()
        for (djs, dpi) in c:
            for (ji, pi) in base:
                for d in djs:
                    jf = ji + d
                    if jf < 0: continue
                    if ji == 0 and jf == 0: continue
                    pf = None
                    if dpi and pi:
                        pf = pi if dpi == "no" else ("-" if pi == "+" else "+")
                    allowed.add((jf, pf))
        cand &= allowed
        reasons.append(f"fed by {gg['E']}|g({gg['M']}) from {gg['owner']['Eraw']}[{gg['owner']['J']}]")

    # collapse parities: (J,'+'/'-'/None)
    spins = {}
    for (j, p) in cand:
        spins.setdefault(j, set()).add(p)
    # keep only values reachable with a consistent parity option
    results.append((v, spins, reasons, len(deex), len(feed)))

def fmt(spins):
    out = []
    for j in sorted(spins):
        ps = spins[j] - {None}
        if not ps:
            out.append(f"{j:g}")
        elif len(ps) == 2:
            out.append(f"{j:g}(+/-)")
        else:
            out.append(f"{j:g}{ps.pop()}")
    return ", ".join(out)

print("\n=== levels with <=3 candidate Jpi (from non-bracketed M and placed gammas) ===")
for v, spins, reasons, nd, nf in results:
    n = len(spins)
    if 0 < n <= 3:
        print(f"\nL{v['line']} E={v['Eraw']} (DE={v['DE']}) T={v['T']} XREF={v['xref']}")
        for r in reasons:
            print("     ", r)
        for c in v["com"]:
            print("      com:", c)
        print("   => CANDIDATES:", fmt(spins))
print("\n=== summary of counts ===")
from collections import Counter
cnt = Counter(len(s) for v, s, r, a, b in results)
print(sorted(cnt.items()))
for v, spins, reasons, nd, nf in results:
    if len(spins) in (1, 2, 3):
        print(f"  n={len(spins)} L{v['line']} E={v['Eraw']} -> {fmt(spins)}")
