"""Read-only forensic dump: current state around level 8185.46 and integrity checks."""
from pathlib import Path

TARGET = Path("A34/S34/new/S34_adopted.ens")
lines = TARGET.read_text(encoding="utf-8").splitlines()

print("--- window 760..782 (spaces as '.') ---")
for k in range(759, 782):
    if k - 1 >= len(lines):
        break
    s = lines[k]
    print(f"{k + 1:5d} len={len(s):3d} clen={len(s.rstrip()):3d} {s.replace(' ', '.')}")

print("\n--- record-type census in window 760..782 ---")
for k in range(759, 782):
    if k - 1 >= len(lines):
        break
    s = lines[k]
    col6, col8 = (s[5] if len(s) > 5 else "?"), (s[7] if len(s) > 7 else "?")
    print(f"{k + 1:5d} col6={col6!r} col8={col8!r}")

print("\n--- search for G 8184.70 records anywhere ---")
for i, s in enumerate(lines, 1):
    if "8184.70" in s:
        print(f"{i:5d} len={len(s):3d} {s.replace(' ', '.')}")

print("\n--- non-80-length lines in whole file (top 20) ---")
bad = [(i, len(s)) for i, s in enumerate(lines, 1) if len(s) != 80]
print(f"count={len(bad)}")
for i, n in bad[:20]:
    print(f"{i:5d} len={n:3d} {lines[i - 1].replace(' ', '.')}")
