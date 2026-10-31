import re, math
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
        cur=dict(line=i,E=v,DE=u or 0.0,J=l[22:39].strip(),x="",xl=None,x2=[]); adt.append(cur)
    elif cur and l[5]=="X" and l[7]=="L":
        if cur["xl"] is None: cur["xl"]=i
        cur["x2"].append(l[9:80].strip())
        cur["x"]+=re.sub(r"^XREF(\+=|=)(.*)$",r"\2",l[9:80].strip())

print("=== malformed XREF strings (non-letter chars outside parentheses) ===")
for v in adt:
    for raw in v["x2"]:
        body=re.sub(r"^XREF(\+=|=)","",raw).strip()
        stripped=re.sub(r"\([^)]*\)","",body)
        bad=[c for c in stripped if not (c.isalpha())]
        if bad: print(f"  L{v['line']}/{v['xl']} E={v['E']:g}: {raw!r}  bad chars {bad}")

print("\n=== (*) label present on only ONE adopted level ===")
from collections import Counter
labs=Counter()
for v in adt:
    for m in re.finditer(r"([A-Za-z#])\(([^)]*\*[^)]*)\)", v["x"]): labs[m.group(0)]+=1
for k,n in sorted(labs.items()):
    if n<2: print(f"  {k} appears {n}x")

DS={}
for fn,letter in MAP.items():
    lv=[]
    for i,l in enumerate(lines(BASE+NUC+"_"+fn+".ens"),1):
        v,u=eu(l[9:19],l[19:21])
        if l[5]==" " and l[6]==" " and l[7]=="L" and v is not None: lv.append((i,v,u))
    DS[letter]=lv
def tol(a,b): return max(3.0,3*math.sqrt((a or 0)**2+(b or 0)**2))

print("\n=== plain citations whose nearest dataset peak is >3 keV away (top 20 by gap) ===")
rows=[]
for v in adt:
    for m in re.finditer(r"([A-Za-z#])(?:\(([^)]*)\))?", v["x"]):
        if m.group(2): continue
        letter=m.group(1); lv=DS.get(letter)
        if not lv: continue
        p=min(lv,key=lambda t:abs(t[1]-v["E"]))
        gap=p[1]-v["E"]
        if abs(gap)>3.0 and v["E"]>1:
            rows.append((abs(gap),letter,v,p,gap))
rows.sort(reverse=True,key=lambda r:r[0])
print(f"  total: {len(rows)}")
for a,letter,v,p,gap in rows[:20]:
    print(f"  {letter}  adopted L{v['line']}/{v['xl']} {v['E']:>10g} ±{v['DE']:>6g}   dataset line {p[0]:>4} {p[1]:>8g} ±{(p[2] if p[2] is not None else 0):g}".replace("±0","±(blank)") + f"   gap={gap:+.1f}")
