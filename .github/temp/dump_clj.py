import io,re
p=r'XUNDL\A58\Ni58\new\Ni58_adopted.ens'
ls=io.open(p,encoding='ascii',errors='replace').read().split('\n')
def fl(x):
    x=x.strip(); return float(x) if x else 0.0
lev=[];cur=None
for i,l in enumerate(ls,1):
    if len(l)>20 and l[5]==' ' and l[6]==' ' and l[7:9] in ('L ','G '):
        if l[7:9]=='L ':
            try: cur={'l':i,'E':float(l[9:19]),'DE':fl(l[19:21]),'J':re.sub(r'\s','',l[21:39]),'g':[],'c':[]}
            except: cur=None
            if cur: lev.append(cur)
        elif cur is not None:
            try: cur['g'].append({'l':i,'E':float(l[9:19]),'DE':fl(l[19:21]),'M':l[31:41].strip(),'FL':None})
            except: pass
        continue
    if cur is not None and len(l)>9 and l[5]!=' ' and l[6]==' ' and l[7:9]=='G ' and 'FL=' in l:
        m=re.search(r'FL=([0-9.]+)\s*(-\d)?',l[9:])
        if cur['g'] and m: cur['g'][-1]['FL']=float(m.group(1))
        continue
    if cur is not None and l[6]=='c' and l[5]==' ' and l[9:].startswith('J$'):
        cur['c'].append([i,l[9:].rstrip()])
    elif cur is not None and l[6]=='c' and l[5]!=' ' and cur['c']:
        cur['c'][-1][1]+=' '+l[9:].rstrip()
def near(d):
    b=None;bd=9e9
    for r in lev:
        dd=abs(r['E']-d)
        if dd<bd: bd=dd;b=r
    return b,bd
for r in lev:
    if not r['c']: continue
    body=' '.join(t for _,t in r['c'])
    if not re.search(r'\|g',body): continue
    print('=== L%-5d E=%-9s J=%-7s  %s'%(r['l'],r['E'],r['J'],body[:95]))
    for g in r['g']:
        if g['FL'] is not None:
            d=g['FL']; note='FL'
        else:
            d=r['E']-g['E']; note='calc'
        b,bd=near(d)
        print('     G%-5d Eg=%-9s M=%-9s %s dest=%-9s gap=%.2f -> L%-5d %-9s J=%s'%(g['l'],g['E'],g['M'],note,d,bd,b['l'],b['E'],b['J']))
