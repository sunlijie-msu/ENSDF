import glob, os, re, sys
files = sorted(glob.glob(r"A34\*\new\*_adopted.ens"))
rows=[]
for f in files:
    L=open(f,encoding="ascii",errors="replace").read().split("\n")
    curL=None; curG=None; block=[]; owner=None
    def flush():
        global block, owner
        if block and owner:
            txt=" ".join(block)
            if "|D|p=" in txt:
                rows.append((f,owner,list(block)))
        block=[]
    for i,ln in enumerate(L):
        ln = ln.rstrip("\n")
        if len(ln)<7: continue
        cont = ln[5]!=" "
        iscom = ln[6]=="c"
        if iscom:
            if not cont:
                flush(); block=[ln[7:].strip()]; owner=("L",curL) if curG is None else ("G",curG)
            else:
                block.append(ln[7:].strip())
            continue
        if ln[6]==" " and ln[7:8] in ("L","G","E","B","A","D"):
            flush(); owner=None
            if ln[7]=="L": curL=(i+1,ln[9:19].strip(),ln[22:39].strip()); curG=None
            if ln[7]=="G": curG=(i+1,ln[9:19].strip(),ln[22:29].strip(),ln[32:41])
        elif cont:
            pass
    flush()
print(len(rows),"clauses")
for f,owner,block in rows:
    txt=" ".join(block)
    rul = "RUL" in txt
    tag = owner[0]
    if tag=="G":
        l,en,ri,m = owner[1]
        M = m.strip()
    else:
        l = owner[1][0]; M="(LEVEL, no G)"
    print("%-24s L%-6s %s%s | M=%-14s RUL=%-5s | %s" % (os.path.basename(f), l, tag, en, M, rul, txt[:150]))
