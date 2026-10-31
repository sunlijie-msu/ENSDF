import re, glob, os
from collections import Counter, defaultdict

D = r"d:/X/ND/ENSDF/XUNDL/A58/Co58/new"
def val(s):
    s=s.strip()
    try: return float(s)
    except: return None

P=D+"/Co58_adopted.ens"
L=[l.ljust(80) for l in open(P,encoding="utf-8",errors="replace").read().split("\n")]
lv=[]; cur=None
for i,l in enumerate(L,1):
    if l[5]==" " and l[6]==" " and l[7]=="L" and val(l[9:19]) is not None:
        cur=dict(line=i,E=val(l[9:19]),DE=val(l[19:21]),J=l[22:39].strip(),
                 c77=l[76],ms=l[77:79],q=l[79],xref="",gam=[],com=[])
        lv.append(cur)
    elif cur and l[5]=="X" and l[7]=="L":
        t=l[9:80]
        t=re.sub(r"^XREF(\+=|=)","",t.strip())
        cur["xref"]=(cur["xref"]+t).strip()
    elif cur and l[6]=="c" and l[7]=="L":
        cur["com"].append((i,l[9:80].rstrip()))
    elif cur and l[5]==" " and l[6]==" " and l[7]=="G" and val(l[9:19]) is not None:
        cur["gam"].append(dict(line=i,E=val(l[9:19]),RI=l[21:29].strip(),M=l[32:41].strip(),
                               c77=l[76],c78=l[77],c79=l[78],q=l[79]))
gams=[x for v in lv for x in v["gam"]]

print("=== A. col-77 letters: L=band labels, G=footnote flags ===")
bands_def=set(); flags_def=set()
for i,l in enumerate(L,1):
    if l[6]!="c": continue
    t=l[9:80].strip()
    for m in re.finditer(r"^BAND\(([A-Za-z])\)\$", t): bands_def.add(m.group(1))
    for m in re.finditer(r"(?:^|[ ,;])([A-Za-z]{1,4})\(([A-Za-z])\)\$", t): flags_def.add(m.group(2))
bused=Counter(v["c77"] for v in lv if v["c77"].strip())
fused=Counter(x["c77"] for x in gams if x["c77"].strip())
print("  bands defined:", sorted(bands_def), " used on L:", dict(sorted(bused.items())))
print("  L bands used but undefined:", sorted(set(bused)-bands_def))
print("  footnote flags defined:", sorted(flags_def), " used on G:", dict(sorted(fused.items())))
print("  G flags used but undefined:", sorted(set(fused)-flags_def))
print("  note: '*' '&' '@' are intrinsic, excluded")

print("\n=== B. L-record MS field (cols 78-79) ===")
for v in lv:
    if v["ms"].strip():
        print(f"  L{v['line']} E={v['E']} J={v['J']} col77={v['c77']!r} MS={v['ms']!r} col80={v['q']!r}")

print("\n=== C. XREF after merging continuations ===")
for v in lv:
    x=v["xref"]
    if not x: continue
    if " " in x: print(f"  SPACE L{v['line']} E={v['E']}: {x!r}")
    letters=re.findall(r"[A-Za-z]", re.sub(r"\([^)]*\)","",x))
    if len(letters)!=len(set(letters)): print(f"  DUPL  L{v['line']} E={v['E']}: {x!r}")
    order=[(ord(c)-65) if c.isupper() else 100+ord(c)-97 for c in letters]
    if order!=sorted(order): print(f"  ORDER L{v['line']} E={v['E']}: {x!r}")

print("\n=== D. (*) ambiguity must appear on >=2 levels ===")
amb=defaultdict(list)
for v in lv:
    for m in re.finditer(r"([A-Za-z])\(([^)]*\*[^)]*)\)", v["xref"]):
        amb[m.group(0)].append(v["E"])
for k,es in sorted(amb.items()):
    if len(es)<2: print(f"  {k} appears on only 1 level: {es}")

print("\n=== E. Q record char map ===")
q=L[4]
for a,b in [(10,19),(20,21),(22,29),(30,31),(32,39),(40,41),(42,49),(50,51),(52,59),(60,61),(62,79)]:
    print(f"   {a:>2}-{b:<2} {q[a-1:b]!r}")

print("\n=== F. X-record order ===")
keys=[l[8] for l in L if l[5]==" " and l[6]==" " and l[7]=="X"]
print("  ", "".join(keys))
print("  sorted?", "".join(keys)=="".join(sorted(keys,key=lambda c:(c.islower(),c))))
