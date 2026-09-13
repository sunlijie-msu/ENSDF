import io, re, sys

SNAP = r"d:\X\ND\ENSDF\.github\temp\2026-09-13_M_xref_Jmerge\snapshot_audited.ens"
P = sys.argv[1] if len(sys.argv) > 1 else SNAP
KEYS = ["1970Mo09", "1971Mu03", "1972Jo10", "1974Gr06", "1971Gr26", "1979Ba54"]

with io.open(P, "r", encoding="utf-8", errors="replace") as f:
    L = [l.rstrip("\n").rstrip("\r") for l in f]

print("total lines:", len(L))

def col7(l):
    return l[6] if len(l) > 6 else ""

# ---- global occurrence scan
print("\n--- GLOBAL OCCURRENCE SCAN (all lines) ---")
for k in KEYS:
    hits = [(i + 1, l) for i, l in enumerate(L) if k in l]
    print("%s : %d occurrence(s)" % (k, len(hits)))
    for n, l in hits:
        print("     line %-5d col7=%r is_cL=%s : %s" % (n, col7(l), l[6:8] == "cL", l.strip()))

# ---- identify all cL comment lines and group them into J$ blocks
print("\n--- cL LINE INVENTORY (label, ident, length) ---")
bad_len = []
groups = []
cur = None
for i, l in enumerate(L):
    if len(l) > 7 and l[6:8] == "cL":
        label = l[5]
        ident = re.match(r"^([A-Za-z][A-Za-z]?)\$", l[9:])
        ident = ident.group(1) if ident else None
        if len(l) != 80:
            bad_len.append((i + 1, len(l)))
        if label == " ":
            cur = {"start": i + 1, "ident": ident, "lines": [(i + 1, l, label)]}
            groups.append(cur)
        else:
            if cur is None:
                print("!!! ORPHAN continuation at line %d: %r" % (i + 1, l))
            else:
                cur["lines"].append((i + 1, l, label))
print("cL lines total:", sum(len(g["lines"]) for g in groups))
print("cL lines not 80 chars:", bad_len if bad_len else "none")

print("\n--- J$ BLOCK CONTINUATION INTEGRITY ---")
jblocks = [g for g in groups if g["ident"] == "J"]
print("number of cL J$ blocks:", len(jblocks))
for g in jblocks:
    labels = [x[2] for x in g["lines"]]
    exp = [" "] + [str(k) for k in range(2, len(labels) + 1)]
    ok = labels == exp
    print("  J$ block start line %-4d nlines=%d labels=%r %s" % (g["start"], len(labels), labels, "OK" if ok else "*** NON-SEQUENTIAL ***"))
    for n, l, lb in g["lines"]:
        if len(l) != 80:
            print("      *** line %d len=%d" % (n, len(l)))

print("\n--- KEY OCCURRENCES INSIDE cL J$ BLOCKS ---")
found = False
for g in jblocks:
    for n, l, lb in g["lines"]:
        for k in KEYS:
            if k in l:
                found = True
                print("  !!! %s at line %d: %s" % (k, n, l.strip()))
print("  none" if not found else "")

print("\n--- cL J$ BLOCK FULL TEXT (final merged) ---")
for g in jblocks:
    print("  --- J$ block starting line %d ---" % g["start"])
    for n, l, lb in g["lines"]:
        print("   %-5d |%s|" % (n, l[9:]))
