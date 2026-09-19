a=open(r"A34\S34\new\S34_adopted.ens","r",encoding="utf-8",errors="replace").read().splitlines()
def find(e,j0=0):
    for i in range(j0,len(a)):
        l=a[i]
        if len(l)>7 and l[5]==" " and l[7]=="L" and l[9:19].strip()==e: return i
    return -1
for e,n in [("10662",5),("12460",5),("13790",5),("14430",5),("9479",8),("9868",8),("10803",8),("10179.59",6)]:
    i=find(e); print("### %s (L at %d)"%(e,i+1))
    for j in range(i,i+n): print("   %d|%s|"%(j+1,a[j].rstrip()))
