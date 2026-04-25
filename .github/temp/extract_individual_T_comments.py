"""Extract cL T$ comment lines from individual datasets for cross-checking."""

base = r'd:\X\ND\ENSDF\A34\Cl34\new'

datasets = {
    'G 31P(a,ng)': f'{base}/Cl34_31p_a_ng.ens',
    'I 32S(3He,pg)': f'{base}/Cl34_32s_3he_pg.ens',
    'K 33S(p,g)': f'{base}/Cl34_33s_p_g.ens',
    'E 24Mg(12C,png)': f'{base}/Cl34_24mg_12c_png.ens',
}

for label, filepath in datasets.items():
    print(f"\n=== Dataset {label} ===")
    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("  FILE NOT FOUND")
        continue
    
    current_lrec = None
    for i, line in enumerate(lines):
        raw = line.rstrip('\n')
        if len(raw) < 8:
            continue
        
        # L-record
        if raw[5] == ' ' and raw[6] == ' ' and raw[7] == 'L':
            E_field = raw[9:19].strip() if len(raw) >= 19 else ''
            T_field = raw[39:49].strip() if len(raw) >= 49 else ''
            DT_field = raw[49:55].strip() if len(raw) >= 55 else ''
            if T_field:
                current_lrec = f"E={E_field} T={T_field} DT={DT_field}"
            else:
                current_lrec = f"E={E_field}"
        
        # cL T$ comment
        if raw[5] == ' ' and raw[6:8] == 'cL' and 'T$' in raw:
            print(f"  Line {i+1} [{current_lrec}]: {raw.strip()}")
        # continuation
        elif raw[5] in '23456789' and raw[6:8] == 'cL' and current_lrec:
            pass  # skip continuation for now
