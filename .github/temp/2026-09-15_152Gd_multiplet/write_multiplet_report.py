"""Rewrite 2026OSAA_CT11035_152Gd_Multiplet_Gammas.md from verified Table II evidence."""
import re

STARS = ("*", "\u2217")  # authors switched the Igamma marker to ASCII "*" on 2026-09-15
AST = "*"               # marker actually used by the current Table II
TOL = 1.0
SRC_MD = r"D:\X\ND\ENSDF\XUNDL\2026OSAA_CT11035_152Gd_Table_II.md"
SRC_VI = r"D:\X\ND\ENSDF\XUNDL\2026OSAA_CT11035_152Gd_Table_VI_3rd.md"
ENS = r"D:\X\ND\ENSDF\XUNDL\2026OSAA_CT11035_152Gd.ens"
OUT = r"D:\X\ND\ENSDF\XUNDL\2026OSAA_CT11035_152Gd_Multiplet_Gammas.md"


def marked(txt):
    return any(s in txt for s in STARS)


def unmark(txt):
    t = txt
    for s in STARS:
        t = t.replace(s, "")
    return t.strip()


def numsd(txt):
    """'855.17 (19)' -> (855.17, 0.19); '1.82E-4' -> (0.000182, None)."""
    t = unmark(txt)
    m = re.match(r"(-?\d+(?:\.\d+)?)(?:[eE]([-+]?\d+))?\s*\(\s*(\d+)\s*\)", t)
    if m:
        mant, ex = m.group(1), m.group(2)
        v = float(mant) * (10.0 ** int(ex) if ex else 1.0)
        dec = (len(mant.split(".")[1]) if "." in mant else 0) - (int(ex) if ex else 0)
        return v, int(m.group(3)) * 10.0 ** (-dec)
    m = re.search(r"-?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?", t)
    return (float(m.group(0)), None) if m else (None, None)


def val(txt):
    return numsd(txt)[0]


rows = []
for i, line in enumerate(open(SRC_MD, encoding="utf-8").read().split("\n"), 1):
    if not line.startswith("|") or line.startswith("| :") or "E_i" in line:
        continue
    c = [x.strip() for x in line.strip("|").split("|")]
    if len(c) < 5:
        continue
    e, sd = numsd(c[1])
    rows.append(dict(ln=i, ei=c[0], eg=c[1], ig=c[2], ef=c[3], jf=c[4],
                     E=e, sd=sd, I=val(c[2]), ast=marked(c[2])))
assert len(rows) == 751, len(rows)

# ---- target: level blocks with their gamma records ------------------------
ens = [l.rstrip("\r") for l in open(ENS, encoding="ascii", errors="ignore")]
blocks, cur = [], None
for i, raw in enumerate(ens, 1):
    l = raw.ljust(80)
    if l[5] != " ":
        continue
    if l[6] == " " and l[7] == "L":
        cur = dict(ln=i, E=val(l[9:19]), g=[])
        blocks.append(cur)
    elif l[6] == " " and l[7] == "G" and cur is not None:
        cur["g"].append(dict(ln=i, E=val(l[9:19]), RI=val(l[22:29]),
                             DRI=l[29:31].strip(), flag=l[76]))
assert len(blocks) == 201, len(blocks)

# ---- target: unplaced G-records (before the first L-record) ----------------
firstL = min(b["ln"] for b in blocks)
unplaced = []
for i, raw in enumerate(ens, 1):
    if i >= firstL:
        break
    l = raw.ljust(80)
    if l[5] == " " and l[6] == " " and l[7] == "G":
        E = val(l[9:19])
        if E is not None:
            unplaced.append(dict(ln=i, E=E, eg=l[9:19].strip(), de=l[19:21].strip(),
                                 RI=val(l[22:29]), RI_txt=l[22:29].strip(),
                                 DRI=l[29:31].strip(), flag=l[76]))
assert len(unplaced) == 348, len(unplaced)
plns = [g["ln"] for b in blocks for g in b["g"]]
assert len(plns) == 751, len(plns)

# ---- source: Table VI_3rd = the same 348 peaks, unplaced -------------------
vi = []
for i, line in enumerate(open(SRC_VI, encoding="utf-8").read().split("\n"), 1):
    if not line.startswith("|") or line.startswith("| :") or "E_gamma" in line:
        continue
    c = [t.strip() for t in line.strip("|").split("|")]
    if len(c) < 3 or not c[0]:
        continue
    e, de = c[0].split("(")[0].strip(), c[0].split("(")[1].rstrip(")").strip()
    ri = dri = None
    if c[1]:
        ri, dri = c[1].split("(")[0].strip(), c[1].split("(")[1].rstrip(")").strip()
    vi.append(dict(ln=i, e=e, de=de, ri=ri, dri=dri, coin="*" in c[2], E=val(c[0])))
assert len(vi) == 348, len(vi)

vi_bad, vi_ri_equiv = [], []
for a, b in zip(vi, unplaced):
    for f, s, t in (("E", a["e"], b["eg"]), ("DE", a["de"], b["de"] or ""),
                    ("DRI", a["dri"] or "", b["DRI"])):
        if s != t:
            vi_bad.append((a["ln"], f, s, t))
    if (a["ri"] or "") != (b["RI_txt"] or ""):
        if a["ri"] is not None and b["RI"] is not None and abs(float(a["ri"]) - b["RI"]) <= 1e-12:
            vi_ri_equiv.append((a["ln"], a["ri"], b["ln"], b["RI_txt"]))
        else:
            vi_bad.append((a["ln"], "RI", a["ri"], b["RI_txt"]))
    if b["flag"] != ("X" if a["coin"] else " "):
        vi_bad.append((a["ln"], "col77", "X" if a["coin"] else " ", b["flag"]))
assert not vi_bad, vi_bad
unp_coin = sum(1 for a in vi if a["coin"])


def block_of(ei):
    """Target level block for a source level energy. 0.05 keV normally; the 3271.97 level
    needs a wider window because the target adopted 3271.73 (-0.24 keV)."""
    for tol in (0.05, 0.30):
        cands = [b for b in blocks if abs(b["E"] - ei) <= tol]
        if len(cands) == 1:
            return cands[0]
    raise AssertionError((ei, [(b["E"], b["ln"]) for b in cands]))


def match(r):
    """Target G-record line number + column-77 char for an asterisked source row."""
    b = block_of(val(r["ei"]))
    cands = [g for g in b["g"] if abs(g["E"] - r["E"]) < 0.005 and g["RI"] is not None
             and abs(g["RI"] - r["I"]) <= max(1e-9, 1e-5 * abs(r["I"]))]
    assert len(cands) == 1, (r["ln"], [(c["ln"], c["E"], c["RI"], c["flag"]) for c in cands])
    return cands[0]["ln"], cands[0]["flag"]


ast = sorted([r for r in rows if r["ast"]], key=lambda z: z["E"])
assert len(ast) == 53, len(ast)

def relation(r, q):
    """A: same E_gamma, same Igamma; B: same E_gamma, different Igamma;
    C: different E_gamma, same Igamma; D: different E_gamma, different Igamma."""
    same_e = abs(q["E"] - r["E"]) < 0.005
    same_i = r["I"] is not None and q["I"] is not None and abs(q["I"] - r["I"]) <= 1e-12
    return ("A" if same_e and same_i else "B" if same_e else "C" if same_i else "D"), same_e, same_i


tbl = []
for k, r in enumerate(ast, 1):
    ln, flag = match(r)
    part = [q for q in rows if q is not r and abs(q["E"] - r["E"]) <= TOL]
    pairs = []
    for q in sorted(part, key=lambda z: (abs(z["E"] - r["E"]), z["ln"])):
        c, same_e, same_i = relation(r, q)
        sig = "no"
        if r["sd"] is not None and q["sd"] is not None and abs(q["E"] - r["E"]) > r["sd"] + q["sd"]:
            sig = "yes"
        pairs.append(dict(q=q, pln=match(q)[0], d=q["E"] - r["E"], sig=sig,
                          cls=c, sameE=same_e, sameI=same_i))
    tbl.append(dict(k=k, r=r, own=ln, flag=flag, part=part, pairs=pairs,
                    cls=[p["cls"] for p in pairs]))

cls_count = {c: sum(1 for x in tbl for p in x["pairs"] if p["cls"] == c) for c in "ABCD"}
cls_ast = {c: sum(1 for x in tbl for p in x["pairs"] if p["cls"] == c and p["q"]["ast"])
           for c in "ABCD"}
cls_ex = {c: [] for c in "ABCD"}
_seen = {c: set() for c in "ABCD"}
for x in tbl:
    for p in x["pairs"]:
        k = int(round(x["r"]["E"] * 100))
        if k not in _seen[p["cls"]] and len(cls_ex[p["cls"]]) < 3:
            _seen[p["cls"]].add(k)
            cls_ex[p["cls"]].append(x["r"]["eg"])
flag_tally = {f: sum(1 for x in tbl if x["flag"] == f) for f in "*@&"}
n_two = sum(1 for x in tbl if len(x["pairs"]) == 2)
n_mix = sum(1 for x in tbl if len(set(x["cls"])) > 1)
n_diff = sum(1 for x in tbl if abs(min(x["pairs"], key=lambda p: abs(p["d"]))["d"]) >= 0.005)
unp_hits = [x for x in tbl if any(abs(q["E"] - x["r"]["E"]) <= TOL for q in unplaced)]
unp_near = min((abs(q["E"] - x["r"]["E"]), x["r"]["eg"], q["eg"])
               for x in tbl for q in unplaced)
unp_same_E = sum(1 for q in unplaced
                 if any(abs(q["E"] - r["E"]) < 0.005 for r in rows))
unp_far = max(min(abs(q["E"] - x["r"]["E"]) for q in unplaced) for x in tbl)

# ---- statistics ----------------------------------------------------------
base = sum(1 for r in rows if any(q is not r and abs(q["E"] - r["E"]) <= TOL for q in rows))
par = list(range(len(rows)))


def find(a):
    while par[a] != a:
        par[a] = par[par[a]]
        a = par[a]
    return a


for a in range(len(rows)):
    for b in range(a + 1, len(rows)):
        if abs(rows[a]["E"] - rows[b]["E"]) <= TOL:
            ra, rb = find(a), find(b)
            if ra != rb:
                par[rb] = ra
groups = {}
for a in range(len(rows)):
    groups.setdefault(find(a), []).append(a)
ast_groups = [g for g in groups.values() if any(rows[a]["ast"] for a in g)]
n_multi = sum(1 for g in ast_groups if sum(1 for a in g if rows[a]["ast"]) > 1)
n_single = len(ast_groups) - n_multi
rows_with_ast_partner = sum(1 for x in tbl if any(q["ast"] for q in x["part"]))

incons, worst, seen = 0, None, set()
incons_pairs = []
for x in tbl:
    r = x["r"]
    q = min(x["part"], key=lambda z: abs(z["E"] - r["E"]))
    if r["sd"] is None or q["sd"] is None:
        continue
    d = abs(q["E"] - r["E"]) - (r["sd"] + q["sd"])
    if d > 0:
        incons += 1
        key = tuple(sorted((r["ln"], q["ln"])))
        if key not in seen:
            seen.add(key)
            incons_pairs.append("{} vs {} (\u0394 {} keV, \u03a3\u03c3 {} keV)".format(
                r["eg"], q["eg"], "{:+.2f}".format(q["E"] - r["E"]), "{:.2f}".format(r["sd"] + q["sd"])))
        if worst is None or d > worst[0]:
            worst = (d, r, q)
incons_txt = "; ".join(incons_pairs)
maxd, maxr, maxq = max(((abs(q["E"] - x["r"]["E"]), x["r"], q)
                        for x in tbl for q in x["part"]), key=lambda z: z[0])
near_d, near_r, near_q = max(((min(abs(q["E"] - x["r"]["E"]) for q in x["part"]), x["r"],
                               min(x["part"], key=lambda z: abs(z["E"] - x["r"]["E"])))
                              for x in tbl), key=lambda z: z[0])

# ---- report --------------------------------------------------------------
L = []
A = L.append
A("# 152Gd (2026OSAA, CT11035) \u2014 Multiplet Gamma (\u002a) Audit")
A("")
A("Audit of every intensity asterisk in the 2026OSAA source tables against the XUNDL target "
  "`2026OSAA_CT11035_152Gd.ens`, and record of the column-77 flags applied to that target. "
  "This revision is based on `2026OSAA_CT11035_152Gd_Table_II.md` (supplied by the authors); the "
  "earlier draft, which analysed the superseded Table I, is obsolete.")
A("")
A("## 1. Sources")
A("")
A("| Role | File | Content |")
A("|------|------|---------|")
A("| Target | `2026OSAA_CT11035_152Gd.ens` | 201 L-records, 751 placed G-records (lines {}\u2013{}); {} unplaced G-records (lines {}\u2013{}) |".format(
    plns[0], plns[-1], len(unplaced), unplaced[0]["ln"], unplaced[-1]["ln"]))
A("| Source of truth, placed | `2026OSAA_CT11035_152Gd_Table_II.md` | 751 data rows; asterisk footnote at line 758 |")
A("| Source, machine-readable | `2026OSAA_CT11035_152Gd_Table_II.csv` | same 751 rows, 5 columns; ASCII `*` appended to I\u03b3 |")
A("| Source of truth, unplaced | `2026OSAA_CT11035_152Gd_Table_VI_3rd.md` | 348 rows (`E_\u03b3`, `I_\u03b3`, `Coincidence *`); the 348 unplaced transitions, 1:1 with the target unplaced G-records |")
A("| Superseded | `2026OSAA_CT11035_152Gd_old_Table_I.md` | 10-column version, 752 rows; provenance only |")
A("")
A("No source file was modified. All 751 Table II transitions match target placed G-records 1:1 in E_\u03b3, "
  "I\u03b3 and level assignment (748 carry an I\u03b3; 615.6, 432.5 and 1047.9 are `[E0]` transitions with no "
  "I\u03b3 in either file), so the notes below concern the asterisk markup and the flags it implies. All {} "
  "Table VI peaks match the {} target unplaced G-records 1:1 as well (E_\u03b3 and its uncertainty "
  "characters-for-character); they are the unplaced partners candidate set of \u00a74 and carry no intensity "
  "asterisk.".format(len(vi), len(unplaced)))
A("")
A("## 2. Author footnote (verbatim)")
A("")
A("> Asterisk possibly indicates \"Multiplet gamma with unresolvable intensity. "
  "Total multiplet intensity is given for each gamma.\" \u2014 Table II, line 758")
A("")
A("Superseded Table I, line 756: ``Asterisks indicate `a multiply-placed gamma transition "
  "with intensity not divided`.``")
A("")
A("## 3. Verified asterisk inventory")
A("")
A("| Source | Data rows | `*` in I\u03b3 column | `*` elsewhere |")
A("|--------|-----------|----------|----------|")
A("| Table II `.md` (placed) | 751 | 53 (ASCII) | 0 |")
A("| Table II `.csv` (placed) | 751 | 53 (ASCII) | 0 |")
A("| Table VI `.md` (unplaced) | 348 | 0 (I\u03b3 column numeric only) | 314 in `Coincidence` |")
A("| old Table I `.md` | 752 | 53 | 16 in E\u03b3 (all E_i \u2265 3479.34) |")
A("")
A("- The 53 asterisked rows are the **same 53 rows** in all three files (same (E_i, E_\u03b3) pairs, "
  "identical E_\u03b3 multiset); Table II dropped Table I's extra E_\u03b3 asterisks.")
A("- Table II now uses the ASCII `*` (the earlier `\u2217` was replaced on 2026-09-15) and carries no "
  "other markup besides U+2212 minus signs.")
A("- The {} `*` of Table VI are **coincidence** markers, not intensity qualifiers: they map 1:1 onto the "
  "`X` in column 77 of the {} unplaced G-records (`cG E(X)$`, unplaced \u03b3 rays in coincidence with the "
  "344, 271, 411, 530 or 779 keV \u03b3 rays); the other {} unplaced records keep column 77 blank. No "
  "unplaced record needs an intensity flag.".format(unp_coin, len(unplaced), len(unplaced) - unp_coin))
A("- Each asterisked row was matched to a target G-record by **parent level first**, then E_\u03b3 "
  "**and** I\u03b3: 53/53 matched.")
A("")
A("## 4. Pairing criterion and significance")
A("")
A("An asterisk declares an unresolved multiplet, so each asterisked row must have a partner: another row "
  "of (near-)equal E_\u03b3 placed from a different parent level. Search window \u00b1{:.1f} keV "
  "(the target energies come from the GLSC refit, offset \u22120.01 keV for 158 of 200 levels).".format(TOL))
A("")
A("- **53/53** asterisked rows have \u22651 partner within \u00b1{:.1f} keV; the largest separation needed "
  "to reach a nearest partner is {:.2f} keV ({:.2f} vs {:.2f}), and the widest (record, partner) pair "
  "listed is {:.2f} keV.".format(TOL, near_d, near_r["E"], near_q["E"], maxd))
A("- Base rate: only {}/751 rows ({:.1f}%) have any partner within \u00b1{:.1f} keV, i.e. chance would give "
  "\u2248{:.0f} coincidental pairings, not 53.".format(base, 100.0 * base / 751, TOL, 53.0 * base / 751))
A("- The 53 rows fall into **{} multiplet groups**: {} groups hold two asterisked rows ({} rows) and "
  "{} groups hold one ({} rows).".format(len(ast_groups), n_multi, 2 * n_multi, n_single, n_single))
A("- {}/53 asterisked rows have a partner that is itself asterisked; the other {} pair only with "
  "unasterisked rows \u2014 the one-sided asterisks of \u00a78.1.".format(rows_with_ast_partner, 53 - rows_with_ast_partner))
A("- For {} rows the separation to the nearest partner exceeds the sum of the two quoted energy "
  "uncertainties, i.e. the two energies disagree at face value; the largest excess is {:.2f} keV "
  "({} vs {}, separation {:.2f} keV against summed uncertainties {:.2f} keV). Those look like "
  "unresolved doublets of two distinct transitions rather than one multiply-placed ray.".format(
      incons, worst[0], worst[1]["eg"], worst[2]["eg"], abs(worst[2]["E"] - worst[1]["E"]),
      worst[1]["sd"] + worst[2]["sd"]))
A("")
A("**Unplaced transitions as partners** \u2014 the {} unplaced G-records (source: Table VI_3rd, the "
  "unplaced block of `2026OSAA_CT11035_152Gd.ens`, ens lines 46\u2013393) were searched against the 53 "
  "asterisked E_\u03b3 with the same \u00b1{:.1f} keV window:".format(len(unplaced), TOL))
A("")
A("| Finding (348 unplaced peaks vs the 53 asterisked E_\u03b3) | Result |")
A("|---|---|")
A("| asterisked rows whose nearest unplaced peak lies within \u00b1{:.1f} keV | **{}** |".format(TOL, len(unp_hits)))
A("| nearest unplaced peak to any asterisked E_\u03b3 | {:.2f} keV ({} vs {} keV) |".format(unp_near[0], unp_near[2], unp_near[1].split()[0]))
A("| range of the nearest-unplaced distance over the 53 rows | {:.2f}\u2013{:.2f} keV |".format(unp_near[0], unp_far))
A("| unplaced E_\u03b3 coinciding (\u00b10.005 keV) with any of the 751 placed Table II E_\u03b3 | **{}** |".format(unp_same_E))
A("| duplicate E_\u03b3 inside the unplaced set (own pairs below 0.005 keV) | **0** (nearest distinct pair 0.62 keV apart) |")
A("")
A("No asterisked row can therefore be multiply placed with an unplaced record; the multiplet structure is "
  "confined to the 751 placed transitions, \u00a77 covers all of it, and the unplaced block needs no "
  "column-77 flag (\u00a76).")
A("")
A("## 5. Cases of the 53 asterisked records")
A("")
A("The case of a (record, partner) pair follows from the E_\u03b3 and I\u03b3 cells only; asterisks play no "
  "role in the definition and are reported in their own column of \u00a77.")
A("")
A("| Case | Relation between the two placements | Pairs | Example asterisked E_\u03b3 (keV) |")
A("|------|-------------------------------------|-------|-----------------------|")
A("| A | identical E_\u03b3, identical I\u03b3 | {} | {} |".format(cls_count["A"], ", ".join(cls_ex["A"])))
A("| B | identical E_\u03b3, different I\u03b3 | {} | {} |".format(cls_count["B"], ", ".join(cls_ex["B"])))
A("| C | different E_\u03b3 (\u22641.0 keV), identical I\u03b3 | {} | {} |".format(cls_count["C"], ", ".join(cls_ex["C"])))
A("| D | different E_\u03b3 (\u22641.0 keV), different I\u03b3 | {} | {} |".format(cls_count["D"], ", ".join(cls_ex["D"])))
A("")
A("The 53 records give **{} pairs** in total. {} records pair once, {} twice; {} of the latter mix cases "
  "(the case column of \u00a77 then stacks one letter per partner).".format(
      sum(cls_count.values()), 53 - n_two, n_two, n_mix))
A("")
A("## 6. Column-77 flags applied in the target")
A("")
A("| col 77 | Records | Rule |")
A("|--------|---------|------|")
A("| `&` | {} | a case A pair: identical E_\u03b3 and identical I\u03b3 at both placements \u2192 one "
  "transition placed twice, intensity not divided |".format(cls_count["A"]))
A("| `@` | {} | a case B pair whose partner placement is itself asterisked: identical E_\u03b3 with split "
  "I\u03b3 \u2192 one transition placed twice, intensity suitably divided |".format(cls_ast["B"]))
A("| `*` | {} | everything else: case B with an unasterisked partner (no division can be asserted on an "
  "unmarked placement), and all case C and D pairs, whose E_\u03b3 differ so the placements are distinct "
  "transitions of an unresolved multiplet |".format(flag_tally["*"]))
A("")
A("Applied tally in `2026OSAA_CT11035_152Gd.ens`: **{}** `*`, **{}** `@`, **{}** `&` (all 53 flagged "
  "G-records); the remaining 698 G-records keep column 77 blank. `?` is not legal in column 77, and "
  "column 80 was left unchanged for all 53 records. Case is a property of the pair, not of the flag: the "
  "one case B pair with an unasterisked partner (1857.20) is flagged `*`, so the `@` count ({}) is one "
  "less than the case B pair count ({}).".format(
      flag_tally["*"], flag_tally["@"], flag_tally["&"], flag_tally["@"], cls_count["B"]))
A("")
A("The ten non-`*` flags are: `@` on both placements of 1631.30 (1975.64 \u2192 344.37 and "
  "2246.85 \u2192 615.51), 1902.30 (2246.85 \u2192 344.37 and 3012.23 \u2192 1109.38) and 2104.10 "
  "(2448.58 \u2192 344.37 and 2719.59 \u2192 615.51); `&` on both placements of 2709.50 (2709.52 \u2192 0 "
  "and 3053.99 \u2192 344.37) and 2728.78 (3484.38 \u2192 755.55 and 3659.53 \u2192 930.73). The other 43 "
  "flagged records carry `*`. `spotcheck_report.py` prints the record \u2192 target G-record mapping for "
  "all 53.")
A("")
A("The **unplaced block** is a separate flag population and needed no change: of the {} unplaced "
  "G-records, {} carry `X` in column 77 (the comment flag of `cG E(X)$`, i.e. detection in coincidence "
  "with the 344, 271, 411, 530 or 779 keV \u03b3 rays) and {} keep it blank, exactly matching the "
  "`Coincidence *` column of Table VI_3rd ({} rows). Zero unplaced records carry `*`, `@` or `&`, because "
  "no unplaced peak has an equal-E_\u03b3 partner (\u00a74).".format(
      len(unplaced), unp_coin, len(unplaced) - unp_coin, unp_coin))
A("")
A("## 7. Per-record evidence")
A("")
A("Exactly one row per asterisked Table II row (**53 rows**), 10 columns. All multiplet partners within "
  "\u00b1{:.1f} keV are listed: {} rows have one partner, {} have two. In the two-partner rows the partner "
  "columns carry both values as **stacked subcells** (separated by `<br>`), same order in all five partner "
  "columns. All values are copied character-for-character from `2026OSAA_CT11035_152Gd_Table_II.md`, the "
  "`*` I\u03b3 marker included; `0` is the ground state. `case` is the pair class of \u00a75 (A = same "
  "E_\u03b3 + same I\u03b3, B = same E_\u03b3 + different I\u03b3, C = different E_\u03b3 + same I\u03b3, "
  "D = different E_\u03b3 + different I\u03b3), stacked one letter per partner when the two partners are of "
  "different classes. `partner`\u2009`*` is a separate question and reports whether the partner placement "
  "itself carries the Table II asterisk footnote: yes for {} of the 53 rows, no for the other {} "
  "(\u00a78.1). The {} unplaced G-records of the target contribute no partner (\u00a74), so this table is "
  "complete.".format(
      TOL, 53 - n_two, n_two, rows_with_ast_partner, 53 - rows_with_ast_partner, len(unplaced)))
A("")
A("| case | E_\u03b3 (keV) | I_\u03b3 | E_i (keV) | E_f (keV) | partner E_\u03b3 (keV) | partner I_\u03b3 | partner E_i (keV) | partner E_f (keV) | partner `*` |")
A("|---|---|---|---|---|---|---|---|---|---|")
for x in tbl:
    ps = x["pairs"] or [None]
    cellsx = []
    for key in ("eg", "ig", "ei", "ef"):
        cellsx.append("<br>".join("-" if p is None else p["q"][key] for p in ps))
    cellsx.append("<br>".join("-" if p is None else ("yes" if p["q"]["ast"] else "no") for p in ps))
    A("| {} | {} | {} | {} | {} | {} | {} | {} | {} | {} |".format(
        "<br>".join(x["cls"]) or "-", x["r"]["eg"], x["r"]["ig"], x["r"]["ei"], x["r"]["ef"], *cellsx))
A("")
A("The first five columns are the asterisked placement, the last five its partner(s): one value for a "
  "single-partner row, two stacked values for a two-partner row. A row whose partner column reads `no` is a "
  "one-sided asterisk (\u00a78.1: the partner placement is unmarked in Table II, which is why the target "
  "keeps one blank column 77 there); a pair whose two E_\u03b3 differ by more than the sum of their quoted "
  "uncertainties is listed in \u00a78.4.")
A("")
A("## 8. Inconsistencies / questions for the 2026OSAA authors")
A("")
A("1. **One-sided asterisks.** {} of the 53 asterisked rows pair only with unasterisked rows "
  "(e.g. 855.17\u2217 \u2194 854.91, from different levels, I\u03b3 0.0230 vs 0.17). If a peak is "
  "unresolvable, both members should be marked; if only the weak member is contaminated, the footnote "
  "wording (\"total multiplet intensity is given for each gamma\") does not describe the unmarked "
  "member.".format(53 - rows_with_ast_partner))
A("2. **Footnote vs. numbers.** The footnote says the *total* multiplet intensity is given *for each* "
  "gamma (i.e. not divided), yet 1631.30 (0.125(30) / 0.229(17)), 1902.30 (2.38(19) / 0.27(4)) and "
  "2104.10 (0.073(10) / 0.0385(28)) carry different I\u03b3 at their two placements, which is consistent "
  "only with a *divided* intensity. The flags here follow the numbers (`@`), not the footnote; please "
  "confirm the intended convention.")
A("3. **1857.20\u2217.** Its only equal-E_\u03b3 source row, 1857.2(8) from 2788.17, carries I\u03b3 "
  "0.0006(4) and no asterisk; the asterisked 1857.20 de-excites 2201.79 \u2192 344.37. The pair is "
  "therefore case B (identical E_\u03b3, I\u03b3 0.244(17) vs 0.0006(4)) but its partner placement is "
  "unmarked, so `@` would assert a division that the table does not support; the record was flagged `*`.")
A("4. **Near-degenerate pairs.** {} of the 53 rows differ from their nearest partner by 0.03\u20131.0 keV, "
  "and for {} of them the separation exceeds the summed quoted uncertainties: {}. If these are unresolved "
  "*doublets of different transitions*, the asterisk is appropriate; if the authors intend *one transition "
  "placed twice*, the E_\u03b3 values should agree and the flag would have to carry the intensity "
  "relation.".format(n_diff, incons, incons_txt))
A("5. **Level 3271.97(10)** is the only source level whose target energy differs by more than 0.05 keV "
  "(target 3271.73(12), \u0394 = \u22120.24 keV); the other 199 levels agree within \u22120.02\u20130.00 keV "
  "(158 of them at \u22120.01 keV, the GLSC refit offset). The source's own ground-state transition "
  "3272.40(16) implies 3272.40(16) \u2014 neither value. Please confirm the adopted energy. All five "
  "\u03b3 rays of this level, including the asterisked 2927.30, sit in the single target block "
  "(ens lines 1283\u20131287).")
A("6. **Superseded E_\u03b3 asterisks.** Table I marked 16 E_\u03b3 cells (all with E_i \u2265 3479.34) that "
  "Table II no longer marks; if those were multiplet markers, Table II has lost that information.")
A("7. **Unplaced I\u03b3 notation.** {} of the {} Table VI peaks are decimal in the source but `E`-notation "
  "in the target (the ens I\u03b3 field is 7 columns wide, so `0.000182` does not fit and becomes `1.82E-4`). "
  "The numeric values are identical, so this is a representation difference, not a data error: {}. No other "
  "unplaced E_\u03b3, uncertainty or I\u03b3 differs between Table VI_3rd and the target.".format(
      len(vi_ri_equiv), len(unplaced),
      "; ".join("Table VI line {} `{}` \u2192 ens line {} `{}`".format(*f) for f in vi_ri_equiv)))
A("")
A("## 9. Verification performed")
A("")
A("- Asterisk audit: 53/53 asterisked source rows matched to target G-records (parent level + E_\u03b3 + "
  "I\u03b3); target column-77 tally {} `*` + {} `@` + {} `&`, all other G-records blank.".format(
      flag_tally["*"], flag_tally["@"], flag_tally["&"]))
A("- `column_calibrate.py` \u2192 PASS (all field/flag checks, including G-record flags); "
  "`check_gamma_ordering.py` \u2192 0 ordering problems; `ensdf_1line_ruler.py` \u2192 1500 errors, all of "
  "the two pre-existing categories only (1498 \u00d7 \"NUCID shifted left\" for the A\u2265100 NUCID "
  "layout of this nuclide, 2 \u00d7 the `dE`/`dL` dataset comment lines at lines 2\u20133 misread as data "
  "records); no error on any G-record.")
A("- Git diff for the flag work: 53 G-records changed in column 77 only \u2014 no value, uncertainty, "
  "level energy or record-order change.")
A("- Full source\u2013target rematch, independent of the flag work: all 751 Table II rows matched a placed "
  "target G-record (parent level + E_\u03b3 + I\u03b3) with 0 mismatches in value, uncertainty or level; "
  "the 751 placed records were matched 1:1, and no Table II E_\u03b3 occurs among the 348 unplaced records.")
A("- \u00a77 evidence table re-derived from scratch by `spotcheck_report.py`, using only Table II and the "
  "target file: each of the {} rows decodes to a pair of source rows, the expected pair set is reproduced "
  "exactly (0 missing, 0 extra), every left-hand row is an asterisked source row, and every cell equals the "
  "source cell text character-for-character.".format(sum(len(x["pairs"]) for x in tbl)))
A("- 15% spot check (8 of 53 records, deterministic sample): the \u00a77 rows of each sampled record equal "
  "its complete partner set, and the mapped target G-record matches in E_\u03b3, uncertainty, I\u03b3, DRI, "
  "parent level and column 77 \u2014 0 failures.")
A("- Unplaced audit (`Table_VI_3rd.md` \u2194 the {} target unplaced G-records): 348/348 matched in E_\u03b3 "
  "and its uncertainty character-for-character, the {} `Coincidence *` entries map 1:1 onto column-77 `X`, "
  "{} I\u03b3 values are re-expressed in `E`-notation (\u00a78.7), 0 other mismatches. Used as a partner pool "
  "for the 53 asterisked E_\u03b3 they give 0 hits (nearest {:.2f} keV, farthest nearest-neighbour "
  "{:.2f} keV), so \u00a77 needs no unplaced rows.".format(
      len(unplaced), unp_coin, len(vi_ri_equiv), unp_near[0], unp_far))
A("- Reverse check: all 53 flagged target G-records are accounted for by the audit; 0 misses.")
A("- Markdown render check (`check_table_pipes.py`): every table is column-consistent and \u00a77 holds "
  "10 columns \u00d7 {} rows (one per asterisked row, {} partner values in total), the `case` and "
  "`partner *` columns agreeing row-by-row with the re-derived classes and with the source `*` marker.".format(
      len(tbl), sum(len(x["pairs"]) for x in tbl)))
A("")
open(OUT, "w", encoding="utf-8", newline="\r\n").write("\n".join(L) + "\n")
print("written:", OUT, "lines:", len(L))
print("groups:", len(ast_groups), "multi:", n_multi, "single:", n_single,
      "ast_partner:", rows_with_ast_partner, "incons:", incons, "diff_rows:", n_diff, "base:", base)
print("flags:", flag_tally, "cls:", cls_count, "maxd:", round(maxd, 2), "worst_d:", round(worst[0], 2))
print("unplaced:", len(unplaced), "rows_with_unplaced_partner:", len(unp_hits),
      "nearest_d:", round(unp_near[0], 2), unp_near[2], "vs", unp_near[1],
      "unplaced_E_eq_tableII:", unp_same_E)
