import pathlib
ls = pathlib.Path("A36/S36/new/S36_34s_t_pg.ens").read_bytes().decode("utf-8").split("\n")
print("lines:", len(ls), "non-80:", [(i+1, len(l)) for i, l in enumerate(ls) if l.strip() and len(l) != 80])
print("Other: (sentence) =", sum(l.count(". Other:") for l in ls))
print("$other: =", sum(l.count("$other:") for l in ls))
print(r"\n".join(l.rstrip() for l in ls if "Other:" in l)[:0])
for i, l in enumerate(ls):
    if "Other:" in l: print(i+1, l.rstrip())
