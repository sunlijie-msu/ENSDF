data=open(r'd:\X\ND\ENSDF\A34\S34\new\S34_31p_a_pg.ens',encoding='utf-8-sig',newline='').read()
lines=data.split('\r\n')
# show suspect L records with energy not numeric
import re
for i,l in enumerate(lines,1):
    if len(l)>9 and l[5:6]==' ' and l[6:7]!='c' and l[7:8]=='L':
        E=l[9:19].strip()
        if not re.match(r'^[0-9E.]+$',E) or 'E' in E.replace('E+','').replace('E-',''):
            print(i,repr(l))
