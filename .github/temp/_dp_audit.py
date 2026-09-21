import re
p=r"d:\X\ND\ENSDF\A34\S34\new\S34_adopted.ens"
L=[l.rstrip("\n") for l in open(p,encoding="ascii")]
L=[l.ljust(80) for l in L]
hits=[]
for i,l in enumerate(L):
    if len(l)>7 and l[6]=="c" and ("|D|p=" in l or "|Dj=" in l):
        hits.append(i)
# group consecutive comment lines into blocks
blocks=[]
for i in hits:
    if blocks and i-blocks[-1][-1]==1:
        blocks[-1].append(i)
    else:
        blocks.append([i])
print("comment blocks mentioning |D|p =", len(blocks))
for b in blocks:
    # find preceding primary data record
    j=b[0]-1
    while j>=0:
        s=L[j]
        if s[5]==" " and s[7] in "LG" and s[6]==" ":
            break
        j-=1
    rec=L[j]
    print("-"*100)
    print("rec %4d |%s|"%(j+1,rec.rstrip()))
    print("   type=%s  M=col33-41=[%s]  RI=col23-29=[%s]"%(rec[7].strip(),rec[32:41],rec[22:29]))
    for i in b:
        print("c %4d |%s|"%(i+1,L[i].rstrip()))
