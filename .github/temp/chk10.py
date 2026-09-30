import pathlib
ls = pathlib.Path("A36/S36/new/S36_34s_t_pg.ens").read_bytes().decode("utf-8").split("\n")
print("non-80:", [(i + 1, len(l)) for i, l in enumerate(ls) if l.strip() and len(l) != 80])
for i in (146, 147, 148, 158, 159):
    print(i + 1, len(ls[i]), repr(ls[i]))
