data=open(r'd:\X\ND\ENSDF\A34\S34\new\S34_31p_a_pg.ens',encoding='utf-8-sig',newline='').read()
lines=data.split('\r\n')
print('python total (raw strip):',len(lines))
if lines and lines[-1]=='': print('note: trailing empty element -> drop'); lines=lines[:-1]
for i in range(129,136):
    print('[PY %d] %s'%(i+1,lines[i].rstrip()))
