import io, sys

def check(path, label):
    raw = io.open(path, "rb").read().replace(b"\r\n", b"\n")
    lines = raw.decode("utf-8", "replace").split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    bad = [(i + 1, len(l), l) for i, l in enumerate(lines) if len(l) != 80]
    print("== %s : %d lines, %d not-80 ==" % (label, len(lines), len(bad)))
    for n, ln, l in bad:
        col7 = l[6] if len(l) > 6 else "?"
        print("   %5d len=%3d col7=%r |%s|" % (n, ln, col7, l))
    return bad

a = check(r"A34\S34\new\S34_adopted.ens", "CURRENT")
b = check(r".github\temp\2026-09-13_M_xref_Jmerge\head_adopted_before.txt", "HEAD(before)")
c = check(r".github\temp\2026-09-13_M_xref_Jmerge\snapshot_audited.ens", "SNAPSHOT 2FACC0A5")
print()
print("HEAD-bad line contents still present in CURRENT:",
      all(x[2] in [y[2] for y in a] for x in b))
