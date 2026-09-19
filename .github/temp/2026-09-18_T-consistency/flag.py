import re
ls=open(r"A34\S34\new\S34_adopted.ens","r",encoding="utf-8",errors="replace").read().splitlines()
pat=re.compile(r"B\(M|R\{-tr\}|M\{-p\}|G\{-\|a\}")
for i,l in enumerate(ls):
    if pat.search(l): print(i+1,"|",l.rstrip())
print("---- col77 flag census on L records ----")
from collections import Counter
c=Counter()
for l in ls:
    if len(l)>=77 and l[5]==" " and l[6]==" " and l[7]=="L":
        c[l[76]]+=1
print(c)
