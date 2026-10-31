import glob, os
D = r"d:/X/ND/ENSDF/XUNDL/A58/Co58/new"
print("illegal column-80 character on L/G records (allowed: space, ?, S)")
for p in sorted(glob.glob(D + "/*.ens")):
    for i, l in enumerate(open(p, encoding="utf-8", errors="replace"), 1):
        l = l.rstrip("\n").ljust(80)
        if l[5] == " " and l[6] == " " and l[7] in "LG" and l[79].strip() not in ("", "?", "S"):
            print(f"  {os.path.basename(p)}:{i} col80={l[79]!r} | {l.rstrip()}")
print("\nnon-blank MS field (cols 78-79) on G records")
for p in sorted(glob.glob(D + "/*.ens")):
    for i, l in enumerate(open(p, encoding="utf-8", errors="replace"), 1):
        l = l.rstrip("\n").ljust(80)
        if l[5] == " " and l[6] == " " and l[7] == "G" and l[77:79].strip():
            print(f"  {os.path.basename(p)}:{i} MS={l[77:79]!r} | {l.rstrip()}")
