import re, math, os, glob
from collections import Counter

D = r"d:/X/ND/ENSDF/XUNDL/A58/Fe58/new"
def g(l,a,b): return l.ljust(80)[a-1:b]
def val(s):
    s=s.strip()
    if not s: return None
    m=re.match(r"^([\d.]+)E([+-]?\d+)$",s)
    if m: return float(m.group(1))*10**int(m.group(2))
    try: return float(s)
    except: return None

def parse(p):
    L=open(p,encoding="utf-8",errors="replace").read().split("\n")
    lv=[]; cur=None
    for i,l in enumerate(L,1):
        l=l.ljust(80)
        if l[5]==" " and l[6]==" " and l[7]=="L" and val(l[9:19]) is not None:
            cur=dict(line=i,E=val(l[9:19]),DE=val(l[19:21]),J=l[22:39].strip(),gam=[],xref="")
            lv.append(cur)
        elif cur and l[7]=="L" and l[5]=="X":
            cur["xref"]=l[9:80].replace("XREF=","").strip()
        elif cur and l[5]==" " and l[6]==" " and l[7]=="G" and val(l[9:19]) is not None:
            cur["gam"].append(dict(line=i,E=val(l[9:19]),DE=val(l[19:21]),
                                   RI=l[21:29].strip(),DRI=l[29:31].strip(),M=l[32:41].strip()))
    return L,lv

print(f"{'file':<32}{'lev':>5}{'gam':>5}{'Econs':>7}{'order':>7}{'dupG':>6}{'noRI100':>9}{'bigDRI':>7}")
allv=[]
for p in sorted(glob.glob(D+"/*.ens")):
    L,lv=parse(p)
    econs=[]; order=[]; dup=[]; nori=[]; baddri=[]
    prev=None
    for v in lv:
        if prev is not None and v["E"]<prev-1e-9: order.append(("level",v["line"],prev,v["E"]))
        prev=v["E"]
        pe=None
        for gg in v["gam"]:
            if gg["E"]>v["E"]+1e-9: econs.append((v["line"],v["E"],v["J"],gg["line"],gg["E"]))
            if pe is not None and gg["E"]<pe-1e-9: order.append(("gamma",gg["line"],pe,gg["E"]))
            pe=gg["E"]
            if gg["DRI"] and gg["DRI"] not in ("GT","LT","LE","GE") and not gg["DRI"].strip().isdigit():
                baddri.append((gg["line"],gg["DRI"],gg["RI"]))
        es=Counter(round(x["E"],3) for x in v["gam"])
        dup += [(v["line"],k,n) for k,n in es.items() if n>1]
        if len(v["gam"])>1 and not any(x["RI"].startswith("100") for x in v["gam"]): nori.append(v["line"])
    name=os.path.basename(p)
    print(f"{name:<32}{len(lv):>5}{sum(len(v['gam']) for v in lv):>5}{len(econs):>7}{len(order):>7}{len(dup):>6}{len(nori):>9}{len(baddri):>7}")
    for tag,items in (("E>Lev",econs),("ORD",order),("DUP",dup),("noRI100",nori),("badDRI",baddri)):
        for it in items[:6]:
            print(f"     {tag}: {it}")
