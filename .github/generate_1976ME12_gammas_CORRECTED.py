"""
CORRECTED G-record generator for 1976ME12 resonances with proper LT marker handling
Fixes issues: missing LT markers for limit values, incorrect spacing
"""
import csv

def format_g_record(eg_kev, ri_value, is_limit=False):
    """
    Format G-record with proper ENSDF 80-column structure
    
    Args:
        eg_kev: Gamma energy in keV
        ri_value: Relative intensity value (numeric part only, no '<')
        is_limit: True if this is a limit value (<X)
    
    Returns:
        80-character G-record string
    """
    # NUCID + continuation + blank + type + blank (cols 1-9)
    nucid_part = " 35CL  G "
    
    # Eg field (cols 10-19) - LEFT-JUSTIFIED
    if isinstance(eg_kev, float) and eg_kev != int(eg_kev):
        eg_str = f"{eg_kev:.1f}"
    else:
        eg_str = str(int(eg_kev))
    eg_field = f"{eg_str:<10}"
    
    # DE field (cols 20-21) - BLANK (no uncertainty)
    de_field = "  "
    
    # Space separator (col 22)
    space = " "
    
    # RI field (cols 23-29) - LEFT-JUSTIFIED
    if isinstance(ri_value, float) and ri_value != int(ri_value):
        ri_str = str(ri_value)
    else:
        ri_str = str(int(ri_value))
    ri_field = f"{ri_str:<7}"
    
    # DRI field (cols 30-31) - LT for limits, blank otherwise
    if is_limit:
        dri_field = "LT"
    else:
        dri_field = "  "
    
    # Remaining fields blank (cols 32-80) - 49 characters
    remaining = " " * 49
    
    # Assemble full record
    record = nucid_part + eg_field + de_field + space + ri_field + dri_field + remaining
    
    # Verify exactly 80 characters
    if len(record) != 80:
        raise ValueError(f"G-record not 80 chars: {len(record)} chars")
    
    return record

# Final level energies in keV (MeV * 1000)
final_levels = {
    '0': 0,
    '1.22': 1220, 
    '1.76': 1760,
    '2.65': 2650,
    '2.69': 2690,
    '3': 3000,
    '3.16': 3160,
    '3.92': 3920,
    '3.94': 3940,
    '3.98': 3980,
    '4.06': 4060,
    '4.11': 4110,
    '4.175': 4175,
    '4.18': 4180
}

# Process CSV data with proper limit handling
gamma_groups = {}

with open('A35/Cl35/temp/1976ME12_Branching_Ratios.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        # Clean keys due to spaces in header
        clean_row = {k.strip(): v.strip() for k, v in row.items() if v.strip()}
        
        ep_kev = int(clean_row['Ep_keV'])
        ex_kev = int(clean_row['Ex_keV'])
        
        gamma_records = []
        
        for final_mev_str, final_kev in final_levels.items():
            if final_mev_str in clean_row and clean_row[final_mev_str]:
                ri_raw = clean_row[final_mev_str]
                
                # Check if this is a limit value
                is_limit = ri_raw.startswith('<')
                if is_limit:
                    ri_value = float(ri_raw[1:])  # Remove '<' and convert
                else:
                    ri_value = float(ri_raw)
                
                # Calculate gamma energy
                eg_kev = ex_kev - final_kev
                
                # Store gamma data: (Eg, RI, is_limit)
                gamma_records.append((eg_kev, ri_value, is_limit))
        
        # Sort by ascending Eg (ENSDF requirement)
        gamma_records.sort(key=lambda x: x[0])
        
        # Store for this Ep
        gamma_groups[ep_kev] = gamma_records

# Generate output
print("[*] Generating CORRECTED G-records for 1976ME12 resonances with proper LT handling...")

output_lines = []
total_gammas = 0

for ep_kev in sorted(gamma_groups.keys()):
    gamma_records = gamma_groups[ep_kev]
    ex_kev = None
    
    # Find Ex_keV for this Ep
    with open('A35/Cl35/temp/1976ME12_Branching_Ratios.csv') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['Ep_keV'].strip() == str(ep_kev):
                ex_kev = int(row[' Ex_keV'].strip())
                break
    
    if ex_kev is None:
        continue
    
    # Header comment
    limit_count = sum(1 for _, _, is_limit in gamma_records if is_limit)
    regular_count = len(gamma_records) - limit_count
    header = f"# Ep={ep_kev} keV, Ex={ex_kev} keV ({len(gamma_records)} gammas: {regular_count} regular + {limit_count} limits)"
    output_lines.append(header)
    
    # Generate G-records
    for eg_kev, ri_value, is_limit in gamma_records:
        g_record = format_g_record(eg_kev, ri_value, is_limit)
        output_lines.append(g_record)
        total_gammas += 1
    
    output_lines.append("")  # Blank line between groups

# Write output file
output_file = "A35/Cl35/temp/1976ME12_gammas_CORRECTED.txt"
with open(output_file, 'w') as f:
    for line in output_lines:
        f.write(line + '\\n')

print(f"[OK] Generated {total_gammas} G-records for {len(gamma_groups)} resonances")
print(f"[OK] Output file: {output_file}")

# Show limit summary
limit_gammas = []
for ep_kev, gammas in gamma_groups.items():
    for eg_kev, ri_value, is_limit in gammas:
        if is_limit:
            limit_gammas.append((ep_kev, eg_kev, ri_value))

print(f"[*] Limit values (should have LT in DRI field): {len(limit_gammas)}")
for ep, eg, ri in limit_gammas:
    print(f"    Ep={ep} keV -> G {eg:<5} {ri:<5} LT")