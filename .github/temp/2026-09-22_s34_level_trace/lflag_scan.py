import sys, collections
sys.path.insert(0, r".github\temp\2026-09-22_s34_level_trace")
from trace_all import ADOPTED, parse_adopted, parse_xref
L = open(ADOPTED, encoding="utf-8", errors="replace").read().split("\n")
ad = parse_adopted(ADOPTED)
flags = collections.Counter()
rows = []
for a in ad:
    l = L[a["lineno"]-1]
    f = l[76] if len(l) > 76 else " "
    ms = l[77:79]
    q = l[79] if len(l) > 79 else " "
    flags[f] += 1
    if f != " ":
        rows.append((a["lineno"], a["E_str"], a["DE_str"], a["nG"], f, ms, q, a["xref"]))
print("col-77 letter tally over 368 L records:", dict(flags))
print()
print("L records carrying a col-77 letter:", len(rows))
for r in rows:
    print("  line %4d E=%-10s DE=%-3s nG=%d flag=%s MS=%r Q=%r xref=%s" %
          (r[0], r[1], r[2] or "-", r[3], r[4], r[5], r[6], r[7]))
