import re
src=r"A34\S34\new\S34_34s_e_eP.ens"
adp=r"A34\S34\new\S34_adopted.ens"
def blocks(p,nl):
    ls=open(p,"rb").read().decode().split(nl)
    lv=[]
    for i,l in enumerate(ls):
        if len(l)<10 or l[6]!=" ": continue
        if l[7]=="L" and l[5]==" ":
            b={"n":i+1,"E":l[9:19].rstrip(),"DE":l[19:21].strip(),"J":l[22:39].rstrip(),
               "T":l[39:55].rstrip(),"xref":"","cmt":[]}
            lv.append(b)
        elif l[7]=="L" and l[5]=="X" and lv:
            lv[-1]["xref"]=l[9:].replace("XREF=","").strip()
        elif l[7]=="L" and l[6]=="c" and lv:
            lv[-1]["cmt"].append(l[8:].rstrip())
    return lv
T=blocks(src,"\r\n")
A=blocks(adp,"\r\n")
print("dataset T levels:",len(T),"| adopted levels:",len(A))
print("\n=== T level -> adopted match ===")
used=set()
for t in T:
    e=float(t["E"])
    dev=float(t["DE"]) if t["DE"] else 0
    cands=[]
    for a in A:
        if "T" not in a["xref"]: continue
        try: ae=float(a["E"])
        except: continue
        ade=float(a["DE"]) if a["DE"] else 0
        if abs(ae-e)<=max(dev,ade,1.0): cands.append(a)
    if len(cands)==1:
        a=cands[0]; used.add(a["n"])
        tag="OK " if abs(float(a["E"])-e)<1e-9 and (a["DE"]==t["DE"]) else "CHK"
        print(f'{tag} T E={t["E"]}+/-{t["DE"]} J={t["J"]:<10} -> adopted L{a["n"]} E={a["E"]} +/-{a["DE"]} J={a["J"]:<10} XREF={a["xref"]}')
    elif not cands:
        print(f'MISS T E={t["E"]}+/-{t["DE"]} J={t["J"]} -> NO adopted record with T in XREF')
    else:
        print(f'MULT T E={t["E"]} -> ' + ", ".join(f'L{c["n"]}({c["E"]},{c["xref"]})' for c in cands))
print("\n=== adopted T-labeled records NOT matched to any T level ===")
for a in A:
    if "T" in a["xref"] and a["n"] not in used:
        print("L%d E=%s +/-%s J=%s XREF=%s"%(a["n"],a["E"],a["DE"],a["J"],a["xref"]))
