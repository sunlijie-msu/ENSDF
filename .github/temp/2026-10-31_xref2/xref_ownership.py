"""XREF ownership audit: adopted XREF tokens <-> dataset levels, both directions."""
import io, math, re, sys, os
from collections import defaultdict, Counter
import numpy as np
from scipy.optimize import linear_sum_assignment

BASE = sys.argv[1] if len(sys.argv) > 1 else "XUNDL/A58/Ni58/new/"
ADOPTED = sys.argv[2] if len(sys.argv) > 2 else "Ni58_adopted.ens"
OUT = sys.argv[3] if len(sys.argv) > 3 else ".github/temp/2026-10-31_xref2/report.md"
KEYCH = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz#")
WP_MIN, WP_SIG = 30.0, 3.0


def lines(p):
    return [x.rstrip("\n").ljust(80) for x in io.open(p, encoding="utf-8", errors="replace")]


def parse_E(rec):
    e = rec[9:19].strip().replace(" ", ""); d = rec[19:21].strip()
    m = re.match(r"^([0-9]+\.?[0-9]*)(?:E([+-]?\d+))?$", e)
    if not m:
        return None, 0.0
    mant = m.group(1); exp = int(m.group(2)) if m.group(2) else 0
    dec = exp - (len(mant.split(".")[1]) if "." in mant else 0)
    return float(mant) * 10.0 ** exp, (int(d) * 10.0 ** dec if d.isdigit() else 0.0)


def parse_J(rec):
    a = rec[22:39].strip(); b = rec[21:39].strip()
    return b if b and (b[0].isdigit() or b[0] in "(+-[") else a


def jset(t):
    out = set()
    for tok in re.split(r"[,\s]+", t.strip()) if t else []:
        if not tok:
            continue
        par = "+" if "+" in tok else ("-" if "-" in tok else None)
        nums = re.findall(r"\d+", tok)
        for n in nums:
            out.add((int(n), par))
    return out


def jbad(a, b):
    sa, sb = jset(a), jset(b)
    if not sa or not sb:
        return False
    return not any((ja == jb) and (pa is None or pb is None or pa == pb) for ja, pa in sa for jb, pb in sb)


def fmt(E, s):
    if s and s > 0:
        dec = 0
        if abs(E - round(E)) > 1e-9:
            dec = len(("%.4f" % E).rstrip("0").split(".")[1])
        return ("%.*f(%d)" % (dec, E, round(s * 10 ** dec))) if s < 1000 else "%g(%g)" % (E, s)
    return "%g" % E


def is_L(r):
    return r[5] == " " and r[6] == " " and r[7] == "L"


# ---- letter -> dataset via DSID ----
AD = lines(os.path.join(BASE, ADOPTED))
norm = lambda s: re.sub(r"\s+", " ", s.upper().strip())
keys = {r[8]: norm(r[9:39]) for r in AD if r[5] == " " and r[6] == " " and r[7] == "X" and r[8] != " "}
files = {}
for fn in os.listdir(BASE):
    if fn.endswith(".ens") and fn != ADOPTED:
        files.setdefault(norm(lines(os.path.join(BASE, fn))[0][9:39]), []).append(fn)
LF, bad_map = {}, []
for k, dsid in keys.items():
    c = files.get(dsid, [])
    if len(c) == 1:
        LF[k] = c[0]
    else:
        bad_map.append((k, dsid, c))

DS = {}
for k, fn in LF.items():
    rows = []
    for r in lines(os.path.join(BASE, fn)):
        if is_L(r):
            E, s = parse_E(r)
            if E is not None:
                rows.append(dict(E=E, s=s, J=parse_J(r), raw=r.rstrip()[9:50].strip()))
    DS[k] = sorted(rows, key=lambda d: d["E"])

# ---- adopted levels ----
idx = [i for i, r in enumerate(AD) if is_L(r)]
ADL = []
for n, i in enumerate(idx):
    E, s = parse_E(AD[i])
    if E is None:
        continue
    xs = ""
    for j in range(i + 1, idx[n + 1] if n + 1 < len(idx) else len(AD)):
        r = AD[j]
        if r[5] != " " and r[7] == "L" and r[9:].lstrip().startswith("XREF"):
            xs += re.sub(r"^XREF[+=]?", "", r[9:80].strip())
        if r[7] == "G" and r[5] == " ":
            break
    ADL.append(dict(E=E, s=s, J=parse_J(AD[i]), xs=xs, lab=fmt(E, s) + " " + parse_J(AD[i])))


def tokenize(xs):
    toks, probs, s = [], [], xs
    m = re.match(r"^-\(([^)]*)\)(.*)$", s)
    if m:
        toks += [(k, "") for k in keys if k not in set(m.group(1))]
        s = m.group(2)
    i = 0
    while i < len(s):
        c = s[i]
        if c in KEYCH:
            lab = c; i += 1; mod = ""
            if i < len(s) and s[i] == "(":
                j = s.find(")", i)
                if j < 0:
                    probs.append("unclosed '('"); break
                mod = s[i:j + 1]; i = j + 1
                if i < len(s) and s[i] == "(":
                    probs.append("second '(...)' after " + lab + mod)
                    j = s.find(")", i); i = (j + 1) if j >= 0 else len(s)
            toks.append((lab, mod))
        elif c == " ":
            probs.append("embedded space"); i += 1
        else:
            probs.append("illegal char " + repr(c)); i += 1
    return toks, probs


F = []   # findings: (severity, kind, letter, adopted label, token, dataset text, detail)
malformed = []
BYL = defaultdict(list)
for a in ADL:
    toks, probs = tokenize(a["xs"])
    for p in probs:
        malformed.append((a["lab"], a["xs"], p))
    for lab, mod in toks:
        BYL[lab].append(dict(a=a, mod=mod))

MODRE = re.compile(r"^\((\d+(?:\.\d+)?)?([*?]*)\)$")
for lab in sorted(DS):
    P, T = DS[lab], BYL.get(lab, [])
    n = len(P)
    owners = [[] for _ in range(n)]
    sig = lambda a, d: max(math.hypot(a["s"], d["s"]), 1.0)
    wp = lambda a, d: max(WP_MIN, WP_SIG * sig(a, d))
    bare, starbare, expl = [], [], []
    for t in T:
        m = MODRE.match(t["mod"]) if t["mod"] else None
        if t["mod"] == "":
            bare.append(t)
        elif m and m.group(1) is None and "*" in m.group(2):
            starbare.append(t)
        elif m and m.group(1) is None:
            pass                               # (?) questionable: not audited
        elif m:
            expl.append((t, float(m.group(1)), "*" in m.group(2), "?" in m.group(2)))
        else:
            malformed.append((t["a"]["lab"], t["a"]["xs"], "unparsable " + lab + t["mod"]))
    # 1) explicit parentheticals pin a dataset level
    pins = []
    for t, st, star, q in expl:
        c = [i for i in range(n) if abs(P[i]["E"] - st) < 0.06]
        if not c:
            j = min(range(n), key=lambda i: abs(P[i]["E"] - st))
            F.append(("A", "PHANTOM-ENERGY", lab, t["a"]["lab"], lab + t["mod"],
                      "nearest %s level %s" % (lab, fmt(P[j]["E"], P[j]["s"])),
                      "stated %g is not a %s level energy" % (st, lab)))
            continue
        c.sort(key=lambda i: (jbad(t["a"]["J"], P[i]["J"]), abs(P[i]["E"] - t["a"]["E"])))
        i = c[0]
        owners[i].append(dict(t=t, kind="pin", star=star))
        pins.append((t, i, star))
    # 2) bare plain tokens: optimal one-to-one assignment on unpinned levels
    free = [i for i in range(n) if not owners[i]]
    if bare:
        nb, nf = len(bare), len(free)
        C = np.full((nb, nf + nb), 55.0)
        for ti, t in enumerate(bare):
            for fi, i in enumerate(free):
                d = abs(P[i]["E"] - t["a"]["E"])
                if d > wp(t["a"], P[i]):
                    C[ti, fi] = 1e6
                else:
                    C[ti, fi] = min(d / sig(t["a"], P[i]), 30.0) + (40.0 if jbad(t["a"]["J"], P[i]["J"]) else 0.0)
        r_, c_ = linear_sum_assignment(C)
        got = {ti: fi for ti, fi in zip(r_, c_) if fi < nf and C[ti, fi] < 1e5}
        for ti, t in enumerate(bare):
            if ti in got:
                owners[free[got[ti]]].append(dict(t=t, kind="bare", star=False))
            else:
                j = min(range(n), key=lambda i: abs(P[i]["E"] - t["a"]["E"]))
                own = "; ".join("adopted " + o["t"]["a"]["lab"] + " via " + lab + o["t"]["mod"]
                                for o in owners[j]) or "unowned"
                F.append(("A", "NO-OWN-LEVEL", lab, t["a"]["lab"], lab,
                          "nearest %s level %s %s (%s)" % (lab, fmt(P[j]["E"], P[j]["s"]), P[j]["J"], own),
                          "no free %s level within window" % lab))
    # 3) bare starred: ambiguous, owns every level in window
    for t in starbare:
        c = [i for i in range(n) if abs(P[i]["E"] - t["a"]["E"]) <= wp(t["a"], P[i])]
        if not c:
            j = min(range(n), key=lambda i: abs(P[i]["E"] - t["a"]["E"]))
            F.append(("B", "STAR-NO-LEVEL", lab, t["a"]["lab"], lab + "(*)",
                      "nearest %s level %s" % (lab, fmt(P[j]["E"], P[j]["s"])), "no level in window"))
        for i in c:
            owners[i].append(dict(t=t, kind="star", star=True))
    # 4) group checks
    grp = Counter(t["mod"] for t, st, star, q in expl if star)
    for t, st, star, q in expl:
        if star and grp[t["mod"]] < 2:
            F.append(("B", "STAR-ONCE", lab, t["a"]["lab"], lab + t["mod"], "", "starred token on a single adopted level"))
    if len(starbare) == 1:
        F.append(("B", "STAR-ONCE", lab, starbare[0]["a"]["lab"], lab + "(*)", "", "bare (*) on a single adopted level"))
    for i in range(n):
        un = [o for o in owners[i] if not o["star"]]
        if len(un) >= 2:
            for o in un:
                F.append(("A", "SHARED-NO-STAR", lab, o["t"]["a"]["lab"], lab + o["t"]["mod"],
                          "%s level %s %s" % (lab, fmt(P[i]["E"], P[i]["s"]), P[i]["J"]),
                          "%d adopted levels claim this level without *" % len(un)))
    # 5) per-pair checks
    for i in range(n):
        for o in owners[i]:
            a, t = o["t"]["a"], o["t"]
            if o["star"]:
                continue
            d = abs(P[i]["E"] - a["E"])
            if jbad(a["J"], P[i]["J"]):
                F.append(("A", "J-CONFLICT", lab, a["lab"], lab + t["mod"],
                          "%s level %s %s" % (lab, fmt(P[i]["E"], P[i]["s"]), P[i]["J"]), "J incompatible, dE=%.1f" % d))
            if o["kind"] == "bare" and d > max(a["s"] + P[i]["s"], 0.5):
                F.append(("C", "MISSING-PARENTHETICAL", lab, a["lab"], lab,
                          "%s level %s" % (lab, fmt(P[i]["E"], P[i]["s"])),
                          "dE=%.1f outside adopted range %.1f: needs %s(%g)" % (d, a["s"] + P[i]["s"], lab, P[i]["E"])))
            if o["kind"] == "pin" and d > wp(a, P[i]):
                F.append(("A", "FAR-PIN", lab, a["lab"], lab + t["mod"],
                          "%s level %s" % (lab, fmt(P[i]["E"], P[i]["s"])), "dE=%.1f" % d))
    # 6) pin is not the closest level
    for t, i, star in pins:
        if star:
            continue
        a = t["a"]; dpin = abs(P[i]["E"] - a["E"])
        alt = [j for j in range(n) if j != i and not owners[j] and abs(P[j]["E"] - a["E"]) < dpin - 1.0
               and not jbad(a["J"], P[j]["J"])]
        if alt:
            j = min(alt, key=lambda j: abs(P[j]["E"] - a["E"]))
            F.append(("A", "SWAPPED", lab, a["lab"], lab + t["mod"],
                      "closer unclaimed %s level %s %s" % (lab, fmt(P[j]["E"], P[j]["s"]), P[j]["J"]),
                      "token names %g (dE=%.1f); unclaimed level is dE=%.1f" % (P[i]["E"], dpin, abs(P[j]["E"] - a["E"]))))
    # 7) dataset levels nobody owns
    for i in range(n):
        if owners[i]:
            continue
        d = P[i]
        cit = sorted([t for t in T if abs(t["a"]["E"] - d["E"]) <= wp(t["a"], d)], key=lambda t: abs(t["a"]["E"] - d["E"]))
        anyad = sorted([a for a in ADL if abs(a["E"] - d["E"]) <= wp(a, d)], key=lambda a: abs(a["E"] - d["E"]))
        dtxt = "%s level %s %s" % (lab, fmt(d["E"], d["s"]), d["J"])
        if cit:
            t = cit[0]
            F.append(("A", "UNCLAIMED-LEVEL", lab, t["a"]["lab"], lab + t["mod"], dtxt,
                      "no adopted level owns it; nearest citing adopted level is dE=%.1f" % abs(t["a"]["E"] - d["E"])))
        elif anyad:
            F.append(("B", "UNCITED-LEVEL", lab, anyad[0]["lab"], "(no %s)" % lab, dtxt,
                      "adopted level at this energy lacks %s in XREF, dE=%.1f" % (lab, abs(anyad[0]["E"] - d["E"]))))
        else:
            F.append(("B", "MISSING-ADOPTED", lab, "-", "-", dtxt, "no adopted level within window"))

# ---- report ----
ORDER = ["NO-OWN-LEVEL", "UNCLAIMED-LEVEL", "SWAPPED", "SHARED-NO-STAR", "PHANTOM-ENERGY", "J-CONFLICT", "FAR-PIN",
         "STAR-ONCE", "STAR-NO-LEVEL", "UNCITED-LEVEL", "MISSING-ADOPTED", "MISSING-PARENTHETICAL"]
out = io.open(OUT, "w", encoding="utf-8")
w = lambda s="": out.write(s + "\n")
w("letter map: %d datasets, unmapped: %s" % (len(LF), bad_map))
w("tokens audited: %d   findings: %d" % (sum(len(v) for v in BYL.values()), len(F)))
w(str(Counter(k for _, k, *_ in F).most_common()))
w("")
for kind in ORDER:
    rows = sorted([f for f in F if f[1] == kind], key=lambda f: (f[2], f[3]))
    if not rows:
        continue
    w("### %s (%d)" % (kind, len(rows)))
    for sev, k, lab, al, tok, dt, det in rows:
        w("| %s | %s | `%s` | %s | %s |" % (lab, al, tok, dt, det))
    w("")
w("### MALFORMED (%d)" % len(malformed))
for al, xs, p in malformed:
    w("| %s | `XREF=%s` | %s |" % (al, xs, p))
out.close()
print(io.open(OUT, encoding="utf-8").read().split("###")[0])
