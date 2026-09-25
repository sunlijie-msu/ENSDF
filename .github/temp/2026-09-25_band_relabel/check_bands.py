import io

A2 = r"d:\X\ND\ENSDF\A34\S34\new\S34_24mg_16o_a2pg.ens"
AD = r"d:\X\ND\ENSDF\A34\S34\new\S34_adopted.ens"


def load(f):
    with io.open(f, newline="") as fh:
        return fh.read().replace("\r\n", "\n").replace("\r", "\n").split("\n")


for name, f in (("a2pg", A2), ("adopted", AD)):
    lines = load(f)
    bad = [(i + 1, len(l)) for i, l in enumerate(lines) if l.strip() and len(l) != 80]
    print("=== %s : %d lines ; non-80: %s" % (name, len(lines), bad[:10]))
    print("  band comments:")
    for i, l in enumerate(lines):
        if "BAND(" in l:
            print("   L%-5d %r  len=%d" % (i + 1, l.strip(), len(l)))
    bands = {}
    for i, l in enumerate(lines):
        if len(l) == 80 and l[5:7] == "  " and l[7] == "L":
            fl = l[76]
            if fl != " ":
                bands.setdefault(fl, []).append(
                    (i + 1, l[9:19].strip(), l[22:39].strip())
                )
    for k in sorted(bands):
        print("  col77 flag %r  n=%d" % (k, len(bands[k])))
        for rec in bands[k]:
            print("     line %-5d E=%-12s J=%s" % rec)
