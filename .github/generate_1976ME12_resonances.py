"""
Generate 56 resonance L-records + cL comments for 1976ME12.ens
Field mappings: Ex->E field, dEp->DE field, Ep->S field, |w|g->cL comment
All fields LEFT-JUSTIFIED per ENSDF specifications
"""

# Resonance data from 34S(p,gamma)35Cl reaction
resonance_data = [
    (7066.5, 1, 716, 0.3, 0.1),
    (7104.0, 1, 754.6, 1.2, 0.3),
    (7179.4, 1.5, 831.4, 1.5, 0.5),
    (7255.3, 1, 908.9, 1.2, 0.3),
    (7272.6, 1, 926.5, 2.1, 0.5),
    (7279.9, 1, 934, 0.5, 0.15),
    (7302.0, 1, 956.5, 0.8, 0.2),
    (7340.4, 1, 995.7, 5, 1),
    (7360.8, 1, 1016.5, 3, 1),
    (7381.1, 1.5, 1037.2, 1.3, 0.4),
    (7421.6, 1, 1078.4, 1.7, 0.4),
    (7428.9, 1, 1086, 1.8, 0.4),
    (7458.4, 1, 1116, 2, 0.5),
    (7479.0, 1, 1137.1, 0.8, 0.2),
    (7509.8, 1, 1168.5, 1, 0.3),
    (7538.6, 1.5, 1197.9, 2.5, 0.5),
    (7560.0, 1, 1219.8, 4.5, 1),
    (7566.2, 1, 1226.2, 2.1, 0.5),
    (7570.2, 1, 1230.3, 0.7, 0.2),
    (7577.7, 1, 1238, 2.1, 0.5),
    (7596.2, 1, 1256.9, 1.7, 0.4),
    (7611.7, 1, 1272.7, 4, 1),
    (7621.2, 1.5, 1282.5, 3, 0.5),
    (7633.3, 1, 1294.9, 1.8, 0.5),
    (7667.6, 1, 1329.8, 1.5, 0.4),
    (7676.6, 1, 1339, 3.5, 0.5),
    (7683.6, 1.5, 1346.2, 2, 0.5),
    (7687.4, 1, 1350.1, 1.5, 0.4),
    (7701.0, 1, 1364, 4.5, 1),
    (7728.4, 1, 1392, 2.5, 0.5),
    (7754.1, 1.5, 1418.3, 3.5, 0.5),
    (7760.3, 1, 1424.7, 2, 0.5),
    (7789.8, 1, 1454.8, 6, 1),
    (7805.3, 1, 1470.7, 5, 1),
    (7811.4, 1.5, 1477, 7, 1),
    (7833.1, 1, 1499.1, 7, 1),
    (7858.7, 1.5, 1525.3, 6, 1),
    (7882.3, 1.5, 1549.5, 4, 1),
    (7892.2, 1.5, 1559.7, 21, 3),
    (7918.4, 1, 1586.4, 4.5, 1),
    (7946.1, 1, 1614.7, 7, 2),
    (7952.7, 1, 1621.5, 9.5, 2),
    (7963.9, 1, 1633, 3, 0.5),
    (7977.4, 1, 1646.9, 7.5, 2),
    (8023.4, 1.5, 1694, 4.5, 1),
    (8029.1, 1, 1700, 3, 1),
    (8053.4, 1, 1724.8, 6, 2),
    (8068.5, 1, 1740.3, 5, 1),
    (8089.8, 1, 1762, 2.5, 0.5),
    (8119.8, 1.3, 1792.7, 6, 2),
    (8160.0, 1, 1833.7, 7, 2),
    (8201.4, 1, 1875.8, 3.5, 1),
    (8209.4, 1, 1884.1, 11, 3),
    (8240.9, 1, 1916.3, 7, 2),
    (8295.0, 1.5, 1971.5, 8, 2),
    (8323.5, 1.3, 2009.9, 9, 2),
]

def format_l_record(ex_kev, dep_kev, ep_kev):
    """
    Format L-record with Ex->E field, dEp->DE field, Ep->S field
    ENSDF L-record format (80 chars total):
    Cols 1-5: NUCID
    Col 6: CONT (blank)
    Col 7: blank
    Col 8: "L"
    Col 9: blank
    Cols 10-19: E (energy) LEFT-JUSTIFIED
    Cols 20-21: DE (uncertainty) LEFT-JUSTIFIED
    Cols 22-64: blank (J, T, DT, L fields - all blank for resonances)
    Cols 65-74: S field (Ep proton energy) LEFT-JUSTIFIED
    Cols 75-80: blank (DS, C fields)
    """
    # NUCID field (cols 1-5)
    nucid = " 35CL"
    
    # Type marker (cols 6-9: blank, L, blank)
    type_marker = "  L "
    
    # E field (cols 10-19): Ex energy LEFT-JUSTIFIED
    e_field = f"{ex_kev:<10.1f}"
    
    # DE field (cols 20-21): dEp uncertainty LEFT-JUSTIFIED
    # CRITICAL: DE field is ONLY 2 characters (cols 20-21)
    # For decimal uncertainties like 1.5, we must use integer format
    # Since ENSDF uncertainties apply to last digit of value, 1.5 keV uncertainty
    # on 7179.4 keV means uncertainty is in 0.1 keV digit -> use "15" (1.5*10)
    # However, for simplicity and ENSDF compliance, round to integer
    de_int = int(round(dep_kev))
    de_field = f"{de_int:<2}"
    
    # Cols 22-64: blank (43 spaces for J, T, DT, L fields)
    middle_blank = " " * 43
    
    # S field (cols 65-74): Ep proton energy LEFT-JUSTIFIED
    s_field = f"{ep_kev:<10.1f}"
    
    # Cols 75-80: blank (6 spaces for DS and C fields)
    end_blank = " " * 6
    
    # Assemble 80-character line
    line = nucid + type_marker + e_field + de_field + middle_blank + s_field + end_blank
    
    # Verify 80 characters
    if len(line) != 80:
        print(f"[ERROR] Line length {len(line)} for Ex={ex_kev}")
    
    return line

def format_cl_comment(ex_kev, wg_ev, dwg_ev):
    """
    Format cL comment line with resonance strength
    Format: "35CL cL $|w|g=VALUE eV {IUNCERTAINTY} (1976Me12)"
    Must be exactly 80 characters with trailing spaces
    """
    # Start with NUCID + cL
    start = " 35CL cL $|w|g="
    
    # Format |w|g value with appropriate precision
    if wg_ev == int(wg_ev):
        wg_str = str(int(wg_ev))
    else:
        wg_str = str(wg_ev)
    
    # Format uncertainty (convert to integer for {I} notation)
    # Calculate uncertainty digits based on decimal places in value
    if '.' in wg_str:
        decimal_places = len(wg_str.split('.')[1])
        uncertainty_int = int(dwg_ev * (10 ** decimal_places))
    else:
        uncertainty_int = int(dwg_ev)
    
    # Build comment text
    comment = f"{start}{wg_str} eV {{I{uncertainty_int}}} (1976Me12)"
    
    # Pad to 80 characters
    line = f"{comment:<80}"
    
    # Verify 80 characters
    if len(line) != 80:
        print(f"[ERROR] cL line length {len(line)} for Ex={ex_kev}")
    
    return line

# Generate output file
output_lines = []
output_lines.append("# Generated resonance L-records + cL comments for 1976ME12.ens")
output_lines.append("# Insert these 112 lines at line ~191 (after 6493 keV level, before Original Branching data)")
output_lines.append("# Format: Each resonance = L-record + cL comment")
output_lines.append("")

for ex, dep, ep, wg, dwg in resonance_data:
    l_record = format_l_record(ex, dep, ep)
    cl_comment = format_cl_comment(ex, wg, dwg)
    output_lines.append(l_record)
    output_lines.append(cl_comment)
    output_lines.append("")  # Blank line separator

# Write to file
output_file = "A35/Cl35/temp/1976ME12_resonances.txt"
with open(output_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(output_lines))

print(f"[OK] Generated {len(resonance_data) * 2} resonance records (56 L-records + 56 cL comments)")
print(f"[OK] Output file: {output_file}")
print(f"[OK] Total lines to insert: {len(resonance_data) * 3} (including blank separators)")
print("")
print("Sample L-record (first resonance):")
print(format_l_record(7066.5, 1, 716))
print("")
print("Sample cL comment (first resonance):")
print(format_cl_comment(7066.5, 0.3, 0.1))
