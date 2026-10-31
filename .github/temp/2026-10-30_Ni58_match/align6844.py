import math
def L(p): return [l.rstrip("\n").ljust(80) for l in open(p, encoding="utf-8", errors="replace")]
DIR = r"XUNDL/A58/Ni58/new/"
C  = L(DIR + "Ni58_58ni_p_pP_pol_p_pP_p_pPg.ens")
AD = L(DIR + "Ni58_adopted.ens")

def val(l):
    e = l[9:19].strip()
    d = l[19:21].strip()
    if not e: return None, None
    try: E = float(e)
    except: return None, None
    dec = len(e.split(".")[1]) if "." in e else 0
    s = (int(d) * 10.0**-dec) if d.isdigit() else 0.0
    return E, s

def jf(l):
    # J may be written starting col 22 (shifted) - take both slices
    a = l[22:39].strip()
    return a

ds, ad = [], []
for i, l in enumerate(C, 1):
    if l[5] == " " and l[6] == " " and l[7] == "L":
        E, s = val(l)
        if E is not None and 6780 <= E <= 6900:
            ds.append((i, E, s, jf(l), l[55:64].strip(), l[64:74].strip(), l.rstrip()))
for i, l in enumerate(AD, 1):
    if l[5] == " " and l[6] == " " and l[7] == "L":
        E, s = val(l)
        if E is not None and 6780 <= E <= 6900:
            xs = ""
            for n in range(i + 1, min(i + 6, len(AD) + 1)):
                if "XREF" in AD[n-1]: xs += AD[n-1][9:80].strip()
                if AD[n-1][7] == "G" and AD[n-1][5] == " ": break
            ad.append((i, E, s, jf(l), xs, l.rstrip()))

print("DATASET C levels 6780-6900:", len(ds))
for i, E, s, J, Lf, S, raw in ds:
    print(f"  :{i:<5} {E:>8.1f} +-{s:<5} J={J:<10} L={Lf:<4} S={S:<7} | {raw[:60]}")
print("\nADOPTED levels 6780-6900:", len(ad))
for i, E, s, J, xs, raw in ad:
    print(f"  :{i:<5} {E:>8.1f} +-{s:<5} J={J:<10} XREF={xs:<40} | {raw[:50]}")

print("\n--- for each dataset C level: nearest adopted levels ---")
for i, E, s, J, Lf, S, raw in ds:
    cands = sorted(ad, key=lambda a: abs(a[1] - E))[:3]
    print(f"  C :{i} {E}+-{s} J={J}")
    for ai, aE, as_, aJ, xs, araw in cands:
        d = abs(aE - E)
        tol = max(3.0, 3 * math.sqrt(s**2 + as_**2))
        print(f"      -> ad :{ai} {aE}+-{as_} J={aJ:<9} dE={d:5.1f} tol={tol:5.1f} "
              f"{'IN' if d <= tol else 'out'}")

print("\n--- for each adopted level: nearest dataset C peaks ---")
for ai, aE, as_, aJ, xs, araw in ad:
    cands = sorted(ds, key=lambda a: abs(a[1] - aE))[:3]
    print(f"  ad :{ai} {aE}+-{as_} J={aJ}  XREF={xs}")
    for i, E, s, J, Lf, S, raw in cands:
        d = abs(aE - E)
        tol = max(3.0, 3 * math.sqrt(s**2 + as_**2))
        print(f"      <- C :{i} {E}+-{s} J={J:<9} dE={d:5.1f} tol={tol:5.1f} "
              f"{'IN' if d <= tol else 'out'}")
