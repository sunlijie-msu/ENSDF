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
    csv_path = r'd:\X\ND\ENSDF\XUNDL\209Po_NDS2015.csv'
    ensdf_path = r'd:\X\ND\ENSDF\XUNDL\2025DOAA_CL10995_209Po.ens'

    # --- 1. Parse CSV (NDS 2015) ---
    csv_levels = []
    current_level = None

    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            
            for row in reader:
                if not row: continue
                if len(row) < 2: continue
                
                e_level_str = row[0]
                
                if e_level_str.strip():
                    e_val = parse_csv_energy(e_level_str)
                    if e_val is not None:
                        current_level = {
                            'E': e_val,
                            'Gammas': []
                        }
                        csv_levels.append(current_level)
                
                # Parse Gamma if present (cols 2,3,4)
                # CSV Header: E(level),Jπ(level),E(γ),M(γ),E(level) final,Jπ(level) final
                # Row indices: 0, 1, 2, 3, 4, 5
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
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return

    # --- 2. Parse ENSDF (2025DOAA) ---
    ensdf_levels = []
    current_ens_level = None
    
    with open(ensdf_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    for i, line in enumerate(lines):
        if len(line) > 8:
            rec_type = line[7]
            if rec_type == 'L':
                e_str = line[9:19]
                e_val = parse_ensdf_energy(e_str)
                if e_val is not None:
                    current_ens_level = {
                        'E': e_val,
                        'Gammas': []
                    }
                    ensdf_levels.append(current_ens_level)
            elif rec_type == 'G' and current_ens_level:
                e_str = line[9:19]
                mult_str = line[32:41] # Col 33-41
                e_val = parse_ensdf_energy(e_str)
                if e_val is not None:
                    current_ens_level['Gammas'].append({
                        'E': e_val,
                        'Mult': mult_str.strip(),
                        'LineIdx': i + 1
                    })

    # --- 3. Compare and Report ---
    print(f"{'Gamma E (keV)':<15} | {'NDS 2015 Mult':<20} | {'2025 ENSDF Mult':<20} | {'Line':<5}")
    print("-" * 70)

    for ens_lvl in ensdf_levels:
        # Find matching level in CSV
        matched_csv_lvl = None
        min_diff = 3.0 # Tolerance for level energy
        
        for csv_lvl in csv_levels:
            diff = abs(ens_lvl['E'] - csv_lvl['E'])
            if diff < min_diff:
                min_diff = diff
                matched_csv_lvl = csv_lvl
        
        if matched_csv_lvl:
            for ens_g in ens_lvl['Gammas']:
                matched_csv_g = None
                min_g_diff = 1.5 # Tolerance for gamma energy
                
                for csv_g in matched_csv_lvl['Gammas']:
                    diff = abs(ens_g['E'] - csv_g['E'])
                    if diff < min_g_diff:
                        min_g_diff = diff
                        matched_csv_g = csv_g
                
                if matched_csv_g:
                    csv_mult = matched_csv_g['Mult']
                    ens_mult = ens_g['Mult']
                    
                    # Filter: Only show if they differ
                    # Normalize for comparison (ignore spaces)
                    if csv_mult.replace(" ", "") != ens_mult.replace(" ", ""):
                         print(f"{ens_g['E']:<15} | {csv_mult:<20} | {ens_mult:<20} | {ens_g['LineIdx']:<5}")

if __name__ == '__main__':
    main()
