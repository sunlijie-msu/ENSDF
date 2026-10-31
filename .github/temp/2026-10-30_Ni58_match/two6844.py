def L(p): return [l.rstrip("\n").ljust(80) for l in open(p, encoding="utf-8", errors="replace")]
DIR = r"XUNDL/A58/Ni58/new/"
C  = L(DIR + "Ni58_58ni_p_pP_pol_p_pP_p_pPg.ens")
AD = L(DIR + "Ni58_adopted.ens")

print("--- dataset C :509-:516 (both levels + their G records) ---")
for n in range(509, 517): print(f"  :{n:<5}{C[n-1].rstrip()}")
print("\n--- adopted :920-:935 ---")
for n in range(920, 936): print(f"  :{n:<5}{AD[n-1].rstrip()}")

print("\n--- 1454 keV level energy + any 1454 G record in dataset C ---")
for i, l in enumerate(C, 1):
    if l[5] == " " and l[6] == " " and l[7] == "L" and l[9:19].strip() == "1454.20":
        print(f"  C level :{i} {l.rstrip()}")
for i, l in enumerate(C, 1):
    if l[5] == " " and l[6] == " " and l[7] == "G" and l[9:19].strip() in ("5390", "5400", "1454.28"):
        print(f"  C gamma :{i} {l.rstrip()}")

import math
print("\n--- arithmetic ---")
print("  C 6844 - 5390 =", 6844 - 5390, " | adopted 6854.5 - 5400 =", 6854.5 - 5400)
d = 6854 - 6844; s = math.sqrt(10**2 + 5**2)
print(f"  C6854 - C6844 = {d} +- {s:.1f}  -> {d/s:.2f} sigma (not resolved)")
for E, s1, name in [(6845.7, 0.7, "adopted 6845.7 (7+)"), (6854.5, 1.0, "adopted 6854.5 (3-)"),
                    (6863.0, 0.6, "adopted 6863.0 (6)")]:
    for cE, cs, cn in [(6844, 10, "C 6844"), (6854, 5, "C 6854")]:
        dd = abs(E - cE); comb = math.sqrt(s1**2 + cs**2)
        print(f"  {name:<22} vs {cn}: dE={dd:5.1f} +- {comb:5.2f} -> {dd/comb:4.2f} sigma")
