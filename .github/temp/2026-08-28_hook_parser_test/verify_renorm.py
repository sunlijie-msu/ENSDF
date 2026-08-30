path = r'd:\X\ND\ENSDF\A34\S34\new\S34_30si_a_g_a_n_resonances.ens'
b = open(path, 'rb').read()
t = b.decode('utf-8').replace('\r\n', '\n')
ls = t.split('\n')
print('CRLF:', b.count(b'\r\n'), 'nonascii:', sum(1 for x in b if x > 127), 'lines:', len(ls))
print('over80:', [(i+1, len(x)) for i, x in enumerate(ls) if len(x) > 80])
print('non-80/0:', [(i+1, len(x)) for i, x in enumerate(ls) if len(x) not in (80,0)][:10])

# expected new RI per level
exp = {
    11165: {'7860':'100','9036':'13.1','11163':'76.9'},
    11220: {'7915':'100','9091':'48.4','11218':'32.3'},
    11233: {'7928':'100','9104':'3.7','11231':'24.4'},
    11358: {'8053':'100','9229':'17.5','11356':'35.7'},
    11372: {'8067':'43.5','9243':'100','11370':'5.9'},
    11381: {'8076':'100','9252':'33.0','11379':'37.0'},
    11545: {'8240':'100','9416':'60.0','11543':'62.5'},
}
# comment expected
com = {11220:'419', 11381:'259', 11545:'1625'}

def ginfo(en):
    for i, x in enumerate(ls):
        if x.startswith(' 34S   G ' + en + ' '):
            return x[22:29].strip()
    return None

bad = []
for lev, gs in exp.items():
    for en, want in gs.items():
        got = ginfo(en)
        if got != want:
            bad.append((lev, en, got, want))
print()
print('=== G RI check ===')
for lev, gs in exp.items():
    for en, want in gs.items():
        got = ginfo(en)
        print(f'  lev {lev} G {en}: RI={got:>5} (want {want:>5}) {"OK" if got==want else "BAD"}')
print('G RI problems:', len(bad))

# comment check
print()
print('=== comment check ===')
for lev, want in com.items():
    for i, x in enumerate(ls):
        if f'intensities = {want}' in x and x.startswith(' 34S  cL $'):
            # ensure it's the right level (within block)
            print(f'  lev {lev}: comment "intensities = {want}" found at line {i+1}')
            break
    else:
        print(f'  lev {lev}: comment {want} NOT FOUND!')

# verify max RI = 100 for the 7 levels
print()
print('=== verify strongest=100 for 7 levels ===')
for lev, gs in exp.items():
    vals = [float(v) for v in gs.values()]
    mx = max(vals)
    print(f'  lev {lev}: max RI = {mx:g} {"OK" if abs(mx-100)<1e-9 else "BAD"}')
