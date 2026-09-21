p=r"d:\X\ND\ENSDF\A34\S34\new\S34_adopted.ens"
raw=open(p,encoding="ascii").read().split("\n")
L=[l.ljust(80) for l in raw]
n=len(L)
recs=[]
for i,l in enumerate(L):
    if l[5]==" " and l[6]==" " and l[7]=="G" and l[8]==" ":
        # collect following comment block
        blk=[];j=i+1
        while j<n and L[j][6] in "cd":
            if L[j][6]=="c": blk.append(L[j].rstrip())
            j+=1
        recs.append((i,l,blk))
print("G records:",len(recs))
c1=[];c2=[];c3=[];c4=[]
for i,l,blk in recs:
    m=l[32:41].strip()
    txt=" ".join(blk)
    has_paren="(" in m
    has_pol=("POL" in txt) or ("(pol" in txt)
    has_rul="RUL" in txt
    has_ls="level scheme" in txt
    if not m: continue
    if not has_paren and has_ls: c1.append((i,m,txt))
    if not has_paren and (("D+Q" in txt) or ("D(+Q)" in txt)) and not has_rul: c2.append((i,m,txt))
    if has_paren and not blk: c3.append((i,m,txt))
    if has_paren and blk and not (has_rul or has_ls or has_pol): c4.append((i,m,txt))
def dump(name,lst):
    print("\n### %s : %d"%(name,len(lst)))
    for i,m,txt in lst:
        print("  rec%5d M=[%-9s] %s"%(i+1,m,txt[:130]))
dump("C1 firm M + comment cites level scheme",c1)
dump("C2 firm M, D+Q comment, no RUL",c2)
dump("C3 parenthesized M, no comment",c3)
dump("C4 parenthesized M, comment lacks RUL/level-scheme/POL",c4)
