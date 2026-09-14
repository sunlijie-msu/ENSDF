path = "A34/S34/new/S34_adopted.ens"
lines = open(path, encoding="ascii").read().split("\n")
for n in (619, 620):
    s = lines[n - 1]
    print("line %d len=%d" % (n, len(s)))
    print("  repr: %r" % s)
