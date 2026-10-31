P = r"d:/X/ND/ENSDF/XUNDL/A58/Co58/new/Co58_adopted.ens"
L = [l.ljust(80) for l in open(P, encoding="utf-8", errors="replace").read().split("\n")]
for n in [5, 143, 257, 399, 443, 466, 481, 487, 507, 512, 526, 545, 548, 634, 715, 854, 861, 985, 994, 1008, 1009, 1010, 1011]:
    l = L[n - 1]
    print(f"{n:>5} {l}")
    print(f"      nonspace cols: {[i+1 for i,c in enumerate(l) if c.strip()][:20]}")
