ls=open(r"A34\S34\new\S34_34s_e_eP.ens","r",encoding="utf-8",errors="replace").read().splitlines()
for i,l in enumerate(ls):
    if len(l)>7 and l[6]=="c" and l[5]!=" ":
        print("%3d | %s"%(i+1,l.rstrip()))
    elif len(l)>7 and l[6]=="c":
        print("%3d | %s"%(i+1,l.rstrip()))
