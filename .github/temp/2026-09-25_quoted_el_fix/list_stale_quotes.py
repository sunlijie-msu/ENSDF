"""List every occurrence of superseded quoted level energies in A34/S34/new/*.ens (read-only).

Pairs: old quoted value -> new adopted record value (from 34.err quoted-inconsistency list).
"""
import glob
import io
import os

PAIRS = [
    ("2127.558", "2127.561"),
    ("3304.207", "3304.210"),
    ("4074.657", "4074.662"),
    ("4624.401", "4624.404"),
    ("4876.839", "4876.842"),
    ("5690.61", "5690.62"),
    ("5755.871", "5755.873"),
    ("5847.517", "5847.521"),
    ("6251.72", "6251.73"),
    ("6342.51", "6342.52"),
    ("6478.765", "6478.768"),
    ("7110.447", "7110.450"),
    ("7629.903", "7629.906"),
    ("5679.925", "5679.928"),
]

files = sorted(glob.glob(r"A34/S34/new/*.ens"))
total = 0
for path in files:
    with io.open(path, newline="") as fh:
        lines = fh.read().replace("\r\n", "\n").split("\n")
    hits = []
    for i, l in enumerate(lines):
        for old, new in PAIRS:
            if old in l:
                hits.append((i + 1, old, new, l.rstrip()))
    if hits:
        print("=== %s" % os.path.basename(path))
        for n, old, new, txt in hits:
            print("  %-5d %-10s -> %-10s | %s" % (n, old, new, txt))
        total += len(hits)
print()
print("total occurrences of superseded values: %d in %d files" % (total, len(files)))
