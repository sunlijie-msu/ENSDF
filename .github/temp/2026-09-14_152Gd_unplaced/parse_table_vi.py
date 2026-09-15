"""Parse Table VI_3rd and report field-level characteristics needed for ENSDF entry."""
import re, json, os

SRC = r"d:\X\ND\ENSDF\XUNDL\2026OSAA_CT11035_152Gd_Table_VI_3rd.md"
NUM_UNC = re.compile(r"^(-?[0-9]*\.?[0-9]+)\s*\(\s*(\d+)\s*\)$")

def parse_unc(cell):
    m = NUM_UNC.match(cell.strip())
    if not m:
        return None
    val, unc = m.group(1), m.group(2)
    dec = len(val.split('.')[1]) if '.' in val else 0
    return val, dec, unc

rows = []
with open(SRC, encoding='utf-8') as fh:
    for ln, line in enumerate(fh, 1):
        s = line.rstrip('\n')
        if not s.startswith('|'):
            continue
        cells = [c.strip() for c in s.strip().strip('|').split('|')]
        if len(cells) != 3:
            print("COLCOUNT", ln, len(cells), s)
            continue
        if cells[0].startswith('E_gamma') or set(cells[0]) <= set(':- '):
            continue
        e = parse_unc(cells[0])
        if e is None:
            print("BAD E", ln, repr(cells[0]))
            continue
        ri = parse_unc(cells[1]) if cells[1] else None
        if cells[1] and ri is None:
            print("BAD RI", ln, repr(cells[1]))
        coinc = cells[2]
        if coinc not in ('*', ''):
            print("BAD COINC", ln, repr(coinc))
        rows.append(dict(line=ln, e_raw=cells[0], e=e[0], e_dec=e[1], de=e[2],
                         ri_raw=cells[1], ri=ri[0] if ri else None,
                         ri_dec=ri[1] if ri else None, dri=ri[2] if ri else None,
                         coinc=coinc))

print("rows:", len(rows))
bad = [(r['line'], rows[i-1]['e'], r['e']) for i, r in enumerate(rows) if i and float(r['e']) <= float(rows[i-1]['e'])]
print("non-ascending pairs:", len(bad), bad[:5])
print("max DE digits:", max(len(r['de']) for r in rows))
print("max E decimals:", max(r['e_dec'] for r in rows))
print("max E str len:", max(len(r['e']) for r in rows))
print("max RI str len:", max((len(r['ri']) for r in rows if r['ri']), default=0))
over = [r for r in rows if r['ri'] and len(r['ri']) > 7]
print("RI strings >7 chars:", len(over), [(r['e'], r['ri'], r['dri']) for r in over][:10])
print("max DRI digits:", max((len(r['dri']) for r in rows if r['dri']), default=0))
print("max RI decimals:", max((r['ri_dec'] for r in rows if r['ri']), default=0))
print("rows with RI:", sum(1 for r in rows if r['ri']), "without:", sum(1 for r in rows if not r['ri']))
print("coinc '*':", sum(1 for r in rows if r['coinc'] == '*'), "blank:", sum(1 for r in rows if r['coinc'] == ''))
print("blank-coinc & no RI:", sum(1 for r in rows if r['coinc'] == '' and not r['ri']))
print("blank-coinc & RI:", sum(1 for r in rows if r['coinc'] == '' and r['ri']))
for r in rows:
    if len(r['e']) > 10:
        print("E too wide", r['e_raw'])
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'table_vi_rows.json')
json.dump(rows, open(out, 'w'), indent=1)
print("wrote", out)
