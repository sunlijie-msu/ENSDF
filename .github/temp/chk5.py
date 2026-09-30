import pathlib
ls = pathlib.Path("A36/S36/new/S36_34s_t_pg.ens").read_bytes().decode("utf-8").split("\n")
print("lines:", len(ls))
print("non-80:", [(i + 1, len(l)) for i, l in enumerate(ls) if l.strip() and len(l) != 80])
for i in (52, 72, 91, 147, 153, 158, 160):
    print(i + 1, len(ls[i]), repr(ls[i]))
print("Other:", sum(l.count("Other:") for l in ls), "other:", sum(l.count("other:") for l in ls))
print("double-space:", [i + 1 for i, l in enumerate(ls) if "  " in l[9:40].replace("  ", "  ") and "Sa09.  " in l])
