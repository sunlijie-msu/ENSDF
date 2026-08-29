path = r'd:\X\ND\ENSDF\A34\S34\new\S34_30si_a_g_a_n_resonances.ens'
b = open(path, 'rb').read()
t = b.decode('utf-8').replace('\r\n', '\n')
ls = t.split('\n')
print('CRLF:', b.count(b'\r\n'), 'nonascii:', sum(1 for x in b if x > 127), 'lines:', len(ls))

V = ['7804','9930','7853','9979','7968','10095','8040','10167','8120','10247',
     '8188','10315','8279','10406','8365','10492','7282','8458','8496','10623',
     '7365','8541','10668','8639','10766']
W = ['8718','8802','8865','8886','8979','9143','9329','9344','9377',
     '9583','9793','11930','9828','12032','12098','12192']

def ginfo(en):
    for i, x in enumerate(ls):
        if x.startswith(' 34S   G ' + en + ' '):
            ri = x[22:29].strip() if len(x) >= 29 else ''
            c77 = x[76] if len(x) >= 77 else '?'
            return i+1, len(x), ri, c77
    return None

bad = []
for en in V:
    g = ginfo(en)
    if not g or g[3] != 'V':
        bad.append(('V', en, g))
for en in W:
    g = ginfo(en)
    if not g or g[2] != '100' or g[3] != 'W':
        bad.append(('W', en, g))
print('V+W flag problems:', len(bad))
for x in bad:
    print('  ', x)

# line length anomalies (excluding EOF blanks)
short = [(i+1, len(x)) for i, x in enumerate(ls) if len(x) not in (80, 0)]
print('non-80/0 lines:', short)
mid_empty = [(i+1) for i, x in enumerate(ls) if len(x) == 0 and i < len(ls)-2]
print('empty lines in body:', mid_empty)

# any leftover cG E,RI comments
print('cG E,RI$from 1965Mc07 count:', sum(1 for x in ls if 'cG E,RI$from 1965Mc07' in x))
print('cG E,RI,M$from 1965Mc07 count:', sum(1 for x in ls if 'cG E,RI,M$from 1965Mc07' in x))
print('cG M$from 1965Mc07 count:', sum(1 for x in ls if 'cG M$from 1965Mc07' in x))
