# Build complete mapping: each ENS level -> E(alpha)(lab) from each source paper.
# Sources: 1964Va08 (res 1-23), 1965Mc07 (res 1-36), 1967Wi01 (res 23-65 + Table 4 subset)
import re

ENS = r'd:\X\ND\ENSDF\A34\S34\new\S34_30si_a_g_a_n_resonances.ens'
RAW = r'd:\X\ND\ENSDF\A34\S34\raw'

# --- parse ENS: levels with E(alpha)(lab) and col77 flag ---
def parse_ens():
    levels = []
    cur = None
    for ln in open(ENS, encoding='utf-8').read().splitlines():
        if len(ln) >= 20 and ln[5:9] == '  L ':
            cur = {'e': ln[9:19].strip(), 'ea': None, 'flag': ln[76] if len(ln) >= 77 else ' ',
                   'j': ln[22:40].strip()}
            levels.append(cur)
        elif cur is not None and len(ln) >= 10 and ln[6:9] == 'cL ':
            m = re.search(r'E\(\|a\)\(lab\)=(\d+)', ln[9:])
            if m:
                cur['ea'] = int(m.group(1))
    return levels

levels = parse_ens()

# --- parse source tables ---
def parse_va08():
    res = {}
    for ln in open(RAW + r'\1964VA08_Table_1.md', encoding='utf-8').read().splitlines():
        m = re.match(r'\|\s*\*?\*?(\d+)\*?\*?\s*\|\s*([\d.]+)\s*\|\s*(\d+)\(5\)', ln)
        if m:
            res[int(m.group(1))] = {'ea': int(m.group(3)), 'emeV': float(m.group(2))}
    return res

def parse_mc07():
    res = {}
    for ln in open(RAW + r'\1965MC07_Table_1.md', encoding='utf-8').read().splitlines():
        m = re.match(r'\|\s*\*?\*?(\d+)\*?\*?\s*\|\s*([\d.]+)\s*\|\s*([\d.]+)\(5\)\s*\|\s*(\d+)\(5\)', ln)
        if m:
            res[int(m.group(1))] = {'ea': int(m.group(4)), 'emeV': float(m.group(3))}
    return res

def parse_wi01():
    res = {}
    for ln in open(RAW + r'\1967WI01_Table_1.md', encoding='utf-8').read().splitlines():
        if ln.strip() and not ln.startswith('Resonance'):
            parts = [p.strip().strip('"') for p in ln.split(',')]
            try:
                num = int(parts[0])
            except (ValueError, IndexError):
                continue
            res[num] = {'ea': round(float(parts[2]) * 1000), 'emeV': float(parts[2]),
                        'prev': parts[1], 'elevel': float(parts[3])}
    # Table 4 (subset, resonance numbers 2..22 are 1965Mc07-numbered)
    res4 = {}
    for ln in open(RAW + r'\1967WI01_Table_4.md', encoding='utf-8').read().splitlines():
        parts = [p.strip() for p in ln.split(',')]
        try:
            num = int(parts[0])
        except (ValueError, IndexError):
            continue
        res4[num] = round(float(parts[1]) * 1000)
    return res, res4

va08 = parse_va08()
mc07 = parse_mc07()
wi01, wi01_t4 = parse_wi01()

# --- classify each ENS level ---
print(f"{'E(level)':>9} {'Ea':>5} {'col77':>5} | {'Va08':>5} {'Mc07':>5} {'Wi01':>5} {'Wi01t4':>6} | category")
print('-' * 78)
for lv in levels:
    ea = lv['ea']
    if ea is None:
        print(f"{lv['e']:>9} {'-':>5} {lv['flag']:>5} |  -  no Ea comment")
        continue
    # which sources have this Ea (or close)?
    in_va08 = next((n for n, r in va08.items() if r['ea'] == ea), None)
    in_mc07 = next((n for n, r in mc07.items() if r['ea'] == ea), None)
    in_wi01 = next((n for n, r in wi01.items() if r['ea'] == ea), None)
    in_t4 = next((n for n, v in wi01_t4.items() if v == ea), None)
    # 1965Mc07 res 23-28 are the same as 1967Wi01 res 23-28 (prev numbers)
    both67_65 = (in_wi01 is not None and in_mc07 is not None and in_wi01 == in_mc07)
    # 1967Wi01 Table1 res 23-28 have previous Mc07 numbers -> both
    both67_65b = in_wi01 is not None and wi01[in_wi01]['prev'] != '—' and wi01[in_wi01]['prev'] != '-'
    cat = ''
    if in_va08 and in_mc07:
        cat = 'Va08+Mc07 (avg)'
    elif in_va08:
        cat = 'Va08 only (Flag V)'
    elif in_mc07 and in_wi01 and both67_65b:
        cat = 'Wi01+Mc07 (S=Wi01, cL=Mc07)'
    elif in_mc07 and in_t4:
        cat = 'Mc07 + Wi01T4 (S=Wi01?, cL=Mc07?)'
    elif in_mc07:
        cat = 'Mc07 only (Flag M)'
    elif in_wi01:
        cat = 'Wi01 only (default)'
    else:
        cat = '??? no source match'
    print(f"{lv['e']:>9} {ea:>5} {lv['flag']:>5} | {str(in_va08):>5} {str(in_mc07):>5} {str(in_wi01):>5} {str(in_t4):>6} | {cat}")

print()
print('1967Wi01 Table1 res with prev(Mc07):', {n: r['prev'] for n, r in wi01.items() if r['prev'] not in ('—', '-')})
print('1967Wi01 Table4 Ea values:', sorted(wi01_t4.items()))
