for p in (r"A34\S34\raw\34.adp",):
    ls=open(p,"r",encoding="utf-8",errors="replace").read().splitlines()
    print(p,"lines",len(ls))
    for i,l in enumerate(ls):
        if "R{-tr}" in l or "BM1" in l or "BM2" in l or "M{-p}" in l:
            print(i+1,"|",l.rstrip()[:120])
