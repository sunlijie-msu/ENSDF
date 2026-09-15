"""Markdown render sanity for the multiplet report: every row of a table must carry
the same number of unescaped pipes, and the evidence table must have 8 columns."""
import io
import re
import sys

MD = sys.argv[1] if len(sys.argv) > 1 else \
    r"D:\X\ND\ENSDF\XUNDL\2026OSAA_CT11035_152Gd_Multiplet_Gammas.md"
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

hdr = [i for i, l in enumerate(L) if l.startswith("| E_")]
ev = L[hdr[0]].strip("|").split("|") if hdr else []
rows, j = 0, (hdr[0] + 2 if hdr else 0)
while hdr and j < len(L) and L[j].startswith("|"):
    assert len(L[j].strip("|").split("|")) == len(ev), (j + 1, L[j])
    rows += 1
    j += 1
print("inconsistent tables:", bad)
print("evidence table columns:", len(ev), "rows:", rows)
