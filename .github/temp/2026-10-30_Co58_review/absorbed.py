import re, math
D = r"d:/X/ND/ENSDF/XUNDL/A58/Co58/new/"
MAP = {"58co_it_decay_8.853_h":"A","51v_10b_p2ng":"B","55mn_a_ng":"C","56fe_t_ng":"D",
 "56fe_3he_p":"E","56fe_3he_pg":"F","56fe_a_d":"G","57fe_p_g":"H","57fe_d_n_d_ng":"I",
 "57fe_3he_d":"J","58fe_p_n_p_ng":"K","58fe_3he_t":"L","58ni_d_2he":"M","58ni_t_3he":"N",
 "59co_n_2ng":"O","59co_p_d":"P","59co_d_t":"Q","59co_3he_a":"R","60ni_d_a_pol_d_a":"S"}
def eu(raw, de):
    raw=raw.strip(); de=de.strip()
    try: v=float(raw)
    except: return None,None
    if not de or de in ("GT","LT","LE","GE"): return v,None
    try: d=float(de)
    except: return v,None
    nd=len(raw.split(".")[1]) if "." in raw else 0
    return v, d*10**(-nd)
def lines(p): return [l.ljust(80) for l in open(p,encoding="utf-8",errors="replace").read().split("\n")]
AD=lines(D+"Co58_adopted.ens"); adt=[]; cur=None
for i,l in enumerate(AD,1):
    v,u=eu(l[9:19],l[19:21])
    if l[5]==" " and l[6]==" " and l[7]=="L" and v is not None:
        cur=dict(line=i,E=v,DE=u or 0.0,J=l[22:39].strip(),x="",xl=None,raw=None); adt.append(cur)
    elif cur and l[5]=="X" and l[7]=="L":
        if cur["xl"] is None: cur["xl"]=i
        cur["raw"]=cur["raw"] or l[9:80].rstrip()
        cur["x"]+=re.sub(r"^XREF(\+=|=)","",l[9:80].strip())

# citation list per letter
CIT={}
for letter in MAP.values():
    out=[]
    for v in adt:
        for m in re.finditer(r"([A-Za-z])(?:\(([^)]*)\))?", v["x"]):
            if m.group(1)!=letter: continue
            arg=m.group(2); e=v["E"]
            if arg:
                n=re.match(r"[\d.]+",arg)
                if n: e=float(n.group(0))
            out.append(dict(lv=v,e=e,lab=m.group(0),star=bool(arg and "*" in arg),
                            par=bool(arg)))
    CIT[letter]=out

print("=== peaks whose energy is NOT the reported energy of any citation (tight 2 keV) ===")
findings=[]
for fn,letter in sorted(MAP.items(), key=lambda kv: kv[1]):
    peaks=[]
    for i,l in enumerate(lines(D+"Co58_"+fn+".ens"),1):
        v,u=eu(l[9:19],l[19:21])
        if l[5]==" " and l[6]==" " and l[7]=="L" and v is not None: peaks.append((i,v,u))
    cit=CIT.get(letter,[])
    for i,v,u in peaks:
        if v==0: continue
        own=[c for c in cit if abs(v-c["e"])<=2.0]
        if own: continue
        near=[c for c in cit if abs(v-c["lv"]["E"])<=60]
        if not near: continue
        findings.append((letter,fn,i,v,u,near))
for letter,fn,i,v,u,near in findings:
    print(f"\n  {letter}  dataset line {i}: E={v:g} ± {u if u is not None else '(blank)'}")
    seen=set()
    for c in near:
        key=(c["lv"]["line"],c["lab"])
        if key in seen: continue
        seen.add(key)
        print(f"      adopted L{c['lv']['line']}/{c['lv']['xl']} E={c['lv']['E']:g} ± {c['lv']['DE']:g} label [{c['lab']}] → reports {c['e']:g}")
print(f"\n  total such peaks: {len(findings)}")
