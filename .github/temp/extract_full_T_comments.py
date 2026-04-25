"""Read full T$ comment blocks (including continuations) from individual datasets."""

base = r'd:\X\ND\ENSDF\A34\Cl34\new'

datasets = {
    'G 31P(a,ng)': f'{base}/Cl34_31p_a_ng.ens',
    'I 32S(3He,pg)': f'{base}/Cl34_32s_3he_pg.ens',
    'K 33S(p,g)': f'{base}/Cl34_33s_p_g.ens',
    'E 24Mg(12C,png)': f'{base}/Cl34_24mg_12c_png.ens',
    'F 27Al(12C,ang)': f'{base}/Cl34_27al_12c_ang.ens',
}

for label, filepath in datasets.items():
    print(f"\n=== Dataset {label} ===")
    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("  FILE NOT FOUND")
        continue
    
    current_lrec_info = None
    in_t_block = False
    t_block_lines = []
    
    for i, line in enumerate(lines):
        raw = line.rstrip('\n')
        if len(raw) < 8:
            continue
        
        # L-record
        if raw[5] == ' ' and raw[6] == ' ' and raw[7] == 'L':
            # flush previous T block
            if in_t_block and t_block_lines:
                for tl in t_block_lines:
                    print(f"  {tl}")
                t_block_lines = []
                in_t_block = False
            
            E_field = raw[9:19].strip() if len(raw) >= 19 else ''
            T_field = raw[39:49].strip() if len(raw) >= 49 else ''
            DT_field = raw[49:55].strip() if len(raw) >= 55 else ''
            current_lrec_info = f"L E={E_field} T={T_field} DT={DT_field}"
        
        # cL T$ comment (first line)
        if raw[5] == ' ' and raw[6:8] == 'cL' and 'T$' in raw:
            in_t_block = True
            t_block_lines = [f"  [{current_lrec_info}] Line {i+1}: {raw.strip()}"]
        # continuation cL lines while in T block
        elif in_t_block and len(raw) >= 8 and raw[6:8] == 'cL' and raw[5] in '23456789':
            t_block_lines.append(f"    (cont) Line {i+1}: {raw.strip()}")
        elif in_t_block:
            # Not a continuation, flush
            for tl in t_block_lines:
                print(tl)
            t_block_lines = []
            in_t_block = False
    
    # flush at end
    if in_t_block and t_block_lines:
        for tl in t_block_lines:
            print(tl)
