"""Independent audit of the multiplet report's per-record evidence table.

Re-derives, from Table II and the .ens target alone, the asterisked rows, their
partner sets and the target G-record mapping, then compares all of that with the
table actually written to the report.  Nothing is trusted from the generator.
"""
import re

TOL = 1.0
AST = "*"
MD = r"D:\X\ND\ENSDF\XUNDL\2026OSAA_CT11035_152Gd_Multiplet_Gammas.md"
SRC = r"D:\X\ND\ENSDF\XUNDL\2026OSAA_CT11035_152Gd_Table_II.md"
ENS = r"D:\X\ND\ENSDF\XUNDL\2026OSAA_CT11035_152Gd.ens"
DIR = r"D:\X\ND\ENSDF\.github\temp\2026-09-15_152Gd_multiplet"
OUT = DIR + r"\spotcheck_report.txt"
OUT2 = DIR + r"\spotcheck_report_encoded.txt"

rep = [l.rstrip("\r\n") for l in open(MD, encoding="utf-8")]
src = [l.rstrip("\r\n") for l in open(SRC, encoding="utf-8")]
ens = [l.rstrip("\r\n") for l in open(ENS, encoding="ascii", errors="ignore")]

# ---- 1. source rows --------------------------------------------------------
rows = []
for i, line in enumerate(src, 1):
    if not line.startswith("|") or line.startswith("| :") or "E_i" in line:
        continue
    c = [x.strip() for x in line.strip("|").split("|")]
    if len(c) < 5:
        continue
    mI = re.match(r"-?\d+(?:\.\d+)?", c[2])
    rows.append(dict(ln=i, ei=c[0], eg=c[1], ig=c[2], ef=c[3],
                     I=float(mI.group(0)) if mI else None,
                     E=float(re.match(r"-?\d+(?:\.\d+)?", c[1]).group(0)), ast=AST in c[2]))
assert len(rows) == 751, len(rows)
ast_rows = [r for r in rows if r["ast"]]
print("source data rows:", len(rows), "| asterisked rows:", len(ast_rows))

# ---- 2. target G-records ---------------------------------------------------
L = [l.ljust(80) for l in ens]
placed, lvl_ln = [], None
for i, e in enumerate(L, 1):
    if e[6] == " " and e[7] == "L":
        lvl_ln = i
    if e[5] == " " and e[6] == " " and e[7] == "G" and lvl_ln:
        placed.append(dict(ln=i, E=float(e[9:19]), DE=e[19:21].strip(), RI=e[22:29].strip(),
                           DRI=e[29:31].strip(), flag=e[76], lvl=float(L[lvl_ln - 1][9:19]),
                           lvl_ln=lvl_ln))
allg = sum(1 for e in L if e[5] == " " and e[6] == " " and e[7] == "G")
assert len(placed) == 751, (len(placed), allg)
print("target G-records:", allg, "(placed", len(placed), ")")


def num(txt):
    return float(re.match(r"-?\d+(?:\.\d+)?", txt).group(0))


def match(r):
    """Mapped target G-record for one source row (parent level, then E_gamma and I_gamma)."""
    out = []
    for x in placed:
        if abs(x["E"] - r["E"]) >= 0.005 or not x["RI"]:
            continue
        qi = num(r["ig"].replace(AST, "").strip())
        if abs(float(x["RI"]) - qi) > max(1e-9, 1e-5 * qi):
            continue
        ei = num(r["ei"])
        if min(abs(x["lvl"] - ei), abs(x["lvl"] - ei - 0.01)) < 0.005:
            out.append(x)
    return out


fail, enc, rev = [], [], {}
for k, r in enumerate(sorted(ast_rows, key=lambda z: (z["E"], z["ln"])), 1):
    m = match(r)
    if len(m) != 1:
        fail.append(("map", k, r["ln"], [(x["ln"], x["E"], x["RI"]) for x in m]))
        continue
    rev[m[0]["ln"]] = (k, r["ln"])
    if m[0]["flag"] not in "*&@":
        fail.append(("flag", k, r["ln"], m[0]["ln"], repr(m[0]["flag"])))
    enc.append("row {:<3} src line {:<5} Ei {:<12} Eg {:<14} Ig {:<16} -> ens line {:<5} "
               "(lvl {}) flag {!r}".format(k, r["ln"], r["ei"], r["eg"], r["ig"],
                                           m[0]["ln"], m[0]["lvl"], m[0]["flag"]))

flagged = [(x["ln"], x["flag"]) for x in placed if x["flag"] in "*&@"]
rev_miss = [(i, f) for i, f in flagged if i not in rev]
print("target flagged G-records:", len(flagged), "| flags:", sorted({f for _, f in flagged}))
print("mapping failures:", len(fail), "| reverse-check misses:", rev_miss)

# ---- 3. report evidence table, re-derived independently --------------------
hdr = ("| case | E_\u03b3 (keV) | I_\u03b3 | partner E_\u03b3 (keV) | partner I_\u03b3 | "
       "E_i (keV) | E_f (keV) | partner E_i (keV) | partner E_f (keV) | "
       "partner `*` |")
assert hdr in rep, "10-column header not found"
ncol = 10
rep_rows, i = [], rep.index(hdr) + 2
while i < len(rep) and rep[i].startswith("|"):
    rep_rows.append([c.strip() for c in rep[i].strip("|").split("|")])
    i += 1
print("report evidence rows:", len(rep_rows), "| columns:",
      len(rep_rows[0]) if rep_rows else 0)

want = set()
for r in sorted(ast_rows, key=lambda z: (z["E"], z["ln"])):
    for q in sorted((q for q in rows if q is not r and abs(q["E"] - r["E"]) <= TOL),
                    key=lambda z: (abs(z["E"] - r["E"]), z["ln"])):
        want.add((r["ln"], q["ln"]))
bycell = {(r["eg"], r["ig"].replace(AST, "").strip(), r["ei"], r["ef"]): r["ln"] for r in rows}
byline = {r["ln"]: r for r in rows}


def partners(c):
    """Expand the four stacked partner subcells into full 4-tuples + asterisk flags.

    Only the partner E_gamma cell carries the added marker; the I_gamma, E_i and E_f
    cells are matched against the source text exactly as written (the Table II asterisk
    lives in the source I_gamma cell and is therefore stripped before comparing).
    """
    parts = [[v.replace(AST, "").strip() for v in c[k].split("<br>")]
             for k in (3, 4, 7, 8)]
    flags = c[9].split("<br>")
    n = len(parts[0])
    if any(len(p) != n for p in parts) or len(flags) != n:
        fail.append(("partner-cell-count-mismatch", c))
        return []
    out = []
    for k in range(n):
        t = tuple(p[k] for p in parts)
        if flags[k] not in ("yes", "no"):
            fail.append(("partner-flag-text", c, flags[k]))
        elif (flags[k] == "yes") != bool(byline[bycell[t]]["ast"] if t in bycell else None):
            fail.append(("partner-flag-mismatch", c, t, flags[k]))
        else:
            out.append(t)
    return out


def sub(cell, k):
    return cell.split("<br>")[k].strip()


def ast_marked(cell, k):
    """True when the k-th `<br>` subcell of a (partner) E_gamma cell carries the marker."""
    return sub(cell, k).endswith(AST)


def check_eg_markers(c, rec):
    """E_gamma / partner E_gamma markers must follow the Table II asterisk of the placement."""
    if not ast_marked(c[1], 0) or not byline[rec]["ast"]:
        fail.append(("record-eg-marker", rec, c[1]))
    for k in range(len(c[3].split("<br>"))):
        q = byline.get(bycell.get((sub(c[3], k).replace(AST, ""), sub(c[4], k),
                                   sub(c[7], k), sub(c[8], k))))
        if q is not None and ast_marked(c[3], k) != q["ast"]:
            fail.append(("partner-eg-marker", rec, q["ln"], sub(c[3], k), q["ast"]))


def want_case(r, q):
    """A same Eg+same Ig, B same Eg+diff Ig, C diff Eg+same Ig, D diff Eg+diff Ig."""
    same_e = abs(q["E"] - r["E"]) < 0.005
    same_i = r["I"] is not None and q["I"] is not None and abs(q["I"] - r["I"]) <= 1e-12
    return "A" if same_e and same_i else "B" if same_e else "C" if same_i else "D"


got = set()
rec_rows = {}
for c in rep_rows:
    if len(c) != ncol:
        fail.append(("cols", len(c), c))
        continue
    a = bycell.get((c[1].replace(AST, "").strip(), c[2].replace(AST, "").strip(), c[5], c[6]))
    if a is None:
        fail.append(("unmatched-record", c))
        continue
    ps = partners(c)
    exp_cls = [want_case(byline[a], byline[bycell[t]]) for t in ps if t in bycell]
    if c[0].split("<br>") != exp_cls:
        fail.append(("case-mismatch", a, c[0], exp_cls))
    if not byline[a]["ast"]:
        fail.append(("left-not-asterisked", c))
    check_eg_markers(c, a)
    if a in rec_rows:
        fail.append(("record-duplicated", a))
    rec_rows[a] = c
    for g in partners(c):
        b = bycell.get(g)
        if b is None:
            fail.append(("unmatched-partner", c, g))
            continue
        if a == b:
            fail.append(("self-pair", c))
        got.add((a, b))
print("pairs expected:", len(want), "| in report:", len(got),
      "| missing:", len(want - got), "| extra:", len(got - want))
for p in sorted(want - got):
    fail.append(("missing-pair", p))
for p in sorted(got - want):
    fail.append(("extra-pair", p))
for a, c in rec_rows.items():
    exp = len([q for q in rows if q is not byline[a] and abs(q["E"] - byline[a]["E"]) <= TOL])
    if len(partners(c)) != exp:
        fail.append(("record-partner-count", a, len(partners(c)), exp))
print("rows: {} | asterisked rows: {} | two-partner rows: {}".format(
    len(rec_rows), len(ast_rows),
    sum(1 for a, c in rec_rows.items() if len(partners(c)) > 1)))
if len(rec_rows) != len(ast_rows):
    fail.append(("row-count", len(rec_rows), len(ast_rows)))

# ---- 4. deterministic 15% spot check (8 of 53 records) ---------------------
sample = [1, 8, 16, 23, 31, 38, 46, 53]
sast = sorted(ast_rows, key=lambda z: (z["E"], z["ln"]))
for k in sample:
    r = sast[k - 1]
    m = match(r)
    ok_map = len(m) == 1
    rp = [rec_rows[r["ln"]]] if r["ln"] in rec_rows else []
    exp_ln = sorted(q["ln"] for q in rows if q is not r and abs(q["E"] - r["E"]) <= TOL)
    got_ln = sorted(bycell[g] for c in rp for g in partners(c))
    ok_rows = got_ln == exp_ln
    ok_part = all(abs(num(g[0]) - r["E"]) <= TOL and g[0] == byline[bycell[g]]["eg"]
                  for c in rp for g in partners(c))
    ok_ens = False
    if ok_map:
        x, e = m[0], L[m[0]["ln"] - 1]
        ev = re.match(r"(-?\d+(?:\.\d+)?)\s*\((\d+)\)", r["eg"])
        iv = re.match(r"([\d.]+)\s*\((\d+)\)", r["ig"].replace(AST, "").strip())
        ok_ens = (e[9:19].strip() == ev.group(1) and e[19:21].strip() == ev.group(2)
                  and e[22:29].strip() == iv.group(1) and e[29:31].strip() == iv.group(2)
                  and e[76] == x["flag"])
    ok = ok_map and ok_rows and ok_part and ok_ens
    if not ok:
        fail.append(("spot", k, r["ln"], ok_map, ok_rows, ok_part, ok_ens))
    enc.append("spot row {:<3} src line {:<5} Ei {:<12} Eg {:<14} rows {} target line {} "
               "flag {!r} {}".format(k, r["ln"], r["ei"], r["eg"], len(rp),
                                     m[0]["ln"] if ok_map else "-",
                                     m[0]["flag"] if ok_map else "?", "OK" if ok else "FAIL"))

print("failures:", len(fail))
with open(OUT, "w", encoding="utf-8") as fh:
    fh.write("source rows {} asterisked {} target placed {} flagged {}\n".format(
        len(rows), len(ast_rows), len(placed), len(flagged)))
    fh.write("\n".join(enc) + "\n")
    fh.write("evidence rows {} expected pairs {} report pairs {} reverse misses {}\n".format(
        len(rep_rows), len(want), len(got), rev_miss))
    fh.write("FAILURES {}\n".format(len(fail)))
    for f in fail:
        fh.write("  {}\n".format(f))
with open(OUT2, "w", encoding="ascii") as fh:
    fh.write("\n".join(l.encode("ascii", "backslashreplace").decode("ascii")
                       for l in open(OUT, encoding="utf-8").read().split("\n")))
