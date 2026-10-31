import re, glob, os
from collections import defaultdict

D = r"d:/X/ND/ENSDF/XUNDL/A58/Fe58/new"
def val(s):
    s=s.strip()
    if not s: return None
    try: return float(s)
    except: return None

MAP = {
 "13c_48ca_3ng":"F","238u_64ni_xg":"d","48ca_13c_3ng":"G","54cr_6li_d":"H","55mn_a_pg":"I",
 "56fe_a_2he":"K","56fe_t_p_pol_t_p":"J","57fe_d_p_pol_d_p":"N","58fe_3he_3heP":"S",
 "58fe_a_aP":"T","58fe_d_dP_pol_d_dP":"R","58fe_e_eP":"O","58fe_n_nPg":"P","58fe_p_pP":"Q",
 "58ni_2b+_decay":"E","59co_d_3he":"Y","59co_g_p":"U","59co_mu-_ng":"V","59co_n_d":"W",
 "59co_p_2p":"X","60ni_mu-_nupng":"Z","62ni_3he_7be":"a","beta_decay_3.0_s":"A",
 "beta_decay_65.4_s":"B","coulex":"c","cu_k-_g":"b","ec_decay_70.885_d":"C",
 "ec_decay_8.853_h":"D","ng_E_th":"L","ng_n_n_resonances":"M",
}

L = open(D+"/Fe58_adopted.ens",encoding="utf-8",errors="replace").read().split("\n")
adt=[]; cur=None
for l in L:
    l=l.ljust(80)
    if l[5]==" " and l[6]==" " and l[7]=="L" and val(l[9:19]) is not None:
        cur=dict(line=None,E=val(l[9:19]),DE=val(l[19:21]) or 0,J=l[22:39].strip(),x="")
        adt.append(cur)
    elif cur and l[5]=="X" and l[7]=="L":
        cur["x"]=l[9:80].replace("XREF=","").strip()

rep=defaultdict(list)
for v in adt:
    for m in re.finditer(r"([A-Za-z])(?:\(([^)]*)\))?", v["x"]):
        ch=m.group(1); arg=m.group(2)
        e=v["E"]; amb=False
        if arg:
            num=re.match(r"([\d.]+)", arg)
            if num: e=float(num.group(1))
            if "*" in arg: amb=True
        if arg=="?": amb=True
        rep[ch].append((e, v, m.group(0), amb))

print(f"{'file':<32}{'dsl':>4}{'L':>3}{'badParen':>9}{'unmatched':>10}   worst")
T1=T2=0
for p in sorted(glob.glob(D+"/*.ens")):
    base=os.path.basename(p)[5:-4]
    if "adopted" in base: continue
    k=MAP.get(base,"?")
    dl=[]
    for l in open(p,encoding="utf-8",errors="replace"):
        l=l.rstrip("\n").ljust(80)
        if l[5]==" " and l[6]==" " and l[7]=="L" and val(l[9:19]) is not None:
            dl.append((val(l[9:19]), val(l[19:21]) or 0, l[22:39].strip()))
    bad=[]
    for e,v,lbl,amb in rep[k]:
        if amb: continue
        tol=max(3.0, v["DE"], 3.0)
        if not any(abs(e-d)<=max(tol,de) for d,de,j in dl): bad.append((lbl,v["E"],v["J"]))
    un=[]
    for d,de,j in dl:
        if not any(abs(d-e)<=max(3.0,de,v["DE"]) for e,v,lbl,amb in rep[k]): un.append((d,de,j))
    T1+=len(bad); T2+=len(un)
    print(f"{os.path.basename(p):<32}{len(dl):>4}{k:>3}{len(bad):>9}{len(un):>10}")
    for b in bad[:6]: print(f"      XREF {b[0]} (adopted {b[1]}, {b[2]}): no matching dataset level")
    for u in un[:6]: print(f"      dataset level {u[0]} (DE {u[1]}) J={u[2]!r}: not cited in adopted XREF")
print(f"\nTOTAL bad parenthetical labels={T1}   uncited dataset levels={T2}")
