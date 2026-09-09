data=open(r'd:\X\ND\ENSDF\A34\S34\new\S34_31p_a_pg.ens',encoding='utf-8-sig',newline='').read()
lines=data.split('\r\n')
if lines and lines[-1]=='': lines=lines[:-1]
targets=[211,216,225,251,274,276,278,305,307,309,311,320,328,330,332,334,336,350,360,362,364,368]
for gi in targets:
    g=lines[gi-1]
    # set col77 (index76) to M
    nl=g[:76]+'M'+g[77:]
    assert len(nl)==80 and nl[79]=='?'
    print('new[%d]=|%s|'%(gi,nl))
