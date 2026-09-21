import glob,os,re
files=[r"A34\Si34\new\Si34_adopted.ens",r"A34\P34\new\P34_adopted.ens",r"A34\Cl34\new\Cl34_adopted.ens",r"A34\Ar34\new\Ar34_adopted.ens"]
base=r"d:\X\ND\ENSDF"
for f in files:
    p=os.path.join(base,f)
    raw=open(p,encoding="ascii").read().split("\n")
    L=[l.ljust(80) for l in raw]
    print("="*100); print(f)
    for i,l in enumerate(L):
        if l[6]=="c" and "|D|p=" in l:
            j=i-1
            while j>=0 and (L[j][6] in "cd" or L[j].strip()==""):
                j-=1
            rec=L[j]
            m=rec[32:41]
            ok="PAREN-OK" if m.strip().startswith("(") else "*** NO-PAREN ***"
            print("  c%5d %-72s | rec%5d M=[%s] %s"%(i+1,l.strip()[:72],j+1,m,ok))
