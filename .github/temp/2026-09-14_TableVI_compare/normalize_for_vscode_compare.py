"""Rewrite both Table VI drafts into a common, fixed-width column layout so that
VS Code's 'Compare Selected' performs a meaningful line-by-line diff.

Rows are aligned 1:1 by E_gamma; rows present in only one draft appear as
inserted/deleted lines instead of shifting every following line.
"""
import os

import compare_vi_lib as L

OUT_DIR = r"d:\X\ND\ENSDF\.github\temp\2026-09-14_TableVI_compare"


def main():
    A = [L.norm_row(x) for x in L.read_table(L.A_PATH)]
    B = [L.norm_row(x) for x in L.read_table(L.B_PATH)]

    we = max([len(r["e_raw"]) for r in A + B] + [len("E_gamma (keV)")])
    wi = max([len(r["i_raw"]) for r in A + B] + [len("I_gamma")])
    wc = 11

    def line(e, i, c):
        return "| %s | %s | %s |" % (e.ljust(we), i.ljust(wi), c.ljust(wc))

    hdr = line("E_gamma (keV)", "I_gamma", "Coincidence")
    sep = "| %s | %s | %s |" % (":" + "-" * (we - 1), ":" + "-" * (wi - 1),
                                ":" + "-" * (wc - 1))

    # map 3rd-draft row index -> 2nd-draft row index
    pairs = L.align(A, B)
    order = []
    for i, j in pairs:
        order.append((i, j))

    def build(side):
        out = ["# TABLE VI (normalized for diff) - %s draft" % side, "", hdr, sep]
        for i, j in order:
            if side == "2nd":
                if i is None:
                    out.append(line("", "", ""))
                else:
                    out.append(line(A[i]["e_raw"], A[i]["i_raw"], A[i]["coinc"]))
            else:
                if j is None:
                    out.append(line("", "", ""))
                else:
                    out.append(line(B[j]["e_raw"], B[j]["i_raw"], B[j]["coinc"]))
        return "\n".join(out) + "\n"

    for side, path in (("2nd", os.path.join(OUT_DIR, "VI_2nd_normalized.md")),
                       ("3rd", os.path.join(OUT_DIR, "VI_3rd_normalized.md"))):
        with open(path, "w", encoding="utf-8") as f:
            f.write(build(side))
        print("wrote", path)

    # sanity: identical line counts and column positions
    a = [l for l in build("2nd").splitlines() if l.startswith("|")]
    b = [l for l in build("3rd").splitlines() if l.startswith("|")]
    print("normalized lines: 2nd=%d 3rd=%d  equal_count=%s"
          % (len(a), len(b), len(a) == len(b)))
    print("identical pipe positions: %s"
          % all(x.index("|", 1) == y.index("|", 1)
                for x, y in zip(a, b)))


main()
