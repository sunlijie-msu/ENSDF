"""Analyze ENSDF comment ordering.

Splits the file into comment units (a unit = one comment record plus its
continuation lines) and groups consecutive units that attach to the same
preceding record type (cL / cG / bare c) into blocks, so ordering violations
against E$ -> J$ -> T$ -> S$ -> general (L) and E$ -> RI$ -> M$ -> MR$ -> general (G)
become visible.
"""
import sys


def col(line, n):
    return line[n - 1] if len(line) >= n else ""


def main(path):
    with open(path, "r", encoding="ascii") as fh:
        lines = [ln.rstrip("\r\n") for ln in fh]

    units = []  # kind, ident, start, lines
    for i, ln in enumerate(lines, 1):
        if col(ln, 7) != "c":
            continue
        tail = col(ln, 8)
        kind = {"L": "cL", "G": "cG"}.get(tail, "c")
        cont = col(ln, 6) not in ("", " ", "0")
        body = ln[8:].rstrip()
        ident = body.split("$", 1)[0].strip() if "$" in body else None
        if cont and units and units[-1]["kind"] == kind:
            units[-1]["lines"].append((i, ln))
            continue
        units.append({"kind": kind, "ident": ident, "start": i, "lines": [(i, ln)]})

    blocks = []
    for u in units:
        if blocks and blocks[-1]["kind"] == u["kind"] and blocks[-1]["last"] + 1 == u["start"]:
            blocks[-1]["units"].append(u)
            blocks[-1]["last"] = u["lines"][-1][0]
        else:
            blocks.append({"kind": u["kind"], "units": [u], "start": u["start"],
                           "last": u["lines"][-1][0]})

    for b in blocks:
        idents = [u["ident"] for u in b["units"]]
        print("=" * 78)
        print("block %d-%d  %s  units=%d" % (b["start"], b["last"], b["kind"], len(b["units"])))
        print("  idents:", idents)
        for u in b["units"]:
            for ln, raw in u["lines"]:
                print("  %5d |%s|" % (ln, raw))


if __name__ == "__main__":
    main(sys.argv[1])
