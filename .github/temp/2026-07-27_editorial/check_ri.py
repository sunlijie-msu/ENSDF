"""Cross-check G-record RI vs CSV Adopted, add cG RI comments."""
import re, csv, io

# Parse CSV
csv_text = open(r'A34\Cl34\raw\2020IA02_TABLE_IV.csv','r',encoding='utf-8-sig').read()
csv_text = csv_text.replace('\u200b','')  # remove zero-width spaces
reader = csv.reader(io.StringIO(csv_text))
header = next(reader)
print(f"CSV columns: {header}")

csv_data = {}  # Egamma_keV -> {1974Ha26, 1990En08, 2020Ia02, Adopted}
for row in reader:
    if not row or not row[0].strip(): continue
    eg = row[0].strip()
    if not eg: continue
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
        try: ri_f = float(ri_str) if ri_str else 0
        except: ri_f = 0
        g_records.append({
            'line': i+1, 'eg': eg_f, 'ri': ri_str, 'dri': dri_str,
            'line_content': l.rstrip()
        })

# Match and compare
print("\n=== RI CROSS-CHECK ===")
issues = []
for gr in g_records:
    # Find closest CSV energy
    best, bd = None, 999
    for csv_e in csv_data:
        d = abs(gr['eg'] - csv_e)
        if d < bd: best, bd = csv_e, d
    if best is None or bd > 2: continue
    
    cd = csv_data[best]
    adopted_raw = cd['adopted']
    ia02_raw = cd['ia02']
    ha26_raw = cd['ha26']
    en08_raw = cd['en08']
    
    # Convert CSV Adopted to ENSDF RI format
    # CSV format: raw number like "0.354(9)", "<0.010", "1"
    # ENSDF: percentage like "35.4" with uncertainty "9", or "1.0" with "LT"
    
    def csv_to_ensdf_ri(val_str):
        """Convert CSV relative intensity (666=1) to ENSDF RI percentage."""
        if not val_str: return (None, None, None)  # value, unc, limit
        is_lt = val_str.startswith('<')
        val_clean = val_str.lstrip('<')
        # Parse value(unc) or just value
        m = re.match(r'([\d.]+)(?:\((\d+)\))?', val_clean)
        if not m: return (None, None, None)
        val = float(m.group(1))
        unc = m.group(2)
        # Convert to percent: multiply by 100
        val_pct = val * 100
        # Determine decimal places matching original
        if '.' in val_clean:
            decimals = len(val_clean.split('.')[1])
        else:
            decimals = 0
        # Format for ENSDF
        if is_lt:
            # Limit: value with LT
            if decimals == 0:
                ensdf_val = f"{val_pct:.1f}" if val_pct < 10 else f"{val_pct:.0f}"
            else:
                ensdf_val = f"{val_pct:.{decimals}f}"
            return (ensdf_val, '', 'LT')
        else:
            if decimals == 0:
                ensdf_val = f"{val_pct:.1f}" if val_pct < 10 else f"{val_pct:.0f}"
            else:
                ensdf_val = f"{val_pct:.{decimals}f}"
            ensdf_unc = unc if unc else ''
            return (ensdf_val, ensdf_unc, '')
    
    a_val, a_unc, a_lim = csv_to_ensdf_ri(adopted_raw)
    
    # Compare with ENSDF
    ens_val = gr['ri']
    ens_unc = gr['dri']
    ens_lim = 'LT' if ens_unc == 'LT' else ''
    
    match = True
    if a_val:
        if ens_lim != a_lim: match = False
        elif abs(float(ens_val) - float(a_val)) > 0.01: match = False
    
    if not match:
        status = f"MISMATCH: ENSDF={ens_val} {ens_unc} {ens_lim} vs Adopted={a_val} {a_unc} {a_lim}"
        issues.append((gr, cd, status))
        print(f"  E{gr['eg']} keV: {status}")
    else:
        # Check if cG RI$ comment needed
        need_comment = False
        comments = []
        
        # 2020Ia02 different from Adopted?
        ia_val, ia_unc, ia_lim = csv_to_ensdf_ri(ia02_raw)
        if ia_val:
            ia_diff = False
            if ia_lim != a_lim: ia_diff = True
            elif ia_val and a_val and abs(float(ia_val) - float(a_val)) > 0.01: ia_diff = True
            if ia_diff:
                comments.append(f"2020Ia02: {ia02_raw}")
                need_comment = True
        
        # 1974Ha26
        ha_val, ha_unc, ha_lim = csv_to_ensdf_ri(ha26_raw)
        if ha_val:
            ha_diff = False
            if ha_lim != a_lim: ha_diff = True
            elif ha_val and a_val and abs(float(ha_val) - float(a_val)) > 0.01: ha_diff = True
            if ha_diff:
                comments.append(f"1974Ha26: {ha26_raw}")
                need_comment = True
        
        if need_comment:
            print(f"  E{gr['eg']} keV: NEED cG RI$ comment: {', '.join(comments)}")

print(f"\n{len(issues)} RI mismatches found.")
