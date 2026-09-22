"""Summarize check_quoted_values.py output into a compact per-line table."""
import re
import sys
from pathlib import Path

src = Path(sys.argv[1] if len(sys.argv) > 1 else
            r"D:\X\ND\ENSDF\.github\temp\quoted_check\fresh.txt")
raw = src.read_bytes()
if raw[:2] in (b"\xff\xfe", b"\xfe\xff"):
    txt = raw.decode("utf-16").split("\n")
else:
    txt = raw.decode("utf-8", errors="replace").split("\n")

ANSI = re.compile(r"\x1b\[[0-9;]*m")
txt = [ANSI.sub("", ln) for ln in txt]

rows = []
i = 0
while i < len(txt):
    m = re.match(r"^\s*#(\d+)\s+\[(\w+)\]\s+line (\d+)", txt[i])
    if m:
        num, kind, line = int(m.group(1)), m.group(2), int(m.group(3))
        body = txt[i + 1].strip() if i + 1 < len(txt) else ""
        ctx = txt[i + 2].strip() if i + 2 < len(txt) else ""
        rows.append((num, kind, line, body, ctx))
        i += 3
    else:
        i += 1

kinds = {}
for r in rows:
    kinds[r[1]] = kinds.get(r[1], 0) + 1
out = []
out.append(f"total coded errors: {len(rows)}")
for k, v in sorted(kinds.items(), key=lambda x: -x[1]):
    out.append(f"  {k:<28} {v}")

out.append("")
out.append(f"{'#':>4} {'line':>5} {'kind':<26} detail")
for num, kind, line, body, ctx in rows:
    out.append(f"{num:>4} {line:>5} {kind:<26} {body} || {ctx}")
out.append("")
lines = sorted({r[2] for r in rows})
out.append(f"distinct comment lines: {len(lines)}")
out.append(str(lines))

Path(src.parent / "fresh_summary.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
print(f"wrote summary: {len(rows)} errors on {len(lines)} lines")
