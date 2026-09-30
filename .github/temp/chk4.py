import pathlib
ls = pathlib.Path("A36/S36/new/S36_34s_t_pg.ens").read_bytes().decode("utf-8").split("\n")
for i in (147, 158, 160):
    l = ls[i]
    print(i + 1, len(l), repr(l))
print("non-80:", [(i + 1, len(l)) for i, l in enumerate(ls) if l.strip() and len(l) != 80])
