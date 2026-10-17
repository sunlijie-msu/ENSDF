"""Validate XUNDL_Compilations.csv against the markdown source tables.

Checks : (1) delimiter columns identical on every line (visual alignment)
         (2) RFC4180 parse -> field count per row
         (3) every parsed value == the value in the markdown tables
         (4) no trailing whitespace at end of any line
Read-only.
"""
import csv
import re
import sys

MD = r"d:\X\ND\ENSDF\XUNDL\Personal\Folder_Lijie_Sun_Updating.md"
CSV = r"d:\X\ND\ENSDF\.github\temp\2026-10-16_xundl_compilations\XUNDL_Compilations.csv"

HEAD_A = "## Data Consistency Check + XUNDL Compilation"
HEAD_C = "## XUNDL Compilation"
COLS = ["Date", "Manuscript", "NSR", "Nucleus", "XUNDL", "Review rounds", "Dataset"]


def grab(lines, heading):
    start = next(i for i, ln in enumerate(lines) if ln.strip() == heading)
    header, rows = None, []
    for ln in lines[start + 1:]:
        s = ln.strip()
        if s.startswith("|"):
            cells = [c.strip() for c in s.strip("|").split("|")]
            if all(re.fullmatch(r"-+", c or "-") for c in cells):
                continue
            if header is None:
                header = cells
            else:
                rows.append(cells)
        elif s.startswith("## ") or (s and not s.startswith("#")):
            if header is not None:
                break
    return header, rows


def delims(line):
    out, in_q = [], False
    for i, ch in enumerate(line):
        if ch == '"':
            in_q = not in_q
        elif ch == "," and not in_q:
            out.append(i)
    return out


def main():
    md = open(MD, encoding="utf-8").read().splitlines()
    raw = open(CSV, encoding="utf-8").read().splitlines()

    _, ra = grab(md, HEAD_A)
    _, rc = grab(md, HEAD_C)
    want = [list(r) for r in ra] + [[r[0], "", r[1], r[2], r[3], "", r[4]] for r in rc]

    fails = 0

    # (1) alignment
    ref = delims(raw[0])
    bad = [n for n, ln in enumerate(raw, 1) if delims(ln) != ref]
    print("delimiter cols : %s" % ref)
    print("aligned lines  : %d/%d %s" % (len(raw) - len(bad), len(raw), "OK" if not bad else "FAIL %s" % bad))
    fails += len(bad)

    # (2) parse + field count
    parsed = list(csv.reader(raw))
    counts = sorted({len(r) for r in parsed})
    print("parsed rows    : %d (md rows %d)" % (len(parsed), len(want) + 1))
    print("field counts   : %s %s" % (counts, "OK" if counts == [7] else "FAIL"))
    if counts != [7]:
        fails += 1
    if parsed[0] != [c.ljust(len(parsed[0][i])) for i, c in enumerate(COLS)]:
        if [c.strip() for c in parsed[0]] != COLS:
            print("header         : FAIL")
            fails += 1
        else:
            print("header         : OK")
    else:
        print("header         : OK")

    # (3) values
    mism = 0
    for n, (got, exp) in enumerate(zip(parsed[1:], want), 2):
        if [c.strip() for c in got] != exp:
            mism += 1
            print("  line %d\n    csv: %s\n    md : %s" % (n, [c.strip() for c in got], exp))
    print("value mismatch : %d %s" % (mism, "OK" if mism == 0 else "FAIL"))
    fails += mism
    if len(parsed) != len(want) + 1:
        print("row count      : FAIL")
        fails += 1

    # (4) trailing whitespace
    tw = [n for n, ln in enumerate(raw, 1) if ln != ln.rstrip()]
    print("trailing space : %s %s" % (tw if tw else "none", "OK" if not tw else "FAIL"))
    fails += len(tw)

    print()
    print("RESULT: %s" % ("PASS" if fails == 0 else "FAIL (%d)" % fails))
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
