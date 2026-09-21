import glob, os
files=[]
for f in glob.glob(r"**\*.ens", recursive=True):
    if "\\temp\\" in f: continue
    try: t=open(f,encoding="ascii",errors="replace").read()
    except: continue
    if "|D|p=" in t: files.append(f)
print(len(files),"files with |D|p=")
for f in files:
    L=open(f,encoding="ascii",errors="replace").read().split("\n")
    curL=None; curG=None; block=[]; owner=None; rows=[]
    def flush(block,owner):
        if block and owner and "|D|p=" in " ".join(block):
            rows.append((owner,list(block)))
    for i,ln in enumerate(L):
        ln=ln.rstrip("\r")
        if len(ln)<7: continue
        cont=ln[5]!=" "; iscom=ln[6]=="c"
        if iscom:
            if not cont: flush(block,owner); block=[ln[7:].strip()]; owner=("G",curG) if curG else ("L",curL)
            else: block.append(ln[7:].strip())
            continue
        if ln[6]==" " and ln[7:8] in ("L","G"):
            flush(block,owner); owner=None; block=[]
            if ln[7]=="L": curL=(i+1,ln[9:19].strip()); curG=None
            else: curG=(i+1,ln[9:19].strip(),ln[22:29].strip(),ln[32:41].strip())
    flush(block,owner)
    for owner,blk in rows:
        txt=" ".join(blk)
        if owner[0]=="G":
            gid,ge,ri,m = owner[1]; M=m.strip()
        else:
            gid,ge,M = owner[1][0],"(L)",""
        firm = M and not (M.startswith("(") or M.startswith("["))
        rul = "RUL" in txt; pol="POL" in txt
        flag = "  <<< FIRM" if firm and not rul and not pol else ""
        if firm or rul or pol:
            print("%-38s L%-6s E=%-11s M=%-14s RUL=%-5s POL=%-5s%s | %s" % (os.path.basename(f),gid,ge,M,rul,pol,flag,txt[:110]))
