import re, glob, os
DIR = r"XUNDL/A58/Ni58/new/"
AD = [l.rstrip("\n").ljust(80) for l in open(DIR + "Ni58_adopted.ens", encoding="utf-8", errors="replace")]

# find dataset files and their assigned XREF letters by reading the adopted header comment block
print("### adopted dataset-letter map (first comments) ###")
for i in range(1, 60):
    l = AD[i-1]
    if l[6] == "c" or (l[5] != " " and l[6] == "c"):
        print(f"  :{i:<5}{l.rstrip()}")

print("\n### which adopted levels cite N(7560*) / C(7590*) ###")
for i, l in enumerate(AD, 1):
    if "N(7560" in l or "C(7590" in l:
        print(f"  :{i:<5}{l.rstrip()}")
print("  context:")
for n in range(1066, 1092):
    print(f"  :{n:<5}{AD[n-1].rstrip()}")
