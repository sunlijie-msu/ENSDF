"""Read-only: show current adopted record values for the affected levels + the XC gamma block."""
import io

AD = r"d:\X\ND\ENSDF\A34\S34\new\S34_adopted.ens"
XC = r"d:\X\ND\ENSDF\A34\S34\new\S34_34cl_ec_decay_31.99_m.ens"

NEW = ["2127.561", "3304.210", "4074.662", "4624.404", "4876.842", "5690.62",
       "5679.928", "5755.873", "5847.521", "6251.73", "6342.52", "6478.768",
       "7110.450", "7629.906"]

with io.open(AD, newline="") as fh:
    ad = fh.read().replace("\r\n", "\n").split("\n")

print("=== adopted L records (new values) ===")
for i, l in enumerate(ad):
    if len(l) == 80 and l[5:7] == "  " and l[7] == "L" and l[9:19].strip() in NEW:
        print("  %-5d %r" % (i + 1, l))

print()
print("=== XC 34Cl ec+b+ decay: levels and gammas ===")
with io.open(XC, newline="") as fh:
    xc = fh.read().replace("\r\n", "\n").split("\n")
for i, l in enumerate(xc):
    if len(l) in (80, 0):
        if l[7:8] in ("L", "G") and l[5:7] == "  ":
            print("  %-5d %d %r" % (i + 1, len(l), l))
        elif l[6:7] == "c" and ("dopted" in l or "4074" in l or "4075" in l or "4073" in l):
            print("  %-5d %d CMT %r" % (i + 1, len(l), l.rstrip()))
    else:
        print("  %-5d NON80 %d %r" % (i + 1, len(l), l))
