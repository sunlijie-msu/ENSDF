data=open(r'd:\X\ND\ENSDF\A34\S34\new\S34_31p_a_pg.ens',encoding='utf-8-sig',newline='').read()
lines=data.split('\r\n')
if lines and lines[-1]=='': lines=lines[:-1]
print('TOTAL:',len(lines))
print('--- top 20 lines ---')
for i in range(0,20):
    print('[%d]|%s|'%(i+1,lines[i]))
