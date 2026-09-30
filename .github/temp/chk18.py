import pathlib
ls = pathlib.Path("A36/S36/new/S36_34s_t_pg.ens").read_bytes().decode("utf-8").split("\n")
for i in range(128, 138):
    print(i + 1, len(ls[i]), "|", ls[i].rstrip())
