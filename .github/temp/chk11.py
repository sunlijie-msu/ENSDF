import pathlib
ls = pathlib.Path("A36/S36/new/S36_34s_t_pg.ens").read_bytes().decode("utf-8").split("\n")
print("lines:", len(ls))
print("non-80:", [(i + 1, len(l)) for i, l in enumerate(ls) if l.strip() and len(l) != 80])
print("Other:", sum(l.count("Other:") for l in ls))
print("stray:", [i + 1 for i, l in enumerate(ls) if " 1972 Sa09" in l or "from  19" in l or "Sa09.  " in l])
print(repr(ls[158]))
