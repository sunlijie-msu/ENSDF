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
                        'Jpi': normalize_string(jpi_level_str)
                    }
                    csv_levels.append(current_level)

    # --- 2. Parse ENSDF ---
    ensdf_levels = []
    
    print(f"Reading ENSDF: {ensdf_path}")
    with open(ensdf_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    for i, line in enumerate(lines):
        if len(line) > 8 and line[7] == 'L':
            e_str = line[9:19]
            jpi_str = line[22:39]
            
            e_val = parse_ensdf_energy(e_str)
            if e_val is not None:
                ensdf_levels.append({
                    'E': e_val,
                    'E_str': e_str.strip(),
                    'Jpi': jpi_str.strip(), # Keep exact spacing from ENSDF for comparison
                    'LineIdx': i,
                    'OriginalLine': line
                })

    # --- 3. Compare ---
    print("\n--- Jpi Mismatches ---")
    
    for ens_lvl in ensdf_levels:
        # Find matching level in CSV
        matched_csv_lvl = None
        min_diff = 2.0 # Tolerance
        
        for csv_lvl in csv_levels:
            diff = abs(ens_lvl['E'] - csv_lvl['E'])
            if diff < min_diff:
                min_diff = diff
                matched_csv_lvl = csv_lvl
        
        if matched_csv_lvl:
            csv_jpi = matched_csv_lvl['Jpi']
            ens_jpi = ens_lvl['Jpi']
            
            # Strict string comparison
            if csv_jpi != ens_jpi:
                print(f"MISMATCH at E={ens_lvl['E']} (CSV E={matched_csv_lvl['E']}):")
                print(f"  CSV:   '{csv_jpi}'")
                print(f"  ENSDF: '{ens_jpi}'")
                print(f"  Line {ens_lvl['LineIdx']+1}")

if __name__ == '__main__':
    main()
