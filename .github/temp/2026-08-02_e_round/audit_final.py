"""Final field-slice audit of S34 34Cl EC decay file L/G records.

Expected after edit:
  - E (10-19): integer (rounded half-up), left-justified
  - DE (20-21): blank (2 spaces)
  - J (L, 23-39) / RI..DMR (G, 23-55): unchanged
Prints each record slice for human verification.
"""
PATH = r"A34\S34\new\S34_34cl_ec_decay_31.99_m.ens"

with open(PATH, encoding="utf-8") as f:
    lines = f.read().splitlines()

print("=== FINAL L/G FIELD SLICE AUDIT ===")
for i, line in enumerate(lines, 1):
    if len(line) < 80 or line[6] != " " or line[7] not in ("L", "G"):
        continue
    e = line[9:19]
    de = line[19:21]
    if line[7] == "L":
        j = line[22:39]
        print(f"L{i} len={len(line)} E='{e.strip()}' DE='{de.strip() or 'blank'}' J='{j.strip()}'")
    else:
        ri = line[22:29]
        dri = line[29:31]
        m = line[32:41]
        mr = line[41:49]
        dmr = line[49:55]
        cc = line[55:62]
        ti = line[64:74]
        print(
            f"L{i} len={len(line)} E='{e.strip()}' DE='{de.strip() or 'blank'}' "
            f"RI='{ri.strip()}' DRI='{dri.strip() or 'blank'}' M='{m.strip()}' "
            f"MR='{mr.strip() or 'blank'}' DMR='{dmr.strip() or 'blank'}' "
            f"CC='{cc.strip() or 'blank'}' TI='{ti.strip() or 'blank'}'"
        )
