ls=open(r"A34\S34\raw\34.mrg","r",encoding="utf-8",errors="replace").read().splitlines()
idx=[i for i,l in enumerate(ls) if "B(M1)" in l or "B(M2)" in l]
print("idx",idx[:6],"...total",len(idx))
for i in idx[:4]:
    for j in range(max(0,i-10),min(len(ls),i+4)): print(j+1,"|",ls[j].rstrip()[:110])
    print("-----")
