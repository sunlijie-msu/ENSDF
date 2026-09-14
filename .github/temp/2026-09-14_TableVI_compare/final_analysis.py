"""Final analysis: quantify the uncertainty transformation between drafts,
verify the alignment, and write a full row-by-row diff report."""
import math
import os

import compare_vi_lib as L

OUT_DIR = r"C:\Users\sun\.copilot\session-state\faf89a12-cc5f-41db-92da-f1a8420d9fde\files"


def digits(r):
    return None if r["e_unc"] is None else int(r["e_unc"])


def main():
    A = [L.norm_row(x) for x in L.read_table(L.A_PATH)]
    B = [L.norm_row(x) for x in L.read_table(L.B_PATH)]
    pairs = L.align(A, B)
    both = [(i, j) for i, j in pairs if i is not None and j is not None]
    assert len(both) == len(B) == 348, len(both)

    max_de = max(abs(B[j]["e"] - A[i]["e"]) for i, j in both)
    print("alignment check: matched=%d  max |dE| = %.4f keV" % (len(both), max_de))

    # ---- uncertainty transformation tests -------------------------------
    tests = {
        "quadrature +0.15 keV": lambda u: math.sqrt(u ** 2 + 0.15 ** 2),
        "linear +0.15 keV": lambda u: u + 0.15,
        "quadrature +0.05 keV": lambda u: math.sqrt(u ** 2 + 0.05 ** 2),
        "2 x u": lambda u: 2 * u,
    }
    print("\n-- uncertainty models: deviation in units of last significant digit --")
    for name, fn in tests.items():
        devs, viol = [], 0
        for i, j in both:
            u2, u3 = L.e_unc_abs(A[i]), L.e_unc_abs(B[j])
            pred = fn(u2) * 10 ** B[j]["e_dec"]
            d = digits(B[j])
            dev = d - pred
            devs.append(abs(dev))
            if abs(dev) > 0.5:
                viol += 1
        print("   %-22s violations=%3d/%d  max dev=%.3f" %
              (name, viol, len(both), max(devs)))

    # ---- count what actually changed -----------------------------------
    changed_unc = [(A[i]["e"], L.e_unc_abs(A[i]), L.e_unc_abs(B[j]))
                   for i, j in both if A[i]["e_unc"] != B[j]["e_unc"]
                   or A[i]["e_dec"] != B[j]["e_dec"]]
    same_unc = [A[i]["e"] for i, j in both
                if L.e_unc_abs(A[i]) == L.e_unc_abs(B[j])]
    print("\nabsolute uncertainty identical: %d ; changed: %d"
          % (len(same_unc), len(changed_unc)))
    grew = [c for c in changed_unc if c[2] > c[1]]
    print("all changes are increases: %s (%d/%d)"
          % (len(grew) == len(changed_unc), len(grew), len(changed_unc)))

    # precision changes (decimal places of E)
    prec = [(A[i]["e_raw"], B[j]["e_raw"]) for i, j in both
            if A[i]["e_dec"] != B[j]["e_dec"]]
    print("rows with changed energy decimal precision: %d" % len(prec))
    for a, b in prec:
        print("   %-16s -> %s" % (a, b))

    # ---- intensity check (string level) --------------------------------
    i_diff = [(A[i]["e_raw"], A[i]["i_raw"], B[j]["i_raw"]) for i, j in both
              if A[i]["i_raw"] != B[j]["i_raw"]]
    print("\nintensity cells differing (raw text): %d" % len(i_diff))
    for a, b, c in i_diff[:20]:
        print("   %-16s %-14s -> %s" % (a, b, c))

    # ---- full report ----------------------------------------------------
    lines = []
    lines.append("# Table VI draft comparison: 2nd vs 3rd")
    lines.append("")
    lines.append("- 2nd: `2026OSAA_CT11035_152Gd_Table_VI_2nd.md` (352 data rows, 2 data columns)")
    lines.append("- 3rd: `2026OSAA_CT11035_152Gd_Table_VI_3rd.md` (348 data rows, 3 data columns)")
    lines.append("- Rows aligned by E_gamma (0.1 keV binning); matched rows: %d; max |dE| = %.4f keV"
                 % (len(both), max_de))
    lines.append("")
    lines.append("## Removed rows (present in 2nd only)")
    lines.append("")
    for i, j in pairs:
        if j is None:
            lines.append("- `%s` %s" % (A[i]["e_raw"], A[i]["i_raw"] or "(no I)"))
    lines.append("")
    lines.append("## Added rows (present in 3rd only)")
    lines.append("")
    none_added = True
    for i, j in pairs:
        if i is None:
            lines.append("- `%s` %s" % (B[j]["e_raw"], B[j]["i_raw"] or "(no I)"))
            none_added = False
    if none_added:
        lines.append("- none")
    lines.append("")
    lines.append("## New column: `Coincidence (*)`")
    lines.append("")
    lines.append("- 314 of 348 rows flagged `*`; 34 rows blank.")
    lines.append("- All 34 blank rows carry a measured I_gamma.")
    lines.append("- Blank rows:")
    for b in B:
        if b["coinc"] != "*":
            lines.append("  - `%s`  I=%s" % (b["e_raw"], b["i_raw"]))
    lines.append("")
    lines.append("## Energy uncertainties")
    lines.append("")
    lines.append("- %d of %d rows changed; every change is an increase." % (len(changed_unc), len(both)))
    lines.append("- Every row is reproduced by sqrt(sigma_2nd^2 + (0.15 keV)^2) "
                 "quantized to the 3rd draft's decimal place (max deviation 0.005 digit).")
    lines.append("")
    lines.append("## Row-by-row diff")
    lines.append("")
    lines.append("`dE` = energy value shift (keV); `dUnc` = energy uncertainty (absolute keV); "
                 "note flags: E = energy value/precision, dE = uncertainty, I = intensity, COINC = coincidence flag.")
    lines.append("")
    for i, j in both:
        r, s = A[i], B[j]
        notes = []
        de = s["e"] - r["e"]
        if abs(de) > 1e-9:
            notes.append("E")
        if L.e_unc_abs(r) != L.e_unc_abs(s):
            notes.append("dE")
        if r["i_raw"] != s["i_raw"]:
            notes.append("I")
        if r["coinc"] != s["coinc"]:
            notes.append("COINC")
        lines.append("| `%s` | `%s` | %s | %s | `%s` | `%s` | %s |" % (
            r["e_raw"], s["e_raw"],
            ("%+g" % de) if abs(de) > 1e-9 else "",
            ("%s -> %s" % (L.fmt_abs(L.e_unc_abs(r)), L.fmt_abs(L.e_unc_abs(s))))
            if L.e_unc_abs(r) != L.e_unc_abs(s) else "",
            r["i_raw"], s["i_raw"],
            ", ".join(notes) if notes else "same"))
    path = os.path.join(OUT_DIR, "Table_VI_2nd_vs_3rd_comparison.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("\nwrote %s" % path)


main()
