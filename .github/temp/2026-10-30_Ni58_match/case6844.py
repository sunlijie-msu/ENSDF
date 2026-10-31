def L(p): return [l.rstrip("\n").ljust(80) for l in open(p, encoding="utf-8", errors="replace")]
DIR = r"XUNDL/A58/Ni58/new/"
C  = L(DIR + "Ni58_58ni_p_pP_pol_p_pP_p_pPg.ens")
AD = L(DIR + "Ni58_adopted.ens")

def fields(l):
    return (f"E[{l[9:19]!r}] DE[{l[19:21]!r}] c22[{l[21]!r}] J[{l[22:39]!r}] "
            f"T[{l[39:49]!r}] DT[{l[49:55]!r}] L[{l[55:64]!r}] S[{l[64:74]!r}]")

print("=== dataset C  (58Ni(p,p'),(pol p,p'),(p,p'g)) levels 6820-6880 ===")
for i, l in enumerate(C, 1):
    if l[5] == " " and l[6] == " " and l[7] == "L":
        try: v = float(l[9:19])
        except: continue
        if 6820 <= v <= 6880:
            print(f"  line {i}")
            print(f"    raw : {l.rstrip()}")
            print(f"    fld : {fields(l)}")
            for k in range(i + 1, min(i + 4, len(C))):
                if C[k-1][7] in "L" and C[k-1][5] == " ": break
                print(f"    +{k-i:<2}  : {C[k-1].rstrip()}")

print("\n=== adopted levels 6820-6880 (record + XREF + comments) ===")
lv = [i for i, l in enumerate(AD, 1) if l[5] == " " and l[6] == " " and l[7] == "L"]
for k, i in enumerate(lv):
    l = AD[i-1]
    try: v = float(l[9:19])
    except: continue
    if 6820 <= v <= 6880:
        end = lv[k+1] if k + 1 < len(lv) else len(AD)
        print(f"  level record line {i}")
        print(f"    raw : {l.rstrip()}")
        print(f"    fld : {fields(l)}")
        for n in range(i + 1, min(i + 4, end)):
            if AD[n-1][7] == "G" and AD[n-1][5] == " ": break
            print(f"    +{n-i:<2}  : {AD[n-1].rstrip()}")
