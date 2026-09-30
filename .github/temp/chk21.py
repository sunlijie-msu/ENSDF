import pathlib
ls = pathlib.Path("A36/S36/new/S36_34s_t_pg.ens").read_bytes().decode("utf-8").split("\n")
for i in (134, 135, 136, 137):
    l = ls[i]
    print(i + 1, "len", len(l), "textlen", len(l.rstrip()), "pad", len(l) - len(l.rstrip()), "|", repr(l.rstrip()))
