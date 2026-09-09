data=open(r'd:\X\ND\ENSDF\A34\S34\new\S34_31p_a_pg.ens',encoding='utf-8-sig',newline='').read()
lines=data.split('\r\n')
if lines and lines[-1]=='': lines=lines[:-1]
for i,l in enumerate(lines,1):
    if 'RI(M)' in l or 'unless otherwise noted' in l or 'otherwise noted' in l:
        print('[%d]|%s|'%(i,l))
