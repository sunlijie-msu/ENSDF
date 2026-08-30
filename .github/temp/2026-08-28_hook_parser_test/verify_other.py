path = r'd:\X\ND\ENSDF\A34\S34\new\S34_33s_d_p.ens'
b = open(path, 'rb').read()
t = b.decode('utf-8').replace('\r\n', '\n')
ls = t.split('\n')
print('CRLF:', b.count(b'\r\n'), 'nonascii:', sum(1 for x in b if x > 127), 'lines:', len(ls))
print('over80:', [(i+1, len(x)) for i, x in enumerate(ls) if len(x) > 80])
print('non-80/0:', [(i+1, len(x)) for i, x in enumerate(ls) if len(x) not in (80,0)][:8])

print()
print('=== E$other: (1971Va21) comments ===')
want = {'2122':'2127','5326':'5318','5683':'5680','5694':'5687','5758':'5759','6422':'6423','4888':'4891'}
found = {}
for lev, val in want.items():
    for i, x in enumerate(ls):
        if x.startswith(' 34S   L ' + lev + ' '):
            # check next lines for other comment
            for j in range(i+1, min(i+4, len(ls))):
                if 'other:' in ls[j]:
                    found[lev] = (ls[j].strip(), i+1)
                    break
            break
for lev, val in want.items():
    if lev in found:
        ok = f'other: {val} (1971Va21)' in found[lev][0]
        print(f'  L {lev:5}: {found[lev][0]:45} line {found[lev][1]} {"OK" if ok else "BAD"}')
    else:
        print(f'  L {lev:5}: NOT FOUND')
