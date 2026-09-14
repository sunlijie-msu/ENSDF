"""Second-stage analysis: characterize the uncertainty change pattern and the
new coincidence column of the 3rd Table VI draft."""
import math
import re

import compare_vi_lib as L  # noqa


def main():
    A = [L.norm_row(r) for r in L.read_table(L.A_PATH)]
    B = [L.norm_row(r) for r in L.read_table(L.B_PATH)]
    pairs = L.align(A, B)
    both = [(i, j) for i, j in pairs if i is not None and j is not None]

    match_hyp, miss_hyp, no_change = [], [], []
    for i, j in both:
        r, s = A[i], B[j]
        u2, u3 = L.e_unc_abs(r), L.e_unc_abs(s)
        if u2 is None or u3 is None:
            continue
        pred = math.sqrt(u2 ** 2 + 0.15 ** 2)
        # quantize prediction to the decimal place used in the 3rd draft
        q = round(pred, s["e_dec"])
        if abs(u3 - q) < 0.5 * 10 ** (-s["e_dec"]):
            match_hyp.append((r["e"], u2, u3, pred))
        elif u3 == u2:
            no_change.append((r["e"], u2, u3))
        else:
            miss_hyp.append((r["e"], u2, u3, pred))

    print("rows compared: %d" % len(both))
    print("quadrature(+0.15 keV) hypothesis matches: %d" % len(match_hyp))
    print("uncertainty unchanged: %d" % len(no_change))
    print("hypothesis fails: %d" % len(miss_hyp))
    print("\n-- hypothesis failures (E, unc_2nd, unc_3rd, predicted) --")
    for e, u2, u3, p in miss_hyp:
        print("   %9.2f  %-8s -> %-8s  pred %s" % (e, u2, u3, round(p, 4)))
    print("\n-- unchanged-uncertainty rows --")
    for e, u2, u3 in no_change:
        print("   %9.2f  %s" % (e, u2))

    print("\n-- largest relative uncertainty increases --")
    rel = sorted(((u3 / u2, e, u2, u3) for e, u2, u3, _ in match_hyp),
                 reverse=True)[:12]
    for ratio, e, u2, u3 in rel:
        print("   %9.2f  %s -> %s  (x%.2f)" % (e, u2, u3, ratio))

    print("\n-- rows WITHOUT '*' in 3rd draft (%d) --"
          % sum(1 for b in B if b["coinc"] != "*"))
    for b in B:
        if b["coinc"] != "*":
            print("   %-16s %s" % (b["e_raw"], b["i_raw"]))

    print("\n-- rows in 2nd draft dropped from 3rd --")
    for i, j in pairs:
        if j is None:
            print("   %-16s %s" % (A[i]["e_raw"], A[i]["i_raw"]))


main()
