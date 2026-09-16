"""Read-only: print full blocks for the five A-flagged levels in the current target (fixed col indices)."""
from pathlib import Path

TARGET = Path("A34/S34/new/S34_adopted.ens")
lines = TARGET.read_text(encoding="utf-8").splitlines()

TARGETS = ["8185.46", "8656", "9479", "9868", "10170", "10803"]

def is_level_start(s):
    # col 6 (index 5) blank, col 8 (index 7) == 'L' -> new level record
    return len(s) > 7 and s[5] == " " and s[7] == "L"

for t in TARGETS:
    idx = [i for i, l in enumerate(lines) if is_level_start(l) and l[9:19].strip() == t]
    print(f"\n=== level {t} -> L line(s) {[i + 1 for i in idx]} ===")
    for i in idx:
        j = i + 1
        while j < len(lines) and not is_level_start(lines[j]) and lines[j].rstrip() != " 34S  d":
            j += 1
        for k in range(i, min(j, len(lines))):
            s = lines[k]
            print(f"{k + 1:5d} len={len(s):3d} clen={len(s.rstrip()):3d} {s.rstrip()!r}")
