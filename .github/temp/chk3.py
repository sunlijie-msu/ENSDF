import pathlib
ls = pathlib.Path("A36/S36/new/S36_34s_t_pg.ens").read_bytes().decode("utf-8").split("\n")
print("Other: count:", sum(l.count("Other:") for l in ls))
print("other: count:", sum(l.count("other:") for l in ls))
bad = [(i + 1, len(l)) for i, l in enumerate(ls) if l.strip() and len(l) != 80]
print("non-80 lines:", bad)
for i in (52, 72, 91, 92, 160, 161):
    print(i + 1, len(ls[i]), repr(ls[i]))
