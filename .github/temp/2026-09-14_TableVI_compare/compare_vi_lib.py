"""Column-aware comparison of two markdown tables with different column counts.

Parses pipe tables, aligns rows by gamma energy (tolerant of differing
decimal precision between drafts), and reports field-level changes.
"""
import re

A_PATH = r"d:\X\ND\ENSDF\XUNDL\2026OSAA_CT11035_152Gd_Table_VI_2nd.md"
B_PATH = r"d:\X\ND\ENSDF\XUNDL\2026OSAA_CT11035_152Gd_Table_VI_3rd.md"

NUM_UNC = re.compile(r"^(-?[0-9]*\.?[0-9]+)\s*\(\s*(\d+)\s*\)$")
NUM = re.compile(r"^-?[0-9]*\.?[0-9]+$")


def parse_val(text):
    text = text.strip()
    if not text:
        return None, None
    m = NUM_UNC.match(text)
    if m:
        return m.group(1), m.group(2)
    if NUM.match(text):
        return text, None
    return text, None


def decimals(s):
    return len(s.split(".")[1]) if "." in s else 0


def read_table(path):
    rows = []
    for ln in open(path, encoding="utf-8"):
        line = ln.rstrip("\n")
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if all(set(c) <= set(":- ") for c in cells):
            continue
        if cells[0].lower().startswith(("e_gamma", "e\\_gamma", "$e_\\gamma$")):
            continue
        rows.append(cells)
    return rows


def norm_row(cells):
    e_val, e_unc = parse_val(cells[0])
    i_val, i_unc = (None, None)
    if len(cells) > 1:
        i_val, i_unc = parse_val(cells[1])
    return {
        "e_raw": cells[0].strip(),
        "e": float(e_val) if e_val and NUM.match(e_val) else None,
        "e_val": e_val,
        "e_dec": decimals(e_val) if e_val and NUM.match(e_val) else 0,
        "e_unc": e_unc,
        "i_raw": cells[1].strip() if len(cells) > 1 else "",
        "i_val": i_val,
        "i_raw_unc": i_unc,
        "coinc": cells[2] if len(cells) > 2 else "",
    }


def e_unc_abs(r):
    if r["e_unc"] is None:
        return None
    return int(r["e_unc"]) * 10 ** (-r["e_dec"])


def key(e):
    return round(e, 1)


def align(a, b):
    pairs = []
    i = j = 0
    while i < len(a) and j < len(b):
        ka, kb = key(a[i]["e"]), key(b[j]["e"])
        if ka == kb:
            pairs.append((i, j))
            i += 1
            j += 1
            continue
        if ka < kb:
            found = next((jj for jj in range(j, min(j + 3, len(b)))
                          if key(b[jj]["e"]) == ka), None)
            if found is not None:
                for jx in range(j, found):
                    pairs.append((None, jx))
                pairs.append((i, found))
                i += 1
                j = found + 1
            else:
                pairs.append((i, None))
                i += 1
        else:
            found = next((ii for ii in range(i, min(i + 3, len(a)))
                          if key(a[ii]["e"]) == kb), None)
            if found is not None:
                for ix in range(i, found):
                    pairs.append((ix, None))
                pairs.append((found, j))
                j += 1
                i = found + 1
            else:
                pairs.append((None, j))
                j += 1
    while i < len(a):
        pairs.append((i, None))
        i += 1
    while j < len(b):
        pairs.append((None, j))
        j += 1
    return pairs


def fmt_abs(unc):
    if unc is None:
        return ""
    s = ("%.6f" % unc).rstrip("0")
    return s.rstrip(".")


def main():
    A = [norm_row(r) for r in read_table(A_PATH)]
    B = [norm_row(r) for r in read_table(B_PATH)]
    print("rows: 2nd=%d  3rd=%d" % (len(A), len(B)))
    bad = [r["e_raw"] for r in A + B if r["e"] is None]
    if bad:
        print("UNPARSED:", bad)
    for name, T in (("2nd", A), ("3rd", B)):
        ks = [key(r["e"]) for r in T if r["e"] is not None]
        dup = sorted({k for k in ks if ks.count(k) > 1})
        if dup:
            print("WARN duplicate keys in %s: %s" % (name, dup))

    pairs = align(A, B)
    only_a = [i for i, j in pairs if j is None]
    only_b = [j for i, j in pairs if i is None]
    both = [(i, j) for i, j in pairs if i is not None and j is not None]

    lines = ["| E(2nd) | E(3rd) | dE | dUnc | I(2nd) | I(3rd) | note |",
             "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |"]
    n_ok = 0
    counts = {"E": 0, "dE": 0, "I": 0, "COINC": 0}
    unc_rows = []
    coinc_rows = []
    for i, j in both:
        r, s = A[i], B[j]
        notes = []
        de = s["e"] - r["e"]
        if abs(de) > 1e-9:
            notes.append("E")
            counts["E"] += 1
        if (r["e_unc"] or "") != (s["e_unc"] or ""):
            notes.append("dE")
            counts["dE"] += 1
            unc_rows.append((r["e"], e_unc_abs(r), e_unc_abs(s)))
        if r["i_val"] != s["i_val"] or r["i_raw_unc"] != s["i_raw_unc"]:
            notes.append("I")
            counts["I"] += 1
        if r["coinc"] != s["coinc"]:
            notes.append("COINC")
            counts["COINC"] += 1
            coinc_rows.append((r["e"], r["coinc"], s["coinc"]))
        if not notes:
            n_ok += 1
        lines.append("| %s | %s | %s | %s | %s | %s | %s |" % (
            r["e_raw"], s["e_raw"],
            ("%+g" % de) if abs(de) > 1e-9 else "",
            ("%s -> %s" % (fmt_abs(e_unc_abs(r)), fmt_abs(e_unc_abs(s))))
            if r["e_unc"] != s["e_unc"] else "",
            r["i_raw"], s["i_raw"], ", ".join(notes) if notes else "same"))

    print("matched=%d same=%d  dE=%d dEunc=%d dI=%d dCoinc=%d only2nd=%d only3rd=%d"
          % (len(both), n_ok, counts["E"], counts["dE"], counts["I"],
             counts["COINC"], len(only_a), len(only_b)))

    print("\n--- only in 2nd ---")
    for i in only_a:
        print("   ", A[i]["e_raw"], "|", A[i]["i_raw"], "|", A[i]["coinc"])
    print("--- only in 3rd ---")
    for j in only_b:
        print("   ", B[j]["e_raw"], "|", B[j]["i_raw"], "|", B[j]["coinc"])

    print("\n--- energy-value changes ---")
    for i, j in both:
        if abs(B[j]["e"] - A[i]["e"]) > 1e-9:
            print("    %.4f -> %.4f  (%s -> %s)" % (
                A[i]["e"], B[j]["e"], A[i]["e_raw"], B[j]["e_raw"]))

    print("\n--- coincidence-flag changes ---")
    for e, r, s in coinc_rows:
        print("    %.2f : '%s' -> '%s'" % (e, r, s))

    print("\n--- energy-uncertainty changes ---")
    if unc_rows:
        ratios = [s / r for _, r, s in unc_rows if r]
        print("    n=%d ratio min/max %.3f/%.3f" % (len(unc_rows), min(ratios), max(ratios)))
        for e, r, s in unc_rows[:20]:
            print("    %.2f : %s -> %s" % (e, fmt_abs(r), fmt_abs(s)))

    print("\n--- coincidence stats (3rd file) ---")
    for v in ("", "*"):
        sel = [r for r in B if r["coinc"] == v]
        withI = [r for r in sel if r["i_val"]]
        print("    coinc='%s': n=%d with_I=%d" % (v, len(sel), len(withI)))

    out = r"d:\X\ND\ENSDF\.github\temp\2026-09-14_TableVI_compare\full_row_diff.md"
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("\nwrote", out)


