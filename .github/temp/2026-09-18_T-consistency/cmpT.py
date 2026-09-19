import re
def lrecs(path):
    ls=open(path,"r",encoding="utf-8",errors="replace").read().splitlines()
    out=[]
    for i,l in enumerate(ls):
        if len(l)>=8 and l[5]==" " and l[6]==" " and l[7]=="L":
            E=l[9:19].strip(); DE=l[19:21].strip()
            xr=""
            for j in range(i+1,min(i+6,len(ls))):
                l2=ls[j]
                if len(l2)>=8 and l2[5]=="X" and l2[6]==" " and l2[7]=="L":
                    xr=l2[9:].strip(); break
                if len(l2)>=8 and l2[7]=="L": break
            out.append((i+1,l,E,DE,xr))
    return out,ls
T,ls= lrecs(r"A34\S34\new\S34_34s_e_eP.ens")
A,als= lrecs(r"A34\S34\new\S34_adopted.ens")
def key(e):
    return float(e) if e else None
def unc(E,DE):
    if not DE: return 0.0
    if "." in E: d=len(E.split(".")[1])
    else: d=0
    return float(DE)*10**(-d)
print("T levels:",len(T))
print("%-6s %-12s %-4s | %-9s %-12s %-4s %-10s | match"%("Tln","TE","DE","Aln","AE","DE","AXREF"))
bad=[]
for ln,e,de,xr in T:
    if not e: continue
    v=float(e); u=unc(e,de)
    best=None
    for aln,ae,ade,axr in A:
        if not ae: continue
        av=float(ae); au=unc(ae,ade)
        if abs(av-v)<=max(u,au)+1e-9:
            if best is None or abs(av-v)<abs(float(best[1])-v): best=(aln,ae,ade,axr)
    if best is None:
        bad.append((ln,e,de,"NOMATCH")); print("%-6d %-12s %-4s | NO MATCH in adopted"%(ln,e,de)); continue
    aln,ae,ade,axr=best
    av=float(ae); au=unc(ae,ade)
    flag="OK" if abs(av-v)<=au+1e-9 else "OUT"
    ttag = re.search(r"T(?:\([^)]*\))?", axr)
    print("%-6d %-12s %-4s | %-9d %-12s %-4s %-10s | %s dt=%s adunc=%s"%(ln,e,de,aln,ae,ade,axr,flag,round(v-av,3),round(au,4)))
