path = r'd:\X\ND\ENSDF\A34\S34\new\S34_33s_d_p.ens'
b = open(path, 'rb').read()
t = b.decode('utf-8').replace('\r\n', '\n')
ls = t.split('\n')
print('CRLF:', b.count(b'\r\n'), 'nonascii:', sum(1 for x in b if x > 127), 'lines:', len(ls))
print('over80:', [(i+1, len(x)) for i, x in enumerate(ls) if len(x) > 80])
print('non-80/0:', [(i+1, len(x)) for i, x in enumerate(ls) if len(x) not in (80,0)][:8])

flags = {'B': ['2122','4702','4888','7398','8299','8622'],
         'C': ['5326','5683','5694','5758','6128','6422','6832','7547','7659','7732','8142'],
         'V': ['3915','4072','4688','4874','5225','5859','6008','6533']}
print()
print('=== flag check (col 77) ===')
tot = 0
for fl, ens in flags.items():
    for en in ens:
        for x in ls:
            if x.startswith(' 34S   L ' + en + ' '):
                c77 = x[76] if len(x) >= 77 else '?'
                q80 = x[79] if len(x) >= 80 else '?'
                ok = (c77 == fl)
                tot += ok
                print(f'  L {en:5} col77={c77} col80={q80!r} {"OK" if ok else "BAD"}')
                break
print(f'flags OK: {tot}/{sum(len(v) for v in flags.values())}')

# check weighted-average comments have no colon after 'of' and use 'and'
print()
print('=== weighted-average comment check ===')
wavg = [x.rstrip() for x in ls if 'weighted average of' in x]
bad = [x for x in wavg if ':' in x or ';' in x or ',' in x]
print(f'comments: {len(wavg)}, with colon/semicolon/comma: {len(bad)}')
for x in bad:
    print('  BAD:', repr(x))
for x in wavg[:3]:
    print('  sample:', repr(x[-75:]))
