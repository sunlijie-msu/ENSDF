path = r'd:\X\ND\ENSDF\A34\S34\new\S34_30si_a_g_a_n_resonances.ens'
b = open(path, 'rb').read()
t = b.decode('utf-8').replace('\r\n', '\n')
ls = t.split('\n')
print('CRLF:', b.count(b'\r\n'), 'nonascii:', sum(1 for x in b if x > 127), 'lines:', len(ls))
print('over80:', [(i+1, len(x)) for i, x in enumerate(ls) if len(x) > 80])
print()

# V-flag targets (25 gammas, RI from 1964Va08)
V = ['7804','9930','7853','9979','7968','10095','8040','10167','8120','10247',
     '8188','10315','8279','10406','8365','10492','7282','8458','8496','10623',
     '7365','8541','10668','8639','10766']
# W-flag targets (16 gammas, RI=100 from 1967Wi01)
W = ['8718','8802','8865','8886','8979','9143','9329','9344','9377',
     '9583','9793','11930','9828','12032','12098','12192']

def ginfo(en):
    for i, x in enumerate(ls):
        if x.startswith(' 34S   G ' + en + ' '):
            ri = x[22:29].strip() if len(x) >= 29 else ''
            c77 = x[76] if len(x) >= 77 else '?'
            return i+1, len(x), ri, c77
    return None

print('=== V-flag gammas (expect col77=V) ===')
vok = 0
for en in V:
    g = ginfo(en)
    ok = g and g[3] == 'V'
    vok += ok
    print(f'  G {en:6} line {g[0] if g else "-":>3} len {g[1] if g else "-"} RI={g[2] if g else "?":>5} col77={g[3] if g else "?"} {"OK" if ok else "BAD"}')
print(f'V OK: {vok}/25')
print()
print('=== W-flag gammas (expect RI=100, col77=W) ===')
wok = 0
for en in W:
    g = ginfo(en)
    ok = g and g[2] == '100' and g[3] == 'W'
    wok += ok
    print(f'  G {en:6} line {g[0] if g else "-":>3} len {g[1] if g else "-"} RI={g[2] if g else "?":>5} col77={g[3] if g else "?"} {"OK" if ok else "BAD"}')
print(f'W OK: {wok}/16')
print()
# stray flags
print('=== stray V/W flags on non-target gammas ===')
stray = 0
for i, x in enumerate(ls):
    if x.startswith(' 34S   G ') and len(x) >= 77:
        c77 = x[76]
        en = x[9:19].strip()
        if c77 in ('V', 'W') and en not in V and en not in W:
            print('  STRAY:', i+1, x.rstrip()[:70])
            stray += 1
print('stray:', stray)
