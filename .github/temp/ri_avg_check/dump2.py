data=open(r'd:\X\ND\ENSDF\A34\S34\new\S34_31p_a_pg.ens',encoding='utf-8-sig',newline='').read()
lines=data.split('\r\n')
if lines and lines[-1]=='': lines=lines[:-1]
def is_cG(l):
    return len(l)>8 and l[6:7]=='c' and l[7:8]=='G'
def is_dataG(l):
    return len(l)==80 and l[5:6]==' ' and l[6:7]!='c' and l[7:8]=='G'
for i,l in enumerate(lines,1):
    if l.startswith(' 34S  cG RI$weighted average'):
        # preceding data G
        j=i-2
        while j>=0 and not is_dataG(lines[j]): j-=1
        g=lines[j]
        ri=g[22:29].strip(); dri=g[29:31].strip()
        print(f'=== L{j+1} E={g[9:19].strip():>9} RI={ri!r} DRI={dri!r}')
        k=i-1
        while k<len(lines) and is_cG(lines[k]):
            print('   ',repr(lines[k])); k+=1
