"""Count rows where the producer's direct rounding differs from the ENSDF
successive 4-up uncertainty rounding, for the sigma_3rd = sqrt(sigma_2nd^2+0.15^2)
transformation."""
import math

import compare_vi_lib as L

A = [L.norm_row(x) for x in L.read_table(L.A_PATH)]
B = [L.norm_row(x) for x in L.read_table(L.B_PATH)]
both = [(i, j) for i, j in L.align(A, B) if i is not None and j is not None]

hot = []
for i, j in both:
    u2 = L.e_unc_abs(A[i])
    pred = math.sqrt(u2 ** 2 + 0.15 ** 2) * 10 ** B[j]["e_dec"]
    dev = int(B[j]["e_unc"]) - pred
    if abs(dev) > 0.4:
        hot.append((A[i]["e_raw"], B[j]["e_raw"], u2, L.e_unc_abs(B[j]), pred, dev))
print("rows where |reported - predicted| > 0.4 digit: %d / %d" % (len(hot), len(both)))
seen = set()
for ea, eb, u2, u3, pred, dev in hot:
    key = (round(u2, 4), round(u3, 4), round(pred, 2))
    seen.add(key)
    print("   %-14s -> %-14s  %s -> %s  (pred %.4f, dev %+.3f)" % (ea, eb, u2, u3, pred, dev))
print("distinct (sigma_2nd, sigma_3rd, predicted) patterns: %d" % len(seen))
