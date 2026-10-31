import re
def L(p): return [x.rstrip("\n").ljust(80) for x in open(p, encoding="utf-8", errors="replace")]
B = r"XUNDL/A58/Ni58/new/"
FILES = {"C": "Ni58_58ni_p_pP_pol_p_pP_p_pPg.ens", "D": "Ni58_58ni_a_aP.ens",
         "H": "Ni58_58ni_3he_3heP.ens", "I": "Ni58_58ni_d_dP.ens", "K": "Ni58_54fe_6li_d.ens",
         "M": "Ni58_54fe_12c_8be.ens", "X": "Ni58_58ni_6li_6liP.ens",
         "j": "Ni58_4he_58ni_4heP_58ni_4he.ens"}
def parse_E(rec):
    e = rec[9:19].strip(); d = rec[19:21].strip()
    m = re.match(r"^([0-9.]+)(?:E([+-]?\d+))?$", e.replace(" ", ""))
    if not m: return None, None
    mant, exp = m.group(1), int(m.group(2)) if m.group(2) else 0
    E = float(mant)*10.0**exp
    dec = exp - (len(mant.split(".")[1]) if "." in mant else 0)
    return E, (int(d)*10.0**dec if d.isdigit() else None)
PK = {}
for k, v in FILES.items():
    rows = []
    for l in L(B+v):
        if l[5] == " " and l[6] == " " and l[7] == "L":
            E, s = parse_E(l)
            if E is not None: rows.append((E, s if s is not None else 0.0, l.rstrip()))
    PK[k] = sorted(rows)

CASES = [("j", 0.0), ("K", 7820.0), ("M", 4574.3), ("H", 6805.5), ("K", 7514.5), ("I", 4474.6),
         ("I", 3593.7), ("H", 5590.3), ("H", 3620.1), ("K", 6460.0), ("K", 7210.4), ("I", 4448.91),
         ("H", 6763.5), ("K", 6425.3), ("H", 7514.5), ("X", 3273.8), ("D", 5394.3), ("M", 7710.3),
         ("C", 9336.0)]
for lab, E in CASES:
    near = min(PK[lab], key=lambda p: abs(p[0]-E))
    print(f"{lab} adopted {E:>9}: dataset level {near[0]:>9.1f} +-{str(near[1]):<6} | {near[2][:62]}")
