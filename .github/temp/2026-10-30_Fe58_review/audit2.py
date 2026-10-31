import re, math
from collections import Counter, defaultdict

P = r"d:/X/ND/ENSDF/XUNDL/A58/Fe58/new/Fe58_adopted.ens"
L = open(P, encoding="utf-8", errors="replace").read().split("\n")
def g(l,a,b): return l.ljust(80)[a-1:b]
def val(s):
    s=s.strip()
    if not s: return None
    m=re.match(r"^([\d.]+)E(\d+)$",s)
    if m: return float(m.group(1))*10**int(m.group(2))
    try: return float(s)
    except: return None

levels, gammas, cur = [], [], None
for i,l in enumerate(L,1):
    rt=g(l,8,8); c6=g(l,6,6); c7=g(l,7,7)
    if rt=="L" and c7==" " and g(l,10,19).strip() and val(g(l,10,19)) is not None:
        cur=dict(line=i,E=val(g(l,10,19)),DE=val(g(l,20,21)),J=g(l,23,39).strip(),
                 T=g(l,40,49).strip(),xref="",com=[],gam=[],tail=g(l,76,80),L=g(l,56,64).strip(),
                 S=g(l,65,74).strip(),raw=l)
        levels.append(cur)
    elif cur and rt=="L" and c6=="X": cur["xref"]=g(l,10,80).replace("XREF=","").strip()
    elif cur and c7=="c" and rt=="L": cur["com"].append((i,g(l,10,80).rstrip()))
    elif rt=="G" and c7==" " and c6==" " and cur and val(g(l,10,19)) is not None:
        gg=dict(line=i,E=val(g(l,10,19)),DE=val(g(l,20,21)),RI=g(l,22,29).strip(),
                DRI=g(l,30,31).strip(),M=g(l,33,41).strip(),MR=g(l,42,49).strip(),tail=g(l,76,80),owner=cur)
        cur["gam"].append(gg); gammas.append(gg)

ES=[v["E"] for v in levels]
print("=== G. ORPHAN GAMMAS (no candidate final level) ===")
for v in levels:
    for gg in v["gam"]:
        d=v["E"]-gg["E"]
        tol=1.2+3*math.sqrt((v["DE"] or 0)**2+(gg["DE"] or 0)**2)
        cand=[e for e in ES if abs(e-d)<=tol]
        if not cand:
            near=min(ES,key=lambda e:abs(e-d))
            print(f"  L{v['line']:>5} E={v['E']:>9} J={v['J']:<9} gE={gg['E']:>8} (line {gg['line']}) -> resid {d:8.2f}; nearest level {near} (diff {d-near:+.2f}, tol {tol:.2f})")

print("\n=== H. duplicate gamma energies inside one level block ===")
for v in levels:
    c=Counter(round(gg["E"],3) for gg in v["gam"] if gg["E"] is not None)
    for k,n in c.items():
        if n>1: print(f"  L{v['line']} E={v['E']} dup gamma {k} x{n}")

print("\n=== I. levels with gammas but no RI=100 ===")
for v in levels:
    if v["gam"] and not any(gg["RI"].replace(".","").replace("0","")=="" for gg in v["gam"] if gg["RI"]):
        ris=[gg["RI"] for gg in v["gam"]]
        print(f"  L{v['line']:>5} E={v['E']:>9} J={v['J']:<9} RI={ris}")

print("\n=== J. flags / bands in L tail (cols 76-80) ===")
tail_c=Counter(v["tail"] for v in levels)
for k,n in sorted(tail_c.items()):
    print(f"  {k!r} x{n}")

print("\n=== K. band labels used ===")
band=Counter()
for v in levels:
    t=v["tail"]
    ch=[c for c in t if c.isalpha()]
    for c in ch: band[c]+=1
print("  ", dict(band))

print("\n=== L. footnote/flag definitions in L/G comments ===")
defs={}
for i,l in enumerate(L,1):
    if g(l,7,7)!="c": continue
    for m in re.finditer(r"([A-Za-z]{1,4}(?:\([A-Za-z]\))?)\$", g(l,10,80)):
        sym=m.group(1)
        if sym[0].isupper() and len(sym)<=4 and sym not in defs:
            defs[sym]=(i,g(l,10,80).strip()[:70])
for k in sorted(defs): print(f"  {k:8} line {defs[k][0]:>5}: {defs[k][1]}")

print("\n=== M. XREF letters used vs X-record dataset keys ===")
keys=[]
for l in L:
    if g(l,8,8)=="X" and g(l,9,9)==" " and g(l,6,6)==" ":
        keys.append((g(l,10,11), g(l,13,74).strip()[:58]))
print("  dataset keys:", [k for k,_ in keys])
used=Counter()
for v in levels:
    for ch in re.findall(r"[A-Za-z](?=[^A-Za-z]|$)", v["xref"]):
        used[ch]+=1
kv={k for k,_ in keys}
print("  letters used but NOT defined as dataset:", sorted(set(used)-kv))
print("  datasets defined but never referenced   :", sorted(kv-set(used)))
star=[v for v in levels if "*" in v["xref"]]
print("  levels with (*) or (energy*):")
for v in star: print(f"     L{v['line']:>5} E={v['E']:<9} XREF={v['xref']}")
paren=[v for v in levels if "(" in v["xref"] and "*" not in v["xref"]]
print("  levels with letter(energy) or (?):")
for v in paren: print(f"     L{v['line']:>5} E={v['E']:<9} XREF={v['xref']}")
