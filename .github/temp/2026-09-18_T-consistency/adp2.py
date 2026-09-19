ls=open(r"A34\S34\raw\34.adp","r",encoding="utf-8",errors="replace").read().splitlines()
import re
n=0
for i,l in enumerate(ls):
    if "BE2=" in l or "B(M1)" in l or "B(M2)" in l or "e,e" in l.lower():
        n+=1
        if n<=15: print(i+1,"|",l.rstrip()[:110])
print("total hits:",n)
