data=open(r'd:\X\ND\ENSDF\A34\S34\new\S34_31p_a_pg.ens',encoding='utf-8-sig',newline='').read()
lines=data.split('\r\n')
if lines and lines[-1]=='': lines=lines[:-1]
want={
135:'RI$from 1970Mo09, 1970Gr11, 1971Mu03, and 1974Gr06.',
214:'RI$from 1970Mo09, 1970Gr11, and 1971Mu03.',
295:'RI$from 1970Mo09 and 1974Gr06.',
314:'RI$from 1970Mo09, 1970Gr11, 1971Mu03, and 1974Gr06',
393:'RI$from 1970Gr11, 1971Mu03, and 1974Gr06',
}
for ln,t in want.items():
    l=lines[ln-1].rstrip()
    ok = (l==' 34S  cG '+t)
    print('[%d] %s | %s'%(ln,'OK ' if ok else 'MISMATCH',l))
# also show what's around 314
for j in range(312,317):
    print('   ctx [%d] %s'%(j,lines[j-1].rstrip()))
