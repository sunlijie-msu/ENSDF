data=open(r'd:\X\ND\ENSDF\A34\S34\new\S34_31p_a_pg.ens',encoding='utf-8-sig',newline='').read()
lines=data.split('\r\n')
if lines and lines[-1]=='': lines=lines[:-1]
# find cG RI$from 1970Mo09. comment lines (single source only)
idx=[]
for i,l in enumerate(lines,1):
    t=l.rstrip()
    if t==' 34S  cG RI$from 1970Mo09.':
        idx.append(i)
print('count single-source Mo09 cG lines:',len(idx))
for ci in idx:
    # walk back to G record
    gi=ci-1
    while gi>=1 and not (lines[gi-1][5]==' ' and lines[gi-1][7]=='G'):
        gi-=1
    g=lines[gi-1]
    col77=g[76] if len(g)>76 else ''
    col80=g[79] if len(g)>79 else ''
    # comment block after G until next G or L
    print('G@%d E=%r col77=%r col80=%r | cG@%d'%(gi,g[9:19].strip(),col77,col80,ci))
