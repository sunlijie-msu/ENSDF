path = "A34/S34/new/S34_adopted.ens"
lines = open(path, encoding="ascii").read().split("\n")
for e in ["1856", "2043", "3428", "4604", "2176", "2242", "4737", "3809", "4985", "7111"]:
    for i, ln in enumerate(lines):
        if len(ln) > 7 and ln[7] == "G" and ln[6] == " " and ln[9:19].strip() == e and i + 1 < len(lines) and "31}P(" in lines[i + 1]:
            print("line %-5d len=%-3d col77=%r E=%-8s |%s|" % (i + 1, len(ln), ln[76:77], e, ln.rstrip()))
