import re
p=r"d:\X\ND\ENSDF\A34\S34\new\S34_adopted.ens"
raw=open(p,encoding="ascii").read().split("\n")
L=[l.ljust(80) for l in raw]
def rec_before(i):
    j=i-1
    while j>=0:
        s=L[j]
        if s[6]=="c" or s[6]=="d":
            j-=1; continue
        if s[5]==" " and s[7] in "LGEBDP":
            return j
        j-=1
    return None
idx=[i for i,l in enumerate(L) if l[6]=="c" and "level scheme" in l]
print("total comment lines with 'level scheme':",len(idx))
# group into blocks of consecutive comment lines
blocks=[]
for i in idx:
    if blocks and i-blocks[-1][-1]<=2 and all(L[k][6] in "cd" for k in range(blocks[-1][-1]+1,i)):
        blocks[-1].append(i)
    else:
        blocks.append([i])
print("blocks:",len(blocks))
for b in blocks:
    r=rec_before(b[0])
    rec=L[r]
    m=rec[32:41]
    par = "(" in m
    tag = "OK " if ("|D|p=" in "".join(L[i] for i in b))==par or ("|D|p=" not in "".join(L[i] for i in b)) else "MISMATCH"
    print("-"*95)
    print("rec%5d [%s] M=[%s] parens=%s %s"%(r+1,rec[7].strip(),m,par, "PAREN-OK" if par else "NO-PAREN"))
    for i in b:
        print("  c%5d %s"%(i+1,L[i].rstrip()))
