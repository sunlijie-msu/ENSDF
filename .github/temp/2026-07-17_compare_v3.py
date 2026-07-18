import re
with open('d:/X/ND/ENSDF/XUNDL/2026OSAA_CT11035_152Gd.ens','r') as f: lines=f.readlines()

ac=[]
lv=None; ge=None
for i,l in enumerate(lines):
    if len(l)<80: continue
    c6=l[5];c7=l[6];c8=l[7]
    if c8=='L' and c7==' ':
        try: lv=float(l[9:19].strip())
        except: lv=None
        ge=None
    elif c8=='G' and c7==' ' and c6==' ':
        try: float(l[9:19].strip()); ge=l[9:19].strip()
        except: pass
    elif c8=='G' and c7=='c':
        cm=l[9:].strip()
        if 'A{-0}' not in cm and 'A{-2}' not in cm: continue
        fu=cm; j=i+1
        while j<len(lines):
            nl=lines[j]
            if len(nl)>=80 and nl[7]=='G' and nl[6]=='c' and nl[5]!=' ':
                fu+=' '+nl[9:].strip(); j+=1
            else: break
        # Find cascade pattern
        m=re.search(r'\$(\d+\.?\d*)\s*-\s*(\d+\.?\d*)\s*\|g\|g',fu)
        if m and lv and ge:
            ac.append({'lv':lv,'g1':ge,'g2':m.group(2),'cm':fu,'li':i})

with open('d:/X/ND/ENSDF/XUNDL/2026OSAA_CT11035_152Gd_Table_IV.md','r',encoding='utf-8') as f: md=f.readlines()
tb=[]
for l in md:
    s=l.strip()
    if not s.startswith('| ') or '$' in s or '---' in s: continue
    p=[x.strip() for x in s.split('|')][1:-1]
    if len(p)<12: continue
    tb.append({'E':p[0],'g1':p[1],'g2':p[2],'A0':p[3],'A2':p[4],'A4':p[5],'d1':p[11]})

matched=0; unmatched=[]
for tr in tb:
    fnd=False
    for ee in ac:
        if abs(float(tr['E'])-ee['lv'])<1.0:
            try:
                if abs(float(tr['g1'])-float(ee['g1']))<1.0 and abs(float(tr['g2'])-float(ee['g2']))<1.0:
                    fnd=True; matched+=1; break
            except: pass
    if not fnd and (tr['A0'].strip() or tr['A2'].strip()):
        unmatched.append(tr)

print(f'Matched: {matched}, Unmatched (with AC): {len(unmatched)}')
for tr in unmatched[:10]:
    print(f'  L={tr["E"]} g={tr["g1"]}-{tr["g2"]}')

print('\n=== DISCREPANCIES ===')
diffs=[]
for tr in tb:
    if not tr['A0'].strip() and not tr['A2'].strip() and not tr['A4'].strip(): continue
    match=None
    for ee in ac:
        if abs(float(tr['E'])-ee['lv'])<1.0:
            try:
                if abs(float(tr['g1'])-float(ee['g1']))<1.0 and abs(float(tr['g2'])-float(ee['g2']))<1.0:
                    match=ee; break
            except: pass
    if not match: continue
    
    for fld, idx in [('A0',0),('A2',2),('A4',4)]:
        tv=tr[fld].strip()
        if not tv: continue
        m=re.match(r'(-?[\d.]+)\s*\((\d+)\)',tv)
        if not m: continue
        tv_v, tv_u = m.group(1), m.group(2)
        cm=match['cm']
        pattern = r'A\{-'+str(idx)+r'\}=(-?[\d.]+)\s*\{I(\d+)\}'
        pm=re.search(pattern,cm)
        if not pm:
            diffs.append((tr['E'],tr['g1'],tr['g2'],fld,tv,'MISSING_IN_ENSDF'))
            continue
        ev_v, ev_u = pm.group(1), pm.group(2)
        if tv_v != ev_v or tv_u != ev_u:
            diffs.append((tr['E'],tr['g1'],tr['g2'],fld,f'{tv_v} ({tv_u})',f'{ev_v} ({ev_u})'))
    
    td=tr['d1'].strip()
    if td:
        cm=match['cm']
        dm=re.search(r'\|d=([+-]?[\d.]+(?:\s*[<>GL]?[T]?\s*)?)\s*(?:\{I(\d+)\})?',cm)
        if dm:
            dv=dm.group(1).strip()
            du=dm.group(2) if dm.lastindex and dm.lastindex>=2 else ''
            if du: e_d=f'{dv} ({du})'
            else: e_d=dv
            if td != e_d:
                try:
                    if td.startswith('>') and dv.startswith('>'):
                        if abs(float(td[1:])-float(dv[1:]))>0.1:
                            diffs.append((tr['E'],tr['g1'],tr['g2'],'delta',td,e_d))
                    elif not td.startswith('>') and not dv.startswith('>') and '(' in td:
                        mt=re.match(r'(-?[\d.]+)\s*\((\d+)\)',td)
                        if mt:
                            if mt.group(1)!=dv or (du and mt.group(2)!=du):
                                diffs.append((tr['E'],tr['g1'],tr['g2'],'delta',td,e_d))
                except: diffs.append((tr['E'],tr['g1'],tr['g2'],'delta',td,e_d))
        elif td.strip():
            diffs.append((tr['E'],tr['g1'],tr['g2'],'delta',td,'MISSING_IN_ENSDF'))

print(f'Discrepancies: {len(diffs)}')
for d in diffs[:80]:
    print(f'  L={d[0]:>6} g={d[1]:>6}-{d[2]:>4} {d[3]:5}: TableIV={d[4]:>15} ENSDF={d[5]:>15}')
