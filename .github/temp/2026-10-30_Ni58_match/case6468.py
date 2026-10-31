AD = [l.rstrip("\n").ljust(80) for l in open(r"XUNDL/A58/Ni58/new/Ni58_adopted.ens", encoding="utf-8", errors="replace")]
C  = [l.rstrip("\n").ljust(80) for l in open(r"XUNDL/A58/Ni58/new/Ni58_58ni_p_pP_pol_p_pP_p_pPg.ens", encoding="utf-8", errors="replace")]

print("=== dataset C: level records 6450-6490 ===")
for i, l in enumerate(C, 1):
    try: v = float(l[9:19])
    except: continue
    if l[5] == " " and l[6] == " " and l[7] == "L" and 6450 <= v <= 6490:
        print(f"  line {i:>4}: E={l[9:19].strip():>8} DE={l[19:21].strip()!r:>5} J={l[22:39].strip()!r:<10} L={l[55:64].strip()!r} S={l[64:74].strip()!r}")

print("\n=== adopted: level + XREF records 6450-6490 ===")
for i, l in enumerate(AD):
    try: v = float(l[9:19])
    except: continue
    if l[5] == " " and l[6] == " " and l[7] == "L" and 6450 <= v <= 6490:
        xl = i + 1
        print(f"  level line {i+1:>5}: E={l[9:19].strip():>8} DE={l[19:21].strip()!r:>5} J={l[22:39].strip()!r}")
        print(f"  XREF  line {xl+1:>5}: {AD[xl][9:80].rstrip()}")
