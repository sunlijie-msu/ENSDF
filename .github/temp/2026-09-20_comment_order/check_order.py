"""Compact listing of comment-block identifier sequences, flagging order violations.

Expected order:
  cL: E-type -> J-type -> T -> S -> general (no identifier)
  cG: E-type -> RI-type -> M-type -> MR -> general (no identifier)
Anything else is reported as "other" and listed after the general comment when no
identifier is present in the block.
"""
import re
import sys


def col(line, n):
    return line[n - 1] if len(line) >= n else ""


def parse(path):
    with open(path, "r", encoding="ascii") as fh:
        lines = [ln.rstrip("\r\n") for ln in fh]
    units = []
    for i, ln in enumerate(lines, 1):
        if col(ln, 7) != "c":
            continue
        kind = {"L": "cL", "G": "cG"}.get(col(ln, 8), "c")
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
    return blocks


def rank(kind, ident):
    """Return (group, key) for ordering.

    Composite identifiers (e.g. "E,RI" or "E(E),J(E)") are ranked by their FIRST
    field, so the category order is enforced for every unit.  Dataset-scoped
    parentheses are stripped before ranking.  The general (identifier-less)
    comment is always last.
    """
    if ident is None or ident == "":
        return (99, "")
    first = re.sub(r"\([^)]*\)", "", ident).split(",")[0].strip()
    up = first.upper()
    if kind == "cL":
        if up.startswith("E"):
            return (1, "")
        if up.startswith("J"):
            return (2, "")
        if up.startswith("T"):
            return (3, "")
        if up.startswith("S"):
            return (4, "")
    if kind == "cG":
        if up.startswith("E"):
            return (1, "")
        if up.startswith("RI"):
            return (2, "")
        if up.startswith("MR"):
            return (4, "")
        if up.startswith("M"):
            return (3, "")
    # Unranked/field-specific identifiers (e.g. MOMM1, BE2) share one group so that
    # only the category order is enforced, not an alphabetical sub-order.
    return (50, "")


def main(path):
    blocks = parse(path)
    bad = 0
    for b in blocks:
        seq = [u["ident"] for u in b["units"]]
        keys = [rank(b["kind"], i)[0] for i in seq]
        ordered = all(keys[i] <= keys[i + 1] for i in range(len(keys) - 1))
        flag = "" if ordered else "  <<< OUT OF ORDER"
        if not ordered:
            bad += 1
        shown = keys
        print("%-5s line %5d-%-5d n=%d %s%s" % (b["kind"], b["start"], b["last"],
                                                len(b["units"]), shown, flag))
    print("\nblocks out of order:", bad, "of", len(blocks))


if __name__ == "__main__":
    main(sys.argv[1])
