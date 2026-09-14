path = "A34/S34/new/S34_adopted.ens"
lines = open(path, encoding="ascii").read().split("\n")
for n in range(618, 626):
    s = lines[n - 1]
    print("line %d len=%-3d %r" % (n, len(s), s))
print()
print("remaining 'E$from {+31}P' comments:", sum(1 for l in lines if "E$from {+31}P(|a,p|g)." in l))
