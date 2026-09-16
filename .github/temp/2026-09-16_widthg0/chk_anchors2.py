"""Verify deletion and insertion anchors (with extended context where needed)."""
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
    prev, rl = L[rec - 2], L[rec - 1]
    c_short = TXT.count(prev + "\n" + rl)
    c_long = TXT.count(L[rec - 3] + "\n" + prev + "\n" + rl)
    cls = []
    for j in range(p + 1, len(L) + 1):
        if is_lrec(L[j - 1]):
            break
        if L[j - 1][6:8] == "cL":
            cls.append(j)
    tail = cls[-1] if cls else None
    if tail:
        nxt = L[tail]  # line after the tail comment
        c_ins = TXT.count(L[tail - 1] + "\n" + nxt)
        nxtinfo = f"next({tail+1})={nxt.rstrip()[:32]!r}"
    else:
        c_ins, nxtinfo = 0, "no cL comments"
    print(f"rec {rec:5d} L{p:5d} del_short={c_short} del_long={c_long} tail={tail} ins_pair={c_ins} {nxtinfo}")
