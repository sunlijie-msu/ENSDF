import re, glob, os, math
from collections import Counter, defaultdict

D = r"d:/X/ND/ENSDF/XUNDL/A58/Co58/new"
MAP = {"58co_it_decay_8.853_h":"A","51v_10b_p2ng":"B","55mn_a_ng":"C","56fe_t_ng":"D",
 "56fe_3he_p":"E","56fe_3he_pg":"F","56fe_a_d":"G","57fe_p_g":"H","57fe_d_n_d_ng":"I",
 "57fe_3he_d":"J","58fe_p_n_p_ng":"K","58fe_3he_t":"L","58ni_d_2he":"M","58ni_t_3he":"N",
 "59co_n_2ng":"O","59co_p_d":"P","59co_d_t":"Q","59co_3he_a":"R","60ni_d_a_pol_d_a":"S"}

def val(s):
    s=s.strip()
    try: return float(s)
    except: return None

def levels(p):
    out=[]
    for i,l in enumerate(open(p,encoding="utf-8",errors="replace"),1):
        l=l.rstrip("\n").ljust(80)
        if l[5]==" " and l[6]==" " and l[7]=="L" and val(l[9:19]) is not None:
            out.append((val(l[9:19]), val(l[19:21]) or 0, l[22:39].strip(), i))
    return out

print(f"{'file':<30}{'L':>4}{'ds':>3}{'Econs':>7}{'unmatched':>10}")
files=sorted(p for p in glob.glob(D+"/*.ens") if "adopted" not in p)
for p in files:
    base=os.path.basename(p)[5:-4]
    k=MAP.get(base,"?")
    dl=levels(p)
    # adopted xref reported energies for this letter
    AL=[l.rstrip("\n").ljust(80) for l in open(D+"/Co58_adopted.ens",encoding="utf-8",errors="replace")]
    adt=[]; cur=None
    for l in AL:
        if l[5]==" " and l[6]==" " and l[7]=="L" and val(l[9:19]) is not None:
            cur=dict(E=val(l[9:19]),DE=val(l[19:21]) or 0,x=""); adt.append(cur)
        elif cur and l[5]=="X" and l[7]=="L":
            t=re.sub(r"^XREF(\+=|=)","",l[9:80].strip()); cur["x"]+=t
    rep=[]
    for v in adt:
        for m in re.finditer(r"([A-Za-z])(?:\(([^)]*)\))?", v["x"]):
            if m.group(1)!=k: continue
            arg=m.group(2); e=v["E"]
            if arg and re.match(r"[\d.]+", arg): e=float(re.match(r"[\d.]+",arg).group(0))
            rep.append((e, v["E"], v["DE"], "(" in m.group(0)))
    un=[(d,de,i) for d,de,j,i in dl if not any(abs(d-r[0])<=max(3.0, de, r[2]) for r in rep)]
    print(f"{os.path.basename(p):<30}{len(dl):>4}{k:>3}{len(un):>10}")
    for u in un[:6]: print(f"      level {u[0]} (DE {u[1]}) line {u[2]} not cited in adopted XREF {k}")
print("\n(adopted: Egamma>Elevel list already reported)")
