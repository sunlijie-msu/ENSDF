import re
ls=open(r"A34\S34\new\S34_adopted.ens","r",encoding="utf-8",errors="replace").read().splitlines()
n=0
for i,l in enumerate(ls):
    if len(l)>=8 and l[5]=="X" and l[6]==" " and l[7]=="L":
        if "(" in l:
            n+=1
            print(i+1,"|",l.rstrip())
print("parenthetical XREF lines:",n)
