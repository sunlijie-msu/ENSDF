# READ-ONLY: build+verify exact old/new for ALL editorial fixes, print for transcription.
path = r'd:\X\ND\ENSDF\A34\S34\new\S34_30si_a_g_a_n_resonances.ens'
t = open(path, encoding='utf-8', newline='').read().replace('\r\n', '\n')
ls = t.split('\n')

def rep(name, old, new):
    print(f'=== {name} === match={old in t}')
    if old in t:
        for o in old.split('\n'):
            print(f'  OLD[{len(o)}sp{len(o)-len(o.rstrip())}]: {o.rstrip()!r}')
        for n in new.split('\n'):
            print(f'  NEW[{len(n)}sp{len(n)-len(n.rstrip())}]: {n.rstrip()!r}')
    print()

# ---- intensity blocks (5) ----
intens = {212: '1300', 265: '700', 299: '1300', 317: '2600', 333: '750'}
# spN per line: cL trailing spaces
cl_sp = {212: 1, 265: 2, 299: 1, 317: 1, 333: 2}
for ln, val in intens.items():
    oldcl = (' 34S  cL $1965Mc07 states that |g intensities = %s from this resonance to 34S' % val).ljust(80)
    # replace the actual trailing with cl_sp[ln]
    oldcl = oldcl[:80 - cl_sp[ln]]
    oldcl += ' ' * cl_sp[ln]
    old2 = ' 34S 2cL levels higher than 3304 keV.'.ljust(80)
    old = oldcl + '\n' + old2
    newcl = (' 34S  cL $1965Mc07 states that |g intensities =%s from this resonance to' % val).ljust(80)
    new2 = ' 34S 2cL {+34}S levels higher than 3304 keV.'.ljust(80)
    new = newcl + '\n' + new2
    rep(f'intensity L(line {ln}, {val})', old, new)

# ---- ground states comment (3 lines) ----
gs_old = []
for i in [4, 5, 6]:  # 0-indexed -> lines 5,6,7
    gs_old.append(ls[i])
gs_old_str = '\n'.join(gs_old)
gs_new = [
    ' 34S  c  The ground states of {+30}Si, |a, and {+34}S are all 0+; therefore, the'.ljust(80),
    ' 34S 2c  resonances in {+34}S populated in {+30}Si+|a have natural parity, and'.ljust(80),
    ' 34S 3c  the |g transitions to the {+34}S g.s. are most likely electric.'.ljust(80),
]
rep('ground-states', gs_old_str, '\n'.join(gs_new))

# ---- 1967Wi01 block (lines 8-15) ----
wi_old = '\n'.join(ls[7:15])
wi_new = [
    ' 34S  c  1967Wi01: {+30}Si(|a,|g) and (|a,n) with 3.25-4.95 MeV |a beams from'.ljust(80),
    ' 34S 2c  the 5.5 MeV Van de Graaff accelerator of the Southern Universities'.ljust(80),
    ' 34S 3c  Nuclear Institute, South Africa. Targets were 15-40 |mg/cm{+2},'.ljust(80),
    ' 34S 4c  45%-95% enriched {+30}Si targets on tantalum backings. |g rays were'.ljust(80),
    ' 34S 5c  detected using NaI(Tl) detectors. Neutrons were detected using a'.ljust(80),
    ' 34S 6c  Harwell-form neutron detector. Measured E|g, I|g, |g(|q), |g|g(|q),'.ljust(80),
    ' 34S 7c  E{-n}, I{-n}, and yields. Deduced resonance levels, J, |p,'.ljust(80),
    ' 34S 8c  multipolarities, mixing ratios, and resonance strengths.'.ljust(80),
]
rep('1967Wi01-block', wi_old, '\n'.join(wi_new))

# ---- E(N)$ bserved -> observed (line 40) ----
old40 = ls[39]
new40 = old40.replace('bserved', 'observed')
rep('E(N) bserved', old40, new40)

# ---- 1975DeZS dangling comma (line 23) ----
old23 = ls[22]
new23 = old23.replace(' strengths. J|p=0+ for {+30}Si ground state,', ' strengths.')
rep('1975DeZS comma', old23, new23)
