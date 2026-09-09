data=open(r'd:\X\ND\ENSDF\A34\S34\new\S34_31p_a_pg.ens',encoding='utf-8-sig',newline='').read()
lines=data.split('\r\n')
if lines and lines[-1]=='': lines=lines[:-1]
for i,l in enumerate(lines,1):
    if l.startswith(' 34S  cG RI$weighted average'):
        # find preceding data G line
        j=i-2
        while j>=0 and not (lines[j][5:6]==' ' and lines[j][6:7]!='c' and lines[j][7:8]=='G' and len(lines[j])==80):
            j-=1
        g=lines[j] if j>=0 else ''
        print('=== G at L',j+1,' comment L',i)
        print('DATA:',repr(g))
        k=i-1
        block=[]
        while k<len(lines) and lines[k].startswith(' 34S  cG '):
            block.append(lines[k].rstrip()); k+=1
        for b in block: print('CMT:',repr(b))
