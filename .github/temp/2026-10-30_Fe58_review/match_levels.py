import re, glob, os
from collections import defaultdict

D = r"d:/X/ND/ENSDF/XUNDL/A58/Fe58/new"
AD = D + "/Fe58_adopted.ens"
def g(l,a,b): return l.ljust(80)[a-1:b]
def val(s):
    s=s.strip()
    if not s: return None
    try: return float(s)
    except: return None

L = open(AD,encoding="utf-8",errors="replace").read().split("\n")
# dataset letter -> description from X records
order=[]
keys={}
for l in L:
    l=l.ljust(80)
    if l[5]==" " and l[6]==" " and l[7]=="X":
        k=l[8]
        keys[k]="/".join(l[10:60].split()[:2])
        order.append(k)
print("dataset letters:", "".join(order))

adt=[]; cur=None
for l in L:
    l=l.ljust(80)
    if l[5]==" " and l[6]==" " and l[7]=="L" and val(l[9:19]) is not None:
        cur=dict(E=val(l[9:19]),DE=val(l[19:21]) or 0,J=l[22:39].strip(),x="")
        adt.append(cur)
    elif cur and l[5]=="X" and l[7]=="L":
        cur["x"]=l[9:80].replace("XREF=","").strip()

letter_energies=defaultdict(list)
for v in adt:
    for ch in re.findall(r"[A-Za-z](?:\([^)]*\))?", v["x"]):
        letter_energies[ch[0]].append((v["E"], v["DE"], ch, v["J"]))

files = sorted(p for p in glob.glob(D+"/*.ens") if "adopted" not in p)
print(f"\n{'dataset file':<32}{'levels':>7}{'noXREFletter':>13}{'unmatched':>10}  worst")
for p in files:
    # infer letter from X-record description match
    base=os.path.basename(p)[6:-4].upper()
    dl=[]; c=None
    for l in open(p,encoding="utf-8",errors="replace"):
        l=l.rstrip("\n").ljust(80)
        if l[5]==" " and l[6]==" " and l[7]=="L" and val(l[9:19]) is not None:
            c=dict(E=val(l[9:19]),DE=val(l[19:21]) or 0)
            dl.append(c)
    # find letter: adopted levels whose xref letter list best covers dl energies
    best=None
    for k in order:
        en=[x[0] for x in letter_energies[k]]
        hits=sum(1 for v in dl if any(abs(v["E"]-e)<=5 for e in en))
        frac=hits/max(1,len(dl))
        if best is None or frac>best[1]: best=(k,frac,hits)
    k,frac,hits=best
    en=[(x[0],x[1],x[2],x[3]) for x in letter_energies[k]]
    unmatched=[]
    for v in dl:
        tol=max(3.0,3*v["DE"])
        cand=[e for e in en if abs(e[0]-v["E"])<=tol]
        if not cand: unmatched.append(v["E"])
    print(f"{os.path.basename(p):<32}{len(dl):>7}{0:>13}{len(unmatched):>10}  letter={k} frac={frac:.2f}")
    if unmatched: print("      unmatched dataset levels:", unmatched[:12])
