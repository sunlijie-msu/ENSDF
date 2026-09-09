data=open(r'd:\X\ND\ENSDF\A34\S34\new\S34_31p_a_pg.ens',encoding='utf-8-sig',newline='').read()
lines=data.split('\r\n')
if lines and lines[-1]=='': lines=lines[:-1]
# For each G record, gather its following comment lines (cG, 2cG... until next L/G/d/PN/data record)
def is_comment_line(l): return len(l)>6 and l[5]!=' ' and l[6]=='c'  # col6 cont not blank? no
# simpler: comment lines have char at index6=='c'
Gidx=[i for i,l in enumerate(lines) if len(l)>7 and l[7]=='G']
print('G count:',len(Gidx))
# gather single-source Mo09 comment indices
mo=[i for i,l in enumerate(lines,1) if l.rstrip()==' 34S  cG RI$from 1970Mo09.']
for ci in mo:
    gi=ci-1
    # find owning G: nearest preceding G line
    g=ci-1
    while g>=1 and lines[g-1][7]!='G': g-=1
    # collect comment lines belonging to this G (cont lines too) after G
    end=ci
    # print G line + its comment block (only RI line expected)
    print('--- G@%d E=%s cG@%d ---'%(g,lines[g-1][9:19].strip(),ci))
