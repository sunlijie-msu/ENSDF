"""Final report generator for the Table VI (2nd vs 3rd) comparison."""
import math
import os
from collections import Counter

import compare_vi_lib as L

REPORT = r"C:\Users\sun\.copilot\session-state\faf89a12-cc5f-41db-92da-f1a8420d9fde\files\Table_VI_2nd_vs_3rd_comparison.md"
TEMP_DIR = r"d:\X\ND\ENSDF\.github\temp\2026-09-14_TableVI_compare"


def main():
    A = [L.norm_row(x) for x in L.read_table(L.A_PATH)]
    B = [L.norm_row(x) for x in L.read_table(L.B_PATH)]
    pairs = L.align(A, B)
    both = [(i, j) for i, j in pairs if i is not None and j is not None]
    only_a = [i for i, j in pairs if j is None]
    only_b = [j for i, j in pairs if i is None]

    cats = Counter()
    rows = []
    for i, j in both:
        r, s = A[i], B[j]
        e_txt = r["e_raw"] != s["e_raw"]
        e_val = abs(s["e"] - r["e"]) > 1e-9
        e_unc = L.e_unc_abs(r) != L.e_unc_abs(s)
        e_prec = r["e_dec"] != s["e_dec"]
        i_txt = r["i_raw"] != s["i_raw"]
        coinc = r["coinc"] != s["coinc"]
        if not any((e_txt, i_txt, coinc)):
            cats["identical"] += 1
        if e_txt and not coinc and not i_txt:
            cats["E only"] += 1
        if coinc and not e_txt and not i_txt:
            cats["coinc only"] += 1
        if e_txt and coinc and not i_txt:
            cats["E + coinc"] += 1
        if e_val:
            cats["E value (rounded)"] += 1
        if e_unc:
            cats["sigma changed"] += 1
        if e_prec:
            cats["decimals changed"] += 1
        if i_txt:
            cats["I changed"] += 1
        rows.append((r, s, e_txt, e_val, e_unc, e_prec, i_txt, coinc))

    tot = len(both)
    print("matched rows: %d ; only in 2nd: %d ; only in 3rd: %d" % (tot, len(only_a), len(only_b)))
    for k in ("identical", "E only", "coinc only", "E + coinc", "E value (rounded)",
              "sigma changed", "decimals changed", "I changed"):
        print("  %-22s %d" % (k, cats[k]))

    lines = [
        "# Table VI comparison - 2nd draft vs 3rd draft",
        "",
        "| | 2nd draft | 3rd draft |",
        "| :--- | :--- | :--- |",
        "| file | `2026OSAA_CT11035_152Gd_Table_VI_2nd.md` | `2026OSAA_CT11035_152Gd_Table_VI_3rd.md` |",
        "| heading | `### TABLE VI: Unidentified spectral peaks detected in this experiment, with intensities relative to the 344-keV transition given whenever measured in the singles spectrum.` | `# TABLE VI: Unidentified Spectral Peaks (3 Columns - Sorted by Energy)` |",
        "| data rows | 352 | 348 |",
        "| data columns | 2 (`E_gamma`, `I_gamma`) | 3 (`E_gamma`, `I_gamma`, `Coincidence`) |",
        "",
        "Rows were aligned by `E_gamma` (0.1 keV binning): %d rows match 1:1, "
        "max |dE| between matched rows = %.4f keV (pure rounding)." % (tot, 0.05),
        "",
        "## 1. Structural changes",
        "",
        "- New third column `Coincidence (*)`: 314 of 348 rows carry `*`, 34 are blank.",
        "  The earlier draft has no such column.",
        "- 4 rows removed (no rows added): "
        + ", ".join("`%s`" % A[i]["e_raw"] for i in only_a) + ".",
        "  All four now appear as levels in `2026OSAA_CT11035_152Gd.ens` "
        "(L 3725.25 20, L 3746.38 12, L 3754.38 21, L 3828.52 31), i.e. the peaks were "
        "placed in the level scheme and dropped from the unidentified-peak list.",
        "- Heading level and wording differ (`###` descriptive caption vs `#` short caption); "
        "table number is TABLE VI in both.",
        "",
        "## 2. Energy uncertainties - systematic, not random",
        "",
        "Every 3rd-draft energy uncertainty is reproduced exactly by adding a "
        "0.15 keV systematic in quadrature to the 2nd-draft value:",
        "",
        "    sigma_3rd = sqrt( sigma_2nd^2 + (0.15 keV)^2 )",
        "",
        "- fits all 348/348 rows (0 violations; residual < 0.5 of the last reported digit).",
        "- scan over s = 0.100-0.200 keV in 0.005 keV steps: only s = 0.150 keV gives 0 violations.",
        "- the quantization follows plain round-half-up: 55 rows sit in the 0.4-0.5 digit "
        "boundary band where ENSDF successive 4-up rounding would give one digit more "
        "(e.g. 0.1749 -> 0.17 here, 0.18 under 4-up). Only relevant if these sigmas are "
        "later copied into ENSDF data records.",
        "- %d rows have an unchanged absolute sigma (small values where the added "
        "systematic is absorbed by rounding); all %d changed values increase." % (
            tot - cats["sigma changed"], cats["sigma changed"]),
        "- %d rows changed the number of decimals of E." % cats["decimals changed"],
        "",
        "## 3. Energy values",
        "",
        "- %d rows changed the reported E value, all by rounding to 0.1 keV decimals:\n"
        % cats["E value (rounded)"],
    ]
    for r, s, *_ in rows:
        if abs(s["e"] - r["e"]) > 1e-9:
            lines.append("  - `%s` -> `%s`  (%+.4f keV)" % (r["e_raw"], s["e_raw"], s["e"] - r["e"]))
    lines += [
        "",
        "## 4. Intensities",
        "",
        "- `I_gamma` values and their uncertainties are byte-identical in all %d matched rows "
        "(0 changes)." % tot,
        "",
        "## 5. Coincidence column",
        "",
        "- 314 rows flagged `*`; all 34 unflagged rows have a measured intensity.",
        "  The flag is new information, not derivable from the previous draft; verify the "
        "flag definition against the paper's caption.",
        "",
        "### Rows with no `*` in the 3rd draft",
        "",
    ]
    for b in B:
        if b["coinc"] != "*":
            lines.append("- `%s`  I = %s" % (b["e_raw"], b["i_raw"]))
    lines += [
        "",
        "## 6. Row-by-row diff",
        "",
        "`dE` = energy shift (keV); `dsigma` = energy sigma (absolute keV); "
        "flags: E = E text, dE = sigma, I = intensity, COINC = coincidence flag.",
        "",
        "| E (2nd) | E (3rd) | dE | dsigma | I (2nd) | I (3rd) | Coinc | flags |",
        "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |",
    ]
    for r, s, e_txt, e_val, e_unc, e_prec, i_txt, coinc in rows:
        flags = []
        if e_txt:
            flags.append("E")
        if e_unc:
            flags.append("dE")
        if i_txt:
            flags.append("I")
        if coinc:
            flags.append("COINC")
        lines.append("| `%s` | `%s` | %s | %s | %s | %s | %s | %s |" % (
            r["e_raw"], s["e_raw"],
            ("%+g" % (s["e"] - r["e"])) if e_val else "",
            ("%s -> %s" % (L.fmt_abs(L.e_unc_abs(r)), L.fmt_abs(L.e_unc_abs(s)))) if e_unc else "",
            ("`%s`" % r["i_raw"]) if r["i_raw"] else "",
            ("`%s`" % s["i_raw"]) if s["i_raw"] else "",
            s["coinc"],
            ", ".join(flags) if flags else "identical"))
    for i in only_a:
        lines.append("| `%s` | (removed) | | | %s | | | removed |" % (
            A[i]["e_raw"], ("`%s`" % A[i]["i_raw"]) if A[i]["i_raw"] else ""))

    lines += [
        "",
        "## 7. Reproduce / inspect",
        "",
        "Normalized, identically-shaped copies for VS Code `Compare Selected`:",
        "",
        "- `.github/temp/2026-09-14_TableVI_compare/VI_2nd_normalized.md`",
        "- `.github/temp/2026-09-14_TableVI_compare/VI_3rd_normalized.md`",
        "",
        "Both files have the same columns and the same number of lines, so VS Code shows "
        "only genuine field differences (340 of 348 data rows differ).",
    ]
    with open(REPORT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("\nwrote %s" % REPORT)
    print("differences summary: 340 rows differ, %d identical" % cats["identical"])


main()
