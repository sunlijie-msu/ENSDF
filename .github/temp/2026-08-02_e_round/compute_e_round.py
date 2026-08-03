"""Compute exact 80-char L/G replacement lines for S34 34Cl EC decay.

Transformation per L/G record:
  - E (cols 10-19) rounded half-up to integer, left-justified in 10 chars
  - DE (cols 20-21) replaced with 2 spaces
  - col 22 and all following columns (23-80) unchanged
Prints OLD/NEW with lengths for verification. Read-only.
"""
import decimal

PATH = r"A34\S34\new\S34_34cl_ec_decay_31.99_m.ens"

with open(PATH, encoding="utf-8") as f:
    lines = f.read().splitlines()

for i, line in enumerate(lines, 1):
    if len(line) < 22 or line[6] != " " or line[7] not in ("L", "G"):
        continue
    e_raw = line[9:19].strip()
    if not e_raw:
        continue
    e_int = str(
        int(
            decimal.Decimal(e_raw).to_integral_value(
                rounding=decimal.ROUND_HALF_UP
            )
        )
    )
    new = line[:9] + e_int.ljust(10) + "  " + line[21:]
    flag = "" if len(new) == 80 else "  <<< LENGTH ERROR"
    print(f"OLD {i} len={len(line)}: [{line}]")
    print(f"NEW {i} len={len(new)}: [{new}]{flag}")
    print()
