"""Short-line ladder: 'M20:' + 20 spaces + 'A', etc. Measures my typed run renders."""
P = r".github/temp/2026-09-17_flagsA\probeLadder2.ens"
rows = []
for run in (20, 30, 40, 50, 56):
    rows.append(f"M{run:02d}:" + " " * run + "A")
open(P, "w", encoding="utf-8", newline="").write("\r\n".join(rows) + "\r\n")
print("written", P)
for r in rows:
    print(repr(r))
