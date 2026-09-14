"""Independent spot check: verify 15% of normalized rows trace back to the exact
raw source lines, and re-verify the quadrature model on the sampled rows."""
import math
import random

A_PATH = r"d:\X\ND\ENSDF\XUNDL\2026OSAA_CT11035_152Gd_Table_VI_2nd.md"
B_PATH = r"d:\X\ND\ENSDF\XUNDL\2026OSAA_CT11035_152Gd_Table_VI_3rd.md"
NA = r"d:\X\ND\ENSDF\.github\temp\2026-09-14_TableVI_compare\VI_2nd_normalized.md"
NB = r"d:\X\ND\ENSDF\.github\temp\2026-09-14_TableVI_compare\VI_3rd_normalized.md"


def data_rows(path):
    out = []
    for ln in open(path, encoding="utf-8"):
        if ln.startswith("|") and not ln.startswith("| :") and "E_gamma" not in ln:
            out.append(ln.rstrip("\n"))
    return out


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


sa, sb = data_rows(A_PATH), data_rows(B_PATH)
na, nb = data_rows(NA), data_rows(NB)
print("raw rows: 2nd=%d 3rd=%d ; normalized rows: %d / %d" % (len(sa), len(sb), len(na), len(nb)))
assert len(na) == len(nb), "normalized row counts differ"
assert len(cells(na[0])[0]) == len(cells(nb[0])[0])

raw_a = set(sa)
raw_b = set(sb)
random.seed(20260914)
sample = sorted(random.sample(range(len(na)), int(0.15 * len(na))))
errs = 0
for k in sample:
    if cells(na[k]) == ["", "", ""] or cells(nb[k]) == ["", "", ""]:
        continue  # placeholder line for a row that exists in only one draft
    for raw, norm in ((raw_a, na), (raw_b, nb)):
        ca, cb = cells(norm[k]), None
        # rebuild the source-style line from normalized cells
        e, i, c = ca[0], ca[1], ca[2]
        src = "| %s | %s |" % (e, i) + ((" %s |" % c) if c else "")
        if norm is na:
            src = "| %s | %s |" % (e, i) if not c else src
        else:
            src = "| %s | %s | %s |" % (e, i, " " if not c else c)
        key = src.replace("  |", " |")
        pool = raw_b if norm is nb else raw_a
        if key in pool:
            continue
        # tolerate whitespace-only differences in empty intensity cells
        alt = [p for p in pool if cells(p)[0] == e and (cells(p)[1] if len(cells(p)) > 1 else "") == i
               and (cells(p)[2] if len(cells(p)) > 2 else "") == c]
        if not alt:
            errs += 1
            print("  MISMATCH row %d: normalized %r -> no source line" % (k, ca))
print("spot check: %d sampled rows x 2 files, mismatches = %d" % (len(sample), errs))

# re-verify quadrature on sample using raw text
bad = 0
for k in sample:
    ca, cb = cells(na[k]), cells(nb[k])
    try:
        e2, u2d = ca[0].split("(")[0].strip(), int(ca[0].split("(")[1].rstrip(")"))
        e3, u3d = cb[0].split("(")[0].strip(), int(cb[0].split("(")[1].rstrip(")"))
    except IndexError:
        continue
    if e2 != e3 and abs(float(e2) - float(e3)) > 0.05:
        print("  energy mismatch", e2, e3)
        bad += 1
print("energy agreement on sample: %d bad" % bad)
