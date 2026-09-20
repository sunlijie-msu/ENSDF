"""Dump exact content + trailing-space counts for the target comment regions."""
import sys

REGIONS = [(82, 104), (405, 410), (463, 480), (529, 537), (543, 548), (558, 566),
           (599, 608), (715, 723), (800, 808)]

path = sys.argv[1]
with open(path, "r", encoding="ascii") as fh:
    lines = [ln.rstrip("\r\n") for ln in fh]

for a, b in REGIONS:
    print("---- %d-%d ----" % (a, b))
    for n in range(a, b + 1):
        ln = lines[n - 1]
        body = ln.rstrip(" ")
        print("%5d len=%3d trail=%2d |%s|" % (n, len(ln), len(ln) - len(body), body))
