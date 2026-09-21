import glob, os
files = sorted(glob.glob(r"A34\*\new\*_adopted.ens"))
for f in files:
    if "S34" not in f: continue
    L=open(f,encoding="ascii",errors="replace").read().split("\n")
    curL=None; curG=None; block=[]; owner=None
    rows=[]
    def flush(block,owner,rows):
        if block and owner:
            txt=" ".join(block)
            if "|D|p=" in txt: rows.append((owner,list(block)))
    for i,ln in enumerate(L):
        ln = ln.rstrip("\n")
        if len(ln)<7: continue
        cont = ln[5]!=" "; iscom = ln[6]=="c"
        if iscom:
            if not cont:
                flush(block,owner,rows); block=[ln[7:].strip()]; owner=("G",curG) if curG else ("L",curL)
            else: block.append(ln[7:].strip())
            continue
        if ln[6]==" " and ln[7:8] in ("L","G"):
            flush(block,owner,rows); owner=None
            if ln[7]=="L": curL=(i+1,ln[9:19].strip(),ln[22:39].strip()); curG=None
            else: curG=(i+1,ln[9:19].strip(),ln[32:41].strip())
    flush(block,owner,rows)
    print("="*20, os.path.basename(f), len(rows))
    for owner,block in rows:
        tag=owner[0]
        if tag=="G":
            gid,ge,gm = owner[1]
            print("  G@%-5s E=%-9s M=%-14s | %s" % (gid,ge,gm.strip()," ".join(block)))
        else:
            print("  L@%-5s %s | %s" % (owner[1][0] if isinstance(owner[1],tuple) else owner[1], "", " ".join(block)))
