import csv
import re
import sys

def parse_energy(e_str):
    e_str = e_str.strip()
    if not e_str:
        return None
    # Handle cases like "1234.5" or "1234" or "1.23E+4"
    # Just take the first float-like sequence
    match = re.match(r'^([\d\.]+)', e_str)
    if match:
        try:
            return float(match.group(1))
        except ValueError:
            return None
    return None

def main():
    csv_path = r'd:\X\ND\ENSDF\XUNDL\209Po_NDS2015.csv'
    ensdf_path = r'd:\X\ND\ENSDF\XUNDL\2025DOAA_CL10995_209Po.ens'

    # --- 1. Load NDS 2015 Data (Known Gammas) ---
    # Structure: list of { 'E': level_E, 'Gammas': [gamma_E, ...] }
    nds_levels = []
    current_nds_level = None

    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader) # Skip header
            
            for row in reader:
                if not row: continue
                if len(row) < 2: continue
                
                # Check for new level
                e_level_str = row[0].strip()
                if e_level_str:
                    e_val = parse_energy(e_level_str)
                    if e_val is not None:
                        current_nds_level = {
                            'E': e_val,
                            'Gammas': []
                        }
                        nds_levels.append(current_nds_level)
                
                # Check for gamma in current level
                # CSV cols: E(level), Jpi, E(gamma), ...
                if len(row) >= 3 and current_nds_level:
                    e_gamma_str = row[2].strip()
                    if e_gamma_str:
                        e_g_val = parse_energy(e_gamma_str)
                        if e_g_val is not None:
                            current_nds_level['Gammas'].append(e_g_val)

    except Exception as e:
        print(f"Error reading CSV: {e}")
        return

    # --- 2. Check ENSDF Gammas ---
    print(f"{'Level E':<10} | {'Gamma E':<10} | {'Status':<30} | {'Line':<5}")
    print("-" * 65)

    with open(ensdf_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    current_ens_level_E = None
    
    mismatch_count = 0
    checked_count = 0

    for i, line in enumerate(lines):
        if len(line) < 8: continue
        
        rec_type = line[7] # Col 8 is index 7
        
        if rec_type == 'L':
            e_str = line[9:19]
            current_ens_level_E = parse_energy(e_str)
            
        elif rec_type == 'G':
            if current_ens_level_E is None:
                continue

            # Check for 'X' flag in column 77 (index 76)
            # Line might be shorter than 77 chars
            has_X_flag = False
            if len(line) > 76:
                if line[76] == 'X':
                    has_X_flag = True
            
            # User Request: "those gammas without labeling asterisks (X flag) are supposed to be known gammas"
            if not has_X_flag:
                checked_count += 1
                e_gamma_str = line[9:19]
                e_gamma_val = parse_energy(e_gamma_str)
                
                if e_gamma_val is None:
                    continue

                # Verify this gamma exists in NDS 2015
                # 1. Find matching level
                matched_level = None
                min_lvl_diff = 3.0 # Tolerance for level energy
                
                for lvl in nds_levels:
                    diff = abs(lvl['E'] - current_ens_level_E)
                    if diff < min_lvl_diff:
                        min_lvl_diff = diff
                        matched_level = lvl
                
                if not matched_level:
                    print(f"{current_ens_level_E:<10} | {e_gamma_val:<10} | {'Level NOT FOUND in NDS2015':<30} | {i+1:<5}")
                    mismatch_count += 1
                    continue
                
                # 2. Find matching gamma in that level
                gamma_found = False
                min_g_diff = 1.5 # Tolerance for gamma energy
                
                for g_e in matched_level['Gammas']:
                    diff = abs(g_e - e_gamma_val)
                    if diff < min_g_diff:
                        gamma_found = True
                        break
                
                if not gamma_found:
                    print(f"{current_ens_level_E:<10} | {e_gamma_val:<10} | {'Gamma NOT FOUND in NDS2015':<30} | {i+1:<5}")
                    mismatch_count += 1

    print("-" * 65)
    print(f"Checked {checked_count} gammas (without 'X' flag).")
    if mismatch_count == 0:
        print("SUCCESS: All non-flagged gammas were found in NDS 2015.")
    else:
        print(f"FOUND {mismatch_count} DISCREPANCIES.")

if __name__ == '__main__':
    main()
