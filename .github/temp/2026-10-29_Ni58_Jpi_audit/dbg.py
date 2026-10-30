import re
p = r"d:/X/ND/ENSDF/XUNDL/A58/Ni58/new/Ni58_adopted.ens"
L = open(p, encoding="utf-8", errors="replace").read().split("\n")
line = L[134]
print(repr(line))
print("col7-8:", repr(line[6:8]))
t = line.ljust(80)[9:80]
print("t:", repr(t[:40]))
pat = r"\b([A-Za-z]{1,4})\(([A-Za-z])\)\s*\$"
print("findall:", re.findall(pat, t))
pat2 = r"([A-Za-z]{1,4})\(([A-Za-z])\)\$"
print("findall2:", re.findall(pat2, t))
