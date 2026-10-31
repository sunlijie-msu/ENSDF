import re, math
D = r"d:/X/ND/ENSDF/XUNDL/A58/Co58/new/"
MAP = {"56fe_a_d":"G","58fe_p_n_p_ng":"K","58fe_3he_t":"L","59co_3he_a":"R"}
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

ORPH = [("56fe_a_d",18,"G"),("56fe_a_d",23,"G"),("56fe_a_d",31,"G"),
        ("58fe_p_n_p_ng",100,"K"),("58fe_p_n_p_ng",101,"K"),
        ("58fe_3he_t",13,"L"),
        ("59co_3he_a",17,"R"),("59co_3he_a",22,"R"),("59co_3he_a",28,"R"),
        ("59co_3he_a",31,"R"),("59co_3he_a",56,"R")]
for fn,ln,letter in ORPH:
    d=lines(D+"Co58_"+fn+".ens")[ln-1]
    v,u=eu(d[9:19],d[19:21])
    print(f"\n{fn}:{ln}  E={v:g} ± {u if u is not None else 'no DE'}  J={d[22:39].strip()!r}")
    near=sorted(adt,key=lambda a:abs(a["E"]-v))[:3]
    for a in near:
        has = letter in re.sub(r"\([^)]*\)","",a["x"])
        m = re.search(letter + r"\([^)]*\)", a["x"])
        tag = ("YES " + m.group(0)) if m else ("YES plain") if has else "no"
        print(f"   nearest adopted L{a['line']}/{a['xl']} E={a['E']:g} ± {a['DE']:g} gap={v-a['E']:+.1f}  cites {letter}? {tag}  XREF={a['x']}")
