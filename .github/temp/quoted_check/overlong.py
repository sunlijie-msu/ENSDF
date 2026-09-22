p = r"d:\X\ND\ENSDF\A34\S34\new\S34_adopted.ens"
lines = open(p, "rb").read().decode("ascii").split("\r\n")
over = [(i + 1, len(l)) for i, l in enumerate(lines) if len(l) > 80]
print("lines > 80 chars:", len(over))
print(over[:40])
for n in range(427, 432):
    l = lines[n - 1]
    print(f"{n:4d} len={len(l)}: {l}")
