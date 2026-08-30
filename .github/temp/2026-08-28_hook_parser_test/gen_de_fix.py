path = r'd:\X\ND\ENSDF\A34\S34\new\S34_33s_d_p.ens'
t = open(path, encoding='utf-8', newline='').read().replace('\r\n', '\n')
ls = t.split('\n')

# level energy -> (new_E, new_DE); None means keep E
changes = {
    '4627': ('4627', '5'),
    '5384': ('5384', '6'),
    '6174': ('6174', '8'),
    '6254': ('6254', '8'),
    '6345': ('6345', '8'),
    '6482': ('6482', '8'),
    '6640': ('6640', '9'),
    '6690': ('6690', '9'),
    '6959': ('6959', '10'),
    '7114': ('7114', '10'),
    '7393': ('7393', '14'),
    '7632': ('7632', '10'),
    '7753': ('7753', '11'),
    '7783': ('7784', '11'),
}

repls = []
for i, x in enumerate(ls):
    if not x.startswith(' 34S   L '):
        continue
    e = x[9:19].strip()
    if e in changes:
        new_e, new_de = changes[e]
        if len(x) != 80:
            print(f'L {e}: len {len(x)}')
            continue
        old_de = x[19:21].strip()
        # E field cols 10-19, DE cols 20-21 left-justified
        newline = x[:9] + new_e.ljust(10) + new_de.ljust(2) + x[21:]
        if len(newline) != 80:
            print(f'L {e}: newline len {len(newline)}')
            continue
        repls.append((e, old_de, new_e, new_de, x, newline))
        print(f'L {e}: E={x[9:19].strip()} DE={old_de!r} -> E={new_e} DE={new_de}')
        print('  OLD:', repr(x))
        print('  NEW:', repr(newline))

print()
print('total:', len(repls))
for e, od, ne, nd, old, newline in repls:
    print(f'  L {e}: unique={t.count(old)==1}')
