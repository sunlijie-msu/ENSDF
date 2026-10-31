P = r"d:/X/ND/ENSDF/XUNDL/A58/Co58/new/Co58_adopted.ens"
L = open(P, encoding="utf-8", errors="replace").read().split("\n")
for a, b in [(1004, 1014), (508, 516), (540, 552), (470, 480), (528, 538), (968, 980), (130, 155)]:
    print(f"--- lines {a}-{b} ---")
    for n in range(a, b + 1):
        print(n, repr(L[n - 1]))
