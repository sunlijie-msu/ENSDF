"""Show each error-attributed comment block with the surrounding level block."""
import re
import sys
from pathlib import Path

ENS = Path(r"D:\X\ND\ENSDF\A34\S34\new\S34_adopted.ens")
SUM = Path(r"D:\X\ND\ENSDF\.github\temp\quoted_check\fresh_summary.txt")

lines = ENS.read_text(encoding="utf-8").split("\n")

# parse summary rows
rows = []
for ln in SUM.read_text(encoding="utf-8").split("\n"):
    m = re.match(r"^\s*(\d+)\s+(\d+)\s+(\w+)\s+(.*)$", ln)
    if m and m.group(3).isupper():
        rows.append((int(m.group(2)), m.group(3), m.group(4)))

byline = {}
for line, kind, detail in rows:
    byline.setdefault(line, []).append((kind, detail))

out = []
for line_no in sorted(byline):
    i = line_no - 1
    # find block start: walk back while previous line is a continuation cL
    start = i
    while start - 1 >= 0:
        p = lines[start - 1]
        if len(p) > 8 and p[5] != " " and p[6] == "c" and p[7] == "L":
            start -= 1
        else:
            break
    # find block end: forward continuations
    end = i
    while end + 1 < len(lines):
        p = lines[end + 1]
        if len(p) > 8 and p[5] != " " and p[6] == "c" and p[7] == "L":
            end += 1
        else:
            break
    # level block context: nearest preceding L data record
    lev = None
    for k in range(start - 1, -1, -1):
        p = lines[k]
        if len(p) > 8 and p[5] == " " and p[6] == " " and p[7] in "LGX":
            lev = k
            break
    out.append("=" * 100)
    out.append(f"### ERRORS AT LINE {line_no}  ({len(byline[line_no])} findings)")
    for kind, detail in byline[line_no]:
        out.append(f"    - {kind}: {detail}")
    if lev is not None and lev < start:
        out.append(f"--- context lines {lev+1}..{start} ---")
        for k in range(lev, start):
            out.append(f"{k+1:>5}|{lines[k]}")
    out.append(f"--- comment block lines {start+1}..{end+1} ---")
    for k in range(start, end + 1):
        out.append(f"{k+1:>5}|{lines[k]}")
    # gammas belonging to this level block: after end, until next L-record
    k = end + 1
    out.append(f"--- following G-records (level {line_no}) ---")
    while k < len(lines):
        p = lines[k]
        if len(p) > 8 and p[5] == " " and p[6] == " " and p[7] in "LG":
            if p[7] == "L":
                break
            if p[7] == "G":
                out.append(f"{k+1:>5}|{p}")
        k += 1

Path(r"D:\X\ND\ENSDF\.github\temp\quoted_check\inspect2.txt").write_text(
    "\n".join(out) + "\n", encoding="utf-8")
print("blocks:", len(byline), "lines out:", len(out))
