p=r"A34\S34\new\S34_adopted.ens"
raw=open(p,"rb").read()
print("len",len(raw),"CRLF",raw.count(b"\r\n"),"LF",raw.count(b"\n"))
ls=raw.decode("utf-8",errors="replace").splitlines()
print("lines",len(ls))
rng=[(960,1000),(1055,1100),(1140,1160),(1220,1285)]
for a,b in rng:
    print("=== %d-%d"%(a,b))
    for i in range(a-1,min(b,len(ls))):
        print(i+1,"|",ls[i].rstrip())
