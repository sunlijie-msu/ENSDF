"""Generate a column-aligned CSV of XUNDL compilations from the markdown tables.

Reads : XUNDL/Personal/Folder_Lijie_Sun_Updating.md
Uses  : table under "## Data Consistency Check + XUNDL Compilation"
        table under "## XUNDL Compilation"
Prints: fixed-width, delimiter-aligned CSV (comma separated) + alignment proof.
Read-only: writes nothing.
"""
import csv
import io
import re
import sys

MD = r"d:\X\ND\ENSDF\XUNDL\Personal\Folder_Lijie_Sun_Updating.md"

HEAD_A = "## Data Consistency Check + XUNDL Compilation"
HEAD_C = "## XUNDL Compilation"

COLS = ["Date", "Manuscript", "NSR", "Nucleus", "XUNDL", "Review rounds", "Dataset"]


def read_lines(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read().splitlines()


def grab_table(lines, heading):
    """Return (header_cells, [row_cells, ...]) for the first table after heading."""
    try:
        start = next(i for i, ln in enumerate(lines) if ln.strip() == heading)
    except StopIteration:
        raise SystemExit("ERROR: heading not found: %s" % heading)

    header, rows = None, []
    for ln in lines[start + 1:]:
        s = ln.strip()
        if s.startswith("|"):
            cells = [c.strip() for c in s.strip("|").split("|")]
            if all(re.fullmatch(r"-+", c or "-") for c in cells):
                continue                      # separator row
            if header is None:
                header = cells
            else:
                rows.append(cells)
        elif s.startswith("## ") or (s and not s.startswith("|") and not s.startswith("#")):
            if header is not None:
                break
    return header, rows


def quote(cell):
    """Render one CSV cell (RFC4180 quoting only when required)."""
    if any(ch in cell for ch in ',"'):
        return '"' + cell.replace('"', '""') + '"'
    return cell


def delimiters(line):
    """Indexes of commas that are NOT inside a quoted section."""
    out, in_q = [], False
    for i, ch in enumerate(line):
        if ch == '"':
            in_q = not in_q
        elif ch == "," and not in_q:
            out.append(i)
    return out


def main():
    lines = read_lines(MD)

    _, rows_a = grab_table(lines, HEAD_A)
    _, rows_c = grab_table(lines, HEAD_C)

    if len(rows_a[0]) != 7 or len(rows_c[0]) != 5:
        raise SystemExit("ERROR: unexpected column counts %d / %d" % (len(rows_a[0]), len(rows_c[0])))

    data = [tuple(r) for r in rows_a]                              # date, ms, nsr, nuc, xundl, rounds, ds
    data += [(r[0], "", r[1], r[2], r[3], "", r[4]) for r in rows_c]

    # column widths from rendered cells (header included)
    rendered = [[quote(c) for c in row] for row in data]
    widths = [len(h) for h in COLS]
    for row in rendered:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(cell))

    out = []
    out.append(",".join(h.ljust(widths[i]) for i, h in enumerate(COLS[:-1])) + "," + COLS[-1])
    for row in rendered:
        left = ",".join(row[i].ljust(widths[i]) for i in range(len(row) - 1))
        out.append(left + "," + row[-1])

    print("=" * 100)
    print("GENERATED CSV  (rows=%d, columns=%d, widths=%s)" % (len(data), len(COLS), widths))
    print("=" * 100)
    for ln in out:
        print(ln)

    # ---- alignment proof -------------------------------------------------
    print()
    print("=" * 100)
    print("ALIGNMENT PROOF")
    print("=" * 100)
    ref = delimiters(out[0])
    bad = [n for n, ln in enumerate(out, 1) if delimiters(ln) != ref]
    print("delimiter columns : %s" % ref)
    print("lines aligned     : %d/%d" % (len(out) - len(bad), len(out)))
    print("misaligned lines  : %s" % (bad if bad else "none"))

    # ---- round-trip validation ------------------------------------------
    print()
    print("=" * 100)
    print("ROUND-TRIP VALIDATION (parse back with csv module, compare to markdown)")
    print("=" * 100)
    parsed = list(csv.reader(io.StringIO("\n".join(out))))
    print("parsed rows       : %d (expect %d)" % (len(parsed), len(data) + 1))
    print("field counts      : %s" % sorted({len(r) for r in parsed}))
    errs = 0
    for n, (got, want) in enumerate(zip(parsed[1:], data), 2):
        got = [c.strip() for c in got]
        if got != list(want):
            errs += 1
            print("  MISMATCH line %d\n    csv : %s\n    md  : %s" % (n, got, list(want)))
    if [c.strip() for c in parsed[0]] != COLS:
        errs += 1
        print("  MISMATCH header")
    print("value mismatches  : %d" % errs)
    print()
    print("RESULT: %s" % ("PASS" if (not bad and not errs and len(parsed) == len(data) + 1) else "FAIL"))
    return 0 if (not bad and not errs) else 1


if __name__ == "__main__":
    sys.exit(main())
