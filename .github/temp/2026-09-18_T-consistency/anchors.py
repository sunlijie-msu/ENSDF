ls=open(r"A34\S34\new\S34_adopted.ens","r",encoding="utf-8",errors="replace").read().splitlines()
targets=[967,1026,1063,1093,1146,1197,1228,1263,1350,1545,1743,1768,1796,1806,1812,1852,1861,1874,1883,1889,1895,1913]
for t in targets:
    i=t-1
    print("=== block L at line %d"%t)
    j=i
    while j<len(ls) and j<i+8:
        l=ls[j]
        if j>i and len(l)>=8 and l[5]==" " and l[6]==" " and l[7]=="L": break
        print("  %4d | %s | len=%d"%(j+1,repr(l),len(l)))
        if len(l)>=8 and l[5]==" " and l[6]!="c" and l[7] in "G":
            print("      --> first G at %d"%(j+1)); break
        if l.strip()=="34S  d" or l.startswith(" 34S  d"):
            print("      --> delimiter at %d"%(j+1)); break
        j+=1
