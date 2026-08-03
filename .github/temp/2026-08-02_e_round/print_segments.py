"""Print exact patch segments (cols 1-21) for each L/G record.

old_seg = original cols 1-21 (E+DE region)
new_seg = new E (rounded, left-justified 10) + 2 spaces for DE
For line 40 (DE already blank) use anchored segment through J-start '0+'.
Segments bracketed with | for exact whitespace visibility.
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
    new_seg = line[:9] + e_int.ljust(10) + "  "
    if line[19:21].strip():  # DE has content -> cols 1-21 is safe (ends in digit)
        old_seg = line[:21]
        print(f"L{i}")
        print(f"  OLDSEG |{old_seg}|")
        print(f"  NEWSEG |{new_seg}|")
    else:  # DE blank (line 40) -> use anchored segment through J start
        anchor = line[22:24]  # e.g. '0+'
        old_seg = line[:22] + anchor
        new_seg = new_seg + " " + anchor
        print(f"L{i} (blank DE, anchored)")
        print(f"  OLDSEG |{old_seg}|")
        print(f"  NEWSEG |{new_seg}|")
    # sanity: applying new_seg to line must give 80 chars
    if line[19:21].strip():
        rebuilt = new_seg + line[21:]
    else:
        rebuilt = new_seg + line[23:]
    print(f"  REBUILT len={len(rebuilt)} : [{rebuilt}]")
    print()
