"""Read-only: locate the five A-flagged levels in the current target and print their full blocks."""
from pathlib import Path

TARGET = Path("A34/S34/new/S34_adopted.ens")
lines = TARGET.read_text(encoding="utf-8").splitlines()

TARGETS = ["8185.46", "8656", "9479", "9868", "10170", "10803"]

for t in TARGETS:
    idx = [i for i, l in enumerate(lines) if l[6:8] == " L" and l[9:19].strip() == t]
    print(f"\n=== level {t} -> matched L lines at {[i + 1 for i in idx]} ===")
    for i in idx:
        # walk forward to the block separator ' d' (or next L)
        j = i + 1
        while j < len(lines) and not (lines[j][6:8] in (" L", " G") or lines[j].rstrip() == " 34S  d"):
            j += 1
        for k in range(i, min(j, i + 14)):
            s = lines[k]
            print(f"{k + 1:5d} len={len(s):3d} content_len={len(s.rstrip()):3d} {s.rstrip()!r}")
