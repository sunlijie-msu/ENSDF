import re, math
D = r"d:/X/ND/ENSDF/XUNDL/A58/Co58/new/"
MAP = {"58co_it_decay_8.853_h":"A","51v_10b_p2ng":"B","55mn_a_ng":"C","56fe_t_ng":"D",
 "56fe_3he_p":"E","56fe_3he_pg":"F","56fe_a_d":"G","57fe_p_g":"H","57fe_d_n_d_ng":"I",
 "57fe_3he_d":"J","58fe_p_n_p_ng":"K","58fe_3he_t":"L","58ni_d_2he":"M","58ni_t_3he":"N",
 "59co_n_2ng":"O","59co_p_d":"P","59co_d_t":"Q","59co_3he_a":"R","60ni_d_a_pol_d_a":"S"}
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
AD=lines(D+"Co58_adopted.ens"); adt=[]; cur=None
for i,l in enumerate(AD,1):
    v,u=eu(l[9:19],l[19:21])
    if l[5]==" " and l[6]==" " and l[7]=="L" and v is not None:
        cur=dict(line=i,E=v,DE=u or 0.0,J=l[22:39].strip(),x="",xl=None); adt.append(cur)
    elif cur and l[5]=="X" and l[7]=="L":
        if cur["xl"] is None: cur["xl"]=i
        cur["x"]+=re.sub(r"^XREF(\+=|=)","",l[9:80].strip())

DS={}
for fn,letter in MAP.items():
    lv=[]
    for i,l in enumerate(lines(D+"Co58_"+fn+".ens"),1):
        v,u=eu(l[9:19],l[19:21])
        if l[5]==" " and l[6]==" " and l[7]=="L" and v is not None: lv.append((i,v,u))
    DS[letter]=lv

rows=[]
for v in adt:
    for m in re.finditer(r"([A-Za-z])(?:\(([^)]*)\))?", v["x"]):
        letter=m.group(1); arg=m.group(2)
        if arg: continue                      # only plain citations
        lv=DS.get(letter)
        if not lv: continue
        near=min(lv,key=lambda t:abs(t[1]-v["E"]))
        gap=near[1]-v["E"]
        if abs(gap)>3.0:
            rows.append((abs(gap),letter,v,near,gap))
rows.sort(reverse=True,key=lambda r:r[0])
print(f"plain-letter citations whose dataset level sits >3 keV away: {len(rows)}\n")
print(f"{'letter':>6} {'adopted L/line':>16} {'adopted E ±':>16} {'dataset line':>12} {'dataset E ±':>16} {'gap':>8}")
for a,letter,v,near,gap in rows:
    du = "?" if near[2] is None else f"{near[2]:g}"
    print(f"{letter:>6} L{v['line']}/{v['xl']:<10} {v['E']:>10g} ±{v['DE']:>5g} {near[0]:>12} {near[1]:>10g} ±{du:>5} {gap:>+8.1f}")
