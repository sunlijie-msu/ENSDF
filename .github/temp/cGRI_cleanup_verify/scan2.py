import io
p=r'd:\X\ND\ENSDF\A34\S34\new\S34_31p_a_pg.ens'
data=open(p,encoding='utf-8-sig').read()
# count lines like PowerShell ReadAllLines does: split on CRLF only
lines=[x for x in data.split('\r\n')]
print('total lines (CRLF split):',len(lines))
targets={
'RI$from 1970Mo09, 1970Gr11, 1971Mu03, and 1974Gr06.':'expect L134',
'RI$from 1970Mo09, 1970Gr11, and 1971Mu03.':'expect L213',
'RI$from 1970Mo09 and 1974Gr06.':'expect L294',
'RI$from 1970Mo09, 1970Gr11, 1971Mu03, and 1974Gr06':'expect L313 (no period)',
'RI$from 1970Gr11, 1971Mu03, and 1974Gr06':'expect L392 (no period)',
}
for t,lab in targets.items():
    hits=[i+1 for i,l in enumerate(lines) if t in l]
    print(lab,'->',t[:40],'at',hits)
# ensure old value-repeating forms gone
old=['RI$<1 (1970Mo09), |<1 (1974Gr06)','RI$100 (1970Mo09), 100 (1970Gr11), 100 (1971Mu03)']
for o in old:
    print('OLD still present:',o[:30], any(o in l for l in lines))
# check L134 full new line correct & pad
for ln in (134,213,294,313,392):
    l=lines[ln-1]
    print('[%d] len=%d |%s|'%(ln,len(l),l.rstrip()))
# any non-80
bad=[(i+1,len(l)) for i,l in enumerate(lines) if len(l)!=80]
print('non-80 lines:',bad[:10])
