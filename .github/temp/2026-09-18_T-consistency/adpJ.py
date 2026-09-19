a=open(r"A34\S34\raw\34.adp","r",encoding="utf-8",errors="replace").read().splitlines()
for i,l in enumerate(a):
    if len(l)>7 and l[5]==" " and l[7]=="L" and any(str(e) in l[9:19] for e in ("10662","12460","12930","14200","14320","14430","12180","13590","13790","14800","13990","11020")):
        print("%4d | %s"%(i+1,l.rstrip()))
print("--- adopted current J for those ---")
b=open(r"A34\S34\new\S34_adopted.ens","r",encoding="utf-8",errors="replace").read().splitlines()
for i,l in enumerate(b):
    if len(l)>7 and l[5]==" " and l[7]=="L" and any(str(e) in l[9:19] for e in ("10662","12460","12930","14200","14320","14430","12180","13590","13790","14800","13990","11020")):
        print("%4d | %s"%(i+1,l.rstrip()))
