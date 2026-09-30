import pathlib
ls = pathlib.Path("A36/S36/new/S36_34s_t_pg.ens").read_bytes().decode("utf-8").split("\n")
print("lines:", len(ls))
for i in range(131, 142):
    l = ls[i]
    print(i + 1, "len", len(l), "pad", len(l) - len(l.rstrip()), "|", repr(l.rstrip()))
