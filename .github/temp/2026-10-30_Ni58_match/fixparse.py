import re
def L(p): return [x.rstrip("\n").ljust(80) for x in open(p, encoding="utf-8", errors="replace")]
B = r"XUNDL/A58/Ni58/new/"

def parse_E(rec):
    e = rec[9:19].strip(); d = rec[19:21].strip()
    m = re.match(r"^([0-9.]+)(?:E([+-]?\d+))?$", e.replace(" ", ""))
    if not m: return None, None
    mant = m.group(1); exp = int(m.group(2)) if m.group(2) else 0
    E = float(mant) * 10.0**exp
    dec = (len(mant.split(".")[1]) if "." in mant else 0) - exp
    return E, (int(d) * 10.0**dec if d.isdigit() else None)

for name in ["Ni58_54fe_16o_12c.ens", "Ni58_58ni_a_aP.ens", "Ni58_58ni_e_eP.ens"]:
    src = L(B + name)
    rows = []
    for l in src:
        if l[5] == " " and l[6] == " " and l[7] == "L":
            E, s = parse_E(l)
            if E is not None: rows.append((E, s, l.rstrip()[:40]))
    rows.sort()
    print("---", name, "n=", len(rows))
    if "16o_12c" in name:
        print("   near 7210:", [(round(e, 1), r) for e, s, r in rows if 6900 <= e <= 7700])
    if "a_aP" in name:
        print("   top 6:", [(round(e, 1), s) for e, s, r in rows][-6:])
    if "e_eP" in name:
        print("   near 8203:", [(round(e, 1), s) for e, s, r in rows if 8100 <= e <= 8300])
