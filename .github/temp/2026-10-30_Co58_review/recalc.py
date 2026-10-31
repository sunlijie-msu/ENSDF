import math
D = r"d:/X/ND/ENSDF/XUNDL/A58/Co58/new/"
def lines(p): return [l.ljust(80) for l in open(p, encoding="utf-8", errors="replace").read().split("\n")]

def eu(l, c1=9, c2=19, d1=19, d2=21):
    raw = l[c1:c2].strip(); de = l[d1:d2].strip()
    try: v = float(raw)
    except: return None, None
    if not de or de in ("GT", "LT", "LE", "GE"): return v, None
    try: d = float(de)
    except: return v, None
    nd = len(raw.split(".")[1]) if "." in raw else 0
    return v, d * 10 ** (-nd)

print("=== Co58_adopted: gamma energy > level energy, correct uncertainties ===")
L = lines(D + "Co58_adopted.ens")
lvE = None
rows = []
for i, l in enumerate(L, 1):
    if l[5] == " " and l[6] == " " and l[7] == "L":
        v, u = eu(l)
        if v is not None: lvE = (v, u, i)
    elif lvE and l[5] == " " and l[6] == " " and l[7] == "G":
        g, gu = eu(l)
        if g is not None and lvE[0] is not None and g > lvE[0] + 1e-9:
            sig = math.hypot(gu or 0, lvE[1] or 0)
            s = f"{(g - lvE[0]) / sig:.2f} sigma" if sig > 0 else "n/a"
            rows.append((lvE[2], i, lvE[0], lvE[1], g, gu, g - lvE[0], s))
for r in rows:
    print(f"  L{r[0]} {r[2]:g} ± {r[3] if r[3] is not None else '?'}  <-  G{r[1]} {r[4]:g} ± {r[5] if r[5] is not None else '?'}   diff={r[6]:.2f} keV  {r[7]}")

print("\n=== XREF item gaps with correct uncertainties ===")
IT = [("G 2260 (56fe_a_d:31)", "Co58_56fe_a_d.ens", 31, "Co58_adopted.ens", 598),
      ("G 3320 (56fe_a_d:35)", "Co58_56fe_a_d.ens", 35, "Co58_adopted.ens", 838),
      ("G 4350 (56fe_a_d:47)", "Co58_56fe_a_d.ens", 47, "Co58_adopted.ens", 1080),
      ("E 3970 (56fe_3he_p:63)", "Co58_56fe_3he_p.ens", 63, "Co58_adopted.ens", 1027),
      ("K 2260 (58fe_p_n_p_ng:94)", "Co58_58fe_p_n_p_ng.ens", 94, "Co58_adopted.ens", 595),
      ("K 2260 (58fe_p_n_p_ng:94)", "Co58_58fe_p_n_p_ng.ens", 94, "Co58_adopted.ens", 598),
      ("K 5800 (58fe_p_n_p_ng:101)", "Co58_58fe_p_n_p_ng.ens", 101, "Co58_adopted.ens", 1173),
      ("M 3410 (58ni_d_2he:46)", "Co58_58ni_d_2he.ens", 46, "Co58_adopted.ens", 854),
      ("S 2849 (60ni_d_a:76)", "Co58_60ni_d_a_pol_d_a.ens", 76, "Co58_adopted.ens", 728),
      ("R 2242 (59co_3he_a:34)", "Co58_59co_3he_a.ens", 34, "Co58_adopted.ens", 598)]
for tag, df, dn, af, an in IT:
    dv, du = eu(lines(D + df)[dn - 1]); av, au = eu(lines(D + af)[an - 1])
    gap = dv - av
    if du is not None and au is not None:
        sig = math.hypot(du, au); s = f"{gap / sig:.2f} sigma"
    else:
        s = "sigma n/a (missing DE)"
    print(f"  {tag:<28} ds {dv:g} ± {du if du is not None else '?'}   ad {av:g} ± {au if au is not None else '?'}   gap {gap:+.1f} keV   {s}")
