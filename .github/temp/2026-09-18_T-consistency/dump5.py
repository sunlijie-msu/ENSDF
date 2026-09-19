ls=open(r"A34\S34\new\S34_adopted.ens","r",encoding="utf-8",errors="replace").read().splitlines()
for i in range(1744,1835): print(i+1,"|",ls[i].rstrip())
