import re
D = r"d:/X/ND/ENSDF/XUNDL/A58/Co58/new/"
def lines(p): return [l.ljust(80) for l in open(p, encoding="utf-8", errors="replace").read().split("\n")]

def parseE(l):
    raw = l[9:19].strip(); de = l[19:21].strip()
    if not raw: return None, None, None
    try: v = float(raw)
    except: return None, None, None
    if not de: return v, None, raw
    if de in ("GT", "LT", "LE", "GE"): return v, None, raw
    try: d = float(de)
    except: return v, None, raw
    ndec = len(raw.split(".")[1]) if "." in raw else 0
    return v, d * 10 ** (-ndec), raw

print(f"{'file:line':<46}{'Efield':>9}{'DE':>5}{'value ± unc (keV)':>24}")
ITEMS = [("Co58_adopted.ens", 595), ("Co58_adopted.ens", 598), ("Co58_adopted.ens", 838),
         ("Co58_adopted.ens", 1080), ("Co58_adopted.ens", 1027), ("Co58_adopted.ens", 854),
         ("Co58_adopted.ens", 728), ("Co58_adopted.ens", 1173),
         ("Co58_56fe_a_d.ens", 31), ("Co58_56fe_a_d.ens", 35), ("Co58_56fe_a_d.ens", 47),
         ("Co58_56fe_3he_p.ens", 63), ("Co58_58fe_p_n_p_ng.ens", 94),
         ("Co58_58fe_p_n_p_ng.ens", 101), ("Co58_58ni_d_2he.ens", 46),
         ("Co58_60ni_d_a_pol_d_a.ens", 76), ("Co58_59co_3he_a.ens", 34)]
for f, n in ITEMS:
    l = lines(D + f)[n - 1]
    v, u, raw = parseE(l)
    us = "no DE" if u is None else f"{v:g} ± {u:g}"
    print(f"{f + ':' + str(n):<46}{raw:>9}{l[19:21]!r:>5}{us:>24}")
