import re, glob, os
from collections import defaultdict

D = r"d:/X/ND/ENSDF/XUNDL/A58/Fe58/new"
AD = D + "/Fe58_adopted.ens"
def val(s):
    s=s.strip()
    if not s: return None
    try: return float(s)
    except: return None

L = open(AD,encoding="utf-8",errors="replace").read().split("\n")
order=[]
for l in L:
    l=l.ljust(80)
    if l[5]==" " and l[6]==" " and l[7]=="X":
        order.append(l[8])

adt=[]; cur=None
for l in L:
    l=l.ljust(80)
    if l[5]==" " and l[6]==" " and l[7]=="L" and val(l[9:19]) is not None:
        cur=dict(E=val(l[9:19]),DE=val(l[19:21]) or 0,J=l[22:39].strip(),x="")
        adt.append(cur)
    elif cur and l[5]=="X" and l[7]=="L":
        cur["x"]=l[9:80].replace("XREF=","").strip()

# map letter -> list of (reported energy, adopted level index, raw label)
rep=defaultdict(list)
for i,v in enumerate(adt):
    for m in re.finditer(r"([A-Za-z])(?:\(([^)]*)\))?", v["x"]):
        ch=m.group(1); arg=m.group(2)
        e=v["E"]
        if arg:
            num=re.match(r"([\d.]+)", arg)
            if num: e=float(num.group(1))
        rep[ch].append((e, i, m.group(0)))

# dataset files -> infer letter by best exact-ish match of reported energies
files=sorted(p for p in glob.glob(D+"/*.ens") if "adopted" not in p)
dlv={}
for p in files:
    dl=[]
    for l in open(p,encoding="utf-8",errors="replace"):
        l=l.rstrip("\n").ljust(80)
        if l[5]==" " and l[6]==" " and l[7]=="L" and val(l[9:19]) is not None:
            dl.append((val(l[9:19]), val(l[19:21]) or 0))
    dlv[p]=dl

print(f"{'file':<32}{'lev':>5}{'letter':>7}{'badParen':>9}{'unmatched':>10}")
tot_bad=tot_un=0
for p in files:
    dl=dlv[p]
    best=None
    for k in order:
        en=[x[0] for x in rep[k]]
        hits=sum(1 for e,de in dl if any(abs(e-r)<=1.0 for r in en))
        f=hits/max(1,len(dl))
        if best is None or f>best[1]: best=(k,f)
    k=best[0]
    # (a) parenthetical energies in adopted that match no dataset level
    bad=[]
    for e,i,lbl in rep[k]:
        if "(" in lbl:
            if not any(abs(e-d)<=0.6 for d,de in dl): bad.append((lbl, adt[i]["E"], adt[i]["J"]))
    # (b) dataset levels not referenced by adopted under this letter
    en=[x[0] for x in rep[k]]
    un=[ (e,de) for e,de in dl if not any(abs(e-r)<=1.0 for r in en)]
    tot_bad+=len(bad); tot_un+=len(un)
    print(f"{os.path.basename(p):<32}{len(dl):>5}{k:>7}{len(bad):>9}{len(un):>10}   f={best[1]:.2f}")
    for b in bad[:8]: print(f"      XREF label {b[0]} vs adopted {b[1]} ({b[2]}) : no dataset level")
    for u in un[:8]: print(f"      dataset level {u[0]} (DE {u[1]}) not in adopted XREF")
print(f"\nTOTAL bad parentheticals={tot_bad}  unmatched dataset levels={tot_un}")
