import re
def L(p): return [l.rstrip("\n").ljust(80) for l in open(p, encoding="utf-8", errors="replace")]
NI = L(r"XUNDL/A58/Ni58/new/Ni58_adopted.ens")
CO = L(r"XUNDL/A58/Co58/new/Co58_adopted.ens")
CDS = L(r"XUNDL/A58/Ni58/new/Ni58_58ni_p_pP_pol_p_pP_p_pPg.ens")

print("--- Ni58 :1512-1519 (duplicate 9870) ---")
for n in range(1512, 1520): print(f"  :{n:<5}{NI[n-1].rstrip()}")

print("\n--- Ni58 :1737-1745 (duplicate 11080) ---")
for n in range(1737, 1746): print(f"  :{n:<5}{NI[n-1].rstrip()}")

print("\n--- Co58: companion forms for single-star labels ---")
for lab in ["J(1743", "S(1743", "I(2770", "J(2781", "S(2456"]:
    hits = [(i, CO[i-1].rstrip()) for i, l in enumerate(CO, 1) if lab in l]
    print(f"  {lab}) -> {len(hits)} hit(s)")
    for i, s in hits: print(f"     :{i:<5}{s}")

print("\n--- dataset C peaks near 9040 and 7580-7620 ---")
for i, l in enumerate(CDS, 1):
    if l[5] == " " and l[6] == " " and l[7] == "L":
        try: v = float(l[9:19])
        except: continue
        if 9020 <= v <= 9060 or 7580 <= v <= 7625:
            print(f"  :{i:<5}E={l[9:19].strip():>8} DE={l[19:21].strip()!r:<5} J={l[22:39].strip()!r}")

print("\n--- Ni58: all levels 9025-9050 and their XREF ---")
for i, l in enumerate(NI, 1):
    if l[5] == " " and l[6] == " " and l[7] == "L":
        try: v = float(l[9:19])
        except: continue
        if 9025 <= v <= 9050:
            print(f"  :{i:<5}E={l[9:19].strip():>8} DE={l[19:21].strip()!r:<4} J={l[22:39].strip()!r}")
            if i < len(NI) and "XREF=" in NI[i]: print(f"  :{i+1:<5}{NI[i].rstrip()}")
