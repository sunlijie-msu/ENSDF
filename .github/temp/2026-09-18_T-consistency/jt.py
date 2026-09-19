ls=open(r"A34\S34\new\S34_34s_e_eP.ens","r",encoding="utf-8",errors="replace").read().splitlines()
print("--- T dataset L fields ---")
for i,l in enumerate(ls):
    if len(l)>7 and l[5]==" " and l[7]=="L":
        print("%3d | E=%-9s DE=%-2s | J=%-12s | T=%-8s DT=%-4s | C=%s"%(i+1,l[9:19].strip(),l[19:21].strip(),l[22:39].strip(),l[39:49].strip(),l[49:55].strip(),l[76]))
print()
print("--- adopted global E(E),J(E) comment (lines 28-40) ---")
a=open(r"A34\S34\new\S34_adopted.ens","r",encoding="utf-8",errors="replace").read().splitlines()
for j in range(26,42):
    print("%4d | %s"%(j+1,a[j].rstrip()))
