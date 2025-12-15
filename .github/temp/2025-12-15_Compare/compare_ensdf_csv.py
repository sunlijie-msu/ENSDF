import csv
import re
import sys

def parse_ensdf_energy(e_str):
    """
    Parses ENSDF energy string to float.
    Handles non-numeric values by returning None.
    """
    e_str = e_str.strip()
    if not e_str:
        return None
    # Remove uncertainty or other chars if attached directly?
    # Usually ENSDF E field is just the number, maybe with letters like 'X', 'Y', 'S', etc.
    # We only care about numeric part for matching.
    # Regex to find the first float number
    match = re.match(r'^([\d\.]+)', e_str)
    if match:
        try:
            return float(match.group(1))
        except ValueError:
            return None
    return None

def parse_csv_energy(e_str):
    """
    Parses CSV energy string like '544.98 8' to float 544.98.
    """
    e_str = e_str.strip()
    if not e_str:
        return None
    # Take the first part before space
    parts = e_str.split()
    if parts:
        try:
            return float(parts[0])
        except ValueError:
            return None
    return None

def normalize_string(s):
    """
    Trims whitespace.
    """
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
        # The file might have non-standard separators or encoding issues based on the snippet
        # But let's try standard csv reader first.
        # The snippet showed "544.98 8 ,5/2-," which suggests comma delimiter.
        reader = csv.reader(f)
        header = next(reader) # Skip header
        
        for row in reader:
            if not row: continue
            if len(row) < 4: continue
            
            # E(level), Jpi(level), E(gamma), M(gamma)
            # Note: The snippet showed 6 columns: E(level),Jπ(level),E(γ),M(γ),E(level) final,Jπ(level) final
            
            e_level_str = row[0]
            jpi_level_str = row[1]
            e_gamma_str = row[2]
            mult_gamma_str = row[3]
            
            # Check if it's a new level
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
            
            # Add gamma to current level
            if current_level and e_gamma_str.strip():
                e_g_val = parse_csv_energy(e_gamma_str)
                if e_g_val is not None:
                    gamma = {
                        'E': e_g_val,
                        'E_str': e_gamma_str.strip(),
                        'M': normalize_string(mult_gamma_str)
                    }
                    current_level['Gammas'].append(gamma)

    print(f"Loaded {len(csv_levels)} levels from CSV.")

    # --- 2. Parse ENSDF ---
    ensdf_levels = []
    current_ensdf_level = None
    
    print(f"Reading ENSDF: {ensdf_path}")
    with open(ensdf_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    for line in lines:
        if len(line) < 10: continue
        
        # L-record
        if line[7] == 'L':
            e_str = line[9:19]
            jpi_str = line[22:39] # J starts at 23 (index 22)
            
            e_val = parse_ensdf_energy(e_str)
            if e_val is not None: # Skip non-numeric levels if any?
                current_ensdf_level = {
                    'E': e_val,
                    'E_str': e_str.strip(),
                    'Jpi': normalize_string(jpi_str),
                    'Gammas': []
                }
                ensdf_levels.append(current_ensdf_level)
            else:
                # Maybe 0.0?
                if "0.0" in e_str:
                     current_ensdf_level = {
                        'E': 0.0,
                        'E_str': e_str.strip(),
                        'Jpi': normalize_string(jpi_str),
                        'Gammas': []
                    }
                     ensdf_levels.append(current_ensdf_level)
                else:
                    current_ensdf_level = None # Skip gammas for unparsed level

        # G-record
        elif line[7] == 'G' and current_ensdf_level:
            e_g_str = line[9:19]
            m_str = line[32:41] # M starts at 33 (index 32)
            
            e_g_val = parse_ensdf_energy(e_g_str)
            if e_g_val is not None:
                gamma = {
                    'E': e_g_val,
                    'E_str': e_g_str.strip(),
                    'M': normalize_string(m_str)
                }
                current_ensdf_level['Gammas'].append(gamma)

    print(f"Loaded {len(ensdf_levels)} levels from ENSDF.")

    # --- 3. Compare ---
    print("\n--- Comparison Results ---")
    print("Checking if CSV data (2015) matches ENSDF data (2025)...")
    
    for csv_lvl in csv_levels:
        # Find matching level in ENSDF
        matched_ensdf_lvl = None
        min_diff = 3.0 # Tolerance in keV
        
        for ens_lvl in ensdf_levels:
            diff = abs(csv_lvl['E'] - ens_lvl['E'])
            if diff < min_diff:
                min_diff = diff
                matched_ensdf_lvl = ens_lvl
        
        if matched_ensdf_lvl:
            # Compare Jpi
            csv_jpi = csv_lvl['Jpi']
            ens_jpi = matched_ensdf_lvl['Jpi']
            
            if csv_jpi != ens_jpi:
                print(f"MISMATCH Level Jpi at E~{csv_lvl['E']}:")
                print(f"  CSV (2015): '{csv_jpi}'")
                print(f"  ENSDF(2025): '{ens_jpi}'")
            
            # Compare Gammas
            for csv_g in csv_lvl['Gammas']:
                matched_ensdf_g = None
                min_g_diff = 2.0 # Tolerance
                
                for ens_g in matched_ensdf_lvl['Gammas']:
                    g_diff = abs(csv_g['E'] - ens_g['E'])
                    if g_diff < min_g_diff:
                        min_g_diff = g_diff
                        matched_ensdf_g = ens_g
                
                if matched_ensdf_g:
                    csv_m = csv_g['M']
                    ens_m = matched_ensdf_g['M']
                    
                    # Normalize empty strings
                    if csv_m == "" and ens_m == "": continue
                    
                    if csv_m != ens_m:
                        print(f"MISMATCH Gamma Mult at E_lvl~{csv_lvl['E']} E_gam~{csv_g['E']}:")
                        print(f"  CSV (2015): '{csv_m}'")
                        print(f"  ENSDF(2025): '{ens_m}'")
                else:
                    # Gamma in CSV but not in ENSDF?
                    # User only asked to check if known ones match.
                    # If it's missing, is it a mismatch? Maybe.
                    # But let's focus on mismatches of values first.
                    pass
        else:
            # Level in CSV but not in ENSDF?
            pass

if __name__ == '__main__':
    main()
