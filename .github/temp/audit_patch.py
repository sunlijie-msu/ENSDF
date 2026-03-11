import csv

# Read current ENSDF file
ensdf_lines = open('A34/Cl34/raw/1977DA02.ens', 'r').readlines()

# Read CSV
csv_path = "d:/X/ND/ENSDF/A34/Cl34/raw/1977DA02_Bound.csv"
with open(csv_path, 'r', encoding='utf-8-sig') as f:
    csv_rows = list(csv.reader(f))

header_ei = [x.strip() for x in csv_rows[1]]
target_levels = ["2610.6", "2721.4", "3128.9", "3333.9"]

print("="*80)
print("SPOT-CHECK AUDIT: ENSDF vs. CSV")
print("="*80)

issues = 0

for level in target_levels:
    # Get ENSDF G-records
    ensdf_gammas = []
    for i, line in enumerate(ensdf_lines):
        if f'L {level}' in line:
            j = i + 1
            while j < len(ensdf_lines):
                if ' 34CL  G ' in ensdf_lines[j]:
                    lstr = ensdf_lines[j].rstrip()
                    # Extract E (columns 10-19), RI (23-29), DRI (30-31)
                    try:
                        e_str = lstr[9:19].strip()
                        ri_str = lstr[22:29].strip()
                        dri_str = lstr[29:31].strip()
                        e = float(e_str)
                        ri = float(ri_str)
                        ensdf_gammas.append((e, ri, dri_str))
                    except:
                        pass
                    j += 1
                elif ' 34CL  L ' in ensdf_lines[j]:
                    break
                else:
                    j += 1
            break
    
    # Get CSV G-records
    csv_gammas = []
    for row in csv_rows[2:]:
        if not row or not row[0].strip():
            continue
        ei = row[0].strip()
        if ei == level:
            for col_idx, (header_ef, value) in enumerate(zip(header_ei, row)):
                if value and value.strip() and col_idx > 0 and col_idx < len(header_ei) - 2:
                    eff = header_ef.strip()
                    val = value.strip()
                    if eff and eff not in ("Other Ef keV", "Ig"):
                        try:
                            egamma = round(float(level) - float(eff), 1)
                            ri = float(val.split("+/-")[0].strip())
                            csv_gammas.append(egamma)
                        except:
                            pass
            csv_gammas.sort()
            break
    
    print(f"\nLevel {level}:")
    print(f"  ENSDF gamma count: {len(ensdf_gammas)}")
    print(f"  CSV gamma count: {len(csv_gammas)}")
    
    if len(ensdf_gammas) != len(csv_gammas):
        print(f"  ❌ MISMATCH: Count differs")
        issues += 1
    
    ensdf_e_list = [e for e, ri, dri in ensdf_gammas]
    if ensdf_e_list != csv_gammas:
        print(f"  ❌ MISMATCH: Energies differ")
        print(f"    ENSDF: {ensdf_e_list}")
        print(f"    CSV: {csv_gammas}")
        issues += 1
    else:
        print(f"  ✓ Energies match: {csv_gammas}")

print("\n" + "="*80)
if issues == 0:
    print("✓ ALL SPOT CHECKS PASSED")
else:
    print(f"❌ {issues} ISSUE(S) FOUND")
print("="*80)
