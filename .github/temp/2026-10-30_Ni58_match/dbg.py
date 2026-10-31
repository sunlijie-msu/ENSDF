import re
def L(p): return [x.rstrip("\n").ljust(80) for x in open(p, encoding="utf-8", errors="replace")]
B = r"XUNDL/A58/Ni58/new/"
FILES = {"D": "Ni58_58ni_a_aP.ens", "F": "Ni58_58ni_e_eP.ens", "C": "Ni58_58ni_p_pP_pol_p_pP_p_pPg.ens",
         "j": "Ni58_4he_58ni_4heP_58ni_4he.ens", "K": "Ni58_54fe_6li_d.ens"}
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

for k, lo, hi in [("D", 17000, 19000), ("F", 8100, 8300), ("C", 9300, 9400), ("j", 0, 2000), ("K", 7700, 7900)]:
    print(f"--- {k} levels {lo}-{hi} ---")
    for E, s, raw in PK[k]:
        if lo <= E <= hi: print(f"   {E:>9.1f} +-{str(s):<6} {raw[:56]}")
