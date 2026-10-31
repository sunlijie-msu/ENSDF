"""Independent verification of the C/F matching table (separate parsing path; raw-text lookups)."""
import io, json, os, random, re, sys
from collections import Counter

B = "XUNDL/A58/Ni58/new/"
OUT = ".github/temp/2026-10-31_Ni58_match_CF/"
FILES = {"C": "Ni58_58ni_p_pP_pol_p_pP_p_pPg.ens", "F": "Ni58_58ni_e_eP.ens"}
rows = json.load(io.open(OUT + "rows.json", encoding="utf-8"))
RE_L = re.compile(r"^(.{5})  L (.{10})(.{2}) ?(.{17})")


def raw(p):
    return [x.rstrip("\n").ljust(80) for x in io.open(p, encoding="utf-8", errors="replace")]


def sigma(etxt, de):
    m = re.match(r"^([0-9]+)(?:\.([0-9]+))?(?:E([+-]?[0-9]+))?$", etxt.replace(" ", ""))
    if not m or not de.strip().isdigit():
        return None
    dec = len(m.group(2) or ""); ex = int(m.group(3) or 0)
    return int(de) * 10.0 ** (ex - dec)


def val(etxt):
    m = re.match(r"^([0-9]+(?:\.[0-9]+)?)(?:E([+-]?[0-9]+))?$", etxt.replace(" ", ""))
    return float(m.group(1)) * 10.0 ** int(m.group(2) or 0)


def levels(lines):
    d = {}
    for n, ln in enumerate(lines):
        m = RE_L.match(ln)
        if m and ln[5] == " " and ln[6] == " ":
            d.setdefault((m.group(2).strip(), m.group(3).strip()), []).append((n, ln[21:39].strip()))
    return d


ADL = raw(B + "Ni58_adopted.ens")
AX = levels(ADL)
DSX = {X: levels(raw(B + FILES[X])) for X in FILES}
DSN = {X: sum(len(v) for v in DSX[X].values()) for X in FILES}


def adopted_xref(n):
    out = ""
    for ln in ADL[n + 1:]:
        if ln[5] == " " and ln[6] == " " and ln[7] == "L":
            break
        if ln[5] != " " and ln[7] == "L" and ln[9:].lstrip().startswith("XREF"):
            out += re.sub(r"^XREF(?:\+=|=)", "", ln[9:80].strip())
    return out.strip().rstrip("$")


# ---- 1) reconciliation from raw text ----
cites = {"C": 0, "F": 0}; union = 0
for (et, de), lst in AX.items():
    for n, j in lst:
        t = adopted_xref(n)
        excl = ""
        m = re.match(r"^-\(([^)]*)\)", t)
        if m:
            excl = m.group(1); body = t[m.end():]
        else:
            body = t
        has = {X: (X in re.sub(r"\([^)]*\)", "", body)) or (m is not None and X not in excl) for X in "CF"}
        for X in "CF":
            cites[X] += has[X]
        union += has["C"] or has["F"]
adopted_rows = [r for r in rows if r["kind"] == "adopted"]
ds_rows = [r for r in rows if r["kind"] == "dataset-only"]
print("1) RECONCILIATION (raw text vs table)")
print("   adopted levels citing C or F : raw %d | table rows %d -> %s" % (union, len(adopted_rows), "OK" if union == len(adopted_rows) else "FAIL"))
for X in "CF":
    tbl_lab = sum(1 for r in adopted_rows if r[X])
    print("   adopted levels citing %s      : raw %d | table %d -> %s" % (X, cites[X], tbl_lab, "OK" if cites[X] == tbl_lab else "FAIL"))
    refs = Counter()
    for r in rows:
        c = r[X]
        if c and c["level"]:
            refs[(c["etxt"], c["de"], c["j"])] += 1
    covered = set(refs)
    raw_lv = {(et, de, j) for (et, de), lst in DSX[X].items() for n, j in lst}
    print("   dataset %s levels             : raw %d (distinct %d) | referenced in table %d -> %s" % (
        X, DSN[X], len(raw_lv), len(covered), "OK" if covered == raw_lv else "FAIL (missing %s)" % sorted(raw_lv - covered)[:5]))

# ---- 2) property checks on every pair ----
def jt(t):
    t = re.sub(r"[\[\]()]", "", t or ""); out = set()
    for tok in re.split(r"[,\s]+", t):
        par = "+" if "+" in tok else ("-" if "-" in tok else None)
        for n in re.findall(r"\d+", tok):
            out.add((n, par))
    return out


def compat(a, b):
    sa, sb = jt(a), jt(b)
    return (not sa) or (not sb) or any(na == nb and (pa is None or pb is None or pa == pb) for na, pa in sa for nb, pb in sb)


fail = []
star_levels = Counter()
for r in adopted_rows:
    for X in "CF":
        c = r[X]
        if not c or not c["level"]:
            continue
        a_et, a_de = r["aetxt"], r["ade"]
        sa = sigma(a_et, a_de) or 0.0
        sd = sigma(c["etxt"], c["de"])
        dE = abs(val(a_et) - val(c["etxt"]))
        if c["cls"] == "match":
            if not compat(r["aj"], c["j"]):
                fail.append(("P2 match with incompatible J\u03c0", r["adopted"], X, c["level"]))
            m = re.search(X + r"\((\d+(?:\.\d+)?)[*?]*\)", r["xref"].replace(" ", ""))
            if m and abs(float(m.group(1)) - val(c["etxt"])) > 1e-6:
                fail.append(("P1 label energy != level energy", r["adopted"], X, c["level"]))
print("2) PROPERTY CHECKS on every paired cell: %s" % ("all pass" if not fail else "%d FAIL" % len(fail)))
for f in fail[:10]:
    print("   ", f)

# ---- 3) raw-record spot check: all flagged rows + 15% random of the rest ----
rnd = random.Random(20261031)
flagged = [r for r in rows if r["flagged"]]
rest = [r for r in rows if not r["flagged"]]
sample = flagged + rnd.sample(rest, max(1, round(0.15 * len(rest))))
bad = []
for r in sample:
    if r["kind"] == "adopted":
        hit = AX.get((r["aetxt"], r["ade"]), [])
        hit = [h for h in hit if h[1] == r["aj"]]
        if len(hit) != 1:
            bad.append(("adopted record not unique/consistent", r["adopted"], r["aj"], len(hit))); continue
        t = adopted_xref(hit[0][0]).replace(" ", "")
        for tok in re.findall(r"[CF](?:\([^)]*\))*", r["xref"].replace(" ", "").replace("(allbutj)", "").replace("(allbut", "(")):
            if tok and not t.startswith("-(") and tok not in t:
                bad.append(("label not in raw XREF", r["adopted"], tok, t))
    for X in "CF":
        c = r[X]
        if c and c["level"]:
            hit = [h for h in DSX[X].get((c["etxt"], c["de"]), []) if h[1] == c["j"]]
            if len(hit) != 1:
                bad.append(("dataset record not unique/consistent", X, c["level"], c["j"], len(hit)))
print("3) RAW SPOT CHECK: %d rows (all %d flagged + %d of %d unflagged = %.0f%%) -> %s" % (
    len(sample), len(flagged), len(sample) - len(flagged), len(rest), 100.0 * (len(sample) - len(flagged)) / len(rest),
    "all consistent" if not bad else "%d FAIL" % len(bad)))
for b in bad[:12]:
    print("   ", b)
