# Generate exact 80-column ENSDF lines for 1975DeZS resonance data (34S)
# Four L records with cL comments only.
def L(e, de, jp):
    # NUCID(1-5) CONT(6) BLANK(7) L(8) BLANK(9) E(10-19) DE(20-21) SPACE(22) J(23-39)
    return (' 34S   L ' + e.ljust(10) + de.rjust(2) + ' ' + jp.ljust(17)).ljust(80)

def cL(t):
    # comment text starts at col 10
    return (' 34S  cL ' + t).ljust(80)

# E(C.N.) keV, Jpi, omegagamma (eV), main branch %, final level (keV)
data = [
    ('10382', '1-', '0.05', '26', '3914'),
    ('10386', '3-', '0.2',  '40', '5680'),
    ('10443', '3-', '0.09', '51', '3303'),
    ('10482', '0+', '0.08', '73', '4073'),
]

lines = []
for e, jp, omegag, ri, ef in data:
    lines.append(L(e, '4', jp))
    lines.append(cL('$(2J+1)|G{-|g}|G{-|a}/|G=%s eV {I20}' % omegag))
    lines.append(cL('$Main |g-decay branch: %s%% to %s level (1975DeZS)' % (ri, ef)))

for ln in lines:
    print(len(ln) - len(ln.rstrip()), '|' + ln.rstrip() + '|')
