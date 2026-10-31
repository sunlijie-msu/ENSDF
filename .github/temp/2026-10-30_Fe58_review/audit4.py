import re
P = r"d:/X/ND/ENSDF/XUNDL/A58/Fe58/new/Fe58_adopted.ens"
L = open(P, encoding="utf-8", errors="replace").read().split("\n")
def g(l,a,b): return l.ljust(80)[a-1:b]

print("=== band/flag column positions (exact) ===")
for i,l in enumerate(L,1):
    if g(l,7,7)==" " and g(l,8,8)=="L" and g(l,6,6)==" ":
        if g(l,76,77).strip() or g(l,78,79).strip() or g(l,77,77).strip():
            print(f"  {i:>4}: cols76-80={g(l,76,80)!r}  E={g(l,10,19).strip():<9} J={g(l,23,39).strip()}")
    if "FLAG=" in l and ("&" in l or "@" in l):
        print(f"  {i:>4}: FLAG& = {l[5:60]!r}")

print("\n=== '&' and '@' occurrences ===")
for i,l in enumerate(L,1):
    if "&" in l or "@" in l:
        print(f"  {i:>4}: {l[5:80]!r}")

print("\n=== levels above S(n)=10044.57 not flagged R / with non-M xref ===")
cur=None
for i,l in enumerate(L,1):
    if g(l,8,8)=="L" and g(l,7,7)==" " and g(l,6,6)==" " and g(l,10,19).strip():
        cur=dict(i=i,E=g(l,10,19).strip(),tail=g(l,76,80),x="")
    elif cur and g(l,6,6)=="X" and g(l,8,8)=="L":
        cur["x"]=g(l,10,80).replace("XREF=","").strip()
    elif cur and g(l,8,8)=="G" and g(l,7,7)==" ":
        try: e=float(cur["E"])
        except: e=None
        if e and e>10044.57:
            letters=set(re.findall(r"[A-Za-z]", re.sub(r"\([^)]*\)","",cur["x"]))) if cur["x"] else set()
            if "R" not in cur["tail"] and letters-{"M"}:
                print(f"  L{cur['i']:>5} E={cur['E']:<10} XREF={cur['x']}")

print("\n=== RI=100 presence per level with gammas ===")
cur=None; blocks=[]
for i,l in enumerate(L,1):
    if g(l,8,8)=="L" and g(l,7,7)==" " and g(l,6,6)==" " and g(l,10,19).strip():
        cur=dict(i=i,E=g(l,10,19).strip(),J=g(l,23,39).strip(),ri=[])
        blocks.append(cur)
    elif cur and g(l,8,8)=="G" and g(l,7,7)==" " and g(l,6,6)==" ":
        cur["ri"].append((g(l,22,29).strip(), g(l,30,31).strip(), g(l,10,19).strip()))
miss=[b for b in blocks if b["ri"] and not any(r[0].startswith("100") for r in b["ri"])]
print("  blocks with gammas lacking RI=100:", len(miss))
for b in miss: print(f"   L{b['i']:>5} E={b['E']:<10} J={b['J']:<10} RI={[r[0] for r in b['ri']]}")

print("\n=== suspicious RI values (RI>1000 or DRI non-numeric) ===")
for b in blocks:
    for ri,dri,e in b["ri"]:
        if ri.replace('.','',1).isdigit() and float(ri)>1000:
            print(f"  L{b['i']:>5} E={b['E']} gamma {e}: RI={ri!r} DRI={dri!r}")
        if dri and dri not in ("GT","LT","LE","GE") and not dri.strip().isdigit():
            print(f"  L{b['i']:>5} gamma {e}: DRI={dri!r} RI={ri!r}")
