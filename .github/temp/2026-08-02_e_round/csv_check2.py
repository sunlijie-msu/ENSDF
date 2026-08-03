"""CSV <-> ENS completeness check matching within rounding tolerance (±1 keV)."""
import csv

ENS = r"A34\S34\new\S34_34cl_ec_decay_31.99_m.ens"
CSV = r"A34\S34\raw\1980WI13.csv"

with open(ENS, encoding="utf-8") as f:
    lines = f.read().splitlines()

ens_E = []
for ln in lines:
    if len(ln) >= 80 and ln[6] == " " and ln[7] == "G":
        ens_E.append(int(ln[9:19].strip()))

with open(CSV, encoding="utf-8-sig", newline="") as f:
    rows = list(csv.reader(f))

missing = []
checked = 0
for r in rows[1:]:
    if not r or not r[0].strip():
        continue
    eg = r[0].strip()
    if eg == "146":
        continue
    checked += 1
    e = int(float(eg))
    if not any(abs(e - x) <= 1 for x in ens_E):
        missing.append(eg)

print(f"CSV gammas checked (excl 146): {checked}")
print(f"ENS G records: {len(ens_E)}")
print("Missing within ±1 keV:", missing if missing else "NONE - all CSV gammas present")
print("ENS G energies:", sorted(ens_E))
