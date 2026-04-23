#!/usr/bin/env python3
"""
Cross-check Cl34_adopted.ens level energies (from L 7018.9 onwards) against
Cl34_33s_p_g.ens (dataset K) and Cl34_33s_p_p_resonances.ens (dataset L).
"""

import re, sys, subprocess

ADOPTED_FILE = r"d:\X\ND\ENSDF\A34\Cl34\new\Cl34_adopted.ens"
K_FILE       = r"d:\X\ND\ENSDF\A34\Cl34\new\Cl34_33s_p_g.ens"
L_FILE       = r"d:\X\ND\ENSDF\A34\Cl34\new\Cl34_33s_p_p_resonances.ens"
JAVA_AVG     = r"d:\X\ND\ENSDF\.github\scripts\Java_Average.py"


def abs_unc(e_str, de_str):
    e_str = e_str.strip(); de_str = de_str.strip()
    if not de_str or de_str in ('LT','GT'): return None
    try: de_int = int(de_str)
    except ValueError: return None
    n_dec = len(e_str.split('.')[1]) if '.' in e_str else 0
    return de_int * (10**(-n_dec))


def parse_source(path):
    recs = []
    with open(path, encoding='ascii', errors='replace') as f:
        lines = f.readlines()
    for line in lines:
        if len(line) < 21: continue
        # 0-based: col5=line[5], col6=line[6], col7=line[7]
        # Primary L: col6=' ', col7=' ', col8='L'
        if len(line) > 7 and line[7]=='L' and line[6]==' ' and line[5]==' ':
            e_str  = line[9:19].strip()
            de_str = line[19:21].strip()
            if not e_str: continue
            try: e_val = float(e_str)
            except ValueError: continue
            recs.append({'e_str':e_str,'de_str':de_str,'e':e_val,'de_abs':abs_unc(e_str,de_str)})
    return sorted(recs, key=lambda r:r['e'])


def find_lv(recs, e_target, tol):
    best,best_diff = None, tol+1e-9
    for r in recs:
        d = abs(r['e']-e_target)
        if d < best_diff: best_diff=d; best=r
    return best


def parse_adopted(path):
    with open(path, encoding='ascii', errors='replace') as f:
        lines = f.readlines()
    start = None
    for i,line in enumerate(lines):
        if len(line)>9 and line[7]=='L' and line[6]==' ' and line[5]==' ' and line[9:19].strip()=='7018.9':
            start=i; break
    if start is None: sys.exit("ERROR: L 7018.9 not found")
    levels=[]; cur=None; in_cl_e=False
    for line in lines[start:]:
        if len(line)<8: continue
        c6,c7,c8 = line[5],line[6],line[7]
        # Primary L-record
        if c6==' ' and c7==' ' and c8=='L':
            if cur: levels.append(cur)
            e_str=line[9:19].strip(); de_str=line[19:21].strip()
            try: e_val=float(e_str)
            except ValueError: e_val=None
            cur={'e_str':e_str,'de_str':de_str,'e':e_val,'de_abs':abs_unc(e_str,de_str) if e_val else None,
                 'xref':None,'has_K':False,'has_L':False,'K_amb':False,'L_amb':False,'cl_e':''}
            in_cl_e=False
        # XREF line: col6='X', col7=' ', col8='L'
        elif c6=='X' and c7==' ' and c8=='L' and cur is not None:
            xtext=line[9:].rstrip().strip()
            if xtext.startswith('XREF='): xtext=xtext[5:]
            cur['xref']=xtext; in_cl_e=False
            tokens=re.findall(r'([A-Z])(\([^)]*\))?', xtext)
            for ltr,mod in tokens:
                amb=(mod=='(*)')
                if ltr=='K': cur['has_K']=True; cur['K_amb']=amb
                elif ltr=='L': cur['has_L']=True; cur['L_amb']=amb
        # cL comment (first line): col6=' ', col7='c', col8='L'
        elif c6==' ' and c7=='c' and c8=='L' and cur is not None:
            text=line[9:].rstrip().strip()
            if text.startswith('E$'): cur['cl_e']=text[2:].strip(); in_cl_e=True
            else: in_cl_e=False
        # Continuation cL: col6=digit, col7='c', col8='L'
        elif c6.isdigit() and c7=='c' and c8=='L' and cur is not None:
            text=line[9:].rstrip().strip()
            if in_cl_e: cur['cl_e']+=' '+text
        else:
            in_cl_e=False
    if cur: levels.append(cur)
    return levels


def java_avg(e1,de1,e2,de2):
    res=subprocess.run([sys.executable,JAVA_AVG,str(e1),str(de1),str(e2),str(de2)],
                       capture_output=True,text=True)
    for line in res.stdout.splitlines():
        if 'suggested adopted result' in line.lower():
            m=re.search(r'([\d.]+)\((\d+)\)', line)
            if m: return m.group(1),m.group(2),res.stdout
    return None,None,res.stdout


def comment_vals(cl_e):
    return re.findall(r'([\d.]+)\s*\{I(\d+)\}', cl_e)


def main():
    print("="*80)
    print("Cl34 Adopted Level Energy Cross-Check (from L 7018.9)")
    print("="*80)
    k_recs=parse_source(K_FILE); l_recs=parse_source(L_FILE); adopted=parse_adopted(ADOPTED_FILE)
    print(f"K: {len(k_recs)} levels,  L: {len(l_recs)} levels,  Adopted: {len(adopted)} levels")
    print()
    mismatches=[]
    def add(lv,t,d): mismatches.append({'lv':f"L {lv['e_str']}  XREF={lv['xref']}","type":t,"detail":d})

    for lv in adopted:
        if lv['e'] is None: continue
        use_K = lv['has_K'] and not lv['K_amb']
        use_L = lv['has_L'] and not lv['L_amb']
        e_adp = lv['e']; de_adp = lv['de_str']

        if use_K and not use_L:
            k=find_lv(k_recs, e_adp, 0.6)
            if k is None: add(lv,'MISSING_IN_K',f"Adopted E={lv['e_str']} not found in K"); continue
            if k['e_str']!=lv['e_str']: add(lv,'E_MISMATCH(K)',f"Adopted={lv['e_str']}, K={k['e_str']}")
            if k['de_str']!=de_adp: add(lv,'DE_MISMATCH(K)',f"Adopted DE={de_adp!r}, K DE={k['de_str']!r}")

        elif use_L and not use_K:
            l=find_lv(l_recs, e_adp, 0.6)
            if l is None: add(lv,'MISSING_IN_L',f"Adopted E={lv['e_str']} not found in L"); continue
            if l['e_str']!=lv['e_str']: add(lv,'E_MISMATCH(L)',f"Adopted={lv['e_str']}, L={l['e_str']}")
            if l['de_str']!=de_adp: add(lv,'DE_MISMATCH(L)',f"Adopted DE={de_adp!r}, L DE={l['de_str']!r}")

        elif use_K and use_L:
            k=find_lv(k_recs, e_adp, 5.0); l=find_lv(l_recs, e_adp, 5.0)
            if k is None: add(lv,'MISSING_IN_K(KL)',f"not found in K"); continue
            if l is None: add(lv,'MISSING_IN_L(KL)',f"not found in L"); continue
            # Check comment quoted values
            cl_e=lv['cl_e']
            if cl_e:
                quoted=comment_vals(cl_e)
                if len(quoted)>=2:
                    (v1,u1),(v2,u2)=quoted[0],quoted[1]
                    try: d1K=abs(float(v1)-k['e']); d1L=abs(float(v1)-l['e'])
                    except ValueError: d1K=d1L=999
                    if d1K<=d1L: qKe,qKu,qLe,qLu=v1,u1,v2,u2
                    else: qLe,qLu,qKe,qKu=v1,u1,v2,u2
                    if qKe!=k['e_str']: add(lv,'COMMENT_K_E',f"comment={qKe}, K file={k['e_str']}")
                    if qKu!=k['de_str']: add(lv,'COMMENT_K_DE',f"comment DE={{I{qKu}}}, K DE={k['de_str']!r}")
                    if qLe!=l['e_str']: add(lv,'COMMENT_L_E',f"comment={qLe}, L file={l['e_str']}")
                    if qLu!=l['de_str']: add(lv,'COMMENT_L_DE',f"comment DE={{I{qLu}}}, L DE={l['de_str']!r}")
            # Check Java_Average
            if k['de_abs'] is not None and l['de_abs'] is not None:
                avg_e,avg_de,out=java_avg(k['e'],k['de_abs'],l['e'],l['de_abs'])
                if avg_e and avg_de:
                    try:
                        n_dec=len(avg_e.split('.')[1]) if '.' in avg_e else 0
                        tol=0.5*10**(-n_dec)
                        if abs(e_adp-float(avg_e))>tol:
                            add(lv,'AVG_E_MISMATCH',
                                f"Adopted={lv['e_str']}, Java({k['e_str']}+/-{k['de_str']},{l['e_str']}+/-{l['de_str']})={avg_e}({avg_de})")
                        if de_adp.strip()!=avg_de.strip():
                            add(lv,'AVG_DE_MISMATCH',
                                f"Adopted DE={de_adp!r}, Java={avg_de!r}")
                    except Exception: pass
                else:
                    print(f"  WARNING: Java parse failed for L {lv['e_str']}")

    print(f"Total mismatches: {len(mismatches)}")
    for i,m in enumerate(mismatches,1):
        print(f"\n[{i:3d}] {m['lv']}")
        print(f"      Type  : {m['type']}")
        print(f"      Detail: {m['detail']}")
    print("\nDone.")

if __name__=='__main__': main()
