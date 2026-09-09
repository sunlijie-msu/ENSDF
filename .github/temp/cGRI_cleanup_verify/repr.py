data=open(r'd:\X\ND\ENSDF\A34\S34\new\S34_31p_a_pg.ens',encoding='utf-8-sig',newline='').read()
lines=data.split('\r\n')
if lines and lines[-1]=='': lines=lines[:-1]
# repr exact for first few targets + comment line
for gi in [211,216,225]:
    print('G%d repr: %r'%(gi,lines[gi-1]))
    print('G%d +1 : %r'%(gi,lines[gi]))
# comment line repr
ci=212
print('comment repr: %r'%lines[ci-1])
print('comment len:',len(lines[ci-1]))
