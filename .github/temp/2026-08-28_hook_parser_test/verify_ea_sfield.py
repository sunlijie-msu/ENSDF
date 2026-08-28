# Cross-check ENS S-field E(alpha) values against the three Table 1 sources.
# Classify each level: Va08-only (V), Mc07-only (M), Wi01-only (default),
# Wi01+Mc07 (Rule 2, cL S$other), Va08+Mc07 (average, 10791), 1975DeZS (Z).
import re

ENS = r'd:\X\ND\ENSDF\A34\S34\new\S34_30si_a_g_a_n_resonances.ens'
RAW = r'd:\X\ND\ENSDF\A34\S34\raw'

# --- parse ENS ---
levels = []  # dicts: e, s, ds, flag, old_comment
cur = None
for ln in open(ENS, encoding='utf-8').read().splitlines():
    if len(ln) >= 20 and ln[5:9] == '  L ':
        cur = {'e': ln[9:19].strip(), 's': None, 'ds': None,
               'flag': ln[76] if len(ln) >= 77 else ' ',
               'old': None}
        # S field cols 65-74, DS cols 75-76
        sf = ln[64:74].strip()
        if sf:
            cur['s'] = int(sf)
            ds = ln[74:76].strip()
            cur['ds'] = ds
        levels.append(cur)
    elif cur is not None and len(ln) >= 10 and ln[6:9] == 'cL ':
        m = re.search(r'E\(\|a\)\(lab\)=(\d+)', ln[9:])
        if m:
            cur['old'] = int(m.group(1))

# --- parse sources ---
def rows_va08():
    out = {}
    for ln in open(RAW + r'\1964VA08_Table_1.md', encoding='utf-8').read().splitlines():
        m = re.match(r'\|\s*\*?\*?(\d+)\*?\*?\s*\|\s*([\d.]+)\s*\|\s*(\d+)\(5\)', ln)
        if m:
            out[int(m.group(1))] = int(m.group(3))
    return out

def rows_mc07():
    out = {}
    for ln in open(RAW + r'\1965MC07_Table_1.md', encoding='utf-8').read().splitlines():
        m = re.match(r'\|\s*\*?\*?(\d+)\*?\*?\s*\|\s*([\d.]+)\s*\|\s*([\d.]+)\(5\)\s*\|\s*(\d+)\(5\)', ln)
        if m:
            out[int(m.group(1))] = int(m.group(4))
    return out

def rows_wi01():
    out = {}  # res# -> (ea, prev)
    for ln in open(RAW + r'\1967WI01_Table_1.md', encoding='utf-8').read().splitlines():
        if ln.strip() and not ln.startswith('Resonance'):
            p = [x.strip().strip('"') for x in ln.split(',')]
            try:
                n = int(p[0])
            except (ValueError, IndexError):
                continue
            out[n] = (round(float(p[2]) * 1000), p[1])
    return out

va08 = rows_va08()
mc07 = rows_mc07()
wi01 = rows_wi01()
va_by_ea = {v: k for k, v in va08.items()}
mc_by_ea = {v: k for k, v in mc07.items()}
wi_by_ea = {v[0]: k for k, v in wi01.items()}

Z_LEVELS = {'10382', '10386', '10443', '10482'}

print(f"{'E(lev)':>9} {'S':>5} {'DS':>2} {'old':>5} {'col77':>4} | cat | S_check")
print('-' * 78)
problems = []
for lv in levels:
    if lv['e'] in Z_LEVELS:
        print(f"{lv['e']:>9} {str(lv['s']):>5} {str(lv['ds']):>2} {str(lv['old']):>5} {lv['flag']:>4} | Z (skip)")
        continue
    e = lv['s']
    if e is None:
        print(f"{lv['e']:>9} {'-':>5} {'':>2} {str(lv['old']):>5} {lv['flag']:>4} | no S")
        continue
    vn = va_by_ea.get(e)
    mn = mc_by_ea.get(e)
    wn = wi_by_ea.get(e)
    cat = ''
    s_check = 'OK'
    if vn is not None and mn is not None:
        cat = 'Va08+Mc07 (avg)'
    elif vn is not None:
        cat = 'Va08 only -> V'
    elif mn is not None and wn is not None and wi01[wn][1] not in ('—', '-'):
        # both Wi01 + Mc07: S should be Wi01 value; verify it equals wi01[wn]
        cat = 'Wi01+Mc07 -> Rule2 (cL S$other)'
        if e != wi01[wn][0]:
            s_check = f'MISMATCH S={e} vs Wi01={wi01[wn][0]}'
            problems.append((lv['e'], s_check))
    elif mn is not None:
        cat = 'Mc07 only -> M'
        if e != mc07[mn]:
            s_check = f'MISMATCH S={e} vs Mc07={mc07[mn]}'
            problems.append((lv['e'], s_check))
    elif wn is not None:
        cat = 'Wi01 only (default)'
        if e != wi01[wn][0]:
            s_check = f'MISMATCH S={e} vs Wi01={wi01[wn][0]}'
            problems.append((lv['e'], s_check))
    else:
        cat = '??? UNMATCHED'
        problems.append((lv['e'], 'UNMATCHED'))
    # old comment consistency
    if lv['old'] is not None and lv['old'] != e:
        s_check += f' | old={lv["old"]} != S'
        problems.append((lv['e'], 'old comment mismatch'))
    print(f"{lv['e']:>9} {e:>5} {str(lv['ds']):>2} {str(lv['old']):>5} {lv['flag']:>4} | {cat:>20} | {s_check}")

print()
print('PROBLEMS:', len(problems))
for p in problems:
    print('  ', p)
