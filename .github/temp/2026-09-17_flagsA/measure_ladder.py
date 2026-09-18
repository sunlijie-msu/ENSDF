"""Measure rendered run lengths from the ladder: @ index - 4 = rendered run."""
P = r".github/temp/2026-09-17_flagsA\probeLadder2.ens"
rows = open(P, encoding="utf-8", newline="").read().replace("\r\n", "\n").split("\n")
labels = [20, 30, 40, 50, 56]
for ln, lab in zip(rows, labels):
    at = ln.index("@")
    print(f"M{lab:02d}: rendered run after prefix = {at - 4}  (intended {lab - 2 if lab in (20, 30, 40, 50) else 54})  line={ln!r}")
