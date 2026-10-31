import re
D=r"d:/X/ND/ENSDF/XUNDL/A58/Ni58/new/"
def lines(p): return [l.ljust(80) for l in open(p,encoding="utf-8",errors="replace").read().split("\n")]
AD=lines(D+"Ni58_adopted.ens")
# where does each label appear?
labs=["C(6474)","C(6844)","C(7590*)","C(7590)","C(9463)","C(9635)","C(11062)"]
for lab in labs:
    hits=[(i,l[9:80].rstrip()) for i,l in enumerate(AD,1) if l[5]=="X" and l[7]=="L" and lab in l[9:80]]
    print(f"{lab:>10} appears on {len(hits)} XREF line(s):")
    for i,t in hits: print(f"      :{i}  {t}")
# dataset C peaks near those energies
print("\ndataset C (58ni_p_pP_pol_p_pP_p_pPg) peaks near each label energy:")
P=[]
for i,l in enumerate(lines(D+"Ni58_58ni_p_pP_pol_p_pP_p_pPg.ens"),1):
    raw=l[9:19].strip(); de=l[19:21].strip()
    try: v=float(raw)
    except: continue
    if l[5]==" " and l[6]==" " and l[7]=="L": P.append((i,v,de))
for target in (6474,6844,7590,7618,9463,9635,11062):
    near=[p for p in P if abs(p[1]-target)<=25]
    print(f"   target {target}: {[(p[0],p[1],p[2]) for p in near]}")
