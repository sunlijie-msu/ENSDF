"""Measure, across adopted datasets, whether dataset-scoped compound E(x),J(x) units
tend to precede or follow the plain general J$ unit within the same cL comment block."""
import glob
import os
import re
import sys

DOLLAR = chr(36)
COMPOUND = re.compile(r"^[A-Z]+\([^)]*\)")


def ident_of(line):
    body = line[8:]
    if DOLLAR in body[:45]:
        return body.split(DOLLAR)[0].strip()
    return ""


def blocks(path):
    out, cur = [], []
    for n, raw in enumerate(open(path, encoding="ascii", errors="ignore"), 1):
        line = raw.rstrip("\n").rstrip("\r")
        if len(line) > 7 and line[6] == "c" and line[7] == "L":
            if len(line) > 8 and line[8].isdigit():
                continue
            cur.append((n, ident_of(line)))
        else:
            if cur:
                out.append(cur)
                cur = []
    if cur:
        out.append(cur)
    return out


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    files = sorted(glob.glob(os.path.join(root, "A*", "*", "new", "*_adopted.ens")))
    files += sorted(glob.glob(os.path.join(root, "A*.ens")))
    before = after = 0
    for f in files:
        for blk in blocks(f):
            idents = [b[1] for b in blk]
            if "J" not in idents:
                continue
            jpos = idents.index("J")
            comp = [i for i, x in enumerate(idents) if COMPOUND.match(x) and "J" in x]
            if not comp:
                continue
            tag = "compound-before-J" if min(comp) < jpos else "J-before-compound"
            if min(comp) < jpos:
                before += 1
            else:
                after += 1
            print(tag, os.path.basename(f), "line", blk[0][0], idents)
    print("compound before plain J:", before, "| plain J before compound:", after)


if __name__ == "__main__":
    main()
