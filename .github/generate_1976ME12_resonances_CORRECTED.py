"""
Generate ENSDF-formatted resonance L-records and cL comments for 1976ME12.ens - CORRECTED VERSION

CRITICAL FIELD MAPPINGS (per user correction):
- Ex_keV → E field (columns 10-19): Excitation energy, NO uncertainty in DE field (blank)
- Ep_keV → S field (columns 65-74): Proton lab energy (spectroscopic strength field)
- dEp_keV → DS field (columns 75-76): Uncertainty in Ep (max 2 digits, LEFT-JUSTIFIED)
- |w|g_eV and d|w|g_eV → cL comment line with proper {I} notation

ENSDF L-Record Structure (80 characters exact):
Columns 1-5: NUCID (" 35CL")
Column 6: CONT (blank)
Column 7: blank
Column 8: "L"
Column 9: blank
Columns 10-19: E field (Ex energy, LEFT-JUSTIFIED)
Columns 20-21: DE field (BLANK - no uncertainty for exact Ex values)
Column 22: space separator
Columns 23-39: J-π field (blank for resonances)
Columns 40-49: T field (half-life, blank for resonances)
Columns 50-55: DT field (blank for resonances)
Columns 56-64: L field (angular momentum, blank for resonances)
Columns 65-74: S field (Ep proton lab energy, LEFT-JUSTIFIED)
Columns 75-76: DS field (dEp uncertainty, LEFT-JUSTIFIED, max 2 digits)
Column 77: C field (comment flag, blank)
Columns 78-79: blank
Column 80: Q field (blank)
"""

def format_l_record(ex_kev, ep_kev, dep_kev):
    """
    Format L-record with CORRECTED field mapping.
    
    Args:
        ex_kev: Excitation energy (exact value, no uncertainty)
        ep_kev: Proton lab energy (goes in S field)
        dep_kev: Proton energy uncertainty (goes in DS field, max 2 digits)
    
    Returns:
        80-character ENSDF L-record string
    """
    # NUCID + type marker (9 chars): " 35CL  L "
    nucid = " 35CL"
    type_marker = "  L "
    
    # E field (10 chars): Ex energy with 1 decimal, LEFT-JUSTIFIED
    # DE field (2 chars): BLANK (no uncertainty for exact Ex)
    e_field = f"{ex_kev:<10.1f}"
    de_field = "  "  # BLANK - Ex values are exact
    
    # Middle section (43 chars): space + J-π(17) + T(10) + DT(6) + L(9) = 43
    # All blank for resonances
    middle_blank = " " * 43  # 1 space + 17 + 10 + 6 + 9 = 43
    
    # S field (10 chars): Ep proton lab energy with 1 decimal, LEFT-JUSTIFIED
    s_field = f"{ep_kev:<10.1f}"
    
    # DS field (2 chars): dEp uncertainty, max 2 digits, LEFT-JUSTIFIED
    # Round dEp to 1 decimal place, then scale by 10 to get integer uncertainty
    ds_int = int(round(dep_kev * 10))  # e.g., 1.0 → 10, 0.7 → 7
    ds_field = f"{ds_int:<2}"
    
    # End section (4 chars): C(1) + blank(2) + Q(1) = 4
    end_blank = " " * 4
    
    # Assemble complete L-record
    l_record = nucid + type_marker + e_field + de_field + middle_blank + s_field + ds_field + end_blank
    
    return l_record

def format_cl_comment(ex_kev, wg_ev, dwg_ev):
    """
    Format cL comment line with resonance strength.
    
    Args:
        ex_kev: Excitation energy (for identification)
        wg_ev: Resonance strength ωγ in eV
        dwg_ev: Uncertainty in ωγ in eV
    
    Returns:
        80-character ENSDF cL comment string
    """
    # Convert wg_ev and dwg_ev to strings, preserving exact decimal places
    wg_str = str(wg_ev) if '.' in str(wg_ev) else f"{int(wg_ev)}"
    
    # Calculate uncertainty integer for {I} notation
    # Count decimal places in wg_ev to determine scaling
    if '.' in str(wg_ev):
        decimal_places = len(str(wg_ev).split('.')[1])
        uncertainty_int = int(dwg_ev * (10 ** decimal_places))
    else:
        uncertainty_int = int(dwg_ev)
    
    # Format cL comment
    cl_base = f" 35CL cL $|w|g={wg_str} eV {{I{uncertainty_int}}} (1976Me12)"
    
    # Pad to exactly 80 characters
    cl_comment = cl_base.ljust(80)
    
    return cl_comment

# Resonance data: (Ex_keV, Ep_keV, dEp_keV, |w|g_eV, d|w|g_eV)
resonance_data = [
    (7066.5, 716.0, 1.0, 0.3, 0.1),
    (7104.0, 754.6, 1.0, 0.5, 0.2),
    (7179.4, 832.2, 1.5, 0.3, 0.1),
    (7194.9, 848.1, 1.0, 1.2, 0.4),
    (7225.2, 879.3, 1.0, 0.3, 0.1),
    (7234.1, 888.5, 1.0, 1.9, 0.6),
    (7273.5, 929.0, 1.0, 2.2, 0.7),
    (7362.8, 1021.0, 1.0, 3.1, 0.9),
    (7397.7, 1056.9, 1.6, 0.5, 0.2),
    (7451.4, 1112.2, 0.6, 0.4, 0.1),
    (7503.1, 1165.4, 0.7, 0.8, 0.2),
    (7518.6, 1181.4, 0.7, 0.4, 0.1),
    (7548.8, 1212.4, 0.7, 21, 3),
    (7561.3, 1225.3, 0.7, 1.5, 0.5),
    (7600.5, 1265.7, 0.8, 2.8, 0.8),
    (7618.8, 1284.5, 0.5, 1.7, 0.5),
    (7657.4, 1324.2, 0.8, 0.8, 0.2),
    (7672.4, 1339.7, 0.8, 1.3, 0.4),
    (7686.1, 1353.8, 0.8, 2.8, 0.8),
    (7694.4, 1362.3, 0.8, 0.6, 0.2),
    (7706.8, 1375.1, 0.8, 4.4, 1.3),
    (7745.3, 1414.7, 0.9, 1.7, 0.5),
    (7777.1, 1447.5, 0.9, 1.5, 0.5),
    (7781.8, 1452.3, 1.3, 0.9, 0.3),
    (7797.3, 1468.2, 0.9, 1.4, 0.4),
    (7838.1, 1510.2, 1.0, 4.8, 1.4),
    (7839.4, 1511.6, 0.9, 6.1, 1.8),
    (7869.1, 1542.2, 1.0, 1.0, 0.3),
    (7881.3, 1554.7, 0.9, 2.2, 0.7),
    (7899.7, 1573.7, 0.7, 2.2, 0.7),
    (7923.7, 1598.4, 0.9, 1.0, 0.3),
    (7971.0, 1647.1, 1.0, 1.9, 0.6),
    (7989.5, 1666.1, 1.0, 1.2, 0.4),
    (7995.9, 1672.7, 1.0, 2.1, 0.6),
    (8001.2, 1678.1, 0.9, 2.9, 0.9),
    (8005.4, 1682.5, 1.0, 4.8, 1.4),
    (8036.9, 1714.9, 1.0, 0.8, 0.2),
    (8039.2, 1717.3, 1.1, 2.9, 0.9),
    (8076.5, 1755.7, 1.1, 1.6, 0.5),
    (8096.3, 1776.0, 1.1, 2.4, 0.7),
    (8106.8, 1786.9, 1.1, 3.7, 1.1),
    (8113.9, 1794.2, 1.1, 1.6, 0.5),
    (8148.2, 1829.5, 1.1, 1.7, 0.5),
    (8157.6, 1839.1, 1.1, 1.9, 0.6),
    (8179.9, 1862.1, 1.2, 0.9, 0.3),
    (8208.3, 1891.3, 1.2, 9.0, 2.7),
    (8216.3, 1899.6, 1.1, 7.1, 2.1),
    (8242.5, 1926.5, 1.2, 2.2, 0.7),
    (8269.5, 1954.3, 1.2, 2.0, 0.6),
    (8277.7, 1962.8, 1.2, 1.5, 0.5),
    (8282.6, 1967.8, 1.2, 1.3, 0.4),
    (8288.4, 1973.8, 1.2, 1.6, 0.5),
    (8298.8, 1984.5, 1.2, 3.5, 1.1),
    (8319.7, 2006.0, 1.3, 4.2, 1.3),
    (8323.5, 2009.9, 1.3, 1.6, 0.5),
]

# Generate output file
output_file = "A35/Cl35/temp/1976ME12_resonances_CORRECTED.txt"

with open(output_file, 'w', encoding='utf-8') as f:
    # Write header comments
    f.write("# CORRECTED ENSDF Resonance Records for 1976ME12.ens\n")
    f.write("# Field mappings:\n")
    f.write("#   E field (10-19): Ex excitation energy (exact, no DE uncertainty)\n")
    f.write("#   S field (65-74): Ep proton lab energy\n")
    f.write("#   DS field (75-76): dEp uncertainty (max 2 digits)\n")
    f.write("#   cL comment: |w|g resonance strength\n")
    f.write("\n")
    
    # Generate L-records and cL comments
    for ex, ep, dep, wg, dwg in resonance_data:
        l_record = format_l_record(ex, ep, dep)
        cl_comment = format_cl_comment(ex, wg, dwg)
        
        # Write L-record, cL comment, and blank separator
        f.write(l_record + "\n")
        f.write(cl_comment + "\n")
        f.write("\n")  # Blank separator

print(f"[OK] Generated {len(resonance_data)} resonance L-records and cL comments")
print(f"[OK] Output file: {output_file}")
print(f"[OK] Total ENSDF lines: {len(resonance_data) * 3} (L + cL + blank)")
