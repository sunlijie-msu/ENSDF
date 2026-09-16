"""Progress check: remaining WIDTH records, width comments, non-80-char lines."""
from pathlib import Path

L = Path("A34/S34/new/S34_adopted.ens").read_text(encoding="utf-8").splitlines()

print("remaining 2 L WIDTH data records:")
for i, s in enumerate(L, 1):
    if s[7:8] == "L" and s[5:6] == "2" and "WIDTH" in s:
        print(f"  {i:5d} len={len(s)} {s.rstrip()!r}")

print("\n|G comments:")
for i, s in enumerate(L, 1):
    if s[6:8] == "cL" and "|G" in s:
        pad = len(s) - len(s.rstrip())
        flag = "" if len(s) == 80 else "  <<< NOT 80"
        print(f"  {i:5d} pad={pad:3d} {s.rstrip()!r}{flag}")

print("\nnon-80 lines:")
for i, s in enumerate(L, 1):
    if len(s) != 80:
        print(f"  {i:5d} len={len(s):3d} {s.rstrip()[:60]!r}")
print("total lines:", len(L))
