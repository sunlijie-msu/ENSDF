path = r'd:\X\ND\ENSDF\A34\S34\new\S34_30si_a_g_a_n_resonances.ens'
t = open(path, encoding='utf-8', newline='').read().replace('\r\n', '\n')
ls = t.split('\n')

# target G energies per Va08 level (col-77 flag -> V)
targets = {
    9932: ['7804', '9930'],
    9981: ['7853', '9979'],
    10097: ['7968', '10095'],
    10169: ['8040', '10167'],
    10249: ['8120', '10247'],
    10317: ['8188', '10315'],
    10408: ['8279', '10406'],
    10494: ['8365', '10492'],
    10587: ['7282', '8458'],
    10625: ['8496', '10623'],
    10670: ['7365', '8541', '10668'],
    10768: ['8639', '10766'],
}

# find G lines: match lines starting with ' 34S   G <energy>'
gmap = {}  # energy -> (lineno, line)
for i, x in enumerate(ls):
    if x.startswith(' 34S   G '):
        e = x[9:19].strip()  # cols 10-19
        if e.isdigit():
            gmap.setdefault(e, []).append((i, x))

problems = []
repls = []
for lev, enes in targets.items():
    for en in enes:
        if en not in gmap:
            problems.append(f'G {en} (lev {lev}): NOT FOUND')
            continue
        if len(gmap[en]) > 1:
            problems.append(f'G {en} (lev {lev}): DUPLICATE {len(gmap[en])}')
            continue
        lineno, line = gmap[en][0]
        if len(line) != 80:
            problems.append(f'G {en}: len {len(line)} != 80')
            continue
        if line[76] != ' ':
            problems.append(f'G {en}: col77 already occupied -> {line[76]!r}')
            continue
        newline = line[:76] + 'V' + line[77:]
        repls.append((en, lev, lineno, line, newline))

print(f'total targets: {sum(len(v) for v in targets.values())}, found: {len(repls)}')
if problems:
    print('PROBLEMS:')
    for p in problems:
        print('  ', p)
else:
    print('no problems; all col-77 are spaces, all unique, all len 80')

# verify uniqueness of old lines across file
for en, lev, lineno, line, newline in repls:
    assert t.count(line) == 1, f'G {en} old line not unique: {t.count(line)}'
    assert len(newline) == 80, f'G {en} newline len {len(newline)}'

# print old/new for transcription
for en, lev, lineno, line, newline in repls:
    print(f'--- G {en} (lev {lev}) line {lineno+1} ---')
    print('OLD:', repr(line))
    print('NEW:', repr(newline))
