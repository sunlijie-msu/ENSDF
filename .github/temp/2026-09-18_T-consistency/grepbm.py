import glob,re
files=[f for f in glob.glob("A*/*/*adopted*.ens")+glob.glob("A*/*/new/*adopted*.ens") if "temp" not in f]
print(len(files),"files")
hits=0
for f in files:
    try: ls=open(f,"r",encoding="utf-8",errors="replace").read().splitlines()
    except: continue
    c=[l for l in ls if "B(M1)" in l or "B(M2)" in l]
    if c:
        hits+=1
        print("--",f,len(c))
        for l in c[:3]: print("   ",l.rstrip()[:100])
print("files with B(M) comments:",hits)
