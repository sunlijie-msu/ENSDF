"""CSV <-> ENS completeness cross-check (robust header handling)."""
import csv

ENS = r"A34\S34\new\S34_34cl_ec_decay_31.99_m.ens"
CSV = r"A34\S34\raw\1980WI13.csv"

with open(ENS, encoding="utf-8") as f:
    lines = f.read().splitlines()

ens_g = []
for ln in lines:
    if len(ln) >= 80 and ln[6] == " " and ln[7] == "G":
        ens_g.append(ln[9:19].strip())

with open(CSV, encoding="utf-8-sig", newline="") as f:
    rows = list(csv.reader(f))

header = rows[0]
print("header:", [repr(h) for h in header])

# find column indices by matching content
def col(name_key):
    for idx, h in enumerate(header):
        if name_key in h.replace("\ufeff", ""):
            return idx
    return None

i_eg = col("E")
i_i80 = col("1980WI13")
i_i75 = col("1975VA02")
print("cols:", i_eg, i_i80, i_i75)

missing = []
for r in rows[1:]:
    if len(r) < 2 or not r[i_eg].strip():
        continue
    eg = r[i_eg].strip()
    if eg == "146":
        continue
    if eg not in ens_g:
        missing.append((eg, r[i_i80].strip(), r[i_i75].strip() if i_i75 is not None else ""))

print()
print("CSV gammas not found in ENS G records:", missing if missing else "NONE - all present")
print("Total CSV gammas (excl 146):", len([r for r in rows[1:] if r and r[0].strip() and r[0].strip() != '146']))
print("Total ENS G records:", len(ens_g))
