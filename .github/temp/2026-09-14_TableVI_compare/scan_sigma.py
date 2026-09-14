"""Determine the additive systematic that maps 2nd-draft energy uncertainties
onto 3rd-draft ones, and inspect the worst-fit rows."""
import math

import compare_vi_lib as L


def main():
    A = [L.norm_row(x) for x in L.read_table(L.A_PATH)]
    B = [L.norm_row(x) for x in L.read_table(L.B_PATH)]
    pairs = L.align(A, B)
    both = [(i, j) for i, j in pairs if i is not None and j is not None]

    print("-- scan additive systematic s in sqrt(u^2 + s^2) --")
    for k in range(20, 41):
        s = k / 200.0  # 0.100 .. 0.200 step 0.005
        viol, devs = 0, []
        for i, j in both:
            u2 = L.e_unc_abs(A[i])
            pred = math.sqrt(u2 ** 2 + s ** 2) * 10 ** B[j]["e_dec"]
            devs.append(abs(int(B[j]["e_unc"]) - pred))
            if abs(int(B[j]["e_unc"]) - pred) > 0.5:
                viol += 1
        print("   s=%.3f keV  violations=%3d  max dev=%.3f" % (s, viol, max(devs)))

    print("\n-- rows with max deviation under s=0.15 --")
    rows = []
    for i, j in both:
        u2 = L.e_unc_abs(A[i])
        pred = math.sqrt(u2 ** 2 + 0.15 ** 2) * 10 ** B[j]["e_dec"]
        rows.append((abs(int(B[j]["e_unc"]) - pred), A[i]["e_raw"], B[j]["e_raw"],
                     u2, L.e_unc_abs(B[j]), pred))
    rows.sort(reverse=True)
    for d, ea, eb, u2, u3, pred in rows[:8]:
        print("   dev=%.3f  %-16s->%-16s  %.4f -> %.4f (pred %.4f)"
              % (d, ea, eb, u2, u3, pred))

    print("\n-- energy-value rounding: rows whose value changed only by rounding --")
    for i, j in both:
        if abs(B[j]["e"] - A[i]["e"]) > 1e-9:
            print("   %-16s -> %-16s  d=%+.4f  dec %d->%d"
                  % (A[i]["e_raw"], B[j]["e_raw"],
                     B[j]["e"] - A[i]["e"], A[i]["e_dec"], B[j]["e_dec"]))


main()
