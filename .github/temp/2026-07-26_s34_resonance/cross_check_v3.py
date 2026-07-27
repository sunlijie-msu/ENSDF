"""Cross-check S34 resonance - final fixed version."""
import re

# ====== PARSE MARKDOWN ======
with open(r'A34\S34\raw\2018MuZY_34S.md', 'r', encoding='utf-8') as f:
    md = f.read()

md_rows = []
in_table = False
for line in md.split('\n'):
    line = line.strip()
    if 'E_0' in line and 'keV' in line: in_table = True; continue
    if in_table and line.startswith('|') and '---' not in line:
        if 'Footnotes' in line: break
        md_rows.append(line)

md_levels = []
for row in md_rows:
    cells = [c.strip() for c in row.split('|')]
    if cells and cells[0] == '': cells = cells[1:]
    if cells and cells[-1] == '': cells = cells[:-1]
    if len(cells) < 3: continue
    
    e0_str = re.sub(r'[\$\^a-z\*]', '', cells[0]).strip()
    if e0_str in ('', '-', '—'): continue
    e0_val = float(e0_str)
    
    def c(n): return cells[n] if n < len(cells) else ''
    
    md_levels.append({
        'e0': e0_val, 'j': c(1), 'l': c(2),
        'gamma': c(3), 'gn': c(4), 'gg': c(5),
        'gn0': c(6), 'gn1': c(7), 'ggn': c(8), 'ga': c(9),
    })

# ====== PARSE ENSDF ======
with open(r'A34\S34\new\S34_n_g_n_n_resonances.ens', 'r') as f:
    ens_lines = f.readlines()

ens_levels = []
cur = None
for i, line in enumerate(ens_lines):
    if len(line) < 10: continue
    if line[7] == 'L' and line[8] == ' ' and line[6] != 'c':
        if cur: ens_levels.append(cur)
        e_str = line[9:19].strip()
        cur = {
            'line': i+1,
            'e_exc': float(e_str) if e_str else 0,
            'j': line[22:39].strip(),
            't': line[39:49].strip(),
            'dt': line[49:55].strip(),
            'l': line[55:64].strip(),
            's': line[64:74].strip(),
            'q': line[79],
            'cl': []
        }
        continue
    if cur and len(line) > 7 and line[6] == 'c' and line[7] == 'L':
        cur['cl'].append(line.rstrip())
if cur: ens_levels.append(cur)

def to_ev(v, u):
    try: f = float(v)
    except: return None
    return f * 1000 if u in ('KEV','keV') else (f * 1e6 if u in ('MEV','meV') else f)

def parse_info(el):
    info = {'ggn':'','gn':'','gn_u':'','gg':'','gg_u':'','ga':'','ga_u':'',
            'gv':'','gu':'EV','glim':''}
    t = el['t'].strip()
    if t:
        m = re.match(r'([\d.]+)\s*(EV|KEV|MEV)?', t)
        if m: info['gv']=m.group(1); info['gu']=m.group(2) or 'EV'
        dt = el['dt'].strip()
        if dt in ('LT','GT','LE','GE'): info['glim']=dt
    for cl in el['cl']:
        for pat, key, uk in [
            (r'g\|G\{-n\}\|G\{-\|g\}/\|G\s*=\s*([\d.]+)', 'ggn', ''),
            (r'\|G\{-n\}\s*=\s*([\d.]+)\s*(EV|KEV|MEV)?', 'gn', 'gn_u'),
            (r'\|G\|g\s*=\s*([\d.]+)\s*(EV|KEV|MEV)?', 'gg', 'gg_u'),
            (r'\|G\{\|g\}\s*=\s*([\d.]+)\s*(EV|KEV|MEV)?', 'gg', 'gg_u'),
            (r'\|G\{-\|a\}\s*=\s*([\d.]+)\s*(EV|KEV|MEV)?', 'ga', 'ga_u'),
        ]:
            m = re.search(pat, cl)
            if m:
                info[key] = m.group(1)
                if uk: info[uk] = m.group(2) or ''
    return info

# ====== COMPARE ======
print("="*75)
print("CROSS-CHECK: S34_n_g_n_n_resonances.ens vs 2018MuZY_34S.md")
print("="*75)

errors = 0
matched = set()

for md in md_levels:
    e0 = md['e0']
    best, bd = None, 999
    for el in ens_levels:
        try: s=float(el['s'])
        except: continue
        d=abs(s-e0)
        if d<bd: bd,best=d,el
    if best is None or bd>0.2:
        print(f"E0={e0}: NO MATCH (best diff={bd:.2f})"); errors+=1; continue
    matched.add(id(best))
    el = best; info = parse_info(el)
    
    hdr_printed = False
    
    # J (strip parity)
    mdj = md['j'].replace(' ','').replace('$','').replace('\\','').replace('≥','GE')
    ensj_np = el['j'].replace(' ','').rstrip('+-')
    if mdj and ensj_np and mdj != ensj_np:
        print(f"\nE0={e0} keV (ENS L{el['line']}, S={el['s']}):")
        print(f"  J: MD='{md['j']}' vs ENS='{el['j']}'")
        hdr_printed = True; errors += 1
    
    # l
    mdl = md['l'].strip('()'); ensl = el['l'].strip('()')
    if mdl and ensl and mdl != ensl:
        if not hdr_printed:
            print(f"\nE0={e0} keV (ENS L{el['line']}, S={el['s']}):")
            hdr_printed = True
        print(f"  L: MD='{md['l']}' vs ENS='{el['l']}'")
        errors += 1
    
    # Gamma (total, eV)
    if md['gamma']:
        m = re.match(r'[<>\u2264\u2265]*\s*([\d.]+)', md['gamma'])
        if m:
            mdg = float(m.group(1))
            ensg = to_ev(info['gv'], info['gu'])
            if ensg and abs(mdg-ensg) > max(mdg,ensg)*0.02:
                if not hdr_printed:
                    print(f"\nE0={e0} keV (ENS L{el['line']}, S={el['s']}):")
                    hdr_printed = True
                print(f"  Gamma: MD={md['gamma']} eV vs ENS={info['gv']} {info['gu']}")
                errors += 1
    
    # Gamma_n
    if md['gn']:
        gn_clean = re.sub(r'\^[a-z]','',md['gn'])
        m = re.match(r'([\d.]+)', gn_clean)
        if m:
            mdgn = float(m.group(1))
            ensgn = to_ev(info['gn'], info['gn_u'])
            if ensgn and abs(mdgn-ensgn) > max(mdgn,ensgn)*0.02:
                if not hdr_printed:
                    print(f"\nE0={e0} keV (ENS L{el['line']}, S={el['s']}):")
                    hdr_printed = True
                print(f"  Gn: MD={md['gn']} eV vs ENS={info['gn']} {info['gn_u']}")
                errors += 1
    
    # Gamma_g
    if md['gg']:
        m = re.match(r'([\d.]+)', md['gg'])
        if m:
            mdgg = float(m.group(1))
            ensgg = to_ev(info['gg'], info['gg_u'])
            if ensgg and abs(mdgg-ensgg) > max(mdgg,ensgg)*0.03:
                if not hdr_printed:
                    print(f"\nE0={e0} keV (ENS L{el['line']}, S={el['s']}):")
                    hdr_printed = True
                print(f"  Gg: MD={md['gg']} eV vs ENS={info['gg']} {info['gg_u']}")
                errors += 1
    
    # gGnGg/G
    if md['ggn']:
        m = re.match(r'([\d.]+)', md['ggn'])
        if m:
            mdggn = float(m.group(1))
            ensggn = float(info['ggn']) if info['ggn'] else None
            if ensggn and abs(mdggn-ensggn) > max(mdggn,ensggn)*0.02:
                if not hdr_printed:
                    print(f"\nE0={e0} keV (ENS L{el['line']}, S={el['s']}):")
                    hdr_printed = True
                print(f"  gGnGg/G: MD={md['ggn']} vs ENS={info['ggn']}")
                errors += 1
    
    # Gamma_a
    mdga = md['ga']; ensga = info['ga']
    has_md = bool(mdga and mdga not in ('','-'))
    has_ens = bool(ensga)
    if has_md != has_ens:
        if not hdr_printed:
            print(f"\nE0={e0} keV (ENS L{el['line']}, S={el['s']}):")
            hdr_printed = True
        print(f"  Ga presence: MD='{mdga}' vs ENS='{ensga}'")
        errors += 1
    elif has_md:
        m = re.match(r'([\d.]+)', mdga)
        if m:
            mdga_v = float(m.group(1))
            ensga_v = to_ev(ensga, info['ga_u'])
            if ensga_v and abs(mdga_v-ensga_v) > max(mdga_v,ensga_v)*0.02:
                if not hdr_printed:
                    print(f"\nE0={e0} keV (ENS L{el['line']}, S={el['s']}):")
                    hdr_printed = True
                print(f"  Ga: MD={mdga} eV vs ENS={ensga} {info['ga_u']}")
                errors += 1

# ENSDF-only
only_ct = 0
for el in ens_levels:
    if id(el) not in matched:
        fict = any('fictitious' in c for c in el['cl'])
        if not fict:
            only_ct += 1
            print(f"\nENS ONLY: L{el['line']} S={el['s']} J={el['j']}")

print(f"\n{'='*75}")
print(f"Errors: {errors}  |  MD: {len(md_levels)}  ENS: {len(ens_levels)}  ENS-only: {only_ct}")
