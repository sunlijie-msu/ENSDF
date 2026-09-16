"""Read-only: print current blocks for the five A-flagged levels (correct level-start test)."""
from pathlib import Path

TARGET = Path("A34/S34/new/S34_adopted.ens")
lines = TARGET.read_text(encoding="utf-8").splitlines()

TARGETS = ["8185.46", "8656", "9479", "9868", "10170", "10803"]

def is_level_start(s):
    # plain level record: col6 blank (idx5), col7 blank (idx6), col8 'L' (idx7)
    return len(s) > 7 and s[5] == " " and s[6] == " " and s[7] == "L"

def is_sep(s):
    return s.rstrip() == " 34S  d"

print("--- raw window 760..776 ---")
for k in range(759, 776):
    s = lines[k]
    print(f"{k + 1:5d} len={len(s):3d} {s.rstrip()!r}")

for t in TARGETS:
    idx = [i for i, l in enumerate(lines) if is_level_start(l) and l[9:19].strip() == t]
    print(f"\n=== level {t} -> L line(s) {[i + 1 for i in idx]} ===")
    for i in idx:
        j = i + 1
        while j < len(lines) and not is_level_start(lines[j]) and not is_sep(lines[j]):
            j += 1
        for k in range(i, min(j + 1, len(lines))):
            s = lines[k]
            print(f"{k + 1:5d} len={len(s):3d} clen={len(s.rstrip()):3d} {s.rstrip()!r}")
