import os
f=r"A34\S34\new\S34_adopted.ens"
L=open(f,encoding="ascii",errors="replace").read().split("\n")
curG=None; block=[]; out=[]
def flush(curG,block,out):
    if curG and block:
        txt=" ".join(block)
        if "M$" in txt or "M,MR$" in txt or "M(A)$" in txt or "M(P)$" in txt:
            out.append((curG,txt))
for i,ln in enumerate(L):
    ln=ln.rstrip("\n")
    if len(ln)<7: continue
    cont=ln[5]!=" "; iscom=ln[6]=="c"
    if iscom:
        if not cont: flush(curG,block,out); block=[ln[7:].strip()]
        else: block.append(ln[7:].strip())
        continue
    if ln[6]==" " and ln[7:8] in ("G","L"):
        flush(curG,block,out); block=[]
        curG = (i+1, ln[9:19].strip(), ln[22:29].strip(), ln[32:41].strip()) if ln[7]=="G" else None
flush(curG,block,out)
print(len(out),"G M-comments")
for (gid,ge,ri,m),txt in out:
    firm = not (m.startswith("(") or m.startswith("["))
    hasrul = "RUL" in txt
    print("G@%-5s E=%-9s M=%-14s firm=%-5s RUL=%-5s %s" % (gid,ge,m.strip(),firm,hasrul,txt[:120]))
