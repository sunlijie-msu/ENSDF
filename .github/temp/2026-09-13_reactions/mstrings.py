path = "A34/S34/new/S34_adopted.ens"
lines = open(path, encoding="ascii").read().split("\n")
for t in [527, 529, 531, 533, 567, 569, 572, 617, 619, 622]:
    g = lines[t - 1]
    c = lines[t]
    print("--- line %d" % t)
    print("G_new: |%s|" % (g.rstrip() + " " * (76 - len(g.rstrip())) + "M   "))
    print("G_old: |%s|" % g.rstrip())
    print("C_old: |%s|" % c.rstrip())
