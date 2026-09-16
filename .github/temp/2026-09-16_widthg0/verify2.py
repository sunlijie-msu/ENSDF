"""Verify T$ comment removal and current block states."""
from pathlib import Path

L = Path("A34/S34/new/S34_adopted.ens").read_text(encoding="utf-8").splitlines()

T = "cL T$from {+34}S(|g,|g"
print("count T$from-{+34}S comments =", sum(1 for s in L if T in s))
for i, s in enumerate(L, 1):
    if T in s:
        print("   remaining:", i, len(s), repr(s.rstrip()))

print("\n--- 806-814 ---")
for n in range(806, 815):
    s = L[n - 1]
    print(n, len(s), repr(s.rstrip()[:68]))

print("\n--- 1286-1296 ---")
for n in range(1286, 1297):
    s = L[n - 1]
    print(n, len(s), len(s.rstrip()), repr(s.rstrip()[:68]))

print("\n--- non-80 lines ---")
for i, s in enumerate(L, 1):
    if len(s) != 80:
        print(i, len(s), repr(s.rstrip()[:56]))
print("total lines", len(L))
