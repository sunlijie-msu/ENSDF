"""Scan all cL T$ comment lines and classify by parent L-record T/DT field state."""
from pathlib import Path

TARGET = Path("A34/S34/new/S34_adopted.ens")
lines = TARGET.read_text(encoding="utf-8").splitlines()

# index L records
lrecs = [(i, s) for i, s in enumerate(lines, 1) if s[7:8] == "L" and "XREF" not in s[7:20]]

for i, s in enumerate(lines, 1):
    if " cL T$" in s or " cL T(" in s or s[7:10] == "cL " and "$" in s[10:16] and "T" == s[10:11]:
        # find nearest preceding L record
        parent = None
        for j, ls in reversed(lrecs):
            if j < i:
                parent = (j, ls)
                break
        pj, ps = parent
        print(f"T$-line {i:5d} len={len(s):3d} {s.rstrip()!r}")
        print(f"   parent L {pj}: T={ps[39:49]!r} DT={ps[49:55]!r}  E={ps[9:19].strip()} J={ps[22:39].strip()!r}")
        print(f"   next line {i+1}: {lines[i][:60]!r}")
