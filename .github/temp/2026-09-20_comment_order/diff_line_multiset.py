"""Verify that comment reordering only permutes existing comment lines.

Compares the multiset of right-stripped lines between the pre-edit (HEAD) copy and the
working copy: any deletion or text alteration shows up as a net decrease, any new
evaluator text as a net increase.
"""
import collections
import sys


def counts(path):
    c = collections.Counter()
    for raw in open(path, encoding="ascii", errors="ignore"):
        c[raw.rstrip("\r\n").rstrip()] += 1
    return c


def main(old, new):
    a, b = counts(old), counts(new)
    removed = sorted((a - b).items())
    added = sorted((b - a).items())
    print("removed/shrunk lines:", len(removed))
    for text, n in removed:
        print("  -", n, repr(text[:78]))
    print("added lines:", len(added))
    for text, n in added:
        print("  +", n, repr(text[:78]))


if __name__ == "__main__":
    main(*sys.argv[1:3])
