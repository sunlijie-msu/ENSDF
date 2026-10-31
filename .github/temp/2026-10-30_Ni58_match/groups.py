import re, math, glob, os
from collections import defaultdict

NUC = "Ni58"
BASE = r"d:/X/ND/ENSDF/XUNDL/A58/" + NUC + "/new/"
MAP = {"ec_decay_3.204_s":"A","59zn_ecp_decay_178.6_ms":"W","9be_74kr_58nig":"#",
 "28si_36ar_a2pg":"T","59cu_p_decay_mixed":"Y","40ca_24mg_a2pg":"U","45sc_16o_p2ng":"R",
 "48ti_12c_2ng":"S","54fe_6li_d":"K","54fe_7li_t":"L","54fe_12c_8be":"M","54fe_16o_12c":"N",
 "56fe_3he_n":"O","56fe_a_2ng":"P","58ni_g_gP_pol_g_gP":"E","58ni_e_eP":"F",
 "58ni_n_nP_n_nPg":"B","58ni_p_pP_pol_p_pP_p_pPg":"C","58ni_d_dP":"I","58ni_3he_3heP":"H",
 "58ni_a_aP":"D","58ni_6li_6liP":"X","coulex":"J","60ni_p_t":"G","ni_k-_xg":"Z",
 "58ni_16o_16oP":"V","58ni_18o_18oP":"Q","4he_58ni_4heP_58ni_4he":"j"}

def eu(raw,de):
    raw=raw.strip(); de=de.strip()
    try: v=float(raw)
    except: return None,None
    if not de or de in ("GT","LT","LE","GE"): return v,None
    try: d=float(de)
    except: return v,None
    nd=len(raw.split(".")[1]) if "." in raw else 0
    return v, d*10**(-nd)
def lines(p): return [l.ljust(80) for l in open(p,encoding="utf-8",errors="replace").read().split("\n")]

AD=lines(BASE+NUC+"_adopted.ens"); adt=[]; cur=None
for i,l in enumerate(AD,1):
    v,u=eu(l[9:19],l[19:21])
    if l[5]==" " and l[6]==" " and l[7]=="L" and v is not None:
        cur=dict(line=i,E=v,DE=u or 0.0,J=l[22:39].strip(),x="",xl=None); adt.append(cur)
    elif cur and l[5]=="X" and l[7]=="L":
        if cur["xl"] is None: cur["xl"]=i
        cur["x"]+=re.sub(r"^XREF(\+=|=)","",l[9:80].strip())
print(f"adopted: {len(adt)} levels")

def lab_of(v,letter):
    out=[]
    for m in re.finditer(r"([A-Za-z#])(?:\(([^)]*)\))?", v["x"]):
        if m.group(1)!=letter: continue
        arg=m.group(2); e=v["E"]
        if arg:
            num=re.match(r"[\d.]+",arg)
            if num: e=float(num.group(0))
        out.append((m.group(0), e))
    return out

DS={}
for fn,letter in MAP.items():
    lv=[]
    for i,l in enumerate(lines(BASE+NUC+"_"+fn+".ens"),1):
        v,u=eu(l[9:19],l[19:21])
        if l[5]==" " and l[6]==" " and l[7]=="L" and v is not None: lv.append((i,v,u))
    DS[letter]=lv

def tol(u,v): return max(3.0, 3*math.sqrt((u or 0)**2+(v or 0)**2))

print("\n### 1) ambiguity groups: identical parenthetical label on >=2 levels")
for letter,lv in sorted(DS.items()):
    groups=defaultdict(list)
    for v in adt:
        for lab,e in lab_of(v,letter):
            if "(" in lab: groups[lab].append((v,e))
    for lab,mem in groups.items():
        if len(mem)<2: continue
        e_rep=mem[0][1]
        win=[p for p in lv if abs(p[1]-e_rep)<=60]
        print(f"\n  {letter}: label [{lab}] repeated on {len(mem)} levels; dataset {NUC}_{[k for k,v2 in MAP.items() if v2==letter][0]} has {len(win)} peak(s) within 60 keV")
        for p in win:
            own=[v for v,e in mem if abs(p[1]-v["E"])<=tol(p[2],v["DE"])]
            print(f"     dataset line {p[0]}: E={p[1]:g} ± {p[2] if p[2] is not None else '?'}  -> exact-energy adopted levels: {[ (v['line'],v['E']) for v in own ] or 'none'}")
        for v,e in mem:
            print(f"     adopted L{v['line']}/{v['xl']}: E={v['E']:g} ± {v['DE']:g}  label [{lab}] -> reported {e:g}  Δ(adopted-peak)={v['E']-e:+.1f}")
