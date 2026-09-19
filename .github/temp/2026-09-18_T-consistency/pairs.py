ls=open(r"A34\S34\new\S34_34s_e_eP.ens","r",encoding="utf-8",errors="replace").read().splitlines()
for i,l in enumerate(ls):
    if len(l)>7 and l[5]==" " and l[7]=="L":
        nxt=[ls[j].rstrip() for j in range(i+1,min(i+6,len(ls))) if len(ls[j])>7 and ls[j][6]=="c" and ls[j][5]==" "]
        print("L%3d | %s  <== %s"%(i+1,l[9:20].rstrip(), nxt[0][9:] if nxt else "(none)"))
