import sys

adp = r"A34\S34\new\S34_adopted.ens"
ls = open(adp, "rb").read().decode().split("\r\n")
want = [967, 1026, 1063, 1093, 1146, 1197, 1228, 1263, 1350, 1545, 1743, 1768,
        1796, 1806, 1812, 1852, 1861, 1874, 1883, 1889, 1895, 1913]
out = []
for n in want:
    i = n - 1
    j = i + 1
    while j < len(ls):
        l = ls[j]
        if len(l) > 7 and l[6] == " " and l[7] in "LG" and l[5] == " ":
            break
        j += 1
    out.append("== line %d  %s" % (n, ls[i][9:39].rstrip()))
    for k in range(i, j):
        l = ls[k]
        if len(l) > 6 and l[6] == "c":
            out.append("    " + l[8:].rstrip())
    out.append("")
sys.stdout.write("\n".join(out))
