import re
def lrecs(path):
    ls=open(path,"r",encoding="utf-8",errors="replace").read().splitlines()
    out=[]
    for i,l in enumerate(ls):
        if len(l)>=8 and l[5]==" " and l[6]==" " and l[7]=="L":
            out.append((i+1,l,l[9:19].strip(),l[19:21].strip()))
    return out,ls
def unc(E,DE):
    if not DE or not E: return 0.0
    try: d=len(E.split(".")[1]) if "." in E else 0
    except Exception: d=0
    try: return float(DE)*10**(-d)
    except Exception: return 0.0
def xref(ls,i):
    for j in range(i,min(i+6,len(ls))):
        l2=ls[j]
        if len(l2)>=8 and l2[5]=="X" and l2[6]==" " and l2[7]=="L": return l2[9:].strip()
        if len(l2)>=8 and l2[5]==" " and l2[6]==" " and l2[7]=="L": break
    return ""
T,tls= lrecs(r"A34\S34\new\S34_34s_e_eP.ens")
A,als= lrecs(r"A34\S34\new\S34_adopted.ens")
print("T levels:",len(T)," adopted levels:",len(A))
print("Tln    TE           DE   | Aln     AE           DE   AXREF            | verdict")
for ln,l,e,de in T:
    if not e: continue
    v=float(e); u=unc(e,de)
    cands=[(aln,ae,ade) for aln,al,ae,ade in A if ae and abs(float(ae)-v)<=max(u,unc(ae,ade))+2.0]
    if not cands:
        print("%-6d %-12s %-4s | NOMATCH"%(ln,e,de)); continue
    aln,ae,ade=min(cands,key=lambda c:abs(float(c[1])-v))
    av=float(ae); au=unc(ae,ade); xr=xref(als,aln)
    verdict = "IN-RANGE" if abs(av-v)<=au+1e-9 else "OUT->needs T(%s)"%e.rstrip("0").rstrip(".") if abs(av-v)>au else ""
    print("%-6d %-12s %-4s | %-7d %-12s %-4s %-16s | %s  dE=%s adoptedUnc=%s"%(ln,e,de,aln,ae,ade,xr,verdict,round(v-av,3),au))
