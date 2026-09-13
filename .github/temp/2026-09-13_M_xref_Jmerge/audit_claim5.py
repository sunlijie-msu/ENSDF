import io, difflib, sys

BEFORE = r"d:\X\ND\ENSDF\.github\temp\2026-09-13_M_xref_Jmerge\head_adopted_before.txt"
AFTER  = sys.argv[1] if len(sys.argv) > 1 else r"d:\X\ND\ENSDF\.github\temp\2026-09-13_M_xref_Jmerge\snapshot_audited.ens"

def rd(p):
    with io.open(p, "r", encoding="utf-8", errors="replace") as f:
        return [l.rstrip("\n").rstrip("\r") for l in f]

A = rd(BEFORE)
B = rd(AFTER)
print("before lines =", len(A), " after lines =", len(B))

sm = difflib.SequenceMatcher(None, A, B, autojunk=False)
print("ratios:", round(sm.ratio(), 6))
print("opcodes:")
added = []
removed = []
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == "equal":
        continue
    print("=" * 90)
    print("%-8s before[%d:%d] after[%d:%d]" % (tag, i1 + 1, i2, j1 + 1, j2))
    for k in range(i1, i2):
        col7 = A[k][6] if len(A[k]) > 6 else "?"
        removed.append((k + 1, A[k], col7))
        print("  - B%-5d col7=%r len=%d %r" % (k + 1, col7, len(A[k]), A[k]))
    for k in range(j1, j2):
        col7 = B[k][6] if len(B[k]) > 6 else "?"
        added.append((k + 1, B[k], col7))
        print("  + A%-5d col7=%r len=%d %r" % (k + 1, col7, len(B[k]), B[k]))

print()
print("=" * 90)
print("SUMMARY")
print("  added   lines:", len(added), " non-comment(col7!=c):", [x[0] for x in added if x[2] != "c"])
print("  removed lines:", len(removed), " non-comment(col7!=c):", [x[0] for x in removed if x[2] != "c"])
print("  added   len!=80:", [(x[0], len(x[1])) for x in added if len(x[1]) != 80])
print("  removed len!=80:", [(x[0], len(x[1])) for x in removed if len(x[1]) != 80])

ncA = [l for l in A if len(l) > 6 and l[6] != "c"]
ncB = [l for l in B if len(l) > 6 and l[6] != "c"]
print("  non-comment lines before:", len(ncA), " after:", len(ncB))
print("  non-comment sequences IDENTICAL:", ncA == ncB)
if ncA != ncB:
    for k, (x, y) in enumerate(zip(ncA, ncB)):
        if x != y:
            print("   first mismatch at non-comment index %d:\n     BEFORE %r\n     AFTER  %r" % (k, x, y))
            break

# also verify per-line: any line differing only in trailing content among non-comment
print()
print("=" * 90)
print("ELEMENTWISE non-comment comparison (positional):")
bad = 0
for k in range(min(len(ncA), len(ncB))):
    if ncA[k] != ncB[k]:
        bad += 1
        if bad <= 10:
            print("  idx", k, "\n    B:", repr(ncA[k]), "\n    A:", repr(ncB[k]))
print("  mismatches:", bad)
