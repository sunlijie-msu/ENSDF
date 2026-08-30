path = r'd:\X\ND\ENSDF\A34\S34\new\S34_33s_d_p.ens'
b = open(path, 'rb').read()
t = b.decode('utf-8').replace('\r\n', '\n')
ls = t.split('\n')
print('CRLF:', b.count(b'\r\n'), 'nonascii:', sum(1 for x in b if x > 127), 'lines:', len(ls))
print('over80:', [(i+1, len(x)) for i, x in enumerate(ls) if len(x) > 80])
print('non-80/0:', [(i+1, len(x)) for i, x in enumerate(ls) if len(x) not in (80,0)][:8])

# expected corrections: level -> (E, DE)
exp = {
    '4627': ('4627','5'), '5384': ('5384','6'), '6174': ('6174','8'),
    '6254': ('6254','8'), '6345': ('6345','8'), '6482': ('6482','8'),
    '6640': ('6640','9'), '6690': ('6690','9'), '6959': ('6959','10'),
    '7114': ('7114','10'), '7632': ('7632','10'), '7753': ('7753','11'),
    '7784': ('7784','11'),
}
print()
print('=== L-record corrections ===')
ok = 0
for lev, (we, wde) in exp.items():
    for i, x in enumerate(ls):
        if x.startswith(' 34S   L '):
            e = x[9:19].strip()
            de = x[19:21].strip()
            if e == we:
                good = (e == we and de == wde)
                ok += good
                print(f'  L {we:5} DE={de!r} {"OK" if good else "BAD (want "+wde+")"}')
                break
print(f'corrections OK: {ok}/13')

print()
print('=== comment standardizations ===')
for marker, want in [('E$from 1972Cr08','no period'), ('other: 7388 {I14} (1972Cr08)','lowercase+unc')]:
    hit = any(marker in x for x in ls)
    print(f'  {marker!r}: {"OK" if hit else "MISSING"} ({want})')
# no residual old forms
print('residual "Other: 7388 (1972Cr08).":', sum(1 for x in ls if 'Other: 7388' in x))
print('residual "E$from 1972Cr08.":', sum(1 for x in ls if 'E$from 1972Cr08.' in x))
