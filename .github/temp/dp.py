import pathlib, collections
lines = pathlib.Path("A34/merged.ens").read_text(encoding="utf-8").splitlines()
D = [l for l in lines if len(l) >= 9 and l[7] == "D" and l[8] in "PNADT" and l[6] == " "]
print("D-family records:", len(D), collections.Counter(l[8] for l in D))
print("col77 non-blank:", sum(1 for l in D if l[76] != " "))
print("col78 non-blank:", sum(1 for l in D if l[77] != " "))
print("col79 non-blank:", sum(1 for l in D if l[78] != " "))
print("col80 non-blank:", sum(1 for l in D if l[79] != " "), collections.Counter(l[79] for l in D if l[79] != " "))
print()
for l in D[:6]:
    print("|" + l + "|")
    print("   40-49:" + repr(l[39:49]) + " 50-64:" + repr(l[49:64]) + " 65-76:" + repr(l[64:76]) + " 77:" + repr(l[76]) + " 78-79:" + repr(l[77:79]) + " 80:" + repr(l[79]))
print()
print("cDP comment identifiers in file:")
import re
ids = [l[9:40].split("$")[0] for l in lines if len(l) > 10 and l[6] == "c" and l[7:9] == "DP"]
print(collections.Counter(ids))
