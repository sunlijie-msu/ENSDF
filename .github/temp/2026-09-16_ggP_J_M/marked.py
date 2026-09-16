"""Read-only: dump exact text with spaces shown as '.' for lines needed by the edits."""
from pathlib import Path

TARGET = Path("A34/S34/new/S34_adopted.ens")
lines = TARGET.read_text(encoding="utf-8").splitlines()

WANT = [767, 771, 873, 874, 875, 991, 992, 993, 994,
        1054, 1055, 1056, 1057, 1122, 1123, 1124]

for n in WANT:
    s = lines[n - 1]
    marked = s.replace(" ", ".")
    print(f"{n:5d} len={len(s):3d} clen={len(s.rstrip()):3d}")
    print(f"      {marked}")
