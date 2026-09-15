"""Markdown render sanity for the multiplet report: every row of a table must carry
the same number of unescaped pipes, and the evidence table must have 10 columns."""
import io
import re
import sys

MD = sys.argv[1] if len(sys.argv) > 1 else \
    r"D:\X\ND\ENSDF\XUNDL\2026OSAA_CT11035_152Gd_Multiplet_Gammas.md"
NCOL = 10
NROW = 53
L = [l.rstrip("\r\n") for l in io.open(MD, encoding="utf-8")]
pipes = lambda line: len(re.findall(r"(?<!\\)\|", line))

bad, i = [], 0
while i < len(L):
    if L[i].startswith("|"):
        start, block = i + 1, []
        while i < len(L) and L[i].startswith("|"):
            block.append(L[i])
            i += 1
        counts = sorted({pipes(l) for l in block})
        if len(counts) != 1:
            bad.append((start, len(block), counts))
    else:
        i += 1

hdr = [i for i, l in enumerate(L) if l.startswith("| case |")]
assert len(hdr) == 1, hdr
ev = [c.strip() for c in L[hdr[0]].strip("|").split("|")]
assert len(ev) == NCOL, (len(ev), ev)
rows, j = 0, hdr[0] + 2
while j < len(L) and L[j].startswith("|"):
    c = [x.strip() for x in L[j].strip("|").split("|")]
    assert len(c) == NCOL, (j + 1, c)
    assert c[0].split("<br>")[0] in ("A", "B", "C", "D") and \
        all(x in ("A", "B", "C", "D") for x in c[0].split("<br>")), (j + 1, c[0])
    assert all(x in ("yes", "no") for x in c[-1].split("<br>")), (j + 1, c[-1])
    rows += 1
    j += 1
assert rows == NROW, rows
print("inconsistent tables:", bad)
print("evidence table columns:", len(ev), "rows:", rows)
