data=open(r'd:\X\ND\ENSDF\A34\S34\new\S34_31p_a_pg.ens',encoding='utf-8-sig',newline='').read()
lines=data.split('\r\n')
def isL(l): return len(l)>8 and l[5:6]==' ' and l[6:7]!='c' and l[7:8]=='L'
def isG(l): return len(l)==80 and l[5:6]==' ' and l[6:7]!='c' and l[7:8]=='G'
def is_cG(l): return len(l)>8 and l[6:7]=='c' and l[7:8]=='G'
# collect all level blocks with their G records
blocks=[]
cur=None
for i,l in enumerate(lines,1):
    if len(l)<9: continue
    if isL(l):
        cur={'ln':i,'E':l[9:19].strip(),'G':[]}
        blocks.append(cur)
    elif isG(l) and cur is not None:
        cur['G'].append({'ln':i,'E':l[9:19].strip(),'RI':l[22:29].strip(),'DRI':l[29:31].strip()})
for b in blocks:
    gs=b['G']
    if not gs: continue
    tot=0.0; allnum=True
    for g in gs:
        try: tot+=float(g['RI'])
        except: allnum=False
    if allnum and abs(tot-100.0)<0.05:
        pass
# print blocks containing one of the weighted-avg E targets
tg=set(['1175.2','3303.1','1945.5','4070.9','1986.9','4113.7','1318.8','2495.5','1571.9','2750.9','1587.9','4890.7','1000','1066'])
for b in blocks:
    hit=[g for g in b['G'] if g['E'] in tg]
    if hit:
        ri=[ (g['E'],g['RI'],g['DRI']) for g in b['G']]
        print(f'LEVEL L{b["ln"]} E={b["E"]}: gammas={ri}')
