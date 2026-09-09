data=open(r'd:\X\ND\ENSDF\A34\S34\new\S34_31p_a_pg.ens',encoding='utf-8-sig',newline='').read()
lines=data.split('\r\n')
if lines and lines[-1]=='': lines=lines[:-1]
# target G indices from map
targets=[211,216,225,251,274,276,278,305,307,309,311,320,328,330,332,334,336,350,360,362,364,368]
for gi in targets:
    g=lines[gi-1]
    # uniqueness check on full line (data lines might have trailing spaces to 80? show len)
    cnt=sum(1 for x in lines if x==g)
    col76=g[76] if len(g)>76 else '-'
    col80=g[79] if len(g)>79 else '-'
    print('G@%d E=%r len=%d col77=%r col80=%r unique=%d'%(gi,g[9:19].strip(),len(g),col76,col80,cnt))
    print('   |%s|'%g)
