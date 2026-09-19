p=r"A34\S34\new\S34_adopted.ens"
ls=open(p,"r",encoding="utf-8",errors="replace").read().split("\r\n")
rng=[(960,1000),(1055,1100),(1140,1160),(1220,1285),(1340,1360),(1540,1560),(1735,1800),(1800,1825),(1845,1925)]
for a,b in rng:
    print("=== %d-%d"%(a,b))
    for i in range(a-1,min(b,len(ls))):
        print(i+1,"|",ls[i].rstrip())
