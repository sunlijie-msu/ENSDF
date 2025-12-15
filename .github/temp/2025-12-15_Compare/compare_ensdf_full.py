import csv
import re
import sys

def parse_ensdf_energy(e_str):
    e_str = e_str.strip()
    if not e_str:
        return None
    match = re.match(r'^([\d\.]+)', e_str)
    if match:
        try:
            return float(match.group(1))
        except ValueError:
            return None
    return None

def parse_csv_energy(e_str):
    e_str = e_str.strip()
    if not e_str:
        return None
    parts = e_str.split()
    if parts:
        try:
            return float(parts[0])
        except ValueError:
            return None
    return None

def normalize_string(s):
    if s is None:
        return ""
    return s.strip()

def main():
    csv_path = r'd:\X\ND\ENSDF\XUNDL\209Po_ENSDF.csv'
    ensdf_path = r'd:\X\ND\ENSDF\XUNDL\2025DOAA_CL10995_209Po.ens'

    # --- 1. Parse CSV ---
    csv_levels = []
    current_level = None

    print(f"Reading CSV: {csv_path}")
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        
        for row in reader:
            if not row: continue
            if len(row) < 2: continue
            
            e_level_str = row[0]
            jpi_level_str = row[1]
            
            if e_level_str.strip():
                e_val = parse_csv_energy(e_level_str)
                if e_val is not None:
                    current_level = {
                        'E': e_val,
                        'E_str': e_level_str.strip(),
                        'Jpi': normalize_string(jpi_level_str),
                        'Gammas': []
                    }
                    csv_levels.append(current_level)
            
            # Parse Gamma if present (cols 2,3,4)
            # CSV: E_level, Jpi, E_gamma, Mult, ...
            if len(row) >= 4 and current_level:
                e_gamma_str = row[2]
                mult_str = row[3]
                if e_gamma_str.strip():
                    e_g_val = parse_csv_energy(e_gamma_str)
                    if e_g_val is not None:
                        current_level['Gammas'].append({
                            'E': e_g_val,
                            'Mult': normalize_string(mult_str)
                        })

    # --- 2. Parse ENSDF ---
    ensdf_levels = []
    current_ens_level = None
    
    print(f"Reading ENSDF: {ensdf_path}")
    with open(ensdf_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    for i, line in enumerate(lines):
        if len(line) > 8:
            rec_type = line[7]
            if rec_type == 'L':
                e_str = line[9:19]
                jpi_str = line[22:39]
                e_val = parse_ensdf_energy(e_str)
                if e_val is not None:
                    current_ens_level = {
                        'E': e_val,
                        'E_str': e_str.strip(),
                        'Jpi': jpi_str.strip(),
                        'LineIdx': i,
                        'Gammas': []
                    }
                    ensdf_levels.append(current_ens_level)
            elif rec_type == 'G' and current_ens_level:
                e_str = line[9:19]
                mult_str = line[32:41] # Col 33-41 (index 32-40)
                e_val = parse_ensdf_energy(e_str)
                if e_val is not None:
                    current_ens_level['Gammas'].append({
                        'E': e_val,
                        'Mult': mult_str.strip(),
                        'LineIdx': i
                    })

    # --- 3. Compare ---
    print("\n--- Jpi Mismatches ---")
    for ens_lvl in ensdf_levels:
        matched_csv_lvl = None
        min_diff = 2.0
        for csv_lvl in csv_levels:
            diff = abs(ens_lvl['E'] - csv_lvl['E'])
            if diff < min_diff:
                min_diff = diff
                matched_csv_lvl = csv_lvl
        
        if matched_csv_lvl:
            if matched_csv_lvl['Jpi'] != ens_lvl['Jpi']:
                print(f"MISMATCH at E={ens_lvl['E']}: CSV='{matched_csv_lvl['Jpi']}' vs ENSDF='{ens_lvl['Jpi']}'")

            # Compare Gammas
            for ens_g in ens_lvl['Gammas']:
                matched_csv_g = None
                min_g_diff = 1.0
                for csv_g in matched_csv_lvl['Gammas']:
                    diff = abs(ens_g['E'] - csv_g['E'])
                    if diff < min_g_diff:
                        min_g_diff = diff
                        matched_csv_g = csv_g
                
                if matched_csv_g:
                    # Normalize Mult strings for comparison (remove spaces, etc if needed)
                    # But here we want to see differences
                    if matched_csv_g['Mult'] != ens_g['Mult']:
                         print(f"  Gamma E={ens_g['E']}: Mult MISMATCH CSV='{matched_csv_g['Mult']}' vs ENSDF='{ens_g['Mult']}'")

if __name__ == '__main__':
    main()
