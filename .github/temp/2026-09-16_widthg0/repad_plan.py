"""List every non-80-char line, grouped by level, with the deficit for padding repair."""
from pathlib import Path

L = Path("A34/S34/new/S34_adopted.ens").read_text(encoding="utf-8").splitlines()

print("=== all non-80 lines ===")
for i, s in enumerate(L, 1):
    if len(s) != 80:
        print(f"  {i:5d} len={len(s):3d} deficit={80-len(s)} {s.rstrip()!r}")

print("\n=== converted width-comment levels and their short lines ===")


def is_lrec(s):
    return s[7:8] == "L" and s[5:6] == " " and s[6:7] == " "


for i, s in enumerate(L, 1):
    if s[6:8] == "cL" and "|G{-" in s and "WIDTH" not in s and "T$" not in s:
        # find the level start: walk back to L record
        p = next(j for j in range(i, 0, -1) if is_lrec(L[j - 1]))
        blk = []
        for j in range(p, min(i + 3, len(L) + 1)):
            t = L[j - 1]
            if j > p and is_lrec(t):
                break
            blk.append((j, len(t), t.rstrip()))
        if any(n != 80 for _, n, _ in blk):
            print(f"--- level L{p} E={L[p-1][9:19].strip()}")
            for j, n, c in blk:
                print(f"    {j:5d} len={n:3d} deficit={80-n} {c!r}")
