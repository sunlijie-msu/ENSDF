path = "A34/S34/new/S34_adopted.ens"
lines = open(path, encoding="ascii").read().split("\n")
print("=== all 'cG E$from {+31}P(|a,p|g).' lines (exact sentence) ===")
n = 0
for i, ln in enumerate(lines):
    if ln.rstrip() == " 34S  cG E$from {+31}P(|a,p|g).":
        n += 1
        # find preceding G record
        j = i - 1
        while j >= 0 and not (len(lines[j]) > 7 and lines[j][7] == "G" and lines[j][6] == " "):
            j -= 1
        g = lines[j] if j >= 0 else ""
        nxt = lines[i + 1].rstrip() if i + 1 < len(lines) else ""
        print("%2d) cmt line %-5d | G line %-5d len=%-3d DE=%-3r flag=%r | G=%r" %
              (n, i + 1, j + 1, len(g), g[19:21], g[76:77], g.rstrip()))
        print("      next: %r" % nxt[:70])
print("total exact-sentence comments:", n)
print()
print("=== other E-source comments mentioning 31P ===")
for i, ln in enumerate(lines, 1):
    if "cG E$" in ln and "31}P" in ln and ln.rstrip() != " 34S  cG E$from {+31}P(|a,p|g).":
        print("  line %-5d %r" % (i, ln.rstrip()))
