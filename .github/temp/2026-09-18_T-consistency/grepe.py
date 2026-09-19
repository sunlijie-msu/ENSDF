import re
ls=open(r"A34\S34\new\S34_adopted.ens","r",encoding="utf-8",errors="replace").read().splitlines()
pat=re.compile(r"e,e",re.I)
for i,l in enumerate(ls):
    if pat.search(l):
        print(i+1,"|",l.rstrip())
