"""Build and verify new L/G/cG records for the 34Clm decay file.

Adds (based on 1980WI13.csv):
  L 4075 (1+), G 4074 ->gs  <0.00081 LT  M=D
  L 4890 (2+), G 1586 ->3303 <0.018 LT, G 2762 ->2127 <0.011 LT, G 4889 ->gs <0.0015 LT M=E2
  G 1384 (4688->3303) <0.021 LT   [under existing L 4689]
  G 4877 (4876->gs)   <0.00076 LT  [under existing L 4877]
E rounding: round-half-up of adopted gamma energies.
cG RI$other comments only where CSV has 1975VA02 values.
"""
import decimal

def rnd(s):
    return str(int(decimal.Decimal(s).to_integral_value(rounding=decimal.ROUND_HALF_UP)))

def l_rec(E, J):
    line = " 34S   L " + E.ljust(10) + "   " + J.ljust(17) + " " * 41
    return line

def g_rec(E, RI, DRI, M):
    line = " 34S   G " + E.ljust(10) + "   " + RI.ljust(7) + DRI + " " + M.ljust(9) + " " * 39
    return line

def cg(text):
    line = (" 34S  cG RI$other: " + text + ".").ljust(80)
    return line

records = []
# Level 4075
records.append(("L4075", l_rec("4075", "1+")))
records.append(("G4074", g_rec("4074", "0.00081", "LT", "D")))
records.append(("cG4074", cg("<0.0023 (1975Va02)")))
# G 1384 under L 4689
records.append(("G1384", g_rec("1384", "0.021", "LT", "")))
# G 4877 under L 4877
records.append(("G4877", g_rec("4877", "0.00076", "LT", "")))
records.append(("cG4877", cg("<0.0010 (1975Va02)")))
# Level 4890
records.append(("L4890", l_rec("4890", "2+")))
records.append(("G1586", g_rec("1586", "0.018", "LT", "")))
records.append(("cG1586", cg("<0.015 (1975Va02)")))
records.append(("G2762", g_rec("2762", "0.011", "LT", "")))
records.append(("G4889", g_rec("4889", "0.0015", "LT", "E2")))
records.append(("cG4889", cg("<0.0010 (1975Va02)")))

for name, line in records:
    status = "OK" if len(line) == 80 else f"LEN={len(line)}"
    print(f"{name}: {status}")
    print(f"  [{line}]")
