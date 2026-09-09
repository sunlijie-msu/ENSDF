data=open(r'd:\X\ND\ENSDF\A34\S34\new\S34_31p_a_pg.ens',encoding='utf-8-sig',newline='').read()
lines=data.split('\r\n')
if lines and lines[-1]=='': lines=lines[:-1]
print('TOTAL RI$ comments:')
for i,l in enumerate(lines,1):
    if l.startswith(' 34S  cG RI$') or l.startswith(' 34S 2cG RI$') or l.startswith(' 34S 3cG RI$'):
        print('  [%d] %s'%(i,l.rstrip()))
# confirm no data-record (L/G) content lines equal 80 and gammas ordered - quick structural
bad=[(i+1,len(l)) for i,l in enumerate(lines) if len(l)!=80]
print('non-80:',bad)
import re
