import re, glob, os, math
from collections import Counter, defaultdict

D = r"d:/X/ND/ENSDF/XUNDL/A58/Co58/new"
def g(l,a,b): return l.ljust(80)[a-1:b]
def val(s):
    s=s.strip()
    if not s: return None
    m=re.match(r"^([\d.]+)E([+-]?\d+)$",s)
    if m: return float(m.group(1))*10**int(m.group(2))
    try: return float(s)
    except: return None

def parse(p, need_xref=False):
    L=open(p,encoding="utf-8",errors="replace").read().split("\n")
    lv=[]; cur=None; com=[]
    for i,l in enumerate(L,1):
        l=l.ljust(80)
        ct=l[5]; c7=l[6]; rt=l[7]
        if ct==" " and c7==" " and rt=="L" and val(l[9:19]) is not None:
            cur=dict(line=i,E=val(l[9:19]),DE=val(l[19:21]),J=l[22:39].strip(),
                     T=l[39:49].strip(),DT=l[49:55].strip(),L=l[55:64].strip(),
                     S=l[64:74].strip(),DS=l[74:76].strip(),c77=l[76],ms=l[77:79],q=l[79],
                     gam=[],xref="",com=[])
            lv.append(cur)
        elif cur and ct=="X" and rt=="L": cur["xref"]=l[9:80].replace("XREF=","").strip()
        elif cur and c7=="c" and rt=="L": cur["com"].append((i,l[9:80].rstrip()))
        elif cur and ct==" " and c7==" " and rt=="G" and val(l[9:19]) is not None:
            cur["gam"].append(dict(line=i,E=val(l[9:19]),DE=val(l[19:21]),RI=l[21:29].strip(),
                DRI=l[29:31],M=l[32:41].strip(),MR=l[41:49].strip(),DMR=l[49:55].strip(),
                CC=l[55:62].strip(),DCC=l[62:64].strip(),TI=l[64:74].strip(),DTI=l[74:76].strip(),
                c77=l[76],c78=l[77],c79=l[78],q=l[79],com=[]))
        elif cur and cur["gam"] and c7=="c" and rt=="G":
            cur["gam"][-1]["com"].append((i,l[9:80].rstrip()))
    return L,lv

P = D+"/Co58_adopted.ens"
L,lv = parse(P)
gams=[x for v in lv for x in v["gam"]]
print(f"levels={len(lv)} gammas={len(gams)}")

print("\n=== 1. gamma energy > level energy ===")
for v in lv:
    for x in v["gam"]:
        if x["E"]>v["E"]+1e-9:
            se=math.hypot(v["DE"] or 0, x["DE"] or 0)
            print(f"  L{v['line']} E={v['E']} J={v['J']} DE={v['DE']}  ->  G{x['line']} E={x['E']} DE={x['DE']}  (+{x['E']-v['E']:.3f} keV, {(x['E']-v['E'])/max(se,1e-6):.1f} sigma)")

print("\n=== 2. duplicate gamma energy in same level block ===")
for v in lv:
    c=Counter(round(x["E"],3) for x in v["gam"])
    for k,n in c.items():
        if n>1: print(f"  L{v['line']} E={v['E']}: gamma {k} x{n}")

print("\n=== 3. duplicate comment identifiers ===")
for v in lv:
    c=Counter()
    for i,t in v["com"]:
        m=re.match(r"^([A-Za-z]{1,3}(?:,[A-Za-z]{1,3})*)\$",t)
        if m:
            for part in m.group(1).split(","): c[part]+=1
    for k,n in c.items():
        if n>1: print(f"  L block {v['line']} (E={v['E']}): {k}$ x{n}")
for v in lv:
    for x in v["gam"]:
        c=Counter()
        for i,t in x["com"]:
            m=re.match(r"^([A-Za-z]{1,3}(?:,[A-Za-z]{1,3})*)\$",t)
            if m:
                for part in m.group(1).split(","): c[part]+=1
        for k,n in c.items():
            if n>1: print(f"  G block {x['line']} (E={x['E']}): {k}$ x{n}")

print("\n=== 4. field-position distributions ===")
for name,items,lo,hi in (("J start col",lv,21,38),("RI start col",gams,21,30),("M start col",gams,31,40)):
    c=Counter()
    for o in items:
        s=o[{"J start col":"J","RI start col":"RI","M start col":"M"}[name]] or ""
        pass
    # recompute from raw lines
print("  J:", dict(sorted(Counter(next(k for k in range(21,39) if L[v['line']-1].ljust(80)[k]!=' ')+1 for v in lv if v["J"]).items())))
print("  RI:", dict(sorted(Counter(next((k for k in range(21,30) if L[x['line']-1].ljust(80)[k]!=' '),99)+1 for x in gams if x["RI"]).items())))
print("  M:", dict(sorted(Counter(next((k for k in range(31,41) if L[x['line']-1].ljust(80)[k]!=' '),99)+1 for x in gams if x["M"]).items())))

print("\n=== 5. flag / indicator legality (per skill) ===")
bad77=[]; bad78=[]; bad79=[]; bad80=[]
for o in lv+gams:
    rt = "L" if o in lv else "G"
    if o["c77"].strip() and o["c77"] not in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz*&@":
        bad77.append((rt,o["line"],o["c77"]))
    if rt=="G":
        if o["c78"].strip() not in ("","C"): bad78.append((o["line"],o["c78"]))
        if o["c79"].strip() not in ("","N"): bad79.append((o["line"],o["c79"]))
    if o["q"].strip() not in ("","?","S"): bad80.append((rt,o["line"],o["q"]))
print("  col77 illegal :", bad77)
print("  G col78 illegal:", bad78)
print("  G col79 illegal:", bad79)
print("  col80 illegal :", bad80)

print("\n=== 6. flags used vs defined (letters only) ===")
defs=set()
for i,l in enumerate(L,1):
    l=l.ljust(80)
    if l[6]!="c": continue
    for m in re.finditer(r"(?:^|[ ,;])([A-Za-z]{1,3})\(([A-Za-z])\)\$", l[9:80]):
        defs.add(m.group(2))
used=Counter()
for o in lv+gams:
    if o["c77"].strip() and o["c77"].isalpha(): used[o["c77"]]+=1
print("  defined flags:", sorted(defs))
print("  used letter flags:", dict(sorted(used.items())))
print("  USED BUT UNDEFINED:", sorted(set(used)-defs))
print("  defined but unused:", sorted(defs-set(used)))

print("\n=== 7. XREF checks ===")
for v in lv:
    x=v["xref"]
    if not x: continue
    if " " in x: print(f"  SPACE  L{v['line']} E={v['E']}: {x!r}")
    letters=re.findall(r"[A-Za-z]", re.sub(r"\([^)]*\)","",x))
    if len(letters)!=len(set(letters)): print(f"  DUP    L{v['line']} E={v['E']}: {x!r}")
    order=[(ord(c)-65) if c.isupper() else 100+ord(c)-97 for c in letters]
    if order!=sorted(order): print(f"  ORDER  L{v['line']} E={v['E']}: {x!r}")

print("\n=== 8. RI blank / no RI=100 ===")
for v in lv:
    if v["gam"]:
        if len(v["gam"])>1 and not any(x["RI"].startswith("100") for x in v["gam"]):
            print(f"  no RI=100  L{v['line']} E={v['E']} J={v['J']} RI={[x['RI'] for x in v['gam']]}")
        for x in v["gam"]:
            if not x["RI"]: print(f"  blank RI   G{x['line']} E={x['E']} (level {v['E']})")
