# -*- coding: utf-8 -*-
"""
INDEPENDENT read-only compliance audit.
Dataset: A34/S34/new/S34_adopted.ens
Rules : .github/skills/gamma-selection-rules/SKILL.md  section '`cL J$` Comment Style Rules'
        R1 weak / LT / '?' col80 / uncertain-final-Jpi
        R2 descending RI order + only strongest per final Jpi
Own parsing only. Does NOT import repo scripts. NEVER writes to the .ens file.
"""
import subprocess, re, os, sys

REPO = r'd:\X\ND\ENSDF'
REL = 'A34/S34/new/S34_adopted.ens'
PATH = os.path.join(REPO, 'A34', 'S34', 'new', 'S34_adopted.ens')
TMP = os.path.join(REPO, '.github', 'temp', '2026-09-24_cL_J_style')
REPORT = os.path.join(TMP, 'audit_independent_output.txt')

OUT = []
def p(s=''):
    OUT.append(s)

def git(args):
    r = subprocess.run(['git', '--no-pager'] + args, cwd=REPO,
                       capture_output=True, text=True)
    return r.returncode, r.stdout

# ---------------------------------------------------------------- 0. status
rc, status = git(['status', '--porcelain', '--', REL])
p('=' * 78)
p('0. git status --porcelain -- %s   (rc=%d)' % (REL, rc))
p('=' * 78)
p(status.rstrip('\n') if status.strip() else '(clean / nothing)')

# ---------------------------------------------------------------- 1. diff
rc, diff = git(['diff', '--unified=0', '--', REL])
with open(os.path.join(TMP, 'diff_u0_audit.txt'), 'w', encoding='utf-8') as fh:
    fh.write(diff)

hunks = []
cur = None
for ln in diff.split('\n'):
    if ln.startswith('@@'):
        m = re.match(r'^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@', ln)
        cur = {'old': int(m.group(1)), 'new': int(m.group(3)),
               'minus': [], 'plus': [], 'hdr': ln}
        hunks.append(cur)
    elif cur is not None:
        if ln.startswith('---') or ln.startswith('+++'):
            continue
        if ln.startswith('-'):
            cur['minus'].append(ln[1:])
        elif ln.startswith('+'):
            cur['plus'].append(ln[1:])

p()
p('=' * 78)
p('1. DIFF SCOPE')
p('=' * 78)
p('hunk count = %d' % len(hunks))
bad = []
touched = []           # (new_line_no, text)
for h in hunks:
    on, nn = h['old'], h['new']
    for l in h['minus']:
        if not (len(l) >= 8 and l[6] == 'c' and l[7] == 'L'):
            bad.append(('REMOVED old-line %d' % on, repr(l)))
        on += 1
    for l in h['plus']:
        if not (len(l) >= 8 and l[6] == 'c' and l[7] == 'L'):
            bad.append(('ADDED new-line %d' % nn, repr(l)))
        touched.append((nn, l))
        nn += 1
nmin = sum(len(h['minus']) for h in hunks)
nplus = sum(len(h['plus']) for h in hunks)
p('removed (old) lines = %d ; added (new) lines = %d' % (nmin, nplus))
p('non-comment (i.e. NOT col7=c,col8=L) changed lines = %d' % len(bad))
for b in bad:
    p('   VIOLATION: %s  %s' % b)
p('added(new) comment line numbers = %s' % [t[0] for t in touched])
p('all changed lines are cL comment records : %s' % ('YES' if not bad else 'NO'))

# ---------------------------------------------------------------- file load
with open(PATH, 'r', encoding='utf-8', newline='') as fh:
    raw = fh.read()
FL = raw.split('\n')
CRLF = '\r\n' in raw
p()
p('file: lines(split \\n)=%d  CRLF=%s' % (len(FL), CRLF))

def core(l):
    return l[:-1] if l.endswith('\r') else l

# ---------------------------------------------------------------- 2. widths
p()
p('=' * 78)
p('2. 80-COLUMN WIDTH OF TOUCHED LINES')
p('=' * 78)
wf = []
for n, _ in touched:
    c = core(FL[n - 1])
    total = len(c)
    rs = len(c.rstrip())
    mark = '' if total == 80 else '   <== NOT 80'
    if total != 80:
        wf.append((n, total))
    p('  line %5d  total_len=%3d  len(rstrip)=%3d%s' % (n, total, rs, mark))
p('width failures = %s' % (wf if wf else 'NONE'))

# ---------------------------------------------------------------- G index
def fld(l, a, b):
    return l[a - 1:b]

GR = []
for i, l in enumerate(FL, start=1):
    c = core(l)
    if len(c) >= 8 and c[5] == ' ' and c[6] == ' ' and c[7] == 'G':
        GR.append({'n': i, 'E': fld(c, 10, 19).strip(),
                   'RI': fld(c, 23, 29), 'DRI': fld(c, 30, 31),
                   'c80': (c[79] if len(c) >= 80 else ' '), 'raw': c})
p()
p('G-record index size = %d' % len(GR))

def num(s):
    s = (s or '').strip()
    if s == '':
        return None
    try:
        return float(s)
    except ValueError:
        return None

def hits_of(E):
    v = float(E)
    return [g for g in GR if num(g['E']) == v]

def fmthits(hs):
    if not hs:
        return '(NO G-record matched)'
    out = []
    for g in hs:
        out.append('L%d RI=%s DRI=%s col80=%r' % (g['n'], g['RI'].strip(),
                                                  g['DRI'].strip(), g['c80']))
    return ' | '.join(out)

# ---------------------------------------------------------------- 3/4/5 named
p()
p('=' * 78)
p('3/4/5. RI EVIDENCE FOR NAMED GAMMAS')
p('=' * 78)
named = ['989.1', '580.3', '1244.32',              # removed trio
         '3392.86', '2680.5', '4799.11',           # survivors
         '2490.6', '3451.5', '8036.6', '925.79',   # reordered lists
         '2363.97', '4540.68', '3002.8', '1461.7', # reordered lists
         '1178', '2333.8']                         # dropped/kept pair
for t in named:
    hs = hits_of(t)
    p('  %-9s -> %s' % (t, fmthits(hs)))

# ---------------------------------------------------------------- 6. walk
p()
p('=' * 78)
p('6. INDEPENDENT cL J$ WALK  (residual violations)')
p('=' * 78)

def is_cL(c):
    return len(c) >= 8 and c[6] == 'c' and c[7] == 'L'

blocks = []
i = 0
while i < len(FL):
    c = core(FL[i])
    if is_cL(c) and c[5] == ' ':
        txt = [c[9:]]
        j = i + 1
        while j < len(FL):
            cj = core(FL[j])
            if is_cL(cj) and cj[5] != ' ':
                txt.append(cj[9:])
                j += 1
            else:
                break
        blocks.append({'start': i + 1, 'text': ''.join(txt)})
        i = j
    else:
        i += 1

JRE = re.compile(r'^J[A-Za-z0-9()]*\$')
jblocks = [b for b in blocks if JRE.match(b['text'])]
p('all cL blocks = %d ; cL J$ blocks = %d' % (len(blocks), len(jblocks)))

TRSTART = re.compile(r'(?<![\d.])(\d+(?:\.\d+)?)\|g')
DTOT = re.compile(r'\b(to|from)\b')

def parse_block(body):
    out = []
    ms = list(TRSTART.finditer(body))
    for k, m in enumerate(ms):
        s = m.start()
        e = ms[k + 1].start() if k + 1 < len(ms) else len(body)
        seg = body[s:e]
        mm = re.match(r'^(\d+(?:\.\d+)?)\|g', seg)
        if not mm:
            continue
        rest = seg[mm.end():]
        d = DTOT.search(rest)
        if not d:
            out.append({'E': mm.group(1), 'dir': None, 'jp': None})
            continue
        tail = rest[d.end():].lstrip()
        mjp = re.match(r'^(.*?)(?:,\s+|\s*,\s*(?=g\.s\.)|\s+g\.s\.'
                       r'|\s+\d+(?:\.\d+)?\s+level|\s+level)', tail)
        jp = (mjp.group(1) if mjp else tail).strip()
        mlv = re.search(r'(\d+(?:\.\d+)?)\s+level|g\.s\.', tail)
        lv = ''
        if mlv:
            lv = mlv.group(1) if mlv.group(1) else 'g.s.'
        out.append({'E': mm.group(1), 'dir': d.group(1), 'jp': jp, 'lv': lv})
    return out

cls = {'weak': [], 'lt': [], 'q80': [], 'jpunc': [], 'order': [], 'dup': [],
       'noGR': [], 'ambig': []}
TRACES = []

for b in jblocks:
    m = JRE.match(b['text'])
    body = b['text'][m.end():]
    trs = parse_block(body)
    if not trs:
        continue
    rows = []
    ris = []
    jps = {}
    for t in trs:
        hs = hits_of(t['E'])
        ris_h = [num(g['RI']) for g in hs]
        ri_use = None
        if len(hs) == 1:
            ri_use = ris_h[0]
        elif len(hs) > 1:
            cls['ambig'].append((b['start'], t['E'],
                                 [(g['n'], g['RI'].strip()) for g in hs]))
            near = min(hs, key=lambda g: abs(g['n'] - b['start']))
            ri_use = num(near['RI'])
        else:
            cls['noGR'].append((b['start'], t['E']))
        ri_disp = fmthits(hs)
        # flags
        if not hs:
            pass
        else:
            if any((r is not None and r < 5) for r in ris_h):
                cls['weak'].append((b['start'], t['E'], ri_disp))
            if any('LT' in g['DRI'] for g in hs):
                cls['lt'].append((b['start'], t['E'], ri_disp))
            if any(g['c80'] == '?' for g in hs):
                cls['q80'].append((b['start'], t['E'], ri_disp))
        jp = t['jp'] or ''
        if jp and ('(' in jp or ')' in jp or ',' in jp):
            cls['jpunc'].append((b['start'], t['E'], jp, t['dir'], t.get('lv', '')))
        jps.setdefault(jp, []).append(t['E'])
        if ri_use is not None:
            ris.append((t['E'], ri_use))
        rows.append('      E=%-9s dir=%-4s Jpi=%-10s lvl=%-9s RI=%s  (orderRI=%s)' %
                    (t['E'], t['dir'], jp, t.get('lv', ''), ri_disp, ri_use))
    # descending order
    vals = [v for _, v in ris]
    if len(vals) >= 2 and any(vals[k] < vals[k + 1] for k in range(len(vals) - 1)):
        cls['order'].append((b['start'], ris))
    for jp, es in jps.items():
        if jp and len(es) > 1:
            cls['dup'].append((b['start'], jp, es))
    TRACES.append('  block@line %-5d  %s' % (b['start'], body.strip()))
    TRACES.extend(rows)

p()
p('--- every cL J$ block (text + extracted transitions) ---')
for t in TRACES:
    p(t)

p()
p('--- residual violation classes ---')
for k in ['weak', 'lt', 'q80', 'jpunc', 'order', 'dup', 'noGR', 'ambig']:
    p('  %-6s count=%d' % (k, len(cls[k])))
    for it in cls[k]:
        p('        %s' % (it,))

total_ex = sum(len(cls[k]) for k in ['weak', 'lt', 'q80', 'jpunc', 'order', 'dup'])
p()
p('TOTAL residual violations (weak+lt+q80+jpunc+order+dup) = %d' % total_ex)
p('  blocks affected = %d' % len(set(x[0] for k in ['weak', 'lt', 'q80', 'jpunc', 'order', 'dup']
                                     for x in cls[k])))
p('  jpunc blocks = %d ; jpunc items = %d ; distinct quoted levels = %d'
  % (len(set(x[0] for x in cls['jpunc'])), len(cls['jpunc']),
     len(set((x[2], x[4]) for x in cls['jpunc']))))
p('  distinct quoted (Jpi,level) pairs:')
for pair in sorted(set((x[2], x[4]) for x in cls['jpunc'])):
    p('        %s' % (pair,))

with open(REPORT, 'w', encoding='utf-8') as fh:
    fh.write('\n'.join(OUT) + '\n')

print('WROTE %s  lines=%d' % (REPORT, len(OUT)))
print('SUMMARY hunks=%d badchanged=%d widthfail=%d jblocks=%d jpunc=%d weak=%d lt=%d q80=%d order=%d dup=%d noGR=%d ambig=%d total_ex=%d'
      % (len(hunks), len(bad), len(wf), len(jblocks), len(cls['jpunc']), len(cls['weak']),
         len(cls['lt']), len(cls['q80']), len(cls['order']), len(cls['dup']),
         len(cls['noGR']), len(cls['ambig']), total_ex))
