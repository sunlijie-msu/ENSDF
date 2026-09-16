"""Verify every (E_i, E_gamma, I_gamma) triple quoted in the 3rd report against Table II.

Also re-derives the Case 1 (identical Eg, different Ig) and Case 2 (different Eg,
identical Ig, one-sided asterisk) pair sets and asserts the report lists them all,
with the partner asterisk state as stated in the report prose.
"""
import re
import sys

TP = r'D:\X\ND\ENSDF\XUNDL\2026OSAA_CT11035_152Gd_Table_II.md'
RP = r'D:\X\ND\ENSDF\XUNDL\2026OSAA_CT11035_152Gd_Data_Check_Report_3rd.txt'
TOL = 1.0

rows = []
for ln in open(TP, encoding='utf-8-sig').read().splitlines():
    if ln.startswith('|'):
        c = [x.strip() for x in ln.strip().strip('|').split('|')]
        if len(c) >= 5 and re.match(r'^[0-9]+\.[0-9]', c[1]):
            rows.append(dict(Ei=c[0], Es=c[1], Is=c[2], star='*' in c[2]))
assert len(rows) == 751, len(rows)


def val(s):
    m = re.match(r'^([0-9.]+)\s*(?:\(([0-9]+)\))?', s.rstrip('*').strip())
    return float(m.group(1)) if m else None


for r in rows:
    r['E'] = val(r['Es'])
    r['I'] = val(r['Is']) if r['Is'].strip() else None
placed = [r for r in rows if r['star']]
assert len(placed) == 53, len(placed)

# ---- quoted triples in the report -----------------------------------------
text = open(RP, encoding='utf-8').read()
QUOTED = re.compile(
    r'E\u03b3=([0-9]+\.[0-9]+)\(([0-9]+)\)(\*?),\s*I\u03b3=([0-9.]+)\(([0-9]+)\)\s*placed at level ([0-9]+\.[0-9]+)')
quoted = [dict(Es='%s (%s)' % (m.group(1), m.group(2)), star=m.group(3) == '*',
               Is='%s (%s)' % (m.group(4), m.group(5)), Ei=m.group(6)) for m in QUOTED.finditer(text)]
print('quoted placements:', len(quoted))

# ---- case pair sets from Table II ----------------------------------------
pairs = {'A': [], 'B': [], 'C': [], 'D': []}
for r in placed:
    for q in rows:
        if q is r or abs(q['E'] - r['E']) > TOL:
            continue
        same_e = abs(q['E'] - r['E']) < 0.005
        same_i = not (r['I'] is None or q['I'] is None) and abs(r['I'] - q['I']) < 1e-12
        pairs['A' if (same_e and same_i) else 'B' if same_e else 'C' if same_i else 'D'].append((r, q))
assert [len(pairs[k]) for k in 'ABCD'] == [4, 7, 15, 40], {k: len(v) for k, v in pairs.items()}
assert all(not q['star'] for _, q in pairs['C']), 'case C partner carries an asterisk'

case1 = sorted({tuple(sorted([r['Es'], q['Es']])) for r, q in pairs['B']})
case2 = sorted({tuple(sorted([r['Es'], q['Es']])) for r, q in pairs['C']})
print('case 1 distinct pairs:', len(case1), 'case 2 distinct pairs:', len(case2))
assert len(case1) == 4 and len(case2) == 15

# every case-1 and case-2 pair must appear in the report as E values with asterisk marks
missing = []


def report_pattern(r):
    es = re.sub(r'\s+', '', r['Es'])
    isv = r['Is'].replace(' ', '').rstrip('*')
    pat = (r'E\u03b3=' + re.escape(es) + (r'\*' if r['star'] else r'') +
           r', I\u03b3=' + re.escape(isv) +
           r' placed at level ' + re.escape(r['Ei'].split(' ')[0]))
    return re.compile(pat)


for a, b in case1 + case2:
    hit = False
    for r in [x for x in rows if x['Es'] in (a, b) and x['Is'].strip()]:
        if report_pattern(r).search(text):
            hit = True
    if not hit:
        missing.append((a, b))
print('case pairs absent from the report:', missing)
assert not missing, missing

# ---- every quoted triple must exist in Table II, asterisk included --------
fail = 0
for t in quoted:
    hit = [r for r in rows if r['Es'] == t['Es'] and r['Is'].replace('*', '').strip() == t['Is']
           and r['Ei'].split(' ')[0] == t['Ei']]
    if len(hit) != 1:
        print('MISSING/AMBIGUOUS', t, len(hit))
        fail += 1
        continue
    if hit[0]['star'] != t['star']:
        print('ASTERISK MISMATCH', t)
        fail += 1
print('triple mismatches:', fail)
print('--- FAILURES:', fail, '---')
sys.exit(1 if fail else 0)
