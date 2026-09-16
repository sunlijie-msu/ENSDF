"""Read-only: block dumps for the 11 WIDTHG0 levels + provenance search in individual datasets."""
import glob
import re
from pathlib import Path

ADOPTED = Path("A34/S34/new/S34_adopted.ens")
lines = ADOPTED.read_text(encoding="utf-8").splitlines()

def is_level_start(s):
    return len(s) > 19 and s[5] == " " and s[6] == " " and s[7] == "L"

targets = [691, 762, 808, 837, 1017, 1028, 1051, 1123, 1290, 1310, 1357]
for t in targets:
    i = t - 1
    j = i + 1
    while j < len(lines) and not is_level_start(lines[j]) and lines[j].rstrip() != " 34S  d":
        j += 1
    print(f"\n=== block for L line {t} ===")
    for k in range(i, min(j, len(lines))):
        s = lines[k]
        print(f"{k + 1:5d} {s.rstrip()!r}")

print("\n=== provenance search: WIDTHG0 / 1.7 eV in individual datasets ===")
for f in sorted(glob.glob("A34/S34/new/*.ens")):
    if "adopted" in Path(f).name:
        continue
    for i, s in enumerate(Path(f).read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        if "WIDTHG0" in s or re.search(r"1\.7\s*EV\b", s):
            print(f"{Path(f).name}:{i}: {s.rstrip()!r}")
