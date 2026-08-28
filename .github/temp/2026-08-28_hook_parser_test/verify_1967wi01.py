# Verify 1967WI01 Table 1 data against the current ENS file.
# Match by E(alpha)(lab) value (keV); report E(level) and FLAG vs remark.
import csv
import io
import re

ENS = r'd:\X\ND\ENSDF\A34\S34\new\S34_30si_a_g_a_n_resonances.ens'
RAW = r'd:\X\ND\ENSDF\A34\S34\raw\1967WI01_Table_1.md'

# --- Parse ENS file: collect L records with their E(level), E(alpha)(lab), FLAG ---
ens_levels = []  # list of dicts
cur = None
for ln in open(ENS, encoding='utf-8').read().splitlines():
    if len(ln) >= 20 and ln[5:9] == '  L ':
        try:
            e_val = float(ln[9:19].strip())
        except ValueError:
            e_val = None
        cur = {
            'line': None,
            'e': e_val,
            'ea': None,
            'flag': None,
        }
        ens_levels.append(cur)
    elif cur is not None and len(ln) >= 10 and ln[6:9] == 'cL ':
        m = re.search(r'E\(\|a\)\(lab\)=(\d+)', ln[9:])
        if m:
            cur['ea'] = int(m.group(1))
    elif cur is not None and ln.startswith(' 34S F L FLAG='):
        cur['flag'] = ln.strip().split('=')[-1]

# --- Parse raw table ---
rows = []
for line in open(RAW, encoding='utf-8').read().splitlines():
    if not line.strip() or line.lstrip().startswith('Resonance'):
        continue
    # CSV-ish: fields separated by commas, some quoted
    parts = next(csv.reader(io.StringIO(line)))
    parts = [p.strip() for p in parts]
    if len(parts) < 4:
        continue
    try:
        num67 = int(parts[0])
    except ValueError:
        continue
    prev = parts[1]
    ea_mev = float(parts[2])
    e_mev = float(parts[3])
    remark = parts[4] if len(parts) > 4 else ''
    rows.append({'num': num67, 'prev': prev, 'ea': ea_mev, 'e': e_mev, 'remark': remark})

# --- Match by E(alpha)(lab) ---
def remark_to_flag(remark):
    if 'Below' in remark or remark.lower().startswith('ibid'):
        return 'B'
    if '(a, n) only' in remark or '(α, n) only' in remark:
        return 'C'
    if '(a, g) only' in remark or '(α, γ) only' in remark:
        return 'D'
    return ''

print(f"{'#67':>4} {'Ea_tab':>8} {'Ea_ens':>8} {'E_tab':>8} {'E_ens':>8} {'flag':>5} {'exp':>5} {'remark'}")
print('-' * 78)
missing = []
mismatch = []
for r in rows:
    ea_kev = round(r['ea'] * 1000)
    match = [l for l in ens_levels if l['ea'] == ea_kev]
    if not match:
        missing.append(r)
        print(f"{r['num']:>4} {ea_kev:>8} {'---':>8} {r['e']*1000:>8.0f} {'---':>8} {'--':>5} {'--':>5}  ** NO MATCH **")
        continue
    l = match[0]
    exp = remark_to_flag(r['remark'])
    flag_ok = (l['flag'] == exp) if exp else True
    status = ''
    if l['flag'] != exp:
        status = '  <-- FLAG MISMATCH'
        mismatch.append((r['num'], ea_kev, l['flag'], exp, r['remark']))
    print(f"{r['num']:>4} {ea_kev:>8} {l['ea']:>8} {r['e']*1000:>8.0f} {l['e']:>8} {str(l['flag']):>5} {exp or '-':>5}  {r['remark']}{status}")

print()
print('Total table rows:', len(rows))
print('No-match (missing in ENS):', len(missing), [r['num'] for r in missing])
print('Flag mismatches:', len(mismatch))
for m in mismatch:
    print('   #%s Ea=%s ENS_flag=%s expected=%s remark=%r' % m)
