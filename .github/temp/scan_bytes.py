import pathlib
p = pathlib.Path("A36/S36/new/S36_34s_t_pg.ens")
b = p.read_bytes()
print("has U+FFFD bytes:", b.count(b"\xef\xbf\xbd"))
print("non-ascii bytes:", sorted(set(x for x in b if x > 127)))
print("has CR:", b.count(b"\r"))
