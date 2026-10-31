import re, math
from collections import defaultdict
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
        cur=dict(line=i,E=v,DE=u or 0.0,J=l[22:39].strip(),x="",xl=None); adt.append(cur)
    elif cur and l[5]=="X" and l[7]=="L":
        if cur["xl"] is None: cur["xl"]=i
        cur["x"]+=re.sub(r"^XREF(\+=|=)","",l[9:80].strip())

def citations(letter):
    out=[]
    for v in adt:
        for m in re.finditer(r"([A-Za-z])(?:\(([^)]*)\))?", v["x"]):
            if m.group(1)!=letter: continue
            arg=m.group(2); e=v["E"]
            if arg:
                num=re.match(r"[\d.]+",arg)
                if num: e=float(num.group(0))
            out.append((v,e,m.group(0)))
    return out

def tol_of(a,b): return max(3.0, 3*math.sqrt(a*a+b*b))

print("== levels whose own energy has NO citation with matching reported energy ==")
for fn,letter in sorted(MAP.items(), key=lambda kv: kv[1]):
    DL=lines(D+"Co58_"+fn+".ens"); cit=citations(letter); bad=[]
    for i,l in enumerate(DL,1):
        v,u=eu(l[9:19],l[19:21])
        if not(l[5]==" " and l[6]==" " and l[7]=="L" and v is not None): continue
        u=u or 0.0
        own=[(av,e,lab) for av,e,lab in cit if abs(v-e)<=tol_of(u,av["DE"])]
        if own: continue
        near=[(av,e,lab) for av,e,lab in cit if abs(v-av["E"])<=tol_of(u,av["DE"])]
        bad.append((i,v,u,near))
    if not bad: continue
    print(f"\n  letter {letter} ({fn}): {len(bad)} dataset level(s) without own citation")
    for i,v,u,near in bad[:6]:
        print(f"    dataset line {i}: E={v:g} ± {u:g}")
        if near:
            for av,e,lab in near:
                print(f"        overlaps adopted L{av['line']}/{av['xl']} E={av['E']:g} ± {av['DE']:g}  which cites {letter} as [{lab}]")
        else:
            print("        no adopted level overlaps at all")
