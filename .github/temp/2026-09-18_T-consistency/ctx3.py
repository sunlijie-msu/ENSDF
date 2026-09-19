a=open(r"A34\S34\new\S34_adopted.ens","r",encoding="utf-8",errors="replace").read().splitlines()
for r in [(974,980),(1033,1040),(1232,1240),(1094,1099),(1263,1268)]:
    print("---")
    for j in range(r[0]-1,r[1]-1):
        if j<len(a): print("%5d|%s|"%(j+1,a[j].rstrip()))
