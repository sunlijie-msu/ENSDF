"""Read-only: locate remaining WIDTHG0 records and dump their blocks with exact pads."""
from pathlib import Path

TARGET = Path("A34/S34/new/S34_adopted.ens")
lines = TARGET.read_text(encoding="utf-8").splitlines()

targets = [i for i, s in enumerate(lines, 1) if "WIDTHG0" in s]
print("WIDTHG0 lines:", targets)

for t in targets:
    print(f"\n--- WIDTHG0 at line {t} ---")
    # walk back to the nearest L record
    start = t
    while start > 1 and lines[start - 1][7:8] != "L":
        start -= 1
    for n in range(start, min(t + 12, len(lines) + 1)):
        s = lines[n - 1]
        print(f"{n:5d} len={len(s):3d} clen={len(s.rstrip()):3d} pad={len(s) - len(s.rstrip()):3d} {s.rstrip()!r}")

print("\n--- lines needing repadding ---")
for n in (839, 1058):
    s = lines[n - 1]
    print(f"{n:5d} len={len(s):3d} clen={len(s.rstrip()):3d} {s.rstrip()!r}")

print("\n--- T/DT of every converted level (cols 40-55) ---")
for lev in ("7781.22", "8185.46", "8385.41", "8506.77", "9640", "9707", "9868", "10170", "10790", "10803"):
    for i, s in enumerate(lines, 1):
        if s[7:8] == "L" and s[9:19].strip() == lev:
            print(f"{i:5d} {lev:10s} T={s[39:49]!r:12s} DT={s[49:55]!r} len={len(s)}")
