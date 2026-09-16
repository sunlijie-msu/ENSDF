"""Read-only verification of the WIDTHG0 conversion."""
from pathlib import Path

TARGET = Path("A34/S34/new/S34_adopted.ens")
lines = TARGET.read_text(encoding="utf-8").splitlines()

W0 = "WIDTHG0"
G0 = "|G{-|g0}"

print("=== remaining WIDTHG0 records ===")
for i, s in enumerate(lines, 1):
    if W0 in s:
        print(f"{i:5d} len={len(s):3d} clen={len(s.rstrip()):3d} {s.rstrip()!r}")
print(f"count WIDTHG0 = {sum(W0 in s for s in lines)}")
print(f"count WIDTH     = {sum('WIDTH' in s for s in lines)}")
print(f"count G-g0      = {sum(G0 in s for s in lines)}")

print("\n=== comment lines containing G-g0 (expect 80) ===")
for i, s in enumerate(lines, 1):
    if G0 in s:
        print(f"{i:5d} len={len(s):3d} clen={len(s.rstrip()):3d} pad={len(s) - len(s.rstrip()):3d} {s.rstrip()!r}")

print("\n=== levels: T/DT must be blank (cols 40-55) ===")
for lev in ("7781.22", "8385.41", "8506.77", "9640", "9707", "9868", "10170", "10790", "10803"):
    for i, s in enumerate(lines, 1):
        if s[8:9] == "L" and s[9:19].strip() == lev:
            print(f"{i:5d} {s[9:19]!r:12s} T={s[39:49]!r:12s} DT={s[49:55]!r} len={len(s)}")

print("\n=== blocks 7781.22 / 8385.41 / 8506.77 ===")
for tag, start, stop in (("7781.22", 688, 700), ("8385.41", 804, 816), ("8506.77", 832, 844)):
    print(f"--- {tag} (lines {start}-{stop}) ---")
    for n in range(start, stop + 1):
        s = lines[n - 1]
        flag = "" if len(s) == 80 else "  <<< NOT 80"
        print(f"{n:5d} len={len(s):3d} {s.rstrip()!r}{flag}")
