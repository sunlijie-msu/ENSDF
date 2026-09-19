old = open(r"A34\S34\raw\34.adp", encoding="utf-8", errors="replace").read().split("\n")
new = open(r"A34\S34\new\S34_adopted.ens", encoding="utf-8", errors="replace").read().split("\n")
def levels(ls):
    out = {}
    for i,l in enumerate(ls):
        if len(l) < 20: continue
        if l[5]==" " and l[6]==" " and l[7]=="L" and l[8]==" ":
            out[l[9:19].rstrip()] = (l[19:21].rstrip(), l[21:39].rstrip(), l[39:49].rstrip(), l[49:55].rstrip(), i+1)
    return out
o = levels(old); n = levels(new)
print(f"{'E':>11} {'adp DE/J/T/DT':<34} {'new DE/J/T/DT':<34}")
cnt=0
for e in sorted(set(o)&set(n), key=lambda s: float(s)):
    a = o[e]; b = n[e]
    if a[:4] != b[:4]:
        cnt+=1
        print(f"{e:>11} {str(a[:4]):<34} {str(b[:4]):<34}")
print("changed rows:", cnt)
