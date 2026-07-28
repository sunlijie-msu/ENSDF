"""Parse revised CSV, cross-check ENSDF RI, generate cG RI$ comments."""
import re, csv, io

# Parse revised CSV
csv_text = open(r'A34\Cl34\raw\2020IA02_TABLE_IV.csv','r',encoding='utf-8-sig').read()
csv_text = csv_text.replace('\u200b','')
reader = csv.reader(io.StringIO(csv_text))
header = next(reader)
print(f"CSV: {header}")

csv_data = {}
for row in reader:
    if not row or not row[0].strip(): continue
    eg = row[0].strip()
    try: eg_f = float(eg)
    except: continue
    csv_data[eg_f] = {
        'ha26': row[1].strip() if len(row)>1 else '',
        'en08': row[2].strip() if len(row)>2 else '',
        'ia02': row[3].strip() if len(row)>3 else '',
        'adopted': row[4].strip() if len(row)>4 else '',
    }

# Parse ENSDF G-records
with open(r'A34\Cl34\new\Cl34_34ar_ec_decay_0.84646_s.ens','r') as f:
    ens_lines = f.readlines()

g_records = []
for i,l in enumerate(ens_lines):
    if len(l)>=80 and l[7]=='G' and l[8]==' ':
        eg_str = l[9:19].strip()
        ri_str = l[22:29].strip()
        dri_str = l[29:31].strip()
        try: eg_f = float(eg_str)
        except: eg_f = 0
        g_records.append({'line':i+1, 'eg':eg_f, 'ri':ri_str, 'dri':dri_str})

def csv_to_pct(val_str):
    """Convert CSV relative intensity (666=1) to ENSDF RI percentage."""
    if not val_str: return (None, None, None)
    is_lt = val_str.startswith('<')
    val_clean = val_str.lstrip('<')
    m = re.match(r'([\d.]+)(?:\((\d+)\))?', val_clean)
    if not m: return (None, None, None)
    val = float(m.group(1)) * 100
    unc = m.group(2)
    ensdf_val = str(val).rstrip('0').rstrip('.') if '.' in str(val) else str(int(val))
    if is_lt: return (ensdf_val, '', 'LT')
    return (ensdf_val, unc if unc else '', '')

print("\n=== RI CROSS-CHECK ===")
ri_fixes = []
cG_comments = []

for gr in g_records:
    best, bd = None, 999
    for csv_e in csv_data:
        d = abs(gr['eg'] - csv_e)
        if d < bd: best, bd = csv_e, d
    if best is None or bd > 2: continue
    
    cd = csv_data[best]
    
    # Compare ENSDF RI with CSV Adopted
    a_val, a_unc, a_lim = csv_to_pct(cd['adopted'])
    ia_val, ia_unc, ia_lim = csv_to_pct(cd['ia02'])
    ha_val, ha_unc, ha_lim = csv_to_pct(cd['ha26'])
    
    ens_val = gr['ri']
    ens_unc = gr['dri']
    ens_lim = 'LT' if ens_unc == 'LT' else ''
    
    # Compare
    match = True
    if a_val:
        if ens_lim != a_lim:
            match = False
        elif abs(float(ens_val) - float(a_val)) > 0.01:
            match = False
        elif a_unc and ens_unc != a_unc:
            # Different uncertainty
            match = False
    
    if not match:
        ri_fixes.append((gr['eg'], gr['line'], ens_val, ens_unc, ens_lim, a_val, a_unc, a_lim))
        print(f"  E{gr['eg']}: MISMATCH ENSDF={ens_val} {ens_unc} {ens_lim} vs ADOPTED={a_val} {a_unc} {a_lim}")
    
    # Check if cG RI$ comment needed
    need_comment = False
    parts = []
    
    # 2020Ia02 different from Adopted?
    if ia_val:
        ia_diff = (ia_lim != a_lim) or (a_val and ia_val and abs(float(ia_val) - float(a_val)) > 0.005)
        if ia_diff:
            ia_raw = cd['ia02']
            ia_clean = re.match(r'([<]?)([\d.]+)(?:\((\d+)\))?', ia_raw)
            if ia_clean:
                ia_sign = ia_clean.group(1)
                ia_v = float(ia_clean.group(2)) * 100
                ia_u = ia_clean.group(3)
                ia_v_str = str(ia_v).rstrip('0').rstrip('.') if '.' in str(ia_v) else str(int(ia_v))
                if ia_sign:
                    parts.append(f"<{ia_v_str} (2020Ia02)")
                elif ia_u:
                    parts.append(f"{ia_v_str} {{I{ia_u}}} (2020Ia02)")
                else:
                    parts.append(f"{ia_v_str} (2020Ia02)")
                need_comment = True
    
    # 1974Ha26 (always add if available and different)
    if ha_val:
        ha_diff = (ha_lim != a_lim) or (a_val and ha_val and abs(float(ha_val) - float(a_val)) > 0.005)
        if ha_diff:
            ha_raw = cd['ha26']
            ha_clean = re.match(r'([<]?)([\d.]+)(?:\((\d+)\))?', ha_raw)
            if ha_clean:
                ha_sign = ha_clean.group(1)
                ha_v = float(ha_clean.group(2)) * 100
                ha_u = ha_clean.group(3)
                ha_v_str = str(ha_v).rstrip('0').rstrip('.') if '.' in str(ha_v) else str(int(ha_v))
                if ha_sign:
                    parts.append(f"<{ha_v_str} (1974Ha26)")
                elif ha_u:
                    parts.append(f"{ha_v_str} {{I{ha_u}}} (1974Ha26)")
                else:
                    parts.append(f"{ha_v_str} (1974Ha26)")
                need_comment = True
    
    if need_comment:
        comment = ". ".join(parts) + "."
        cG_comments.append((gr['eg'], gr['line'], comment.strip()))
        print(f"  E{gr['eg']}: NEED cG RI$ {comment}")

print(f"\n{len(ri_fixes)} RI mismatches, {len(cG_comments)} cG comments needed")

# Check: any existing cG RI$ lines need to be removed?
print("\n=== Existing cG RI$ lines ===")
for i,l in enumerate(ens_lines):
    if 'cG RI' in l:
        print(f"  L{i+1}: [{l.rstrip()}]")
