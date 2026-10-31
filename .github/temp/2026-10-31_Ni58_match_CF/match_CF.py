"""Level-by-level matching of Ni-58 adopted levels against dataset C and dataset F, per .github/skills/xref-level-matching."""
import io, json, math, os, re, sys
from collections import Counter, defaultdict
import numpy as np
from scipy.optimize import linear_sum_assignment

BASE = "XUNDL/A58/Ni58/new/"
ADOPTED = "Ni58_adopted.ens"
SET = ["C", "F"]
OUT = ".github/temp/2026-10-31_Ni58_match_CF/"
KEYCH = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz#")
WMIN, WSIG, JPEN, WRONG_MARGIN = 3.0, 3.0, 2.0, 1.0
norm = lambda s: re.sub(r"\s+", " ", s.upper().strip())
isL = lambda r: r[5] == " " and r[6] == " " and r[7] == "L"


def rd(p):
    return [x.rstrip("\n").ljust(80) for x in io.open(p, encoding="utf-8", errors="replace")]


def fields(r):
    t = r[9:19].strip().replace(" ", ""); d = r[19:21].strip()
    m = re.match(r"^([0-9]+\.?[0-9]*)(?:E([+-]?\d+))?$", t)
    if not m:
        return None
    mant = m.group(1); ex = int(m.group(2)) if m.group(2) else 0
    dec = ex - (len(mant.split(".")[1]) if "." in mant else 0)
    return dict(val=float(mant) * 10.0 ** ex, sig=(int(d) * 10.0 ** dec if d.isdigit() else None),
                etxt=r[9:19].strip(), de=d, jraw=r[21:39].strip(),
                shown=r[9:19].strip() + ("(" + d + ")" if d.isdigit() else (" " + d if d else "")))


def jtok(t):
    t = re.sub(r"[\[\]()]", "", t or "")
    out = set()
    for tok in re.split(r"[,\s]+", t):
        par = "+" if "+" in tok else ("-" if "-" in tok else None)
        for n in re.findall(r"\d+", tok):
            out.add((n, par))
    return out or None


def jbad(a, b):
    sa, sb = jtok(a), jtok(b)
    if sa is None or sb is None:
        return False
    return not any(na == nb and (pa is None or pb is None or pa == pb) for na, pa in sa for nb, pb in sb)


# ---------- adopted + datasets ----------
AD = rd(BASE + ADOPTED)
keys = {r[8]: norm(r[9:39]) for r in AD if r[5] == " " and r[6] == " " and r[7] == "X" and r[8] != " "}
byid = {}
for fn in os.listdir(BASE):
    if fn.endswith(".ens") and fn != ADOPTED:
        byid.setdefault(norm(rd(BASE + fn)[0][9:39]), []).append(fn)
LF = {k: byid[v][0] for k, v in keys.items() if len(byid.get(v, [])) == 1}

DS = {}
for X in SET:
    rows = [f for f in (fields(r) for r in rd(BASE + LF[X]) if isL(r)) if f]
    rows.sort(key=lambda d: d["val"])
    pos = sorted(d["sig"] for d in rows if d["sig"] is not None)
    med = pos[len(pos) // 2] if pos else 10.0
    for d in rows:
        d["se"] = d["sig"] if d["sig"] is not None else med
    DS[X] = dict(rows=rows, med=med, file=LF[X])

idx = [i for i, r in enumerate(AD) if isL(r)]
ADL = []
for n, i in enumerate(idx):
    f = fields(AD[i])
    if not f:
        continue
    xs, cm = "", ""
    for j in range(i + 1, idx[n + 1] if n + 1 < len(idx) else len(AD)):
        r = AD[j]
        if r[7] == "L" and r[5] != " " and r[9:].lstrip().startswith("XREF"):
            xs += re.sub(r"^XREF(?:\+=|=)", "", r[9:80].strip())
        elif r[6] == "c" and r[7] == "L":
            cm += " " + r[9:80]
    f.update(xs=xs.strip().rstrip("$"), cm=cm.lower(), sa=f["sig"] if f["sig"] is not None else 0.0)
    ADL.append(f)


def tokenize(xs):
    labels, probs, s = [], [], xs
    m = re.match(r"^-\(([^)]*)\)", s)
    if m:
        for k in keys:
            if k not in set(m.group(1)):
                labels.append(dict(letter=k, has_q=False, q="", energy=None, star=False, quest=False, extra=None,
                                   bad=[], shown="all but " + m.group(1)))
        s = s[m.end():]
    s = s.strip()
    i = 0; prev = None; gap = False
    while i < len(s):
        c = s[i]
        if c == " ":
            gap = True; i += 1
            if prev is not None:
                prev["bad"].append("blank within the XREF text")
            continue
        if c not in KEYCH:
            probs.append("illegal character " + repr(c)); i += 1; continue
        lab = dict(letter=c, has_q=False, q="", energy=None, star=False, quest=False, extra=None, bad=[])
        if gap and prev is not None:
            lab["bad"].append("blank within the XREF text")
        gap = False
        i += 1
        while i < len(s) and s[i] == "(":
            j = s.find(")", i)
            if j < 0:
                lab["bad"].append("unclosed qualifier"); i = len(s); break
            inner = s[i + 1:j]; i = j + 1
            if not lab["has_q"]:
                lab["has_q"] = True; lab["q"] = inner
            else:
                lab["bad"].append("double qualifier"); lab["extra"] = inner
        if lab["has_q"]:
            m2 = re.match(r"^(\d+(?:\.\d+)?)?([*?]*)$", lab["q"])
            if m2:
                lab["energy"] = float(m2.group(1)) if m2.group(1) else None
                lab["star"] = "*" in m2.group(2); lab["quest"] = "?" in m2.group(2)
            else:
                lab["bad"].append("unparsable qualifier")
        lab["shown"] = lab["letter"] + ("(" + lab["q"] + ")" if lab["has_q"] else "") + \
            ("(" + lab["extra"] + ")" if lab["extra"] is not None else "")
        labels.append(lab); prev = lab
    return labels, probs


LAB, TXTPROB = {}, {}
for ai, a in enumerate(ADL):
    LAB[ai], TXTPROB[ai] = tokenize(a["xs"])

sc = lambda a, d: max(math.hypot(a["sa"], d["se"]), 0.5)
win = lambda a, d: max(WMIN, WSIG * sc(a, d))
RX = {"C": r"\((?:pol )?p,p'", "F": r"\(e,e'"}
DOC = {X: {ai for ai, a in enumerate(ADL) if re.search(RX[X], a["cm"]) and "disagree" in a["cm"]} for X in SET}
same = lambda a, b: jtok(a) is not None and jtok(a) == jtok(b)


def jcost(X, ai, a, d):
    pen = JPEN if (jbad(a["jraw"], d["jraw"]) and ai not in DOC[X]) else 0.0
    return pen - (0.25 if same(a["jraw"], d["jraw"]) else 0.0)

# ---------- pairing per dataset ----------
RES = {}
for X in SET:
    P = DS[X]["rows"]; n = len(P)
    items = [(ai, lab) for ai in LAB for lab in LAB[ai] if lab["letter"] == X]
    pair, owners = {}, defaultdict(list)
    located = set()
    for ai, lab in items:                                    # 1) (energy) locates the dataset level
        if lab["energy"] is None:
            continue
        c = [d for d in range(n) if abs(P[d]["val"] - lab["energy"]) < 1e-6]
        if not c:
            pair[ai] = dict(level=None, kind="located", star=lab["star"], flags=["missing match: stated energy is not a level of dataset " + X])
            continue
        c.sort(key=lambda d: (jbad(ADL[ai]["jraw"], P[d]["jraw"]), abs(P[d]["val"] - ADL[ai]["val"]), d))
        pair[ai] = dict(level=c[0], kind="located", star=lab["star"], flags=[])
        owners[c[0]].append((ai, "located", lab["star"])); located.add(c[0])
    plain = [(ai, lab) for ai, lab in items if lab["energy"] is None and not lab["star"]]
    free = [d for d in range(n) if d not in located]
    if plain:                                                # 2) one-to-one pairing of unqualified labels
        nb, nf = len(plain), len(free)
        M = np.full((nb, nf + nb), 60.0)
        for ti, (ai, lab) in enumerate(plain):
            a = ADL[ai]
            for fi, d in enumerate(free):
                dE = abs(P[d]["val"] - a["val"])
                M[ti, fi] = 1e6 if dE > win(a, P[d]) else dE / sc(a, P[d]) + jcost(X, ai, a, P[d])
        for ti, fi in zip(*linear_sum_assignment(M)):
            ai, lab = plain[ti]
            if fi < nf and M[ti, fi] < 1e5:
                d = free[fi]; pair[ai] = dict(level=d, kind="bare", star=False, flags=[]); owners[d].append((ai, "bare", False))
            else:
                pair[ai] = dict(level=None, kind="bare", star=False, flags=["missing match: no unpaired level of dataset %s within the window" % X])
    for ai, lab in items:                                    # 3) bare (*) shares the best level in the window
        if lab["energy"] is None and lab["star"]:
            a = ADL[ai]
            c = sorted(((abs(P[d]["val"] - a["val"]) / sc(a, P[d]) + jcost(X, ai, a, P[d]), d)
                        for d in range(n) if abs(P[d]["val"] - a["val"]) <= win(a, P[d])))
            if c:
                d = c[0][1]; pair[ai] = dict(level=d, kind="bare*", star=True, flags=[]); owners[d].append((ai, "bare*", True))
            else:
                pair[ai] = dict(level=None, kind="bare*", star=True, flags=["missing match: no level of dataset %s within the window" % X])
    paired = {pr["level"] for pr in pair.values() if pr["level"] is not None}
    unpaired = [d for d in range(n) if d not in paired]
    for ai, pr in pair.items():                              # 4) classify
        a = ADL[ai]; d = pr["level"]
        if d is None:
            if pr["kind"] == "bare":
                near = [k for k in range(n) if abs(P[k]["val"] - a["val"]) <= win(a, P[k])]
                if near:
                    k = min(near, key=lambda k: abs(P[k]["val"] - a["val"]))
                    own = ", ".join("%s %s" % (ADL[o[0]]["shown"], ADL[o[0]]["jraw"] or "-") for o in owners.get(k, []))
                    pr["flags"] = ["missing match: nearest %s level %s %s is paired with adopted %s" % (X, P[k]["shown"], P[k]["jraw"] or "-", own)]
                else:
                    pr["flags"] = ["missing match: no %s level within the window" % X]
            continue
        dE = abs(P[d]["val"] - a["val"]); s_ = sc(a, P[d])
        if pr["kind"] == "located" and not pr["star"]:
            alt = [u for u in unpaired if not jbad(a["jraw"], P[u]["jraw"]) and abs(P[u]["val"] - a["val"]) < dE - WRONG_MARGIN]
            if alt:
                u = min(alt, key=lambda u: abs(P[u]["val"] - a["val"]))
                pr["flags"].append("wrong match: closer compatible level %s %s stays unpaired" % (P[u]["shown"], P[u]["jraw"] or "-"))
        if jbad(a["jraw"], P[d]["jraw"]):
            doc = re.search(r"\((?:pol )?p,p'" if X == "C" else r"\(e,e'", a["cm"]) and re.search(r"disagree", a["cm"])
            pr["flags"].append("mismatch: J\u03c0 incompatible (%s)" % ("noted in adopted comment" if doc else "not noted in adopted comment"))
        if (not pr["star"]) and dE > WSIG * s_:
            pr["flags"].append("mismatch: energy differs by %.1f keV (%.1f\u03c3)" % (dE, dE / s_))
    for d, lst in owners.items():
        non = [o for o in lst if not o[2]]
        for ai, kind, star in lst:
            if not star and len(lst) >= 2:
                pair[ai]["flags"].append("redundant match: %d adopted levels claim this level, no *" % len(lst))
        if sum(1 for o in lst if o[2]) == 1:
            ai = [o for o in lst if o[2]][0][0]
            pair[ai]["flags"].append("redundant match: * on a single adopted level")
    cnt = Counter(lab["letter"] for lab in LAB_all) if False else None
    RES[X] = dict(pair=pair, owners=owners, unpaired=unpaired, items=items)

# repeated labels and malformed text apply to the row
for ai in LAB:
    cnt = Counter(lab["letter"] for lab in LAB[ai] if not lab["shown"].startswith("all but"))
    for X in SET:
        pr = RES[X]["pair"].get(ai)
        if pr is None:
            continue
        if cnt[X] > 1:
            pr["flags"].append("redundant match: label repeated")
        bad = [b for lab in LAB[ai] if lab["letter"] == X for b in lab["bad"]]
        for b in dict.fromkeys(bad):
            pr["flags"].append("malformed label: " + b)

# ---------- rows ----------
def cell(X, ai):
    pr = RES[X]["pair"].get(ai)
    if pr is None:
        return None
    P = DS[X]["rows"]
    lvl = P[pr["level"]] if pr["level"] is not None else None
    return dict(level=(lvl["shown"] if lvl else None), j=(lvl["jraw"] if lvl else None),
                etxt=(lvl["etxt"] if lvl else None), de=(lvl["de"] if lvl else None),
                cls="; ".join(dict.fromkeys(pr["flags"])) if pr["flags"] else "match", flagged=bool(pr["flags"]))


rows = []
for ai, a in enumerate(ADL):
    labs = [lab for lab in LAB[ai] if lab["letter"] in SET]
    if not labs:
        continue
    shown = " ".join(lab["shown"] if not lab["shown"].startswith("all but") else "(" + lab["shown"] + ")" for lab in labs
                     if not (lab["shown"].startswith("all but") and lab["letter"] != "C"))
    row = dict(kind="adopted", key=a["val"], adopted=a["shown"], aj=a["jraw"], aetxt=a["etxt"], ade=a["de"], xref=shown)
    for X in SET:
        row[X] = cell(X, ai)
    row["flagged"] = any(row[X] and row[X]["flagged"] for X in SET)
    rows.append(row)

for X in SET:
    P = DS[X]["rows"]
    for u in RES[X]["unpaired"]:
        d = P[u]
        near = sorted(((abs(a["val"] - d["val"]) / sc(a, d), ai) for ai, a in enumerate(ADL) if abs(a["val"] - d["val"]) <= win(a, d)))
        if near:
            a = ADL[near[0][1]]
            cites = [lab["shown"] for lab in LAB[near[0][1]] if lab["letter"] == X]
            note = "nearest adopted %s %s (%s)" % (a["shown"], a["jraw"] or "-", ("cites " + cites[0]) if cites else "no %s label" % X)
        else:
            note = "no adopted level within the window"
        row = dict(kind="dataset-only", key=d["val"], adopted="\u2014", aj="", aetxt="", ade="", xref="\u2014", flagged=True)
        for Y in SET:
            row[Y] = None
        row[X] = dict(level=d["shown"], j=d["jraw"], etxt=d["etxt"], de=d["de"],
                      cls="missing match: dataset level unpaired; " + note, flagged=True)
        rows.append(row)
rows.sort(key=lambda r: (r["key"], r["kind"] != "adopted"))

# ---------- reconciliation ----------
rec = []
for X in SET:
    n_lab = len(RES[X]["items"]); n_pair = sum(1 for pr in RES[X]["pair"].values() if pr["level"] is not None)
    n_unp_lab = sum(1 for pr in RES[X]["pair"].values() if pr["level"] is None)
    n_lv = len(DS[X]["rows"]); n_cov = len({pr["level"] for pr in RES[X]["pair"].values() if pr["level"] is not None})
    rec.append((X, DS[X]["file"], n_lab, n_pair, n_unp_lab, n_lv, n_cov, len(RES[X]["unpaired"]), DS[X]["med"]))

# ---------- write ----------
os.makedirs(OUT, exist_ok=True)
H = ["\u26a0", "adopted E(DE)", "adopted J\u03c0", "XREF (C, F)", "C level E(DE)", "C J\u03c0", "C class", "F level E(DE)", "F J\u03c0", "F class"]


def line(r):
    out = ["\u26a0" if r["flagged"] else "", r["adopted"], r["aj"] or "-", r["xref"]]
    for X in SET:
        c = r[X]
        out += ([c["level"] or "\u2014", c["j"] or "-", c["cls"]] if c else ["\u2014", "", ""])
    return "| " + " | ".join(x.replace("|", "\\|") for x in out) + " |"


with io.open(OUT + "Ni58_adopted_vs_C_F_level_matching.md", "w", encoding="utf-8") as f:
    f.write("# Ni-58 adopted levels vs. dataset C (58Ni(p,p')) and dataset F (58Ni(e,e'))\n\n")
    f.write("Parameters: candidate window max(%g keV, %g sigma_combined); J-pi-incompatible pairs penalised by %g sigma; blank dataset DE replaced by the dataset median (C %g keV, F %g keV); wrong-match margin %g keV.\n\n"
            % (WMIN, WSIG, JPEN, DS["C"]["med"], DS["F"]["med"], WRONG_MARGIN))
    f.write("| " + " | ".join(H) + " |\n|" + "---|" * len(H) + "\n")
    for r in rows:
        f.write(line(r) + "\n")
with io.open(OUT + "flagged.md", "w", encoding="utf-8") as f:
    f.write("| " + " | ".join(H) + " |\n|" + "---|" * len(H) + "\n")
    for r in rows:
        if r["flagged"]:
            f.write(line(r) + "\n")
json.dump(rows, io.open(OUT + "rows.json", "w", encoding="utf-8"), ensure_ascii=False)

cls = Counter()
for r in rows:
    for X in SET:
        if r[X] and r[X]["flagged"]:
            for part in r[X]["cls"].split("; "):
                cls[(X, part.split(":")[0])] += 1
print("rows:", len(rows), "flagged rows:", sum(1 for r in rows if r["flagged"]))
for x in rec:
    print("%s %-40s labels=%d paired=%d unpaired_labels=%d | levels=%d covered=%d unpaired_levels=%d | median DE=%g" % x)
for k, v in sorted(cls.items()):
    print("  ", k, v)
