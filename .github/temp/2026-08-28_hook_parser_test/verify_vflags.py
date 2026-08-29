path = r'd:\X\ND\ENSDF\A34\S34\new\S34_30si_a_g_a_n_resonances.ens'
b = open(path, 'rb').read()
t = b.decode('utf-8').replace('\r\n', '\n')
ls = t.split('\n')
print('CRLF:', b.count(b'\r\n'), 'nonascii:', sum(1 for x in b if x > 127), 'lines:', len(ls))
print('over80:', [(i + 1, len(x)) for i, x in enumerate(ls) if len(x) > 80])
print('lines!=80:', [(i + 1, len(x)) for i, x in enumerate(ls) if len(x) != 80][:10])

targets = ['7804','9930','7853','9979','7968','10095','8040','10167','8120','10247',
           '8188','10315','8279','10406','8365','10492','7282','8458','8496','10623',
           '7365','8541','10668','8639','10766']
print()
print('=== V-flag check (col 77) ===')
ok = 0
for en in targets:
    for i, x in enumerate(ls):
        if x.startswith(' 34S   G ' + en + ' '):
            c77 = x[76] if len(x) >= 77 else '?'
            status = 'OK' if c77 == 'V' else 'BAD->' + repr(c77)
            if c77 == 'V':
                ok += 1
            print(f'  G {en:6} line {i+1:3} len {len(x)} col77={c77} {status} | {x.rstrip()[:60]}')
print(f'V flags correct: {ok}/25')

# verify no OTHER gamma got V
print()
print('=== any stray V flags on non-target G records? ===')
stray = 0
for i, x in enumerate(ls):
    if x.startswith(' 34S   G ') and len(x) >= 77 and x[76] == 'V':
        en = x[9:19].strip()
        if en not in targets:
            print('  STRAY:', i + 1, x.rstrip()[:60])
            stray += 1
print('stray V flags:', stray)
