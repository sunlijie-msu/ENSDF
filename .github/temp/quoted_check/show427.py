TMP = r"d:\X\ND\ENSDF\.github\temp\quoted_check"
sim = open(TMP + r"\simulated.ens", "rb").read().decode("ascii").split("\r\n")
orig = open(r"d:\X\ND\ENSDF\A34\S34\new\S34_adopted.ens", "rb").read().decode("ascii").split("\r\n")
print("=== ORIGINAL 425..462")
for n in range(425, 463):
    print(f"{n:4d}|{orig[n-1][:80]}")
print("=== SIMULATED 425..470")
for n in range(425, 471):
    print(f"{n:4d}|{sim[n-1][:80]}")
