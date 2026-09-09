data=open(r'd:\X\ND\ENSDF\A34\S34\new\S34_31p_a_pg.ens',encoding='utf-8-sig',newline='').read()
lines=data.split('\r\n')
if lines and lines[-1]=='': lines=lines[:-1]
targets={
'RI$from 1970Mo09, 1970Gr11, 1971Mu03, and 1974Gr06.':None,
'RI$from 1970Mo09, 1970Gr11, and 1971Mu03.':None,
'RI$from 1970Mo09 and 1974Gr06.':None,
'RI$from 1970Mo09, 1970Gr11, 1971Mu03, and 1974Gr06':None,
'RI$from 1970Gr11, 1971Mu03, and 1974Gr06':None,
}
for i,l in enumerate(lines,1):
    for t in targets:
        if t in l and targets[t] is None:
            targets[t]=i
for t,ln in targets.items():
    print('=== %r at line %s ==='%(t,ln))
    for j in range(ln-2,ln+1):
        print('   [%d] %s'%(j,lines[j-1].rstrip()))
