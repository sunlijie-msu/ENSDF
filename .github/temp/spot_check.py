import random, subprocess, sys, re

JAVA_AVG = r"d:\X\ND\ENSDF\.github\scripts\Java_Average.py"
random.seed(42)

def abs_unc(e_str, de_str):
    e_str=e_str.strip(); de_str=de_str.strip()
    if not de_str or de_str in ("LT","GT"): return None
    try: de_int=int(de_str)
    except ValueError: return None
    n_dec=len(e_str.split(".")[1]) if "." in e_str else 0
    return de_int*(10**(-n_dec))

def parse_source(path):
    recs=[]
    with open(path, encoding="ascii", errors="replace") as f: lines=f.readlines()
    for line in lines:
        if len(line)>7 and line[7]=="L" and line[6]==" " and line[5]==" ":
            e=line[9:19].strip(); de=line[19:21].strip()
            if not e: continue
            try: ev=float(e)
            except ValueError: continue
            recs.append({"e_str":e,"de_str":de,"e":ev,"de_abs":abs_unc(e,de)})
    return sorted(recs,key=lambda r:r["e"])

def parse_adopted(path):
    with open(path, encoding="ascii", errors="replace") as f: lines=f.readlines()
    start=None
    for i,line in enumerate(lines):
        if len(line)>9 and line[7]=="L" and line[6]==" " and line[5]==" " and line[9:19].strip()=="7018.9":
            start=i; break
    levels=[]; cur=None; in_cl_e=False
    for line in lines[start:]:
        if len(line)<8: continue
        c6,c7,c8=line[5],line[6],line[7]
        if c6==" " and c7==" " and c8=="L":
            if cur: levels.append(cur)
            e=line[9:19].strip(); de=line[19:21].strip()
            try: ev=float(e)
            except ValueError: ev=None
            cur={"e_str":e,"de_str":de,"e":ev,"xref":None,"has_K":False,"has_L":False,"K_amb":False,"L_amb":False,"cl_e":""}
            in_cl_e=False
        elif c6=="X" and c7==" " and c8=="L" and cur:
            xt=line[9:].rstrip().strip()
            if xt.startswith("XREF="): xt=xt[5:]
            cur["xref"]=xt; in_cl_e=False
            for ltr,mod in re.findall(r"([A-Z])(\([^)]*\))?",xt):
                amb=(mod=="(*)")
                if ltr=="K": cur["has_K"]=True; cur["K_amb"]=amb
                elif ltr=="L": cur["has_L"]=True; cur["L_amb"]=amb
        elif c6==" " and c7=="c" and c8=="L" and cur:
            t=line[9:].rstrip().strip()
            if t.startswith("E$"): cur["cl_e"]=t[2:].strip(); in_cl_e=True
            else: in_cl_e=False
        elif c6.isdigit() and c7=="c" and c8=="L" and cur:
            if in_cl_e: cur["cl_e"]+=" "+line[9:].rstrip().strip()
        else: in_cl_e=False
    if cur: levels.append(cur)
    return levels

def find_lv(recs,e,tol):
    best,bd=None,tol+1e-9
    for r in recs:
        d=abs(r["e"]-e)
        if d<bd: bd=d; best=r
    return best

def jav_clean(k_e_str, k_de_str, l_e_str, l_de_str):
    nd_k=len(k_e_str.split(".")[1]) if "." in k_e_str else 0
    nd_l=len(l_e_str.split(".")[1]) if "." in l_e_str else 0
    de_k=int(k_de_str)*(10**(-nd_k))
    de_l=int(l_de_str)*(10**(-nd_l))
    de_k_s=f"{de_k:.{nd_k}f}"; de_l_s=f"{de_l:.{nd_l}f}"
    r=subprocess.run([sys.executable,JAVA_AVG,k_e_str,de_k_s,l_e_str,de_l_s],capture_output=True,text=True)
    for line in r.stdout.splitlines():
        if "suggested adopted result" in line.lower():
            m=re.search(r"([\d.]+)\((\d+)\)",line)
            if m: return m.group(1),m.group(2)
    return None,None

k_recs=parse_source(r"d:\X\ND\ENSDF\A34\Cl34\new\Cl34_33s_p_g.ens")
l_recs=parse_source(r"d:\X\ND\ENSDF\A34\Cl34\new\Cl34_33s_p_p_resonances.ens")
adopted=parse_adopted(r"d:\X\ND\ENSDF\A34\Cl34\new\Cl34_adopted.ens")

total=len(adopted)
n_sample=max(30,int(total*0.15))
sample_idx=sorted(random.sample(range(total),n_sample))

print(f"Total adopted levels: {total}")
print(f"Sample size: {n_sample} ({100*n_sample/total:.1f}%)")
print()

errors=0
for idx in sample_idx:
    lv=adopted[idx]
    if lv["e"] is None: continue
    use_K=lv["has_K"] and not lv["K_amb"]
    use_L=lv["has_L"] and not lv["L_amb"]
    status="OK"; detail=""

    if use_K and not use_L:
        k=find_lv(k_recs,lv["e"],0.6)
        if k is None: status="ERROR"; detail="K not found"
        elif k["e_str"]!=lv["e_str"]: status="MISMATCH"; detail="E: adp="+lv["e_str"]+" K="+k["e_str"]
        elif k["de_str"]!=lv["de_str"]: status="MISMATCH"; detail="DE: adp="+lv["de_str"]+" K="+k["de_str"]
    elif use_L and not use_K:
        l=find_lv(l_recs,lv["e"],0.6)
        if l is None: status="ERROR"; detail="L not found"
        elif l["e_str"]!=lv["e_str"]: status="MISMATCH"; detail="E: adp="+lv["e_str"]+" L="+l["e_str"]
        elif l["de_str"]!=lv["de_str"]: status="MISMATCH"; detail="DE: adp="+lv["de_str"]+" L="+l["de_str"]
    elif use_K and use_L:
        k=find_lv(k_recs,lv["e"],5.0); l=find_lv(l_recs,lv["e"],5.0)
        if k is None or l is None: status="WARN"; detail="K or L not found"
        else:
            avg_e,avg_de=jav_clean(k["e_str"],k["de_str"],l["e_str"],l["de_str"])
            if avg_e and avg_de:
                nd_adp=len(lv["e_str"].split(".")[1]) if "." in lv["e_str"] else 0
                tol=0.5*10**(-nd_adp)
                adp_abs=abs_unc(lv["e_str"],lv["de_str"])
                avg_abs=abs_unc(avg_e,avg_de)
                e_diff=abs(lv["e"]-float(avg_e))
                if e_diff>tol:
                    status="MISMATCH"; detail="E: adp="+lv["e_str"]+" Java="+avg_e+"("+avg_de+")"
                elif adp_abs and avg_abs:
                    rounded_unc=round(avg_abs,nd_adp)
                    if abs(adp_abs-rounded_unc)>5e-10:
                        status="MISMATCH"; detail="DE: adp="+lv["de_str"]+" Java="+avg_de

    if status!="OK": errors+=1
    tag="  " if status=="OK" else "!!"
    print(tag+" ["+str(idx).rjust(3)+"] L "+lv["e_str"].ljust(10)+" XREF="+str(lv["xref"]).ljust(30)+" useK="+str(use_K)+" useL="+str(use_L)+" "+status+" "+detail)

print()
print("Spot-check errors: "+str(errors)+"/"+str(n_sample))
