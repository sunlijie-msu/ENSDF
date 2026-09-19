a=open(r"A34\S34\new\S34_adopted.ens","r",encoding="utf-8",errors="replace").read().splitlines()
targets=["10000","10430","11350","11500","12120","12180","12660","12930","13590","13990","14200","14320","14800"]
for t in targets:
    for i,l in enumerate(a):
        if len(l)>7 and l[5]==" " and l[7]=="L" and l[9:19].strip()==t:
            print("### %s"%t)
            for j in range(i,i+4):
                print("   %d|%s|"%(j+1,a[j].rstrip()))
            break
