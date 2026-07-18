"""
Fix ENSDF angular correlation cG lines to match Table IV.
Category A: Fix A-value uncertainties (different sig fig counts)
Category B: Add missing delta (mixing ratio) values
"""
import re

with open('d:/X/ND/ENSDF/XUNDL/2026OSAA_CT11035_152Gd.ens','r') as f:
    lines = f.readlines()

# Parse Table IV for reference data
with open('d:/X/ND/ENSDF/XUNDL/2026OSAA_CT11035_152Gd_Table_IV.md','r',encoding='utf-8') as f:
    md = f.readlines()
tb = {}
for l in md:
    s = l.strip()
    if not s.startswith('| ') or '$' in s or '---' in s: continue
    p = [x.strip() for x in s.split('|')][1:-1]
    if len(p) < 12: continue
    key = (p[0], p[1], p[2])  # (E_level, Eg1, Eg2)
    tb[key] = {'A0':p[3], 'A2':p[4], 'A4':p[5], 'd1':p[11]}

# Parse ENSDF to find cG lines with AC data
fixes_a = []  # uncertainty fixes
fixes_b = []  # missing delta additions

def unc_to_str(val_str, unc_int, dec_places):
    """Convert '0.103' and 4 to '0.103 {I4}'"""
    # Actually we need to preserve the original ENSDF format
    # Just return the unc part
    return f'{{I{unc_int}}}'

level = None; g_eg = None
for i, line in enumerate(lines):
    if len(line) < 80: continue
    c6 = line[5]; c7 = line[6]; c8 = line[7]
    
    if c8 == 'L' and c7 == ' ':
        try: level = float(line[9:19].strip())
        except: level = None
        g_eg = None
    elif c8 == 'G' and c7 == ' ' and c6 == ' ':
        try: float(line[9:19].strip()); g_eg = line[9:19].strip()
        except: pass
    elif c8 == 'G' and c7 == 'c':
        if 'A{-0}' not in line and 'A{-2}' not in line: continue
        if not level or not g_eg: continue
        
        # Find matching Table IV entry
        # Build cascade comment
        cm = line[9:].strip()
        m_cascade = re.search(r'\$(\d+\.?\d*)\s*-\s*(\d+\.?\d*)\s*\|g\|g', cm)
        if not m_cascade: continue
        eg2 = m_cascade.group(2)
        
        # Find Table IV match
        tkey = None
        for k in tb:
            try:
                if abs(float(k[0]) - level) < 1.0 and abs(float(k[1]) - float(g_eg)) < 1.0 and abs(float(k[2]) - float(eg2)) < 1.0:
                    tkey = k; break
            except: pass
        if not tkey: continue
        trow = tb[tkey]
        
        # Check A-value uncertainties
        for aname, idx in [('A0',0), ('A2',2), ('A4',4)]:
            tv = trow[aname].strip()
            if not tv: continue
            m = re.match(r'(-?[\d.]+)\s*\((\d+)\)', tv)
            if not m: continue
            tv_v, tv_u = m.group(1), m.group(2)
            
            # Find in ENSDF
            pattern = r'(A\{-'+str(idx)+r'\}=)(-?[\d.]+)(\s*\{I)(\d+)(\})'
            m2 = re.search(pattern, line)
            if not m2: continue
            ev_v, ev_u = m2.group(2), m2.group(4)
            
            if tv_v == ev_v and tv_u != ev_u:
                # Fix uncertainty
                old = m2.group(0)
                new_unc = tv_u
                new = m2.group(1) + ev_v + m2.group(3) + new_unc + m2.group(5)
                fixes_a.append({
                    'line': i,
                    'old_text': old,
                    'new_text': new,
                    'field': aname,
                    'level': level,
                    'desc': f'{aname}={tv_v} ({tv_u}) was ({ev_u})'
                })
        
        # Check delta
        td = trow['d1'].strip()
        if td:
            # Does ENSDF already have |d=...?
            has_delta = bool(re.search(r'\|d=', line))
            if has_delta:
                # Compare values
                dm = re.search(r'\|d=([+-]?[\d.]+(?:\s*[<>GL]?[T]?\s*)?)\s*(?:\{I(\d+)\})?', line)
                if dm:
                    dv = dm.group(1).strip()
                    du = dm.group(2) if dm.lastindex and dm.lastindex >= 2 else ''
                    # Compare with Table IV
                    if td.startswith('>'):
                        if not dv.startswith('>') or abs(float(td[1:]) - float(dv[1:])) > 0.1:
                            fixes_b.append({
                                'line': i, 'action': 'fix_delta',
                                'old': dm.group(0).strip(),
                                'new': f'|d={td}',
                                'desc': f'delta: {dm.group(0).strip()} -> {td}'
                            })
                    else:
                        mt = re.match(r'(-?[\d.]+)\s*\((\d+)\)', td)
                        if mt:
                            # Table IV format: '0.006 (6)'
                            # ENSDF format: '+0.006 {I6}' or '-0.006 {I6}'
                            td_val, td_unc = mt.group(1), mt.group(2)
                            if du and (dv.lstrip('+') != td_val or du != td_unc):
                                sign = '+' if float(td_val) >= 0 else ''
                                new_d = f'|d={sign}{td_val} {{I{td_unc}}}'
                                fixes_b.append({
                                    'line': i, 'action': 'fix_delta',
                                    'old': dm.group(0).strip(),
                                    'new': new_d,
                                    'desc': f'delta: {dm.group(0).strip()} -> {new_d}'
                                })
            else:
                # Missing delta - need to add
                if td.startswith('>'):
                    # Limit value
                    new_d = f'|d={td}'
                else:
                    mt = re.match(r'(-?[\d.]+)\s*\((\d+)\)', td)
                    if mt:
                        td_val, td_unc = mt.group(1), mt.group(2)
                        sign = '+' if float(td_val) >= 0 else ''
                        new_d = f'|d={sign}{td_val} {{I{td_unc}}}'
                    else:
                        new_d = f'|d={td}'
                fixes_b.append({
                    'line': i, 'action': 'add_delta',
                    'new': new_d,
                    'desc': f'add {new_d}'
                })

print(f"Category A (uncertainty fixes): {len(fixes_a)}")
for f in fixes_a:
    print(f"  L{f['line']+1} {f['desc']}")

print(f"\nCategory B (delta fixes): {len(fixes_b)}")
for f in fixes_b:
    print(f"  L{f['line']+1} {f['action']}: {f['desc']}")
