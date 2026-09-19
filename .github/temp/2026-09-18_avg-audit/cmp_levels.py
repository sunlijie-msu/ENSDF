import re, io, sys
old = open(r"A34\S34\raw\34.adp", encoding="utf-8", errors="replace").read().split("\n")
new = open(r"A34\S34\new\S34_adopted.ens", encoding="utf-8", errors="replace").read().split("\n")

def levels(ls):
    out = []
    for i,l in enumerate(ls):
        if len(l) < 20: continue
        if l[5]==" " and l[6]==" " and l[7]=="L" and l[8]==" ":
            e = l[9:19].rstrip(); de = l[19:21].rstrip()
            t = l[39:49].rstrip(); dt = l[49:55].rstrip()
            j = l[21:39].rstrip()
            out.append((e,de,j,t,dt,i+1))
    return out
o = levels(old); n = levels(new)
print("old L count", len(o), "new L count", len(n))
om = {}
for e,de,j,t,dt,i in o:
    om.setdefault(e, []).append((de,t,dt,j,i))
nm = {}
for e,de,j,t,dt,i in n:
    nm.setdefault(e, []).append((de,t,dt,j,i))
same = 0; onlyold=[]; onlynew=[]
for e in sorted(set(list(om)+list(nm)), key=lambda s: float(s)):
    if e in om and e in nm:
        same += 1
    elif e in om:
        onlyold.append((e, om[e]))
    else:
        onlynew.append((e, nm[e]))
print("matching E values:", same)
print("--- only in 34.adp:", len(onlyold))
for e,v in onlyold: print("   ", e, v)
print("--- only in new:", len(onlynew))
for e,v in onlynew: print("   ", e, v)
