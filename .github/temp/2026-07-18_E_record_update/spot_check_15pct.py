"""15% random spot-check: verify E-record fields against Table III."""
import re, random, sys

ENSDF = 'd:/X/ND/ENSDF/XUNDL/2026OSAA_CT11035_152Gd.ens'
T3    = 'd:/X/ND/ENSDF/XUNDL/2026OSAA_CT11035_152Gd_Table_III.md'

# ── Load ENSDF E-records ──
erecs = []
cur = None
with open(ENSDF, 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        r = line.rstrip('\n\r')
        if len(r) >= 9 and r[5:7] == '  ' and r[7:8] == 'L':
            e = r[9:19].strip()
            if e: cur = e
        if len(r) >= 80 and r[5:7] == '  ' and r[7:8] == 'E':
            erecs.append({
                'level': cur,
                'line': i + 1,
                'ib': r[22:29].strip(),
                'dib': r[29:31].strip(),
                'ie': r[31:39].strip(),
                'die': r[39:41].strip(),
                'ti': r[64:74].strip(),
                'dti': r[74:76].strip(),
            })

print(f'Total E-records: {len(erecs)}')

# ── Load Table III ──
def conv(v):
    if not v: return v
    return v.replace('\u00d7' + '10', 'E').replace('\u2212', '-')

def parse(cell):
    cell = cell.strip()
    if not cell:
        return '', '', True
    m = re.match(r'^(.+?)\s*\((.+?)\)$', cell)
    if m:
        return conv(m.group(1).strip()), m.group(2).strip(), False
    return conv(cell), '', False

t3_entries = []
with open(T3, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line.startswith('|') or '---' in line or 'TABLE' in line:
            continue
        parts = [p.strip() for p in line.split('|')]
        if len(parts) < 8:
            continue
        m = re.match(r'([\d.]+)', parts[1])
        if not m:
            continue
        ex = float(m.group(1))
        ibv, ibu, ibb = parse(parts[3])
        iev, ieu, ieb = parse(parts[4])
        itv, itu, itb = parse(parts[5])
        t3_entries.append({
            'ex': ex,
            'ib': ibv, 'ibu': ibu, 'ibb': ibb,
            'ie': iev, 'ieu': ieu, 'ieb': ieb,
            'it': itv, 'itu': itu, 'itb': itb,
        })

# ── Match and verify ──
random.seed(42)
sample = random.sample(erecs, 30)

errors = 0
for rec in sample:
    level_e = float(rec['level'])
    t3_key = round(level_e)
    matches = [e for e in t3_entries if round(e['ex']) == t3_key]
    if not matches:
        print(f'FAIL {rec["level"]} line {rec["line"]}: no T3 match')
        errors += 1
        continue
    d = matches[0] if len(matches) == 1 else min(matches, key=lambda e: abs(e['ex'] - level_e))

    # Check each field pair
    for field, ens_val, t3_val, t3_blank in [
        ('IB', rec['ib'], d['ib'], d['ibb']),
        ('IE', rec['ie'], d['ie'], d['ieb']),
        ('TI', rec['ti'], d['it'], d['itb']),
    ]:
        ens_val = ens_val.strip() if ens_val else ''
        if t3_blank:
            if ens_val:
                print(f'FAIL {rec["level"]} line {rec["line"]}: {field}=[{ens_val}] should be blank')
                errors += 1
        else:
            if not ens_val:
                print(f'FAIL {rec["level"]} line {rec["line"]}: {field}=blank, T3=[{t3_val}]')
                errors += 1
            elif ens_val != t3_val:
                try:
                    ef = float(ens_val)
                    tf = float(t3_val)
                    if abs(ef - tf) / max(abs(tf), 0.001) > 0.015:
                        print(f'FAIL {rec["level"]} line {rec["line"]}: {field}=[{ens_val}], T3=[{t3_val}]')
                        errors += 1
                except:
                    print(f'FAIL {rec["level"]} line {rec["line"]}: {field}=[{ens_val}], T3=[{t3_val}]')
                    errors += 1

print()
if errors == 0:
    print('SPOT-CHECK PASSED: 30/30 entries verified (0 errors)')
    sys.exit(0)
else:
    print(f'SPOT-CHECK FAILED: {errors} mismatches')
    sys.exit(1)
