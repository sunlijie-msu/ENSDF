import re
from collections import Counter, defaultdict

def load(p):
    return open(p, encoding="utf-8", errors="replace").read().split("\n")

FILES = {
 "Fe58_adopted": r"d:/X/ND/ENSDF/XUNDL/A58/Fe58/new/Fe58_adopted.ens",
 "Ni58_adopted": r"d:/X/ND/ENSDF/XUNDL/A58/Ni58/new/Ni58_adopted.ens",
 "A60_13NDS":    r"d:/X/ND/ENSDF/A60/A60_13NDS.ens",
}
def g(l,a,b): return l.ljust(80)[a-1:b]

for name, p in FILES.items():
    try: L = load(p)
    except FileNotFoundError:
        print(name, "missing"); continue
    ri, jj = Counter(), Counter()
    for l in L:
        if g(l,8,8)=="G" and g(l,6,6)==" " and g(l,7,7)==" " and g(l,10,19).strip():
            s = l.ljust(80)
            k = 21
            while k < 31 and s[k]==" ": k+=1
            if s[k:k+2] not in ("GT","LT","LE","GE") and k < 31: ri[k+1]+=1
        if g(l,8,8)=="L" and g(l,7,7)==" " and g(l,10,19).strip():
            s=l.ljust(80); k=21
            while k<39 and s[k]==" ": k+=1
            if k<39: jj[k+1]+=1
    print(f"{name}: RI start col {dict(ri)}   J start col {dict(jj)}")
