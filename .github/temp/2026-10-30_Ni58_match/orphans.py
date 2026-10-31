import re, math
from collections import defaultdict
NUC="Ni58"; BASE=r"d:/X/ND/ENSDF/XUNDL/A58/Ni58/new/"
MAP={"ec_decay_3.204_s":"A","59zn_ecp_decay_178.6_ms":"W","9be_74kr_58nig":"#","28si_36ar_a2pg":"T",
"59cu_p_decay_mixed":"Y","40ca_24mg_a2pg":"U","45sc_16o_p2ng":"R","48ti_12c_2ng":"S","54fe_6li_d":"K",
"54fe_7li_t":"L","54fe_12c_8be":"M","54fe_16o_12c":"N","56fe_3he_n":"O","56fe_a_2ng":"P",
"58ni_g_gP_pol_g_gP":"E","58ni_e_eP":"F","58ni_n_nP_n_nPg":"B","58ni_p_pP_pol_p_pP_p_pPg":"C",
"58ni_d_dP":"I","58ni_3he_3heP":"H","58ni_a_aP":"D","58ni_6li_6liP":"X","coulex":"J","60ni_p_t":"G",
"ni_k-_xg":"Z","58ni_16o_16oP":"V","58ni_18o_18oP":"Q","4he_58ni_4heP_58ni_4he":"j"}
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
def cites(letter):
    out=[]
    for v in adt:
        for m in re.finditer(r"([A-Za-z#])(?:\(([^)]*)\))?", v["x"]):
            if m.group(1)!=letter: continue
            arg=m.group(2); e=v["E"]
            if arg:
                n=re.match(r"[\d.]+",arg)
                if n: e=float(n.group(0))
            out.append((v,e,m.group(0)))
    return out
def tol(a,b): return max(3.0,3*math.sqrt(a*a+b*b))
DS={}
for fn,letter in MAP.items():
    lv=[]
    for i,l in enumerate(lines(BASE+NUC+"_"+fn+".ens"),1):
        v,u=eu(l[9:19],l[19:21])
        if l[5]==" " and l[6]==" " and l[7]=="L" and v is not None: lv.append((i,v,u))
    DS[letter]=(fn,lv)

print("### 2) dataset peaks with NO citation that matches their own energy")
tot=0
for letter,(fn,lv) in sorted(DS.items(),key=lambda kv:kv[0]):
    cit=cites(letter); bad=[]
    for i,v,u in lv:
        if any(abs(v-e)<=tol(u or 0,av["DE"]) for av,e,l in cit): continue
        near=[(av,e,l) for av,e,l in cit if abs(v-av["E"])<=80]
        bad.append((i,v,u,near))
    if not bad: continue
    tot+=len(bad)
    print(f"\n  letter {letter} ({NUC}_{fn}.ens): {len(bad)} peak(s) without own citation")
    for i,v,u,near in bad:
        print(f"    peak line {i}: E={v:g} ± {u if u is not None else '(blank)'}")
        for av,e,l in near[:5]:
            print(f"        near adopted L{av['line']}/{av['xl']} E={av['E']:g} ± {av['DE']:g} label [{l}] (reported {e:g}) Δad={v-av['E']:+.1f}")
print(f"\n  TOTAL orphaned peaks: {tot}")
