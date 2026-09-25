"""Build exact 80-column replacement strings for the Cl34 cL J$ block at lines 680-681 (read-only)."""
import io

F = r"d:\X\ND\ENSDF\A34\Cl34\new\Cl34_adopted.ens"
with io.open(F, newline="") as fh:
    lines = fh.read().replace("\r\n", "\n").split("\n")

old1, old2, old3 = lines[679], lines[680], lines[681]
print("old1 len %d: %r" % (len(old1), old1))
print("old2 len %d: %r" % (len(old2), old2))
print("old3 len %d: %r" % (len(old3), old3))
print()

P1 = " 34CL cL J$"          # 11
P2 = " 34CL2cL "            # 9
text = "|g to 2+, 2157.9 level, 3+, 146.36 level, and 4+, 2375.67 level; |p=+ from L=2 from 3/2+ in {+35}Cl({+3}He,|a)."
print("new text len", len(text))
print("first-line capacity", 80 - len(P1))
print("second-line capacity", 80 - len(P2))
split = text.rfind(" ", 0, 80 - len(P1) + 1)
t1, t2 = text[:split], text[split + 1:]
new1 = P1 + t1 + " " * (80 - len(P1) - len(t1))
new2 = P2 + t2 + " " * (80 - len(P2) - len(t2))
print()
print("new1 len %d: %r" % (len(new1), new1))
print("new2 len %d: %r" % (len(new2), new2))
print("joined text preserved:", (t1 + " " + t2) == text)
print()
print("OLD 1: %s" % repr(old1 + "\n" + old2 + "\n" + old3[:9]))
print("NEW 1: %s" % repr(new1 + "\n" + new2 + "\n" + old3[:9]))
