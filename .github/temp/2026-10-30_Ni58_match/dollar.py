import re
L = [l.rstrip("\n").ljust(80) for l in open(r"XUNDL/A58/Ni58/new/Ni58_adopted.ens", encoding="utf-8", errors="replace")]
n = 0; ex = []
for i, l in enumerate(L, 1):
    if l[6] == "c" and l[7] in "LG":
        t = l[9:80]
        m = re.match(r"^([A-Za-z]{1,3}(?:\([A-Za-z]\))?)(\s{2,})(\S)", t)
        if m:
            n += 1
            ex.append((i, t.rstrip()[:64]))
print("comment identifiers not followed by dollar-delimiter:", n)
for e in ex[:12]:
    print("  ", e[0], repr(e[1]))
