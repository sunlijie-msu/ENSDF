"""Read-only: exact current text of the five A-flagged L records."""
from pathlib import Path

TARGET = Path("A34/S34/new/S34_adopted.ens")
lines = TARGET.read_text(encoding="utf-8").splitlines()

WANT = ["8185.46", "8656", "9479", "9868", "10170"]

for t in WANT:
    hits = [i for i, l in enumerate(lines)
            if len(l) > 19 and l[5] == " " and l[6] == " " and l[7] == "L" and l[9:19].strip() == t]
    for i in hits:
        s = lines[i]
        print(f"line {i + 1}: len={len(s)} J=[{s[22:39]}] T=[{s[39:49]}] DT=[{s[49:55]}] flag77=[{s[76:77]}]")
        print(f"    content = {s.rstrip()!r}")
        print(f"    pad = {len(s) - len(s.rstrip())}")
