# READ-ONLY: build+verify exact old/new for partial-width labels and editorial fixes.
path = r'd:\X\ND\ENSDF\A34\S34\new\S34_30si_a_g_a_n_resonances.ens'
t = open(path, encoding='utf-8', newline='').read().replace('\r\n', '\n')
lines = t.split('\n')

print('======= PART 1: partial widths (add (1965Mc07)) =======')
# unique values: substring + 12 spaces
unique = {
    '3 eV': '10791', '2.6 eV': '11142', '2.8 eV': '11233', '0.08 eV': '11315',
    '2.2 eV': '11323', '1.5 eV': '11372', '0.1 eV': '11381', '4.4 eV': '11420',
    '0.6 eV': '11490', '1.0 eV': '11545', '2.3 eV': '11643',
}
for val, lev in unique.items():
    sub = '$|G{-|g}=%s' % val
    old = sub + ' ' * 12
    cnt = t.count(sub)
    print(f'L{lev}: {sub!r} cnt={cnt} match={old in t}')
# duplicates: need L-record context
dups = [('1.7 eV', '11025'), ('1.7 eV', '11165'), ('0.2 eV', '11088'), ('0.2 eV', '11220')]
for val, lev in dups:
    sub = '$|G{-|g}=%s' % val
    # find L record line
    lrec = None
    for x in lines:
        if len(x) >= 19 and x[5:9] == '  L ' and x[9:19].strip() == lev:
            lrec = x
            break
    old = lrec + '\n' + ' 34S  cL ' + sub + ' ' * 12
    print(f'L{lev}: dup {val!r} lrec-found={lrec is not None} match={old in t}')
