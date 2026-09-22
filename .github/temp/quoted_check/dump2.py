p = r"d:\X\ND\ENSDF\A34\S34\new\S34_adopted.ens"
lines = open(p, "rb").read().decode("ascii").split("\r\n")
for n in list(range(405, 433)) + [475, 476, 512, 513]:
    l = lines[n - 1]
    print(f"{n:4d} len={len(l):3d}: {l}")
