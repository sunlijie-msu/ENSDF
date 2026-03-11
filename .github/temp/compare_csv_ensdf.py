import csv

csv_path = "d:/X/ND/ENSDF/A34/Cl34/raw/1977DA02_Bound.csv"
with open(csv_path, 'r', encoding='utf-8-sig') as f:
    rows = list(csv.reader(f))

header_ei = [x.strip() for x in rows[1]]
target_levels = ["2610.6", "2721.4", "3128.9", "3333.9"]

print("="*80)
print("REVISED G-RECORD DATA FROM CSV")
print("="*80)

for level in target_levels:
    for i, row in enumerate(rows[2:], start=2):
        if not row or not row[0].strip():
            continue
        ei = row[0].strip()
        if ei == level:
            print(f"\nLEVEL Ei = {ei} keV")
            gammas = []
            for col_idx, (header_ef, value) in enumerate(zip(header_ei, row)):
                if value and value.strip() and col_idx > 0 and col_idx < len(header_ei) - 2:
                    eff = header_ef.strip()
                    val = value.strip()
                    if eff and eff not in ("Other Ef keV", "Ig"):
                        try:
                            egamma = round(float(ei) - float(eff), 1)
                            parts = val.split("+/-")
                            ri = parts[0].strip()
                            unc = parts[1].strip() if len(parts) > 1 else ""
                            gammas.append((egamma, ri, unc))
                        except:
                            pass
            gammas.sort()
            for egamma, ri, unc in gammas:
                ristr = f"{ri}+/-{unc}" if unc else ri
                print(f"  G {egamma:>7} RI = {ristr}")
            break

print("\n" + "="*80)
