a=open(r"A34\S34\new\S34_adopted.ens","r",encoding="utf-8",errors="replace").read().splitlines()
for i,l in enumerate(a):
    if "B(M1)|^=0.11" in l or "R{-tr}" in l: print(i+1,len(l),"|%s|"%l)
print("--- global E(E),J(E) comment")
for i,l in enumerate(a):
    if "e,e" in l and i<60: print(i+1,len(l),"|%s|"%l)
