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
AD=lines(BASE+NUC+"_adopted.ens")

# g.s. XREF
for i,l in enumerate(AD,1):
    if l[5]==" " and l[6]==" " and l[7]=="L" and l[9:19].strip() in ("0.0","0"):
        print("g.s. L",i,repr(l[9:19]),"XREF line",i+1); gs=i
        break
gsx=re.sub(r"^XREF(\+=|=)","",AD[gs][9:80].strip())
print("g.s. XREF =",gsx)
have=set(re.findall(r"[A-Za-z#]",gsx))
zero=[]
for fn,letter in MAP.items():
    for i,l in enumerate(lines(BASE+NUC+"_"+fn+".ens"),1):
        v,u=eu(l[9:19],l[19:21])
        if l[5]==" " and l[6]==" " and l[7]=="L" and v is not None and v==0:
            zero.append((letter,fn,i)); break
print("datasets listing a 0 level:",[z[0] for z in zero])
print("letters MISSING from g.s. XREF:",[z[0] for z in zero if z[0] not in have])

# coverage probe for C and F windows
adt=[]; cur=None
for i,l in enumerate(AD,1):
    v,u=eu(l[9:19],l[19:21])
    if l[5]==" " and l[6]==" " and l[7]=="L" and v is not None:
        cur=dict(line=i,E=v,DE=u or 0.0,x="",xl=None); adt.append(cur)
    elif cur and l[5]=="X" and l[7]=="L":
        if cur["xl"] is None: cur["xl"]=i
        cur["x"]+=re.sub(r"^XREF(\+=|=)","",l[9:80].strip())
def probe(letter,lo,hi):
    fn=[k for k,v in MAP.items() if v==letter][0]
    print(f"\n--- letter {letter} ({fn}) window {lo}-{hi} ---")
    print("  dataset peaks:")
    for i,l in enumerate(lines(BASE+NUC+"_"+fn+".ens"),1):
        v,u=eu(l[9:19],l[19:21])
        if l[5]==" " and l[6]==" " and l[7]=="L" and v is not None and lo<=v<=hi:
            print(f"    line {i}: {v:g} ± {u if u is not None else '(blank)'}")
    print("  adopted levels citing it:")
    for v in adt:
        for m in re.finditer(r"([A-Za-z#])(?:\(([^)]*)\))?", v["x"]):
            if m.group(1)!=letter: continue
            e=v["E"]
            if m.group(2):
                n=re.match(r"[\d.]+",m.group(2))
                if n: e=float(n.group(0))
            if lo-40<=e<=hi+40:
                print(f"    L{v['line']}/{v['xl']}: E={v['E']:g} ± {v['DE']:g} label [{m.group(0)}] → reported {e:g}")
probe("F",10300,10700)
probe("C",10280,10700)
probe("F",9200,9400)
