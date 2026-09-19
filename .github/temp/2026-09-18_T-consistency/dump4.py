ls=open(r"A34\S34\new\S34_adopted.ens","r",encoding="utf-8",errors="replace").read().splitlines()
for a,b in [(1005,1030),(1190,1200),(1345,1355),(1540,1550)]:
    print("=== %d-%d"%(a,b))
    for i in range(a-1,b): print(i+1,"|",ls[i].rstrip())
