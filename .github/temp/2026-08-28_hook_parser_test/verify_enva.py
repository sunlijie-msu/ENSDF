path = r'd:\X\ND\ENSDF\A34\S34\new\S34_33s_d_p.ens'
b = open(path, 'rb').read()
t = b.decode('utf-8').replace('\r\n', '\n')
ls = t.split('\n')
print('CRLF:', b.count(b'\r\n'), 'nonascii:', sum(1 for x in b if x > 127), 'lines:', len(ls))
print('over80:', [(i+1, len(x)) for i, x in enumerate(ls) if len(x) > 80])
print('non-80/0:', [(i+1, len(x)) for i, x in enumerate(ls) if len(x) not in (80,0)][:8])

# verify the 8 levels
want = ['3914','4072','4688','4875','5227','5848','5993','6533']
print()
print('=== revised levels ===')
for w in want:
    for i, x in enumerate(ls):
        if x.startswith(' 34S   L ' + w + ' '):
            e = x[9:19].strip()
            de = x[19:21].strip()
            ok = (e == w and de == '')
            print(f'  L {w:5} line {i+1}: E={e!r} DE={de!r} len={len(x)} {"OK" if ok else "BAD"}')
            break
    else:
        print(f'  L {w}: NOT FOUND!')

# verify no old decimal values remain
print()
print('=== residual old decimal 1973EnVA energies ===')
for i, x in enumerate(ls):
    if x.startswith(' 34S   L '):
        e = x[9:19].strip()
        if e in ('3914.1','4072.4','4687.5','4875.1'):
            print('  STILL PRESENT line', i+1, repr(x))
print('done')
