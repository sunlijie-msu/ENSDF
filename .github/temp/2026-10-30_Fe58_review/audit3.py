import re
from collections import Counter, defaultdict

P = r"d:/X/ND/ENSDF/XUNDL/A58/Fe58/new/Fe58_adopted.ens"
L = open(P, encoding="utf-8", errors="replace").read().split("\n")
def g(l,a,b): return l.ljust(80)[a-1:b]

print("=== X records (repr of cols 1-30) ===")
for i,l in enumerate(L,1):
    if g(l,8,8)=="X":
        print(f"  {i:>4}: col8={g(l,8,8)} col9={g(l,9,9)!r} cols10-12={g(l,10,12)!r} cols13-20={g(l,13,20)!r} | {l[5:40]!r}")

print("\n=== flag letters used at col 77 / 78-79 / FLAG= ===")
c77=Counter(); c7879=Counter(); flag_eq=Counter()
for l in L:
    if g(l,7,7)==" " and g(l,8,8) in "LG" and g(l,6,6) in (" ",) :
        if g(l,77,77).strip(): c77[g(l,77,77)]+=1
        if g(l,78,79).strip(): c7879[g(l,78,79).strip()]+=1
    if "FLAG=" in l:
        flag_eq[l.split("FLAG=")[1].strip()]+=1
print("  col77 :", dict(c77))
print("  col78-79:", dict(c7879))
print("  FLAG= :", dict(flag_eq))

print("\n=== flag/band definition lines ===")
pat=re.compile(r"(?:^|[ ,;])([A-Za-z]{1,3}(?:\([A-Za-z]\))?|BAND [A-Za-z]|BAND\([A-Za-z]\))\$")
defs=set()
for i,l in enumerate(L,1):
    if g(l,7,7)!="c": continue
    t=g(l,10,80)
    if "BAND" in t or "$" in t:
        m=pat.search(t)
        if m:
            defs.add(m.group(1))
            print(f"  {i:>4}: {t.strip()[:76]}")

print("\n  defined:", sorted(defs))
used=set(c77)|set(k for k in flag_eq)
print("  used at col77/FLAG=:", sorted(used))
print("  used but not defined:", sorted(u for u in used if u not in defs and "BAND" not in u))

print("\n=== XREF format: embedded spaces / duplicate letters / letter order ===")
for i,l in enumerate(L,1):
    if g(l,6,6)=="X" and g(l,8,8)=="L":
        x=g(l,10,80).replace("XREF=","").rstrip()
        if " " in x: print(f"  SPACE  line {i}: {x!r}")
        letters=re.findall(r"[A-Za-z]", re.sub(r"\([^)]*\)","",x))
        if len(letters)!=len(set(letters)): print(f"  DUP    line {i}: {x!r}")
        order=[ (ord(c)-ord('A')) if c.isupper() else (100+ord(c)-ord('a')) for c in letters]
        if order!=sorted(order): print(f"  ORDER  line {i}: {x!r}")

print("\n=== comment identifier order within L block (expect E,J,T,S then general) ===")
rank={"E":0,"J":1,"T":2,"S":3}
cur=None
for i,l in enumerate(L,1):
    if g(l,8,8)=="L" and g(l,7,7)==" ":
        cur=(i,g(l,10,19).strip()); seq=[]
    elif cur and g(l,7,7)=="c" and g(l,8,8)=="L":
        t=g(l,10,80)
        m=re.match(r"^([A-Za-z]{1,3}(?:\([A-Za-z]\))?)\$",t)
        if m and m.group(1)[0] in rank:
            seq.append((rank[m.group(1)[0]], m.group(1), i))
    elif cur and g(l,8,8)=="G" and g(l,7,7)==" ":
        r=[s[0] for s in seq]
        if r!=sorted(r):
            print(f"  L{cur[0]} E={cur[1]}: order {[ (s[1],s[2]) for s in seq]}")
