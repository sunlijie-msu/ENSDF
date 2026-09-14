path = "A34/S34/new/S34_adopted.ens"
lines = open(path, encoding="ascii").read().split("\n")
for n in range(572, 579):
    s = lines[n - 1]
    print("line %d len=%d %r" % (n, len(s), s))
