data=open(r'd:\X\ND\ENSDF\A34\S34\new\S34_31p_a_pg.ens',encoding='utf-8-sig',newline='').read()
lines=data.split('\r\n')
targs=[168,181,228,235,249,257,273,280,321,327,345,348,413,419]
for t in targs:
    l=lines[t-1]
    print(f'L{t}: RI=[{l[22:29]}] DRI=[{l[29:31]}]  E=[{l[9:19]}] M=[{l[32:41]}] C77=[{l[76]}] Q80=[{l[79]}]')
    print('     ',l.rstrip())
