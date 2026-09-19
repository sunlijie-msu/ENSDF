ls=open(r"A34\S34\raw\34.adp","r",encoding="utf-8",errors="replace").read().splitlines()
for i in range(1855,1920):
    print(i+1,"|",ls[i].rstrip()[:100])
