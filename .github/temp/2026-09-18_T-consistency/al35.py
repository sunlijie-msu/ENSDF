ls=open(r"A34\A35\Al35\new\Al35_adopted.ens","r",encoding="utf-8",errors="replace").read().splitlines() if False else open(r"A35\Al35\new\Al35_adopted.ens","r",encoding="utf-8",errors="replace").read().splitlines()
idx=[i for i,l in enumerate(ls) if "B(M1)" in l]
print(idx)
for i in idx:
    for j in range(max(0,i-8),min(len(ls),i+5)):
        print(j+1,"|",ls[j].rstrip())
    print("-----")
