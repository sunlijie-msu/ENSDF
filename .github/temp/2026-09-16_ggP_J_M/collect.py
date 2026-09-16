"""Read-only: exact padded text + uniqueness for all lines affected by the g_gP J/M update."""
from pathlib import Path

TARGET = Path("A34/S34/new/S34_adopted.ens")
lines = TARGET.read_text(encoding="utf-8").splitlines()

L_EDIT = [763, 866, 985, 1047, 1118]          # J field (1) -> 1+
G_EDIT = [768, 873, 991, 1054, 1122]          # M field blank -> M1
CONTEXT = [769, 770, 771, 874, 987, 988, 989, 992, 993, 1055, 1056, 1123]

print("=== lines to edit ===")
for n in L_EDIT + G_EDIT:
    s = lines[n - 1]
    print(f"{n:5d} len={len(s):3d} content_len={len(s.rstrip()):3d} pad={len(s) - len(s.rstrip()):3d}")
    print(f"      {s!r}")

print("=== context lines (anchors) ===")
for n in CONTEXT:
    s = lines[n - 1]
    txt = s.rstrip()
    occurrences = sum(1 for x in lines if x.rstrip() == txt)
    print(f"{n:5d} len={len(s):3d} pad={len(s) - len(txt):3d} identical_lines={occurrences}")
    print(f"      {s!r}")

print("=== proposed new lines (content) ===")
new_j = {763: " 34S   L 8185.46   12 1+               0.78 EV   20",
         866: " 34S   L 8656      5  1+               0.41 EV   19",
         985: " 34S   L 9479      4  1+               1.1 EV    3",
         1047: " 34S   L 9868      5  1+               0.60 EV   12",
         1118: " 34S   L 10170     5  1+               1.06 EV   20"}
for n, c in new_j.items():
    print(f"L {n:5d} Jfield=[{c[22:39]}] len={len(c)}")

new_m = {768: " 34S   G 8184.70   24 100",
         873: " 34S   G 8656      7",
         991: " 34S   G 9477      4",
         1054: " 34S   G 9858      7",
         1122: " 34S   G 10168     5"}
for n, c in new_m.items():
    full = c + " " * (33 - 1 - len(c)) + "M1"
    print(f"G {n:5d} Mfield=[{full[32:41]}] content_len={len(full)} pad_needed={80 - len(full)}")

j_cmt = " 34S  cL J$from {+34}S(|g,|g'),(pol |g,|g')."
m_cmt = " 34S  cG M$from {+34}S(|g,|g'),(pol |g,|g')."
print(f"J comment len={len(j_cmt)} pad_needed={80 - len(j_cmt)}")
print(f"M comment len={len(m_cmt)} pad_needed={80 - len(m_cmt)}")
