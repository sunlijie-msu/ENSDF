import os
base=r"d:\X\ND\ENSDF"
files=[r"A34\S34\new\S34_adopted.ens",r"A34\Si34\new\Si34_adopted.ens",r"A34\P34\new\P34_adopted.ens",r"A34\Cl34\new\Cl34_adopted.ens",r"A34\Ar34\new\Ar34_adopted.ens"]
for f in files:
    p=os.path.join(base,f)
    L=[l.ljust(80) for l in open(p,encoding="ascii").read().split("\n")]
    print("="*110); print(f,"lines=",len(L))
    for i,l in enumerate(L):
        if l[5]==" " and l[6]=="c" and "|D|p=" in l:
            j=i-1
            while j>=0:
                if L[j][5]==" " and L[j][6]==" ":
                    break
                j-=1
            r=L[j]; t=r[7]
            print("  rec%5d %s %-6s E=[%s] M=[%s] %s" % (j+1,t,r[1:6].strip(),r[9:19].strip(),r[32:41],("PAREN" if r[32:41].strip().startswith("(") else ("EMPTY" if r[32:41].strip()=="" else "*** FLAT ***"))))
            # print following comment block
            k=i
            while k<len(L) and ((L[k][5]==" " and L[k][6]=="c") or (L[k][5]!=" " and L[k][6]=="c")):
                print("        | "+L[k].rstrip()[8:])
                k+=1
