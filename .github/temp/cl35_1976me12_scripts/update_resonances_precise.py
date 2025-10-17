"""
Update resonance L-records with precise Ex, Ep, and Gamma-width data.
ENSDF L-record format:
- Columns 10-19: Ex (LEFT-JUSTIFIED)
- Columns 20-21: DE (uncertainty in Ex, LEFT-JUSTIFIED)
- Columns 65-74: S field (Ep value, LEFT-JUSTIFIED)
- Columns 75-76: DS field (uncertainty in Ep, LEFT-JUSTIFIED)

cL comment format:
- Add Gamma|g width in ENSDF notation after Ep information
"""

# High-precision data from user
resonance_data = [
    (7067.5, 716.0, 1.0, 0.3, 0.1),
    (7105.0, 754.6, 1.0, 0.5, 0.2),
    (7180.4, 832.2, 1.5, 0.3, 0.1),
    (7195.9, 848.1, 1.0, 1.2, 0.4),
    (7226.2, 879.3, 1.0, 0.3, 0.1),
    (7235.1, 888.5, 1.0, 1.9, 0.6),
    (7274.5, 929.0, 1.0, 2.2, 0.7),
    (7363.8, 1021.0, 1.0, 3.1, 0.9),
    (7398.7, 1056.9, 1.6, 0.5, 0.2),
    (7452.4, 1112.2, 0.6, 0.4, 0.1),
    (7504.1, 1165.4, 0.7, 0.8, 0.2),
    (7519.6, 1181.4, 0.7, 0.4, 0.1),
    (7549.8, 1212.4, 0.7, 21, 3),
    (7562.3, 1225.3, 0.7, 1.5, 0.5),
    (7601.5, 1265.7, 0.8, 2.8, 0.8),
    (7619.8, 1284.5, 0.5, 1.7, 0.5),
    (7658.4, 1324.2, 0.8, 0.8, 0.2),
    (7673.4, 1339.7, 0.8, 1.3, 0.4),
    (7687.1, 1353.8, 0.8, 2.8, 0.8),
    (7695.4, 1362.3, 0.8, 0.6, 0.2),
    (7707.8, 1375.1, 0.8, 4.4, 1.3),
    (7746.3, 1414.7, 0.9, 1.7, 0.5),
    (7778.1, 1447.5, 0.9, 1.5, 0.5),
    (7782.8, 1452.3, 1.3, 0.9, 0.3),
    (7798.3, 1468.2, 0.9, 1.4, 0.4),
    (7839.1, 1510.2, 1.0, 4.8, 1.4),
    (7840.4, 1511.6, 0.9, 6.1, 1.8),
    (7870.1, 1542.2, 1.0, 1.0, 0.3),
    (7882.3, 1554.7, 0.9, 2.2, 0.7),
    (7900.7, 1573.7, 0.7, 2.2, 0.7),
    (7924.7, 1598.4, 0.9, 1.0, 0.3),
    (7972.0, 1647.1, 1.0, 1.9, 0.6),
    (7990.5, 1666.1, 1.0, 1.2, 0.4),
    (7996.9, 1672.7, 1.0, 2.1, 0.6),
    (8002.2, 1678.1, 0.9, 2.9, 0.9),
    (8006.4, 1682.5, 1.0, 4.8, 1.4),
    (8037.9, 1714.9, 1.0, 0.8, 0.2),
    (8040.2, 1717.3, 1.1, 2.9, 0.9),
    (8077.5, 1755.7, 1.1, 1.6, 0.5),
    (8097.3, 1776.0, 1.1, 2.4, 0.7),
    (8107.8, 1786.9, 1.1, 3.7, 1.1),
    (8114.9, 1794.2, 1.1, 1.6, 0.5),
    (8149.2, 1829.5, 1.1, 1.7, 0.5),
    (8158.6, 1839.1, 1.1, 1.9, 0.6),
    (8180.9, 1862.1, 1.2, 0.9, 0.3),
    (8209.3, 1891.3, 1.2, 9.0, 2.7),
    (8217.3, 1899.6, 1.1, 7.1, 2.1),
    (8243.5, 1926.5, 1.2, 2.2, 0.7),
    (8270.5, 1954.3, 1.2, 2.0, 0.6),
    (8278.7, 1962.8, 1.2, 1.5, 0.5),
    (8283.6, 1967.8, 1.2, 1.3, 0.4),
    (8289.4, 1973.8, 1.2, 1.6, 0.5),
    (8299.8, 1984.5, 1.2, 3.5, 1.1),
    (8320.7, 2006.0, 1.3, 4.2, 1.3),
    (8324.5, 2009.9, 1.3, 1.6, 0.5),
]

def format_uncertainty(value):
    """Format uncertainty as left-justified 2-char string."""
    if value < 10:
        return f"{int(value)} "
    else:
        return f"{int(value)}"

def format_gamma_width_eV(width_eV,unc_eV):
    """Format gamma width in eV for cL comment."""
    # Convert to ENSDF uncertainty notation
    # E.g., 0.3(1) eV, 1.5(5) eV, 21(3) eV
    if width_eV >= 10:
        # Integer values
        return f"{int(width_eV)}{{I{int(unc_eV)}}} eV"
    elif width_eV >= 1:
        # One decimal place
        unc_last_digit = int(unc_eV * 10)
        return f"{width_eV:.1f}{{I{unc_last_digit}}} eV"
    else:
        # One decimal place for values < 1
        unc_last_digit = int(unc_eV * 10)
        return f"{width_eV:.1f}{{I{unc_last_digit}}} eV"

def generate_L_record(ex, dex, ep, dep):
    """Generate L-record with precise Ex, DE, Ep (S field), and DEp (DS field)."""
    # ENSDF L-record format (80 characters):
    # Cols 1-5: NUCID, 6: blank, 7: blank, 8: "L", 9: blank
    # Cols 10-19: Ex (LEFT-JUSTIFIED)
    # Cols 20-21: DE (LEFT-JUSTIFIED)
    # Cols 22-64: other fields (blank for resonances)
    # Cols 65-74: S field (Ep value, LEFT-JUSTIFIED)
    # Cols 75-76: DS field (DEp uncertainty, LEFT-JUSTIFIED)
    # Cols 77-80: flags/blank
    
    nucid = " 35CL"
    
    # Format Ex with one decimal place (LEFT-JUSTIFIED in 10-char field)
    ex_str = f"{ex:.1f}".ljust(10)
    
    # Format DE (uncertainty) - left-justified in 2-char field
    de_str = format_uncertainty(dex * 10)  # Convert 1.0 keV → 10 (last digit)
    
    # Format Ep (S field) - left-justified in 10-char field
    ep_str = f"{ep:.1f}".ljust(10)
    
    # Format DEp (DS field) - left-justified in 2-char field
    dep_str = format_uncertainty(dep * 10)  # Convert 1.0 keV → 10 (last digit)
    
    # Build L-record: cols 1-5, 6, 7, 8, 9, 10-19, 20-21, 22-64, 65-74, 75-76, 77-80
    # CRITICAL: Cols 22-64 is 43 spaces (64-22+1), not 42!
    line = f"{nucid}  L {ex_str}{de_str}{' ' * 43}{ep_str}{dep_str}    "
    
    return line.ljust(80)

def generate_cL_record(ep, gamma_width_eV, unc_eV):
    """Generate cL comment with Ep and Gamma-width."""
    # Format: " 35CL cL $\|w|g=VALUE, (1976Me12,Ep=XXX keV)"
    
    nucid = " 35CL"
    
    # Format gamma width
    gamma_str = format_gamma_width_eV(gamma_width_eV, unc_eV)
    
    # Format Ep (no decimal if integer, one decimal otherwise)
    if ep == int(ep):
        ep_str = f"{int(ep)}"
    else:
        ep_str = f"{ep:.1f}"
    
    # Build comment
    comment = f"{nucid} cL $\|w|g={gamma_str} (1976Me12,Ep={ep_str} keV)"
    
    return comment.ljust(80)

# Read existing file to extract gamma data
print("Reading existing resonance data...")
import os
file_path = os.path.join('A35', 'Cl35', 'temp', '1976ME12.ens')
with open(file_path, 'r') as f:
    lines = f.readlines()

# Find resonance section (starts at line 191, index 190)
resonance_start = 190

# Parse existing gamma data for each resonance
current_resonances = {}
current_ep = None
current_gammas = []

for i in range(resonance_start, len(lines)):
    line = lines[i]
    if len(line) < 10:
        break
    
    # Check record type: position 7 is 'L' for L-record, 'c' for cL, 'G' for G-record
    if line[7] == 'L' and line[6] == ' ':  # "  L " pattern
        # New L-record - save previous
        if current_ep is not None and current_gammas:
            current_resonances[current_ep] = current_gammas
        
        # Extract Ep from S field (cols 65-74)
        ep_field = line[64:74].strip()
        try:
            current_ep = float(ep_field) if ep_field else None
        except:
            current_ep = None
        current_gammas = []
    
    elif line[7] == 'c':  # cL comment
        # cL comment - skip
        continue
    
    elif line[7] == 'G' and current_ep is not None:
        # Gamma record - save
        current_gammas.append(line)

# Save last resonance
if current_ep is not None and current_gammas:
    current_resonances[current_ep] = current_gammas

# Save last resonance
if current_ep is not None and current_gammas:
    current_resonances[current_ep] = current_gammas

print(f"Found {len(current_resonances)} existing resonances")

# Generate updated resonances
output_lines = []
debug_matches = []

for ex, ep, dep, gamma_eV, unc_eV in resonance_data:
    # Calculate dEx from dEp (uncertainty in Ex = uncertainty in Ep)
    dex = dep
    
    # Generate L-record
    l_record = generate_L_record(ex, dex, ep, dep)
    output_lines.append(l_record)
    
    # Generate cL comment
    cl_record = generate_cL_record(ep, gamma_eV, unc_eV)
    output_lines.append(cl_record)
    
    # Find matching gamma records from existing data
    # Match by approximate Ep value (within 10 keV tolerance for now)
    gamma_records = []
    best_match_ep = None
    best_match_diff = 999999
    
    for existing_ep, gammas in current_resonances.items():
        if existing_ep is not None:
            diff = abs(existing_ep - ep)
            if diff < best_match_diff:
                best_match_diff = diff
                best_match_ep = existing_ep
                gamma_records = gammas
    
    debug_matches.append((ep, best_match_ep, best_match_diff, len(gamma_records)))
    
    # Add gamma records (preserve original formatting with 80 chars)
    for gamma in gamma_records:
        output_lines.append(gamma)

# Write output
output_file = os.path.join('A35', 'Cl35', 'temp', '1976ME12_UPDATED_RESONANCES.txt')
with open(output_file, 'w') as f:
    for line in output_lines:
        f.write(line if line.endswith('\n') else line + '\n')

print(f"\nGenerated {len(output_lines)} lines")
print(f"Output written to: {output_file}")

# Debug matching
print("\nDebug: Ep matching (first 10):")
for i, (new_ep, matched_ep, diff, num_gammas) in enumerate(debug_matches[:10]):
    print(f"  {i+1}. New Ep={new_ep:.1f} -> Matched Ep={matched_ep} (diff={diff:.1f}), {num_gammas} gammas")

# Verification
print("\nFirst 5 L-records for verification:")
line_count = 0
for line in output_lines[:50]:
    if line[7] == 'L':
        print(f"Length: {len(line.rstrip())} | {repr(line.rstrip())}")
        line_count += 1
        if line_count >= 5:
            break
