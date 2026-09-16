"""Read-only: chunked exact dump for the user's new M$ comment line and current J$ line."""
from pathlib import Path

TARGET = Path("A34/S34/new/S34_adopted.ens")
lines = TARGET.read_text(encoding="utf-8").splitlines()

WANT = [767, 771]
DOT = "\u00b7"

for n in WANT:
    s = lines[n - 1]
    content = s.rstrip()
    pad = len(s) - len(content)
    print(f"\nline {n}: content_len={len(content)} pad={pad}")
    for i in range(0, len(content), 10):
        chunk = content[i:i + 10].replace(" ", DOT)
        print(f"    C{i // 10 + 1:02d}={chunk}")
