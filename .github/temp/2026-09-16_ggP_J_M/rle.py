"""Read-only: run-length-exact decomposition of lines needed for anchors."""
import re
from pathlib import Path

TARGET = Path("A34/S34/new/S34_adopted.ens")
lines = TARGET.read_text(encoding="utf-8").splitlines()

WANT = [874, 875, 992, 993, 994, 1055, 1056, 1057, 1123, 1124]

for n in WANT:
    s = lines[n - 1]
    content = s.rstrip()
    print(f"\nline {n}: total_len={len(s)} content_len={len(content)} pad={len(s) - len(content)}")
    toks = re.findall(r"\S+|\s+", content)
    for t in toks:
        if t.strip():
            print(f"    text {t!r}")
        else:
            print(f"    SPACE x{len(t)}")
    print(f"    PAD_SPACE x{len(s) - len(content)}")
