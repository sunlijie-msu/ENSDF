"""Read-only full verification after the WIDTHG0 conversion."""
from pathlib import Path

TARGET = Path("A34/S34/new/S34_adopted.ens")
lines = TARGET.read_text(encoding="utf-8").splitlines()
text = "\n".join(lines)

W0 = "WIDTHG0"
G0 = "|G{-|g0}"

print("=== remaining WIDTHG0 records (expect only 11024.95) ===")
for i, s in enumerate(lines, 1):
    if W0 in s:
        print(f"{i:5d} len={len(s):3d} {s.rstrip()!r}")

print("\n=== comment lines containing |G{-|g0} ===")
for i, s in enumerate(lines, 1):
    if G0 in s:
        flag = "" if len(s) == 80 else "  <<< NOT 80"
        print(f"{i:5d} len={len(s):3d} pad={len(s) - len(s.rstrip()):3d} {s.rstrip()!r}{flag}")

print("\n=== levels T/DT col 40-55 (must be blank for all) ===")
for lev in ("7781.22", "8185.46", "8385.41", "8506.77", "9640", "9707", "9868", "10170", "10790", "10803", "11024.95"):
    for i, s in enumerate(lines, 1):
        if s[7:8] == "L" and s[9:19].strip() == lev:
            print(f"{i:5d} {lev:10s} T={s[39:49]!r:12s} DT={s[49:55]!r} len={len(s)}")

print("\n=== non-80-char lines ===")
for i, s in enumerate(lines, 1):
    if len(s) != 80:
        print(f"{i:5d} len={len(s):3d} {s.rstrip()!r}")

print("\n=== G records missing padding (len<80 starting at col 8 'G') ===")
for i, s in enumerate(lines, 1):
    if s[7:8] == "G" and len(s) < 80:
        print(f"{i:5d} len={len(s):3d} {s.rstrip()!r}")

print(f"\ntotal lines = {len(lines)}")
print(f"WIDTH* records = {sum('WIDTH' in s for s in lines)}")
print(f"WIDTHG=3 EV present = {'yes' if 'WIDTHG=3 EV' in text else 'NO'}")
