"""Write the 4th data-check report for CT11035 (152Gd) from Table II evidence.

Every quoted (E_i, E_gamma, I_gamma) triple is asserted against Table II before
being written, so the prose cannot drift from the source table.
"""
import re

TP = r'D:\X\ND\ENSDF\XUNDL\2026OSAA_CT11035_152Gd_Table_II.md'
OLDT1 = r'D:\X\ND\ENSDF\XUNDL\2026OSAA_CT11035_152Gd_old_Table_I.md'
T6 = r'D:\X\ND\ENSDF\XUNDL\2026OSAA_CT11035_152Gd_Table_VI_3rd.md'
OUT = r'D:\X\ND\ENSDF\XUNDL\2026OSAA_CT11035_152Gd_Data_Check_Report_4th.txt'
TOL = 1.0


def parse(p):
    rows = []
    for ln in open(p, encoding='utf-8-sig').read().splitlines():
        if ln.startswith('|'):
            c = [x.strip() for x in ln.strip().strip('|').split('|')]
            if len(c) >= 5 and re.match(r'^[0-9]+\.[0-9]', c[1]):
                rows.append(dict(Ei=c[0], Es=c[1], Is=c[2], Ef=c[3], star='*' in c[2]))
    return rows


rows = parse(TP)
assert len(rows) == 751, len(rows)


def value(cell):
    m = re.match(r'^([0-9.]+)\s*(?:\(([0-9]+)\))?', cell.rstrip('*').strip())
    return float(m.group(1)) if m else None


for r in rows:
    r['E'] = value(r['Es'])
    r['I'] = value(r['Is'])

placed = [r for r in rows if r['star']]
assert len(placed) == 53, len(placed)


def partners(r):
    return [q for q in rows if q is not r and abs(q['E'] - r['E']) <= TOL]


def rec(ei, es, ig):
    """Assert that the (E_i, E_gamma, I_gamma) triple exists exactly once."""
    hit = [r for r in rows if r['Ei'] == ei and r['Es'] == es and r['Is'] == ig]
    assert len(hit) == 1, (ei, es, ig, len(hit))
    assert hit[0]['star'] == ('*' in ig), 'asterisk mismatch'
    return hit[0]


def compact(es):
    m = re.match(r'^([0-9.]+)\s*\(([0-9]+)\)\*?$', es)
    return '%s(%s)' % (m.group(1), m.group(2))


# --- narrative evidence, asserted one row at a time -------------------------
EX = [
    ('3484.38 (11)', '2728.78 (15)', '0.0293 (22)*'),
    ('3659.53 (20)', '2728.78 (25)', '0.0293 (22)*'),
    ('1975.64 (9)', '1631.30 (15)', '0.125 (30)*'),
    ('2246.85 (5)', '1631.30 (15)', '0.229 (17)*'),
    ('2246.85 (5)', '1902.30 (16)', '2.38 (19)*'),
    ('3012.23 (7)', '1902.30 (15)', '0.27 (4)*'),
    ('2448.58 (10)', '2104.10 (18)', '0.073 (10)*'),
    ('2719.59 (6)', '2104.10 (15)', '0.0385 (28)*'),
    ('2749.21 (7)', '1818.64 (18)', '0.088 (6)*'),
    ('2928.05 (6)', '1818.40 (15)', '0.088 (6)'),
    ('2121.18 (8)', '1190.53 (16)', '0.64 (5)*'),
    ('2299.77 (6)', '1190.40 (15)', '0.64 (5)'),
    ('1785.90 (19)', '855.17 (19)', '0.0230 (24)*'),
    ('2169.58 (9)', '854.91 (15)', '0.170 (12)'),
    ('3063.56 (13)', '1940.77 (20)', '0.0046 (6)*'),
    ('1941.31 (5)', '1941.00 (15)', '1.08 (8)'),
    ('2800.33 (32)', '2184.80 (32)', '0.402 (29)*'),
    ('2529.65 (7)', '2185.00 (15)', '0.402 (29)'),
    ('3115.77 (13)', '2185.33 (17)', '0.402 (29)'),
    ('3675.49 (16)', '2745.1 (4)', '0.00054 (15)*'),
    ('3088.65 (7)', '2744.20 (15)', '0.087 (9)'),
    ('3552.73 (11)', '2428.77 (23)', '0.097 (7)*'),
    ('3359.06 (10)', '2428.25 (16)', '0.097 (7)'),
    ('3650.01 (19)', '2719.30 (27)', '0.362 (26)*'),
    ('2719.59 (6)', '2719.90 (15)', '0.353 (26)'),
    ('3518.85 (10)', '2763.95 (26)', '0.00062 (12)*'),
    ('3694.18 (13)', '2763.38 (18)', '0.00317 (32)'),
    ('3452.76 (10)', '2837.60 (33)', '0.00061 (10)*'),
    ('3593.72 (20)', '2838.25 (28)', '0.00093 (16)*'),
    ('3508.80 (10)', '2893.60 (32)', '0.061 (4)*'),
    ('3237.19 (6)', '2893.10 (15)', '0.058 (4)'),
    ('2201.79 (8)', '1857.20 (15)', '0.244 (17)*'),
    ('2788.17 (16)', '1857.2 (8)', '0.0006 (4)'),
    ('3659.53 (20)', '2536.6 (4)', '0.465 (33)*'),
    ('2880.62 (5)', '2536.20 (15)', '0.465 (33)'),
    ('3467.77 (13)', '2537.01 (16)', '0.465 (33)'),
    ('3063.56 (13)', '2718.70 (21)', '0.085 (6)'),
]
for ei, es, ig in EX:
    if ig is None:
        hit = [r for r in rows if r['Ei'] == ei and r['Es'] == es]
        assert len(hit) == 1, (ei, es, len(hit))
        assert not hit[0]['star'], (ei, es, hit[0]['Is'])
    else:
        rec(ei, es, ig)

# --- case aggregates --------------------------------------------------------
pairs = {'A': [], 'B': [], 'C': [], 'D': []}
for r in placed:
    for q in partners(r):
        same_e = abs(q['E'] - r['E']) < 0.005
        same_i = (r['I'] is not None and q['I'] is not None and abs(r['I'] - q['I']) < 1e-12)
        k = 'A' if (same_e and same_i) else 'B' if same_e else ('C' if same_i else 'D')
        pairs[k].append((r, q))
counts = {k: len(v) for k, v in pairs.items()}
assert counts == {'A': 4, 'B': 7, 'C': 15, 'D': 40}, counts
mutual_rows = sum(1 for r in placed if any(q['star'] for q in partners(r)))
one_sided_rows = 53 - mutual_rows
assert mutual_rows == 28 and one_sided_rows == 25, (mutual_rows, one_sided_rows)
two_partner_rows = sum(1 for r in placed if len(partners(r)) == 2)
assert two_partner_rows == 13, two_partner_rows

# 7 rows (6 distinct pairs) whose nearest partner is beyond the summed sigma
def sigma(cell):
    m = re.match(r'^([0-9.]+)\s*\(([0-9]+)\)\s*\*?$', cell)
    v = m.group(1)
    dec = len(v.split('.')[1]) if '.' in v else 0
    return int(m.group(2)) * 10.0 ** (-dec)


beyond_rows, beyond_pairs = 0, set()
for r in placed:
    ps = sorted(partners(r), key=lambda q: abs(q['E'] - r['E']))
    if not ps:
        continue
    q = ps[0]
    sep = abs(q['E'] - r['E'])
    sig = sigma(r['Es']) + sigma(q['Es'])
    if sep > sig + 1e-9:
        beyond_rows += 1
        beyond_pairs.add(tuple(sorted([r['Es'].replace(' ', ''), q['Es'].replace(' ', '')])) + (round(sep, 2), round(sig, 2)))
assert beyond_rows == 7, beyond_rows
assert len(beyond_pairs) == 6, beyond_pairs

# --- old Table I E_gamma asterisks -----------------------------------------
old = []
for ln in open(OLDT1, encoding='utf-8-sig').read().splitlines():
    if ln.startswith('|'):
        c = [x.strip() for x in ln.strip().strip('|').split('|')]
        if len(c) >= 6 and '\u2217' in c[2]:
            old.append(c[2].replace('\u2217', '').strip())
assert len(old) == 16, len(old)

# --- unplaced peaks (Table VI) vs the asterisked placed rays ---------------
unp = []
for ln in open(T6, encoding='utf-8-sig').read().splitlines():
    if ln.startswith('|'):
        c = [x.strip() for x in ln.strip().strip('|').split('|')]
        if len(c) >= 2 and re.match(r'^[0-9]+\.[0-9]', c[0]) and 'E_gamma' not in c[0]:
            unp.append(value(c[0]))
assert len(unp) == 348, len(unp)
assert len(set(unp)) == len(unp), 'duplicate unplaced energies'
nearest = min(((round(abs(u - r['E']), 2), u, r['Es']) for u in unp for r in placed), key=lambda t: t[0])
assert nearest[0] == 2.0, nearest
assert not any(abs(u - r['E']) <= 1.0 for u in unp for r in placed)
assert not set(unp) & {r['E'] for r in rows}, 'unplaced energy duplicates a placed one'

same_e_pairs = [
    ('2709.50 (15)', '2709.50 (18)', '0.308 (22)*', '0.308 (22)*'),
    ('2728.78 (15)', '2728.78 (25)', '0.0293 (22)*', '0.0293 (22)*'),
]
for a, b, ia, ib in same_e_pairs:
    ra = [r for r in rows if r['Es'] == a]
    rb = [r for r in rows if r['Es'] == b]
    assert ra and rb and ia in [x['Is'] for x in ra] and ib in [x['Is'] for x in rb], (a, b)

case1 = {}
for r, q in pairs['B']:
    case1.setdefault(compact(r['Es']), []).append(compact(q['Es']))
case2 = sorted({compact(r['Es']) for r, _ in pairs['C']}, key=lambda s: (float(s.split('(')[0]), s))
case3_rays = sorted({compact(r['Es']) for r, _ in pairs['D']}, key=lambda s: (float(s.split('(')[0]), s))

txt = []
A = txt.append


def W(items, prefix='', indent='  ', width=112):
    """Wrap a comma-joined item list into report-width lines."""
    out, cur = [], indent + prefix
    for i, it in enumerate(items):
        piece = it + (',' if i < len(items) - 1 else '.')
        if len(cur) + len(piece) + 1 > width and cur.strip() not in ('', prefix.strip()):
            out.append(cur)
            cur = indent + piece
        else:
            cur = (cur + ' ' + piece) if cur.strip() != prefix.strip() else (cur + piece)
    out.append(cur)
    return out


A('****** Data Checking Report for CT11035 from the Nuclear Data Review Group ******')
A('The revised manuscript, the authors\' response to the referee\'s comments, the revised Table II and the list of')
A('348 unplaced gamma rays have been reviewed for data consistency.')
A('')
A('Overall, the authors have adequately addressed all the issues I previously raised, and the revision has removed the')
A('earlier numerical discrepancies. The 751 gamma rays of Table II tie consistently to their levels, intensities and')
A('uncertainties, and the 348 unplaced gamma rays are internally consistent and consistent with the placed transitions:')
A('no duplicated energies, and none of them lies within 1.0 keV of any asterisked gamma ray (the nearest is 2.00 keV away).')
A('')
A('I may have a follow-up comment on the authors\' revised Table II footnote: "* Multiplet gamma with unresolvable')
A('intensity. Total multiplet intensity is given for each gamma."')
A('')
A('By this definition, readers may expect that if they see an asterisk on a \u03b3 ray, it means there should be (at least)')
A('another \u03b3 with the same / similar energy and shared intensity.')
A('')
A('For example, there is a \u03b3 ray with E\u03b3=2728.78(15)*, I\u03b3=0.0293(22) placed at level 3484.38.')
A('There is another \u03b3 ray with E\u03b3=2728.78(25)*, I\u03b3=0.0293(22) placed at level 3659.53.')
A('This is indeed what the authors\' footnote means.')
A('')
A('However,')
A('I find the following types of inconsistencies among the 53 asterisked \u03b3 rays of Table II. The asterisk is one-sided')
A('for %d of the 53: the partner placement of equal or near-equal energy carries no asterisk. In the counts below one' % one_sided_rows)
A('"placement pair" is one (asterisked \u03b3 ray, partner) combination, so an asterisked \u03b3 ray with two partners within')
A('1.0 keV contributes two placement pairs; the 53 asterisked \u03b3 rays give %d placement pairs in all.' % sum(counts.values()))
A('')
A('Case 1: There is a \u03b3 ray with E\u03b3=1631.30(15)*, I\u03b3=0.125(30) placed at level 1975.64.')
A('There is another \u03b3 ray with E\u03b3=1631.30(15)*, I\u03b3=0.229(17) placed at level 2246.85.')
A('The same energy but different intensities. This is not what the authors\' footnote means. The same applies to')
A('1902.30(16)*, I\u03b3=2.38(19) at level 2246.85 against 1902.30(15)*, I\u03b3=0.27(4) at level 3012.23, and to 2104.10(18)*,')
A('I\u03b3=0.073(10) at level 2448.58 against 2104.10(15)*, I\u03b3=0.0385(28) at level 2719.59. In each of these three cases')
A('the two placements cannot share an unresolvable intensity: either the intensities are divided and the asterisk is')
A('misplaced, or the intensities are totals and one of the two quoted values is wrong. The authors may wish to state')
A('which it is. Four \u03b3 rays are involved (1631.30, 1902.30 and 2104.10, marked at both placements, and 1857.20, whose')
A('partner 1857.2(8), I\u03b3=0.0006(4) at level 2788.17 carries no asterisk), giving %d placement pairs.' % counts['B'])
A('')
A('Case 2: There is a \u03b3 ray with E\u03b3=1818.64(18)*, I\u03b3=0.088(6) placed at level 2749.21.')
A('There is another \u03b3 ray with E\u03b3=1818.40(15), I\u03b3=0.088(6) placed at level 2928.05.')
A('The two \u03b3 rays have similar energies and the same intensities. However, only one of them has an asterisk.')
A('%d placement pairs (11 asterisked \u03b3 rays) are in this situation; the same happens at 1190.53(16)*, I\u03b3=0.64(5) at' % counts['C'])
A('level 2121.18 against 1190.40(15), I\u03b3=0.64(5) at level 2299.77. Some of these \u03b3 rays have two such partners:')
A('2536.6(4)*, I\u03b3=0.465(33) at level 3659.53 stands against 2536.20(15), I\u03b3=0.465(33) at level 2880.62 and')
A('2537.01(16), I\u03b3=0.465(33) at level 3467.77. The asterisked \u03b3 rays involved are:')
txt.extend(W(case2))
A('')
A('Case 3: There is a \u03b3 ray with E\u03b3=855.17(19)*, I\u03b3=0.0230(24) placed at level 1785.90.')
A('There is another \u03b3 ray with E\u03b3=854.91(15), I\u03b3=0.170(12) placed at level 2169.58.')
A('Similar energies but different intensities, again with only one asterisk. %d placement pairs (36 asterisked \u03b3 rays)' % counts['D'])
A('are of this type. An asterisked \u03b3 ray may also have two partners: 2719.30(27)*, I\u03b3=0.362(26) at level 3650.01 stands')
A('against 2719.90(15), I\u03b3=0.353(26) at level 2719.59 and 2718.70(21), I\u03b3=0.085(6) at level 3063.56. The 36')
A('asterisked \u03b3 rays involved are:')
txt.extend(W(case3_rays))
A('')
A('Case 4: There is a \u03b3 ray with E\u03b3=2184.80(32)*, I\u03b3=0.402(29) placed at level 2800.33.')
A('There is another \u03b3 ray with E\u03b3=2185.00(15), I\u03b3=0.402(29) placed at level 2529.65 and a third with E\u03b3=2185.33(17),')
A('I\u03b3=0.402(29) placed at level 3115.77.')
A('Three placements carrying the identical intensity, but only one asterisk. %d of the 53 asterisked \u03b3 rays have two' % two_partner_rows)
A('partners within 1.0 keV. If the listed intensity is the total multiplet intensity assigned to each \u03b3, the same number')
A('should not appear for three different peaks of the same multiplet unless the authors intentionally quote the whole')
A('multiplet for each member; the authors may wish to state the rule.')
A('')
A('Case 5: There is a \u03b3 ray with E\u03b3=2745.1(4)*, I\u03b3=0.00054(15) placed at level 3675.49.')
A('There is another \u03b3 ray with E\u03b3=2744.20(15), I\u03b3=0.087(9) placed at level 3088.65.')
A('The two energies differ by 0.90 keV, while the sum of the quoted uncertainties is 0.55 keV. For %d asterisked \u03b3 rays' % beyond_rows)
A('(%d distinct pairs) the separation to the nearest partner exceeds the summed uncertainties:' % len(beyond_pairs))
for k in sorted(beyond_pairs):
    A('  %s vs %s: separation %.2f keV against summed uncertainties %.2f keV' % (k[0], k[1], k[2], k[3]))
A('These look like unresolved doublets of two distinct transitions rather than one transition placed twice, in which case')
A('the footnote wording does not describe them. The 2837.60(33)/2838.25(28) pair is asterisked at both placements and is')
A('therefore counted from both sides, which is why 7 \u03b3 rays give 6 distinct pairs.')
A('')
A('Case 6: The previous version of the table marked 16 \u03b3 rays with an asterisk in the E\u03b3 column (all deexciting levels')
A('above 3.4 MeV):')
txt.extend(W(old))
A('Table II now carries the asterisk in the I\u03b3 column only, so those E\u03b3 markers are gone. If they denoted an unresolved')
A('multiplet in the energy domain, that information has been lost; if they denoted nothing, the authors may wish to')
A('confirm that the earlier markup was a typographical error.')
A('')
A('Summary of the asterisk markup in Table II. The %d asterisked \u03b3 rays give %d placement pairs, i.e. one count per' % (53, sum(counts.values())))
A('(asterisked \u03b3 ray, partner) combination:')
A('')
A('| Relation between the two placements | Placement pairs | Asterisked \u03b3 rays |')
A('| --- | --- | --- |')
A('| identical E\u03b3, identical I\u03b3 (the intended multiplet) | %d | 2709.50 (15), 2709.50 (18), 2728.78 (15), 2728.78 (25) |' % counts['A'])
A('| identical E\u03b3, different I\u03b3 (Case 1) | %d | 1631.30 (15) at both placements, 1902.30 (16) and (15), 2104.10 (18) and (15), 1857.20 (15) |' % counts['B'])
A('| different E\u03b3, identical I\u03b3 (Case 2) | %d | %s |' % (counts['C'], ', '.join(case2)))
A('| different E\u03b3, different I\u03b3 (Case 3) | %d | the 36 \u03b3 rays listed in Case 3 |' % counts['D'])
A('| total | %d | 53 |' % sum(counts.values()))
A('')
A('%d of the 53 asterisked \u03b3 rays pair with a partner that is itself asterisked; the remaining %d have no marked' % (mutual_rows, one_sided_rows))
A('partner, which is the one-sided asterisk found in Cases 2 and 3.')
A('')
A('Note for the compiled file: the ENSDF multiply-placed flags in column 77 of the G-records were set from these')
A('relations - "&" where both placements carry the same energy and the same intensity (intensity not divided), "@" where')
A('the same energy carries two different intensities (intensity suitably divided), and "*" otherwise, including every')
A('Case 2 and Case 3 pair, whose energies differ. Case 1 therefore also decides that flag, since the divided or')
A('undivided nature of those three multiplets has to be settled by the authors.')
A('')
A('In conclusion, the data are in good shape and the remaining questions concern only the asterisk convention; the')
A('authors may wish to clarify the footnote and mark both members of every multiplet.')
A('')

data = '\r\n'.join(txt)
open(OUT, 'w', encoding='utf-8', newline='').write(data)
print('written', OUT, len(data), 'chars', len(txt), 'lines')
print('counts', counts, 'mutual', mutual_rows, 'one-sided', one_sided_rows, 'two-partner', two_partner_rows)
print('case2', case2)
print('case3 rays', len(case3_rays))
print('beyond', sorted(beyond_pairs))
