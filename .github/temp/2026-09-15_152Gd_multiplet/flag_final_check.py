"""Final check: target .ens column-77 flags vs the claims of the multiplet report.

Independent of the report generator: re-parses Table II, the report's section 7 table
and the target file, then verifies

  (1) the flag tally of the placed G-records,
  (2) that every flagged record maps to an asterisked Table II row,
  (3) the section 6 flag rule  & = case A,  @ = case B with asterisked partner,
      * = everything else,
  (4) section 7's `partner *` column against the source asterisks,
  (5) that the unplaced block carries X / blank only.
"""
import io
import os
import re
import collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
TBL = os.path.join(ROOT, "XUNDL", "2026OSAA_CT11035_152Gd_Table_II.md")
REP = os.path.join(ROOT, "XUNDL", "2026OSAA_CT11035_152Gd_Multiplet_Gammas.md")
ENS = os.path.join(ROOT, "XUNDL", "2026OSAA_CT11035_152Gd.ens")
TOL = 1.0
NUM = re.compile(r"^[0-9]")


def num(s):
    m = re.match(r"-?[0-9]*\.?[0-9]+(?:[eE][-+]?[0-9]+)?", s.strip())
    return float(m.group(0)) if m else None


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


# ---- source ---------------------------------------------------------------
rows = []
for ln, raw in enumerate(io.open(TBL, encoding="utf-8").read().split("\n"), 1):
    line = raw.rstrip("\r")
    if not line.startswith("|"):
        continue
    c = cells(line)
    if len(c) < 5 or not NUM.match(c[1]):
        continue
    rows.append(dict(ln=ln, eg=c[1], ig=c[2], ei=c[0], ef=c[3],
                     E=num(c[1]), ast="*" in c[2]))
astro = [r for r in rows if r["ast"]]

multi = {}
for r in astro:
    p = [q for q in rows if q is not r and abs(q["E"] - r["E"]) <= TOL]
    p.sort(key=lambda q: (abs(q["E"] - r["E"]), q["ln"]))
    multi[r["ln"]] = p


def cls(r, q):
    se = abs(r["E"] - q["E"]) < 0.005
    a, b = num(r["ig"]), num(q["ig"])
    si = a is not None and b is not None and abs(a - b) < 1e-12
    return "A" if se and si else "B" if se else "C" if si else "D"


def expect(r):
    """Section 6 flag for one asterisked source row."""
    cs = [(q, cls(r, q)) for q in multi[r["ln"]]]
    if any(c == "A" for _, c in cs):
        return "&"
    if all(c != "B" or q["ast"] for q, c in cs) and any(c == "B" for _, c in cs):
        return "@"
    return "*"


# ---- target ---------------------------------------------------------------
L = [l.rstrip("\r\n").ljust(80) for l in
     io.open(ENS, encoding="ascii", errors="ignore").read().split("\n")]
placed, unplaced, lvl = [], [], None
for i, e in enumerate(L, 1):
    if e[5] == " " and e[6] == " " and e[7] == "L":
        lvl = i
    elif e[5] == " " and e[6] == " " and e[7] == "G":
        rec = dict(ln=i, E=num(e[9:19]), DE=e[19:21].strip(), RI=e[22:29].strip(),
                   flag=e[76], col80=e[79],
                   lvlE=num(L[lvl - 1][9:19]) if lvl else None)
        (placed if lvl else unplaced).append(rec)
print("target G-records:", len(placed) + len(unplaced),
      "| before first L (unplaced):", len(unplaced), "| placed:", len(placed))
assert len(placed) == 751 and len(unplaced) == 348

tally = collections.Counter(r["flag"] for r in placed)
print("placed col-77 tally:", dict(tally))
assert tally["*"] == 43 and tally["@"] == 6 and tally["&"] == 4 and tally[" "] == 698
utally = collections.Counter(r["flag"] for r in unplaced)
print("unplaced col-77 tally:", dict(utally))
assert set(utally) <= {" ", "X"}, utally
print("col-80 values on flagged records:",
      sorted({r["col80"] for r in placed if r["flag"] != " "} |
             {r["col80"] for r in unplaced}))

# ---- flagged record -> source row ----------------------------------------
def maprow(rec):
    """Placed target record -> asterisked source row (parent level, then E_g and I_g)."""
    ri = num(rec["RI"]) if rec["RI"] else None
    out = []
    for r in astro:
        if abs(r["E"] - rec["E"]) >= 0.005:
            continue
        if rec["DE"] != r["eg"].split("(")[1].rstrip(") "):
            continue
        qi = num(r["ig"].replace("*", ""))
        if ri is None or qi is None or abs(ri - qi) > max(1e-9, 1e-5 * qi):
            continue
        ei = num(r["ei"])
        if rec["lvlE"] is not None and min(abs(rec["lvlE"] - ei),
                                           abs(rec["lvlE"] - ei - 0.01)) < 0.005:
            out.append(r)
    return out


fails = []
seen = collections.Counter()
for rec in placed:
    if rec["flag"] == " ":
        continue
    ms = maprow(rec)
    if len(ms) != 1:
        fails.append(("map", rec["ln"], rec["E"], rec["flag"], len(ms)))
        continue
    r = ms[0]
    seen[(r["ln"], rec["flag"])] += 1
    exp = expect(r)
    if exp != rec["flag"]:
        fails.append(("flag-rule", r["ln"], r["eg"], rec["flag"], exp))
print("\nflagged records mapped:", sum(seen.values()), "| distinct source rows:",
      len({k[0] for k in seen}))
badpair = sorted(k for k, v in seen.items() if v != 1)
print("source rows mapped more than once (row, flag):", badpair)
fails += [("dup-map",) + k for k in badpair]

allast = {r["ln"] for r in astro}
unflagged_ast = sorted(allast - {k[0] for k in seen})
print("asterisked source rows left unflagged:", unflagged_ast)
fails += [("unflagged", k) for k in unflagged_ast]

# ---- report section 6 statements -----------------------------------------
txt = io.open(REP, encoding="utf-8").read().split("\n")
sec6 = [l for l in txt if l.startswith("| `") and l.count("|") >= 4]
print("\nsection 6 flag table rows:", len(sec6))
for l in sec6:
    print("  ", l)
print("non-* enumeration present:", any("The ten non-" in l for l in txt))
LISTED = [("1631.30", "@"), ("1902.30", "@"), ("2104.10", "@"),
          ("2709.50", "&"), ("2728.78", "&")]
for eg, fl in LISTED:
    hits = [r for r in placed if abs(r["E"] - float(eg)) < 0.005 and r["flag"] == fl]
    if len(hits) != 2:
        fails.append(("listed-nonstar", eg, fl, len(hits)))
    print("  non-* listed {}: {} target records flagged {}".format(eg, len(hits), fl))
others = [r for r in placed if r["flag"] in "@&"
          and not any(abs(r["E"] - float(e)) < 0.005 for e, _ in LISTED)]
if others:
    fails.append(("extra-nonstar", [(r["ln"], r["E"], r["flag"]) for r in others]))
print("non-* flags outside the listed five pairs:", len(others))

# ---- report section 7 vs source ------------------------------------------
insec, sec7 = False, []
for ln, line in enumerate(txt, 1):
    if line.startswith("## 7."):
        insec = True
        continue
    if insec and line.startswith("## 8."):
        break
    if insec and line.startswith("|"):
        c = cells(line)
        if c and c[0].split("<br>")[0] in ("A", "B", "C", "D"):
            sec7.append((ln, c))
print("\nsection 7 rows:", len(sec7), "| columns:", len(sec7[0][1]))


def sub(cell, k):
    return cell.split("<br>")[k].strip()


rowfails = []
for ln, c in sec7:
    rec = (sub(c[1], 0).replace("*", ""), sub(c[2], 0), sub(c[5], 0), sub(c[6], 0))
    r = [x for x in astro
         if (x["eg"], x["ig"].replace("*", "").strip(), x["ei"], x["ef"]) == rec]
    if len(r) != 1:
        rowfails.append(("row-map", ln, rec, len(r)))
        continue
    r = r[0]
    ps = [(sub(c[3], k).replace("*", ""), sub(c[4], k), sub(c[7], k), sub(c[8], k))
          for k in range(len(c[3].split("<br>")))]
    qs = [(q["eg"], q["ig"].replace("*", "").strip(), q["ei"], q["ef"])
          for q in multi[r["ln"]]]
    if ps != qs:
        rowfails.append(("partner-set", ln, ps, qs))
    flags = [f.strip() for f in c[9].split("<br>")]
    want = ["yes" if q["ast"] else "no" for q in multi[r["ln"]]]
    if flags != want:
        rowfails.append(("partner-star", ln, flags, want))
    if not sub(c[1], 0).endswith("*"):
        rowfails.append(("record-marker", ln, sub(c[1], 0)))
    tgt = [x for x in placed if abs(x["E"] - r["E"]) < 0.005 and x["flag"] != " "
           and x["RI"] and abs(num(x["RI"]) - num(r["ig"])) <= 1e-6 * abs(num(r["ig"]))
           and x["lvlE"] is not None
           and min(abs(x["lvlE"] - num(r["ei"])),
                   abs(x["lvlE"] - num(r["ei"]) - 0.01)) < 0.005]
    if len(tgt) != 1:
        rowfails.append(("flag-lookup", ln, r["eg"], r["ei"], len(tgt)))
    elif tgt[0]["flag"] != expect(r):
        rowfails.append(("flag-rule-s7", ln, r["eg"], tgt[0]["flag"], expect(r)))
print("section 7 rows with a problem:", len(rowfails))
for f in rowfails:
    print("  ", f)

print("\n--- FAILURES: {} ---".format(len(fails) + len(rowfails)))
for f in fails:
    print("  ", f)

# ---- target-only cross-check --------------------------------------------
tgt_fails = []
for rec in placed:
    if rec["flag"] == " ":
        continue
    ns = [x for x in placed if x is not rec and abs(x["E"] - rec["E"]) <= TOL]
    cs = []
    for x in ns:
        se = abs(x["E"] - rec["E"]) < 0.005
        ri, xr = num(rec["RI"]) if rec["RI"] else None, num(x["RI"]) if x["RI"] else None
        si = ri is not None and xr is not None and abs(ri - xr) < 1e-12
        cs.append("A" if se and si else "B" if se else "C" if si else "D")
    if "A" in cs and rec["flag"] != "&":
        tgt_fails.append(("no-&", rec["ln"], rec["E"], rec["flag"]))
    if "B" in cs and "A" not in cs:
        sib = [x for x in ns if abs(x["E"] - rec["E"]) < 0.005]
        marked = [x for x in sib if x["flag"] in ("@", "&")]
        if marked and rec["flag"] != "@":
            tgt_fails.append(("no-@", rec["ln"], rec["E"], rec["flag"]))
        if not marked and rec["flag"] != "*":
            tgt_fails.append(("no-*", rec["ln"], rec["E"], rec["flag"]))
    if not cs and rec["flag"] != "*":
        tgt_fails.append(("no-partner", rec["ln"], rec["E"], rec["flag"]))
print("\ntarget-only flag/partner consistency failures:", len(tgt_fails))
for f in tgt_fails:
    print("  ", f)

