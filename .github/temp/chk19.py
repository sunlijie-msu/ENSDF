import pathlib
ls = pathlib.Path("A36/S36/new/S36_34s_t_pg.ens").read_bytes().decode("utf-8").split("\n")
for i, l in enumerate(ls):
    if "cL T$" in l or "cG M$" in l or "cG M,MR$" in l or "2cL" in l:
        print(i + 1, "|", l.rstrip())
