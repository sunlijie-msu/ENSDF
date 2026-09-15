"""Rewrite 2026OSAA_CT11035_152Gd_Multiplet_Gammas.md from verified Table II evidence."""
import re

AST = "\u2217"
TOL = 1.0
SRC_MD = r"D:\X\ND\ENSDF\XUNDL\2026OSAA_CT11035_152Gd_Table_II.md"
ENS = r"D:\X\ND\ENSDF\XUNDL\2026OSAA_CT11035_152Gd.ens"
OUT = r"D:\X\ND\ENSDF\XUNDL\2026OSAA_CT11035_152Gd_Multiplet_Gammas.md"


def numsd(txt):
    """'855.17 (19)' -> (855.17, 0.19); '0.308' -> (0.308, None)."""
    t = txt.replace(AST, "").strip()
    m = re.match(r"(-?\d+(?:\.\d+)?)\s*\(\s*(\d+)\s*\)", t)
    if m:
        v = float(m.group(1))
        dec = len(m.group(1).split(".")[1]) if "." in m.group(1) else 0
        return v, int(m.group(2)) * 10.0 ** (-dec)
    m = re.search(r"-?\d+(?:\.\d+)?", t)
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
                     E=e, sd=sd, I=val(c[2]), ast=AST in c[2]))
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

tbl = []
for k, r in enumerate(ast, 1):
    ln, flag = match(r)
    part = [q for q in rows if q is not r and abs(q["E"] - r["E"]) <= TOL]
    exact = [q for q in part if abs(q["E"] - r["E"]) < 0.005]
    twin = [q for q in part if q["ast"] and abs(q["E"] - r["E"]) < 0.005
            and abs(q["I"] - r["I"]) <= 1e-12]
    if exact:
        assert all(q["ast"] for q in exact) or all(not q["ast"] for q in exact), r
        cls = ("A" if abs(exact[0]["I"] - r["I"]) < 1e-12 else "B") if exact[0]["ast"] else "C"
    else:
        cls = "D"
    lines = [ln] + [match(q)[0] for q in twin] if cls == "A" else [ln]
    ps = []
    for q in sorted(part, key=lambda z: abs(z["E"] - r["E"])):
        eq = "=" if abs(q["I"] - r["I"]) < 1e-12 else "\u2260"
        ps.append("{:.2f}{} (\u0394{:+.2f} keV, I\u03b3 {} {})".format(
            q["E"], AST if q["ast"] else "", q["E"] - r["E"], eq, "{:g}".format(q["I"])))
    tbl.append(dict(k=k, r=r, tln="/".join(str(x) for x in sorted(lines)), flag=flag,
                    cls=cls, part=part, txt="<br>".join(ps)))

cls_count = {c: sum(1 for x in tbl if x["cls"] == c) for c in "ABCD"}
flag_tally = {f: sum(1 for x in tbl if x["flag"] == f) for f in "*@&"}
d_both = sum(1 for x in tbl if x["cls"] == "D" and any(q["ast"] for q in x["part"]))

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

incons, worst = 0, None
for x in tbl:
    r = x["r"]
    q = min(x["part"], key=lambda z: abs(z["E"] - r["E"]))
    if r["sd"] is None or q["sd"] is None:
        continue
    d = abs(q["E"] - r["E"]) - (r["sd"] + q["sd"])
    if d > 0:
        incons += 1
        if worst is None or d > worst[0]:
            worst = (d, r, q)
maxd, maxr, maxq = max(((abs(q["E"] - x["r"]["E"]), x["r"], q)
                        for x in tbl for q in x["part"]), key=lambda z: z[0])

# ---- report --------------------------------------------------------------
L = []
A = L.append
A("# 152Gd (2026OSAA, CT11035) \u2014 Multiplet Gamma (\u2217) Audit")
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
A("| Target | `2026OSAA_CT11035_152Gd.ens` | 201 L-records, 751 placed G-records; 348 further unplaced G-records (lines 44\u2013391) |")
A("| Source of truth | `2026OSAA_CT11035_152Gd_Table_II.md` | 751 data rows; asterisk footnote at line 758 |")
A("| Source, machine-readable | `2026OSAA_CT11035_152Gd_Table_II.csv` | same 751 rows, 5 columns; ASCII `*` appended to I\u03b3 |")
A("| Superseded | `2026OSAA_CT11035_152Gd_old_Table_I.md` | 10-column version, 752 rows; provenance only |")
A("")
A("No source file was modified. All 751 Table II transitions match target placed G-records 1:1 in E_\u03b3, "
  "I\u03b3 and level assignment (748 carry an I\u03b3; 615.6, 432.5 and 1047.9 are `[E0]` transitions with no "
  "I\u03b3 in either file), so the notes below concern the asterisk markup and the flags it implies. The 348 "
  "unplaced G-records have no counterpart in Table II (no shared E_\u03b3) and are outside this audit.")
A("")
A("## 2. Author footnote (verbatim)")
A("")
A("> Asterisk (\\*) possibly indicates \"Multiplet gamma with unresolvable intensity. "
  "Total multiplet intensity is given for each gamma.\" \u2014 Table II, line 758")
A("")
A("Superseded Table I, line 756: ``Asterisks indicate `a multiply-placed gamma transition "
  "with intensity not divided`.``")
A("")
A("## 3. Verified asterisk inventory")
A("")
A("| Source | Data rows | \u2217 in I\u03b3 | \u2217 in E\u03b3 |")
A("|--------|-----------|-----------|-----------|")
A("| Table II `.md` | 751 | 53 | 0 |")
A("| Table II `.csv` | 751 | 53 (ASCII `*`) | 0 |")
A("| old Table I `.md` | 752 | 53 | 16 (all with E_i \u2265 3479.34) |")
A("")
A("- The 53 asterisked rows are the **same 53 rows** in all three files (same (E_i, E_\u03b3) pairs, "
  "identical E_\u03b3 multiset); Table II dropped Table I's extra E_\u03b3 asterisks.")
A("- Table II carries no other markup: `\u2217` (53) and U+2212 minus signs only.")
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
  "is {:.2f} keV ({:.2f} vs {:.2f}).".format(TOL, maxd, maxr["E"], maxq["E"]))
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
A("## 5. Classification of the 53 asterisked records")
A("")
A("| Group | Records | E_\u03b3 (keV) | Description |")
A("|-------|---------|--------------|-------------|")
A("| A | {} | 2709.50, 2728.78 | identical E_\u03b3, both placements asterisked, identical I\u03b3 |".format(cls_count["A"]))
A("| B | {} | 1631.30, 1902.30, 2104.10 | identical E_\u03b3, both placements asterisked, different I\u03b3 |".format(cls_count["B"]))
A("| C | {} | 1857.20 | identical E_\u03b3, partner not asterisked |".format(cls_count["C"]))
A("| D | {} | the remaining near-degenerate rows | 0.03 \u2264 |\u0394E_\u03b3| \u2264 1.0 keV; {} have both members "
  "asterisked, {} only one |".format(cls_count["D"], d_both, cls_count["D"] - d_both))
A("")
A("## 6. Column-77 flags applied in the target")
A("")
A("| Group | Records | col 77 | Rationale |")
A("|-------|---------|--------|-----------|")
A("| A | {} | `&` | identical E_\u03b3 and identical I\u03b3 at both placements \u2192 one transition placed "
  "twice, intensity not divided |".format(cls_count["A"]))
A("| B | {} | `@` | identical E_\u03b3 but different I\u03b3 \u2192 one transition placed twice, intensity "
  "suitably divided |".format(cls_count["B"]))
A("| C | {} | `*` | multiply-placed gamma ray; the partner placement is unmarked, so no division can be "
  "asserted |".format(cls_count["C"]))
A("| D | {} | `*` | the two energies differ by 0.03\u20131.0 keV, so they are distinct transitions in an "
  "unresolved multiplet; `&`/`@` would assert one transition placed twice |".format(cls_count["D"]))
A("")
A("Applied tally in `2026OSAA_CT11035_152Gd.ens`: **{}** `*`, **{}** `@`, **{}** `&` (all 53 flagged "
  "G-records); the remaining 698 G-records keep column 77 blank. `?` is not legal in column 77, and "
  "column 80 was left unchanged for all 53 records.".format(flag_tally["*"], flag_tally["@"], flag_tally["&"]))
A("")
A("## 7. Per-record evidence")
A("")
A("| # | Table II line | E_i (keV) | E_\u03b3 (keV) | I\u03b3\u2217 | E_f (keV) | ens line | col 77 | group | partner(s) within \u00b1{:.1f} keV".format(TOL))
A("|---|---------------|-----------|--------------|--------|-----------|----------|--------|-------|----------------------------------")
for x in tbl:
    r = x["r"]
    A("| {} | {} | {} | {} | {} | {} | {} | `{}` | {} | {} |".format(
        x["k"], r["ln"], r["ei"], r["eg"], r["ig"].replace(AST, ""), r["ef"],
        x["tln"], x["flag"], x["cls"], x["txt"]))
A("")
A("`ens line` is the target G-record (line number) matched on parent level + E_\u03b3 + I\u03b3; two numbers "
  "(`866/1094`) mean the same transition is placed in two target level blocks. A `\u2217` after a partner "
  "energy means that partner row is also asterisked in the source.")
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
  "0.0006(4) and no asterisk; the asterisked 1857.20 de-excites 2201.79 \u2192 344.37. The asterisk "
  "therefore has no confirmed partner in the table and was flagged `*`.")
A("4. **Near-degenerate pairs.** {} of the 53 rows differ from their nearest partner by 0.03\u20131.0 keV, "
  "and for {} of them the separation exceeds the summed quoted uncertainties. If these are unresolved "
  "*doublets of different transitions*, the asterisk is appropriate; if the authors intend *one transition "
  "placed twice*, the E_\u03b3 values should agree and the flag would have to carry the intensity "
  "relation.".format(cls_count["D"], incons))
A("5. **Level 3271.97(10)** is the only source level whose target energy differs by more than 0.05 keV "
  "(target 3271.73(12), \u0394 = \u22120.24 keV); the other 199 levels agree within \u22120.02\u20130.00 keV "
  "(158 of them at \u22120.01 keV, the GLSC refit offset). The source's own ground-state transition "
  "3272.40(16) implies 3272.40(16) \u2014 neither value. Please confirm the adopted energy. All five "
  "\u03b3 rays of this level, including the asterisked 2927.30, sit in the single target block "
  "(ens lines 1283\u20131287).")
A("6. **Superseded E_\u03b3 asterisks.** Table I marked 16 E_\u03b3 cells (all with E_i \u2265 3479.34) that "
  "Table II no longer marks; if those were multiplet markers, Table II has lost that information.")
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
A("- 15% spot check (8 of 53 rows, deterministic sample) re-derived from Table II and re-read from the "
  "target file: E_\u03b3, I\u03b3, parent level, target line number and column 77 match in both directions.")
A("")
open(OUT, "w", encoding="utf-8", newline="\r\n").write("\n".join(L) + "\n")
print("written:", OUT, "lines:", len(L))
print("groups:", len(ast_groups), "multi:", n_multi, "single:", n_single,
      "ast_partner:", rows_with_ast_partner, "incons:", incons, "d_both:", d_both, "base:", base)
print("flags:", flag_tally, "cls:", cls_count, "maxd:", round(maxd, 2), "worst_d:", round(worst[0], 2))
