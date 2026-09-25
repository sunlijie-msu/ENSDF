"""Dump exact bytes of the 7 comment-unit order violations (read-only)."""
import io

F = r"d:\X\ND\ENSDF\A34\S34\new\S34_30si_a_g_a_n_resonances.ens"
PAIRS = [(157, 158), (165, 166), (170, 171), (175, 176), (193, 194), (226, 227), (346, 347)]

with io.open(F, newline="") as fh:
    raw = fh.read()
lines = raw.replace("\r\n", "\n").split("\n")
print("CRLF count: %d  (file uses CRLF: %s)" % (raw.count("\r\n"), raw.count("\r\n") > 0))
print()

for a, b in PAIRS:
    la, lb = lines[a - 1], lines[b - 1]
    print("block %d/%d" % (a, b))
    for tag, l in (("gen", la), ("id ", lb)):
        core = l.rstrip()
        print("   %s len=%d  text=%d  trail=%d  prefix=%r" % (tag, len(l), len(core), len(l) - len(core), l[:9]))
        print("      %r" % core)
    # suggested new strings (identifier line first, general last)
    ta = la[9:].rstrip()
    tb = lb[9:].rstrip()
    new_first = tb + " " * (80 - 9 - len(tb))
    new_second = ta + " " * (80 - 9 - len(ta))
    print("   -> new line %d: %r  (len %d)" % (a, new_first, len(new_first)))
    print("   -> new line %d: %r  (len %d)" % (b, new_second, len(new_second)))
    print()
