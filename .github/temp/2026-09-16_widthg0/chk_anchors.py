"""Check that every planned edit anchor pair is unique in the file."""
from pathlib import Path

P = Path("A34/S34/new/S34_adopted.ens")
TXT = P.read_text(encoding="utf-8")
L = TXT.splitlines()

RECS = [1210, 1222, 1236, 1262, 1288, 1376, 1393, 1404, 1421, 1432, 1452, 1463, 1477, 1488, 1505,
        1522, 1620, 1786, 1720, 1631, 1635, 1640, 1666, 1684, 1688, 1692, 1699, 1712, 1716, 1747,
        1751, 1755, 1762, 1773, 1777, 1782, 1797, 1804, 1809]


def is_lrec(s):
    return s[7:8] == "L" and s[5:6] == " " and s[6:7] == " "


for rec in RECS:
    p = next(j for j in range(rec, 0, -1) if is_lrec(L[j - 1]))
    prev = L[rec - 2]
    rl = L[rec - 1]
    pair1 = prev + "\n" + rl
    c1 = TXT.count(pair1)
    # tail = last cL line of the level
    cls = [j for j in range(p + 1, len(L) + 1) if not is_lrec(L[j - 1]) and L[j - 1][6:8] == "cL"
           and all(not is_lrec(L[k - 1]) for k in range(p + 1, j))]
    tail = cls[-1] if cls else None
    first = None
    start = (tail or p) + 1
    for j in range(start, len(L) + 1):
        s = L[j - 1]
        if is_lrec(s):
            break
        if s[7:8] in ("G", "F", "S"):
            first = j
            break
    if tail and first:
        pair2 = L[tail - 1] + "\n" + L[first - 1]
        c2 = TXT.count(pair2)
    else:
        pair2, c2 = None, 0
    flag = "" if (c1 == 1 and (pair2 is None or c2 == 1)) else "   <<< CHECK"
    print(f"rec {rec:5d} L{p:5d} pair1={c1} pair2={c2} "
          f"tail={tail} first={first}{flag}")
    if pair2 is None:
        print(f"        (no cL/first-G: insert right after XREF line {rec-1})")
