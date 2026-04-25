"""
Extract all L-record lifetime data (T field) from individual Cl34 datasets
and the adopted file T$ comments for cross-checking.
"""
import re

def get_lrecords_with_T(filepath, dataset_label):
    """Extract L-records that have T field values (non-blank cols 40-49)."""
    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        return []
    
    results = []
    current_lrec = None
    
    for i, line in enumerate(lines):
        raw = line.rstrip('\n')
        if len(raw) < 8:
            continue
        
        # L-record: col6=blank, col7=blank, col8='L'
        # Actually ENSDF: col6 = continuation (blank for first), col7 = blank, col8 = L
        # In 0-indexed: raw[5]=' ', raw[6]=' ', raw[7]='L'
        if len(raw) >= 8 and raw[5] == ' ' and raw[6] == ' ' and raw[7] == 'L':
            # This is an L-record
            E_field = raw[9:19].strip() if len(raw) >= 19 else ''
            T_field = raw[39:49].strip() if len(raw) >= 49 else ''
            DT_field = raw[49:55].strip() if len(raw) >= 55 else ''
            
            if T_field:
                current_lrec = {
                    'line': i+1,
                    'raw': raw,
                    'E': E_field,
                    'T': T_field,
                    'DT': DT_field,
                    'dataset': dataset_label
                }
                results.append(current_lrec)
    
    return results

base = r'd:\X\ND\ENSDF\A34\Cl34\new'

datasets = {
    'G (31P,a,ng)':  f'{base}/Cl34_31p_a_ng.ens',
    'I (32S,3He,pg)': f'{base}/Cl34_32s_3he_pg.ens',
    'K (33S,p,g)':   f'{base}/Cl34_33s_p_g.ens',
    'E (24Mg,12C,png)': f'{base}/Cl34_24mg_12c_png.ens',
    'H (32S,3He,p)': f'{base}/Cl34_32s_3he_p.ens',
}

for label, filepath in datasets.items():
    records = get_lrecords_with_T(filepath, label)
    print(f"\n=== Dataset {label} ===")
    print(f"  L-records with T field: {len(records)}")
    for r in records:
        print(f"  Line {r['line']:4d} | E={r['E']:12s} | T={r['T']:12s} | DT={r['DT']:6s}")
