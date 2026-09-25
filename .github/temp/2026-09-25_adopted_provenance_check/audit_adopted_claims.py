"""Audit 'From the Adopted ...' provenance claims in the S34 individual datasets.

For each dataset carrying a comment that claims data comes from the Adopted
Levels / Adopted Gammas:
  * the claim is scoped by the flag letters in the comment identifier
    (e.g. cL E(A),J(A)$ -> only records flagged 'A' in col 77);
  * the precision is read from the comment text ('nearest integer',
    'nearest 0.1 keV', or exact when no rounding is stated);
  * level E is compared with the adopted level of the same Jpi; gamma E and M
    with the nearest adopted gamma.

Usage: python audit_adopted_claims.py
"""
import glob
import math
import os
import re

ADOPTED = r'A34/S34/new/S34_adopted.ens'


def parse(path):
    levels, gammas = [], []
    cur = None
    for i, l in enumerate(open(path, encoding='utf-8', newline='').read().split('\r\n'), 1):
        if len(l) < 20 or l[6] in 'cCdD':
            continue
        if l[7] == 'L' and l[5:7] == '  ':
            cur = {'line': i, 'e': l[9:19].strip(), 'de': l[19:21].strip(),
                   'j': l[22:39].strip(), 'flag': l[76:77], 'g': []}
            levels.append(cur)
        elif l[7] == 'G' and l[5:7] == '  ':
            g = {'line': i, 'e': l[9:19].strip(), 'm': l[32:41].strip(),
                 'flag': l[76:77], 'lvl': cur}
            gammas.append(g)
            if cur is not None:
                cur['g'].append(g)
    return levels, gammas


def num(s):
    try:
        return float(s)
    except ValueError:
        return None


def rnd(x, step):
    return math.floor(x / step + 0.5) * step


def fmt(x):
    return str(int(x)) if abs(x - int(x)) < 1e-9 else ('%.1f' % x)


def text_of(line):
    if len(line) < 12:
        return line.strip()
    return line[11:].strip() if line[5] == ' ' else line[9:].strip()


def scope_flags(first_line):
    """Flag letters named in the comment identifier, e.g. cL E(A),J(A)$ -> {'A'}."""
    m = re.match(r'\s*\S{0,4}\s{0,2}\S{0,2}\s(\S*?)\$', first_line)
    ident = m.group(1) if m else ''
    letters = set()
    for grp in re.findall(r'\(([A-Za-z,()]+)\)', ident):
        letters |= {c for c in grp if c.isalpha()}
    return letters


def precision(txt):
    if re.search(r'nearest\s+integer', txt, re.I):
        return 1.0
    m = re.search(r'nearest\s+([\d.]*)\s*keV', txt, re.I)
    if m:
        return float(m.group(1)) if m.group(1) else 1.0
    return None  # exact


alvl, agam = parse(ADOPTED)
ag = [(num(g['e']), g['m'].strip(), g['line']) for g in agam if num(g['e']) is not None]

for path in sorted(glob.glob(r'A34/S34/new/*.ens')):
    name = os.path.basename(path)
    if name == 'S34_adopted.ens':
        continue
    lines = open(path, encoding='utf-8', newline='').read().split('\r\n')
    claims = []           # (line_no, ident_first_line, full_text)
    for i, l in enumerate(lines):
        if len(l) > 7 and l[6] in 'cCdD' and 'dopted' in l and 'rom the Adopted' in l:
            blk = [l]
            for k in range(i + 1, min(i + 5, len(lines))):
                if len(lines[k]) > 7 and lines[k][6] in 'cCdD':
                    blk.append(lines[k])
                else:
                    break
            claims.append((i + 1, l, ' '.join(text_of(b) for b in blk)))
    if not claims:
        continue
    print('=' * 100)
    print(name)
    lvl_e = [c for c in claims if re.search(r'\bE[A-Za-z(,]', text_of(c[1])) and 'level' in (c[2] + text_of(c[1])).lower()]
    lvl_any = [c for c in claims if 'Levels' in c[2]]
    gam_e = [c for c in claims if 'Gammas' in c[2]]
    levels, gammas = parse(path)
    problems = []
    for ln, first, txt in lvl_any:
        flags = scope_flags(first)
        step = precision(txt)
        for lv in levels:
            if flags and lv['flag'] not in flags:
                continue
            e = num(lv['e'])
            if e is None:
                continue
            cands = [a for a in alvl if num(a['e']) is not None and
                     (not lv['j'] or not a['j'] or a['j'].strip() == lv['j'].strip())]
            if not cands:
                problems.append(('LVL-J', lv['line'], lv['e'], lv['j'], 'no adopted level with this J', ln))
                continue
            best = min(cands, key=lambda a: abs(num(a['e']) - e))
            ae = num(best['e'])
            if step:
                want = fmt(rnd(ae, step))
                ok = abs(rnd(ae, step) - e) < 1e-9
            else:
                want = best['e']
                ok = abs(ae - e) < 0.006
            if not ok:
                problems.append(('LVL-E', lv['line'], lv['e'], lv['j'],
                                 f'adopted {best["e"]} -> expect {want}', ln))
    for ln, first, txt in gam_e:
        flags = scope_flags(first)
        step = precision(txt)
        for g in gammas:
            if flags and g['flag'] not in flags:
                continue
            e = num(g['e'])
            if e is None:
                continue
            ae, am, aline = min(ag, key=lambda a: abs(a[0] - e))
            if abs(ae - e) > 2.0:
                problems.append(('GAM-none', g['line'], g['e'], g['m'], f'nearest adopted gamma {ae}', ln))
                continue
            if step:
                want = fmt(rnd(ae, step))
                ok = abs(rnd(ae, step) - e) < 1e-9
            else:
                want = fmt(ae)
                ok = abs(ae - e) < 0.006
            if not ok:
                problems.append(('GAM-E', g['line'], g['e'], g['m'],
                                 f'adopted gamma {fmt(ae)} -> expect {want}', ln))
    for ln, first, txt in claims:
        print('   claim line', ln, '|', text_of(first)[:95])
    if problems:
        print('   FLAGGED', len(problems))
        for p in problems:
            print('      ', p[0], 'line', p[1], repr(lines[p[1] - 1].rstrip()[:60]), '|', p[4],
                  '| claim line', p[5])
    else:
        print('   OK - all records covered by the claim match the adopted values')
