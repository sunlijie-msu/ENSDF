"""Final audit: all G records vs CSV gammas + field slices of new records."""
import csv

ENS = r"A34\S34\new\S34_34cl_ec_decay_31.99_m.ens"
CSV = r"A34\S34\raw\1980WI13.csv"

with open(ENS, encoding="utf-8") as f:
    lines = f.read().splitlines()

# G records in ENS (E, RI, DRI, M)
ens_g = []
cur_level = None
for i, ln in enumerate(lines, 1):
    if len(ln) >= 80 and ln[6] == " " and ln[7] == "L":
        cur_level = ln[9:19].strip()
    elif len(ln) >= 80 and ln[6] == " " and ln[7] == "G":
        ens_g.append({
            "line": i, "level": cur_level, "E": ln[9:19].strip(),
            "RI": ln[22:29].strip(), "DRI": ln[29:31].strip(),
            "M": ln[32:41].strip(), "len": len(ln),
        })

print("=== ALL G RECORDS IN ENS ===")
for g in ens_g:
    print(f"L{g['line']} level={g['level']:>5} E={g['E']:>5} RI={g['RI']:>7} DRI={g['DRI']:>2} M={g['M']:>6} len={g['len']}")

# CSV gammas (skip 146 -> 34Cl internal)
with open(CSV, encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    csv_g = []
    for row in reader:
        eg = row["Eγ (keV)"].strip()
        if eg == "146":
            continue
        csv_g.append((eg, row["Iγ (1980WI13)"].strip(), row["Iγ (1975VA02)"].strip()))

print()
print("=== CSV GAMMAS (excluding 146) vs ENS G ===")
ens_E = {g["E"] for g in ens_g}
for eg, i80, i75 in csv_g:
    # match by rounded integer (ENS uses rounded adopted energies)
    match = eg in ens_E
    print(f"Eγ={eg:>5} Iγ80={i80:>10} Iγ75={i75:>8} -> ENS record: {'YES' if match else 'MISSING'}")
