import re
def L(p): return [l.rstrip("\n").ljust(80) for l in open(p, encoding="utf-8", errors="replace")]
NI = L(r"XUNDL/A58/Ni58/new/Ni58_adopted.ens")
CO = L(r"XUNDL/A58/Co58/new/Co58_adopted.ens")

def raw(src, tag, ranges):
    print(f"--- {tag} ---")
    for a, b in ranges:
        for n in range(a, b + 1):
            print(f"  :{n:<5}{src[n-1].rstrip()}")
        print()

raw(NI, "Ni58 malformed/order", [(207,210),(216,219),(240,243),(403,406),(536,539),(906,910),(921,925),(1196,1200),(1453,1456),(1534,1537),(1736,1746),(1346,1350),(976,987)])
raw(CO, "Co58 malformed/order/dup", [(403,410),(504,509),(732,739),(804,811),(858,863),(864,871),(982,987),(1006,1011)])

print("=== star-label raw counts (regex on full file text) ===")
for src, tag, labs in [(NI, "Ni58", ["C(7590*)", "C(9044*)", "F(7109*)", "L(*)", "L(6780*)", "M(6800*)", "N(6800*)"]),
                       (CO, "Co58", ["I(2770*)", "J(1743*)", "J(2781*)", "R(1729*)", "R(1778*)", "S(1743*)", "S(2456*)"])]:
    for lab in labs:
        hits = [i for i, l in enumerate(src, 1) if lab in l]
        print(f"  {tag} {lab:<12} count={len(hits):<3} lines={hits}")

print("\n=== duplicate level energies IGNORING DE ===")
for src, tag in [(NI, "Ni58"), (CO, "Co58")]:
    lv = [(i, l) for i, l in enumerate(src, 1) if l[5] == " " and l[6] == " " and l[7] == "L"]
    from collections import Counter, defaultdict
    d = defaultdict(list)
    for i, l in lv:
        d[l[9:19].strip()].append(i)
    n = 0
    for e, ls in d.items():
        if len(ls) > 1:
            n += 1
            if n <= 12:
                print(f"  {tag} E={e:<10} lines={ls}")
    print(f"  {tag} total duplicate-energy groups: {n}")
