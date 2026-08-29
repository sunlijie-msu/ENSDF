path = r'd:\X\ND\ENSDF\A34\S34\new\S34_30si_a_g_a_n_resonances.ens'
t = open(path, encoding='utf-8', newline='').read().replace('\r\n', '\n')
ls = t.split('\n')

# Wi01 single-gamma levels: gamma -> level
targets = [
    ('8718', 10847), ('8802', 10931), ('8865', 10994), ('8886', 11015),
    ('8979', 11108), ('9143', 11272), ('9329', 11458), ('9344', 11473),
    ('9377', 11506), ('9583', 11712), ('9793', 11922), ('11930', 11932),
    ('9828', 11957), ('12032', 12034), ('12098', 12100), ('12192', 12194),
]

gmap = {}
for i, x in enumerate(ls):
    if x.startswith(' 34S   G '):
        e = x[9:19].strip()
        if e.isdigit():
            gmap.setdefault(e, []).append((i, x))

problems = []
repls = []
for en, lev in targets:
    if en not in gmap:
        problems.append(f'G {en}: NOT FOUND'); continue
    if len(gmap[en]) > 1:
        problems.append(f'G {en}: DUP {len(gmap[en])}'); continue
    lineno, line = gmap[en][0]
    if len(line) != 80:
        problems.append(f'G {en}: len {len(line)}'); continue
    ri = line[22:29]  # cols 23-29
    if ri.strip() != '':
        problems.append(f'G {en}: RI not blank -> {ri!r}'); continue
    if line[76] != ' ':
        problems.append(f'G {en}: col77 occupied -> {line[76]!r}'); continue
    newline = line[:22] + '100    ' + line[29:76] + 'W' + line[77:]
    assert len(newline) == 80
    repls.append((en, lev, lineno, line, newline))

print(f'targets: {len(targets)}, found: {len(repls)}')
if problems:
    print('PROBLEMS:')
    for p in problems: print('  ', p)
else:
    print('all RI blank, all col77 blank, all len 80')

# uniqueness check + print
for en, lev, lineno, line, newline in repls:
    assert t.count(line) == 1, f'G {en} not unique: {t.count(line)}'
    print(f'--- G {en} (lev {lev}) line {lineno+1} ---')
    print('OLD:', repr(line))
    print('NEW:', repr(newline))
