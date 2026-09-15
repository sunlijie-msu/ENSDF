"""Generate ENSDF unplaced G-records (80 cols) from the parsed Table VI_3rd rows.

Layout (G record):
  cols 1-5   NUCID      152GD
  col  6     continuation (blank)
  col  7     blank
  col  8     'G'
  col  9     blank
  cols 10-19 E   (left justified)
  cols 20-21 DE  (left justified, digits in last place of E)
  col  22    blank
  cols 23-29 RI  (left justified; E-notation when the plain value needs > 7 chars)
  cols 30-31 DRI (left justified)
  cols 32-76 blank
  col  77    comment flag: 'X' where the source marks coincidence, else blank
  cols 78-80 blank
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
rows = json.load(open(os.path.join(HERE, 'table_vi_rows.json')))
NUCID = '152GD'


def sci(value):
    """0.000182 -> '1.82E-4' (keeps all source significant digits)."""
    intpart, frac = value.split('.')
    assert intpart == '0', value
    lead = len(frac) - len(frac.lstrip('0'))
    sig = frac[lead:]
    return '%s.%sE-%d' % (sig[0], sig[1:], lead + 1)


def ri_field(ri, dri):
    if not ri:
        return ' ' * 7, ' ' * 2
    s = ri if len(ri) <= 7 else sci(ri)
    assert len(s) <= 7, s
    return s.ljust(7), dri.ljust(2)


lines = []
for r in rows:
    ri, dri = ri_field(r['ri'], r['dri'])
    line = (NUCID + '  G ' + r['e'].ljust(10) + r['de'].ljust(2) + ' ' +
            ri + dri + ' ' * 45 + ('X' if r['coinc'] == '*' else ' ') + '   ')
    assert len(line) == 80, (len(line), line)
    lines.append(line)

existing = '152GD  G 136.0     9                                                        X   '
print("row 1 reproduces existing record:", lines[0] == existing)
print("records generated:", len(lines))
print("first:", lines[0])
print("last :", lines[-1])
for l in lines:
    if 'E-' in l[22:31]:
        print("ENOTATION:", l)
out = os.path.join(HERE, 'expected_block.txt')
with open(out, 'w', encoding='ascii', newline='\n') as fh:
    fh.write('\n'.join(lines) + '\n')
print("wrote", out)
