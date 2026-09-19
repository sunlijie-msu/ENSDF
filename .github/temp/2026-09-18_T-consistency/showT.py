ls=open(r"A34\S34\new\S34_34s_e_eP.ens","r",encoding="utf-8",errors="replace").read().splitlines()
for i,l in enumerate(ls):
    print("%3d|%s| len=%d"%(i+1,l[:12]+"..." if False else l.rstrip(),len(l)))
