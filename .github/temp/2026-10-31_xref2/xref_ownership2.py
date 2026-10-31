"""XREF ownership audit v2: adopted XREF tokens <-> dataset levels, both directions."""
import io, math, os, re, sys
from collections import Counter, defaultdict
import numpy as np
from scipy.optimize import linear_sum_assignment

BASE = sys.argv[1] if len(sys.argv) > 1 else "XUNDL/A58/Ni58/new/"
ADOPTED = sys.argv[2] if len(sys.argv) > 2 else "Ni58_adopted.ens"
OUT = sys.argv[3] if len(sys.argv) > 3 else ".github/temp/2026-10-31_xref2/report2.md"
KEYCH = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz#")
MODRE = re.compile(r"^\((\d+(?:\.\d+)?)?([*?]*)\)$")


def lines(p):
    return [x.rstrip("\n").ljust(80) for x in io.open(p, encoding="utf-8", errors="replace")]


def is_L(r):
    return r[5] == " " and r[6] == " " and r[7] == "L"


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


def raw_label(rec):
    d = rec[19:21].strip()
    return rec[9:19].strip() + ("(" + d + ")" if d.isdigit() else "")


def jset(t):
    out = set()
    for tok in re.split(r"[,\s]+", t.strip()) if t else []:
        par = "+" if "+" in tok else ("-" if "-" in tok else None)
        for n in re.findall(r"\d+", tok):
            out.add((int(n), par))
    return out


def jbad(a, b):
    sa, sb = jset(a), jset(b)
    if not sa or not sb:
        return False
    return not any(ja == jb and (pa is None or pb is None or pa == pb) for ja, pa in sa for jb, pb in sb)


norm = lambda s: re.sub(r"\s+", " ", s.upper().strip())
AD = lines(os.path.join(BASE, ADOPTED))
keys = {r[8]: norm(r[9:39]) for r in AD if r[5] == " " and r[6] == " " and r[7] == "X" and r[8] != " "}
files = {}
for fn in os.listdir(BASE):
    if fn.endswith(".ens") and fn != ADOPTED:
        files.setdefault(norm(lines(os.path.join(BASE, fn))[0][9:39]), []).append(fn)
LF = {k: files[v][0] for k, v in keys.items() if len(files.get(v, [])) == 1}
unmapped = [k for k in keys if k not in LF]

DS = {}
for k, fn in LF.items():
    rows = []
    for r in lines(os.path.join(BASE, fn)):
        if is_L(r):
            E, s = parse_E(r)
            if E is not None:
                rows.append(dict(E=E, s=s, J=parse_J(r), lab=raw_label(r) + " " + parse_J(r)))
    rows.sort(key=lambda d: d["E"])
    pos = sorted(d["s"] for d in rows if d["s"] > 0)
    med = pos[len(pos) // 2] if pos else 10.0
    for d in rows:
        d["se"] = d["s"] if d["s"] > 0 else med
    DS[k] = rows

idx = [i for i, r in enumerate(AD) if is_L(r)]
ADL = []
for n, i in enumerate(idx):
    E, s = parse_E(AD[i])
    if E is None:
        continue
    end = idx[n + 1] if n + 1 < len(idx) else len(AD)
    xs, cm = "", ""
    for j in range(i + 1, end):
        r = AD[j]
        if r[5] != " " and r[7] == "L" and r[9:].lstrip().startswith("XREF"):
            xs += re.sub(r"^XREF(?:\+=|=)", "", r[9:80].strip())
        if r[6] == "c" and r[7] == "L":
            cm += " " + r[9:80]
    ADL.append(dict(E=E, s=s, J=parse_J(AD[i]), xs=xs, cm=cm.lower(), lab=raw_label(AD[i]) + " " + parse_J(AD[i])))


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


F, malformed = [], []
BYL = defaultdict(list)
for a in ADL:
    toks, probs = tokenize(a["xs"])
    malformed += [(a["lab"], a["xs"], p) for p in probs]
    for lab, mod in toks:
        BYL[lab].append(dict(a=a, mod=mod))

sg = lambda a, d: max(math.hypot(a["s"], d["se"]), 0.5)
wp = lambda a, d: max(3.0, 3.0 * math.hypot(a["s"], d["se"]))

for lab in sorted(DS):
    P, T = DS[lab], BYL.get(lab, [])
    n = len(P)
    owners = [[] for _ in range(n)]
    tok_owner = {}
    bare, starbare, expl = [], [], []
    for t in T:
        if t["mod"] == "":
            bare.append(t); continue
        m = MODRE.match(t["mod"])
        if not m:
            malformed.append((t["a"]["lab"], t["a"]["xs"], "unparsable " + lab + t["mod"])); continue
        num, fl = m.group(1), m.group(2)
        if num is None and "*" in fl:
            starbare.append(t)
        elif num is None:
            t["q"] = True; bare.append(t)
        else:
            expl.append((t, float(num), "*" in fl))
    pins = []
    for t, st, star in expl:
        c = [i for i in range(n) if abs(P[i]["E"] - st) <= 2.0]
        if not c:
            j = min(range(n), key=lambda i: abs(P[i]["E"] - st))
            F.append(("A", "PHANTOM-ENERGY", lab, t["a"]["lab"], lab + t["mod"], "nearest " + P[j]["lab"],
                      "stated %g is not a %s level energy" % (st, lab)))
            continue
        c.sort(key=lambda i: (round(abs(P[i]["E"] - st), 1), jbad(t["a"]["J"], P[i]["J"]), abs(P[i]["E"] - t["a"]["E"])))
        i = c[0]
        owners[i].append(dict(t=t, kind="pin", star=star)); tok_owner[id(t)] = i
        pins.append((t, i, star))
    free = [i for i in range(n) if not owners[i]]
    unassigned = []
    if bare:
        nb, nf = len(bare), len(free)
        C = np.full((nb, nf + nb), 60.0)
        for ti, t in enumerate(bare):
            for fi, i in enumerate(free):
                d = abs(P[i]["E"] - t["a"]["E"])
                C[ti, fi] = 1e6 if d > wp(t["a"], P[i]) else d / sg(t["a"], P[i]) + (2.0 if jbad(t["a"]["J"], P[i]["J"]) else 0.0)
        r_, c_ = linear_sum_assignment(C)
        got = {ti: fi for ti, fi in zip(r_, c_) if fi < nf and C[ti, fi] < 1e5}
        for ti, t in enumerate(bare):
            if ti in got:
                i = free[got[ti]]
                owners[i].append(dict(t=t, kind="bare", star=False)); tok_owner[id(t)] = i
            elif not t.get("q"):
                unassigned.append(t)
    for t in starbare:
        c = [i for i in range(n) if abs(P[i]["E"] - t["a"]["E"]) <= wp(t["a"], P[i])]
        if not c:
            j = min(range(n), key=lambda i: abs(P[i]["E"] - t["a"]["E"]))
            F.append(("B", "STAR-NO-LEVEL", lab, t["a"]["lab"], lab + "(*)", "nearest " + P[j]["lab"], "no level in window"))
        for i in c:
            owners[i].append(dict(t=t, kind="star", star=True))
    for t in unassigned:
        j = min(range(n), key=lambda i: abs(P[i]["E"] - t["a"]["E"]))
        own = [o["t"]["a"]["lab"] + " via " + lab + o["t"]["mod"] for o in owners[j] if not o["star"]]
        F.append(("A", "NO-OWN-LEVEL", lab, t["a"]["lab"], lab + t["mod"], "nearest " + P[j]["lab"],
                  ("level already claimed by adopted " + "; ".join(own)) if own else "level outside window"))
    grp = Counter(t["mod"] for t, st, star in expl if star)
    for t, st, star in expl:
        if star and grp[t["mod"]] < 2:
            F.append(("B", "STAR-ONCE", lab, t["a"]["lab"], lab + t["mod"], "", "starred token used on one adopted level only"))
    if len(starbare) == 1:
        F.append(("B", "STAR-ONCE", lab, starbare[0]["a"]["lab"], lab + "(*)", "", "bare (*) used on one adopted level only"))
    for i in range(n):
        un = [o for o in owners[i] if not o["star"]]
        if len(un) >= 2:
            for o in un:
                F.append(("A", "SHARED-NO-STAR", lab, o["t"]["a"]["lab"], lab + o["t"]["mod"], P[i]["lab"],
                          "%d adopted levels claim this dataset level, none starred" % len(un)))
    for i in range(n):
        for o in owners[i]:
            if o["star"]:
                continue
            t = o["t"]; a = t["a"]; d = abs(P[i]["E"] - a["E"])
            if jbad(a["J"], P[i]["J"]):
                doc = "documented in adopted comment" if "disagree" in a["cm"] else "UNDOCUMENTED"
                F.append(("A" if doc == "UNDOCUMENTED" else "C", "J-CONFLICT", lab, a["lab"], lab + t["mod"],
                          P[i]["lab"], "J incompatible, dE=%.1f, %s" % (d, doc)))
            if o["kind"] == "pin" and d > wp(a, P[i]):
                F.append(("A", "FAR-PIN", lab, a["lab"], lab + t["mod"], P[i]["lab"], "dE=%.1f beyond window %.1f" % (d, wp(a, P[i]))))
            if o["kind"] == "bare" and d > max(a["s"] + P[i]["s"], 0.5):
                F.append(("C", "MISSING-PARENTHETICAL", lab, a["lab"], lab, P[i]["lab"],
                          "dE=%.1f; convention is %s(%g)" % (d, lab, P[i]["E"])))
    for t, i, star in pins:
        if star:
            continue
        a = t["a"]; dpin = abs(P[i]["E"] - a["E"])
        alt = [j for j in range(n) if j != i and not owners[j] and abs(P[j]["E"] - a["E"]) < dpin - 1.0
               and not jbad(a["J"], P[j]["J"])]
        if alt:
            j = min(alt, key=lambda j: abs(P[j]["E"] - a["E"]))
            F.append(("A", "SWAPPED", lab, a["lab"], lab + t["mod"], "unclaimed " + P[j]["lab"],
                      "token names %g (dE=%.1f); unclaimed level is dE=%.1f" % (P[i]["E"], dpin, abs(P[j]["E"] - a["E"]))))
    for i in range(n):
        if owners[i]:
            continue
        d = P[i]
        cands = sorted([a for a in ADL if abs(a["E"] - d["E"]) <= wp(a, d)],
                       key=lambda a: (jbad(a["J"], d["J"]), abs(a["E"] - d["E"])))
        if not cands:
            F.append(("B", "MISSING-ADOPTED", lab, "-", "-", d["lab"], "no adopted level within window")); continue
        b = cands[0]; dd = abs(b["E"] - d["E"])
        if jbad(b["J"], d["J"]):
            F.append(("A", "MISSING-ADOPTED", lab, b["lab"], "-", d["lab"],
                      "only J-incompatible adopted level nearby (dE=%.1f)" % dd)); continue
        tk = [t for t in T if t["a"] is b]
        if tk:
            t = tk[0]; oi = tok_owner.get(id(t))
            F.append(("A", "UNCLAIMED-LEVEL", lab, b["lab"], lab + t["mod"], d["lab"],
                      "dE=%.1f; that adopted level's token owns %s" % (dd, P[oi]["lab"] if oi is not None else "a (*) group")))
        else:
            F.append(("B", "UNCITED-LEVEL", lab, b["lab"], "(no %s)" % lab, d["lab"], "dE=%.1f, J compatible" % dd))

ORDER = ["NO-OWN-LEVEL", "UNCLAIMED-LEVEL", "SWAPPED", "SHARED-NO-STAR", "PHANTOM-ENERGY", "FAR-PIN", "J-CONFLICT",
         "STAR-ONCE", "STAR-NO-LEVEL", "UNCITED-LEVEL", "MISSING-ADOPTED", "MISSING-PARENTHETICAL"]
out = io.open(OUT, "w", encoding="utf-8")
w = lambda s="": out.write(s + "\n")
w("datasets mapped: %d  unmapped: %s" % (len(LF), unmapped))
w("tokens audited: %d  findings: %d" % (sum(len(v) for v in BYL.values()), len(F)))
w(str(Counter(f[1] for f in F).most_common()))
w("")
for kind in ORDER:
    rows = sorted([f for f in F if f[1] == kind], key=lambda f: (f[2], f[3]))
    if rows:
        w("### %s (%d)" % (kind, len(rows)))
        for sev, k, lab, al, tok, dt, det in rows:
            w("| %s | %s | `%s` | %s | %s |" % (lab, al, tok, dt, det))
        w("")
w("### MALFORMED (%d)" % len(malformed))
for al, xs, p in malformed:
    w("| %s | `XREF=%s` | %s |" % (al, xs, p))
out.close()
print("\n".join(io.open(OUT, encoding="utf-8").read().split("\n")[:4]))
