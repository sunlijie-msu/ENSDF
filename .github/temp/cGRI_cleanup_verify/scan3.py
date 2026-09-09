import io
p=r'd:\X\ND\ENSDF\A34\S34\new\S34_31p_a_pg.ens'
data=open(p,encoding='utf-8-sig',newline='').read()
lines=data.split('\r\n')
if lines and lines[-1]=='': lines=lines[:-1]
print('total lines:',len(lines))
for ln in (134,213,294,313,392):
    l=lines[ln-1]
    print('[%d] len=%d |%s|'%(ln,len(l),l.rstrip()))
old=['RI$<1 (1970Mo09), |<1 (1974Gr06)','RI$100 (1970Mo09), 100 (1970Gr11), 100 (1971Mu03)']
for o in old:
    print('OLD present:', any(o in l for l in lines))
bad=[(i+1,len(l)) for i,l in enumerate(lines) if len(l)!=80]
print('non-80 lines:',bad[:10],'total',len(bad))
