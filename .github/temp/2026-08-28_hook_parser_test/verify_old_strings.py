# Verify exact OLD strings (content + explicit spaces) are present in the file.
path = r'd:\X\ND\ENSDF\A34\S34\new\S34_30si_a_g_a_n_resonances.ens'
t = open(path, encoding='utf-8', newline='').read().replace('\r\n', '\n')

def gx(val, sp):
    return ' 34S   G x            ' + str(val) + ' ' * sp  # NOTE: uses full width

# Build exact lines from verified sp counts
GX1300 = ' 34S   G x            1300' + ' ' * 54
GX700  = ' 34S   G x            700'  + ' ' * 55
GX2600 = ' 34S   G x            2600' + ' ' * 54
GX750  = ' 34S   G x            750'  + ' ' * 55
CGRI   = ' 34S  cG RI$from 1965Mc07'  + ' ' * 55
G7915  = ' 34S   G 7915         130'  + ' ' * 55
G8075  = ' 34S   G 8075         270'  + ' ' * 55

cases = {
    'A L11220 old': GX1300 + '\n' + G7915,
    'B L11381 old': GX700,
    'C L11490 old': GX1300 + '\n' + CGRI,
    'D L11545 old': GX2600 + '\n' + CGRI,
    'E L11643 old': GX750 + '\n' + CGRI,
}
for name, s in cases.items():
    print(f'{name}: {"MATCH" if s in t else "NO-MATCH"} (len={len(s)})')
    if s not in t:
        # find closest
        for probe in t.split('\n'):
            if 'G x' in probe:
                pass
