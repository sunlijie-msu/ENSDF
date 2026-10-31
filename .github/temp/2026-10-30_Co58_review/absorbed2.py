import re, math
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

def audit(base, nuc, MAP, exact=2.0):
    AD=lines(base+nuc+"_adopted.ens"); adt=[]; cur=None
    for i,l in enumerate(AD,1):
        v,u=eu(l[9:19],l[19:21])
        if l[5]==" " and l[6]==" " and l[7]=="L" and v is not None:
            cur=dict(line=i,E=v,DE=u or 0.0,x="",xl=None,segs=[]); adt.append(cur)
        elif cur and l[5]=="X" and l[7]=="L":
            if cur["xl"] is None: cur["xl"]=i
            cur["segs"].append(l[9:80].rstrip())
            cur["x"]+=re.sub(r"^XREF(\+=|=)","",l[9:80].strip())
    out=[]
    for fn,letter in sorted(MAP.items(), key=lambda kv: kv[1]):
        peaks=[]
        for i,l in enumerate(lines(base+nuc+"_"+fn+".ens"),1):
            v,u=eu(l[9:19],l[19:21])
            if l[5]==" " and l[6]==" " and l[7]=="L" and v is not None: peaks.append((i,v,u))
        for i,p,pu in peaks:
            if p==0: continue
            for v in adt:
                if abs(v["E"]-p)>exact: continue
                for m in re.finditer(r"([A-Za-z#])(?:\(([^)]*)\))?", v["x"]):
                    if m.group(1)!=letter or not m.group(2): continue
                    n=re.match(r"[\d.]+",m.group(2))
                    if not n: continue
                    e=float(n.group(0))
                    if abs(e-p)>exact:
                        out.append(dict(letter=letter,fn=fn,pline=i,p=p,pu=pu,
                                        av=v,lab=m.group(0),e=e))
    return out

CO = {"58co_it_decay_8.853_h":"A","51v_10b_p2ng":"B","55mn_a_ng":"C","56fe_t_ng":"D",
 "56fe_3he_p":"E","56fe_3he_pg":"F","56fe_a_d":"G","57fe_p_g":"H","57fe_d_n_d_ng":"I",
 "57fe_3he_d":"J","58fe_p_n_p_ng":"K","58fe_3he_t":"L","58ni_d_2he":"M","58ni_t_3he":"N",
 "59co_n_2ng":"O","59co_p_d":"P","59co_d_t":"Q","59co_3he_a":"R","60ni_d_a_pol_d_a":"S"}
NI = {"ec_decay_3.204_s":"A","59zn_ecp_decay_178.6_ms":"W","9be_74kr_58nig":"#","28si_36ar_a2pg":"T",
"59cu_p_decay_mixed":"Y","40ca_24mg_a2pg":"U","45sc_16o_p2ng":"R","48ti_12c_2ng":"S","54fe_6li_d":"K",
"54fe_7li_t":"L","54fe_12c_8be":"M","54fe_16o_12c":"N","56fe_3he_n":"O","56fe_a_2ng":"P",
"58ni_g_gP_pol_g_gP":"E","58ni_e_eP":"F","58ni_n_nP_n_nPg":"B","58ni_p_pP_pol_p_pP_p_pPg":"C",
"58ni_d_dP":"I","58ni_3he_3heP":"H","58ni_a_aP":"D","58ni_6li_6liP":"X","coulex":"J","60ni_p_t":"G",
"ni_k-_xg":"Z","58ni_16o_16oP":"V","58ni_18o_18oP":"Q","4he_58ni_4heP_58ni_4he":"j"}
for nuc,base,MAP in (("Co58",r"d:/X/ND/ENSDF/XUNDL/A58/Co58/new/",CO),
                     ("Ni58",r"d:/X/ND/ENSDF/XUNDL/A58/Ni58/new/",NI)):
    res=audit(base,nuc,MAP)
    print(f"\n########## {nuc}: dataset peak sits on an adopted level whose own label names a DIFFERENT energy ##########")
    print(f"  count = {len(res)}")
    for r in res:
        print(f"  {r['letter']}  dataset[{r['fn']}:{r['pline']}] = {r['p']:g} ± {r['pu'] if r['pu'] is not None else '(blank)'}")
        print(f"      adopted L{r['av']['line']}/{r['av']['xl']} = {r['av']['E']:g} ± {r['av']['DE']:g}  label [{r['lab']}] names {r['e']:g}   Δpeak={r['p']-r['e']:+.1f}  Δadopted={r['p']-r['av']['E']:+.1f}")
        print(f"      raw: {r['av']['segs'][0]}")
