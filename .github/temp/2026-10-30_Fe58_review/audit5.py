import re
P = r"d:/X/ND/ENSDF/XUNDL/A58/Fe58/new/Fe58_adopted.ens"
L = open(P,encoding="utf-8",errors="replace").read().split("\n")
def g(l,a,b): return l.ljust(80)[a-1:b]

print("=== duplicate identifiers within one G comment block ===")
block=[]; start=None
def flush():
    global block,start
    if not block: return
    ids=[]
    for i,t in block:
        m=re.match(r"^([A-Za-z]{1,3}(?:,[A-Za-z]{1,3})*)\$", t)
        ids.append((m.group(1) if m else "general", i))
    seen={}
    for k,i in ids:
        if k!="general":
            for part in k.split(","):
                if part in seen:
                    print(f"  G block at line {start}: identifier {part}$ twice (lines {seen[part]} and {i})")
                seen[part]=i
    block=[]; start=None

prevG=None
for i,l in enumerate(L,1):
    l=l.ljust(80)
    rt=l[7]; c7=l[6]; c6=l[5]
    if c7==" " and rt=="G" and c6==" ":
        flush(); prevG=i
    elif c7=="c" and rt=="G":
        if start is None: start=i
        block.append((i,l[9:80].rstrip()))
    elif c7=="c" and rt=="L":
        flush(); prevG=None
flush()

print("\n=== notation / typo suspects ===")
pats = [r"\|J=", r"from ,", r"\|\|", r"the the", r"\bof of\b", r"with with", r"\)was", r"\|g\) \.", r"\bJ\|p=", r"\bkeV level\.", r" {3,}\$", r":[ ]*$", r"\bmetastable\b"]
for i,l in enumerate(L,1):
    l=l.ljust(80)
    if l[6]!="c": continue
    t=l[9:80].rstrip()
    for p in pats:
        if re.search(p,t):
            print(f"  {i:>5} [{p}] {t[:74]}")
            break
