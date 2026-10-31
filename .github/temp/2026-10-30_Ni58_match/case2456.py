def L(p): return [l.rstrip("\n").ljust(80) for l in open(p, encoding="utf-8", errors="replace")]
CO = L(r"XUNDL/A58/Co58/new/Co58_adopted.ens")
S  = L(r"XUNDL/A58/Co58/new/Co58_60ni_d_a_pol_d_a.ens")

print("--- Co58_adopted: every line containing R(2456 or S(2456 ---")
for i, l in enumerate(CO, 1):
    if "R(2456" in l or "S(2456" in l:
        print(f"  :{i:<5}{l.rstrip()}")

print("\n--- Co58_adopted :627-636 raw ---")
for n in range(627, 637): print(f"  :{n:<5}{CO[n-1].rstrip()}")

print("\n--- dataset S (=60Ni(d,a)) level peaks 2435-2470 ---")
for i, l in enumerate(S, 1):
    if l[5] == " " and l[6] == " " and l[7] == "L":
        try: v = float(l[9:19])
        except: continue
        if 2435 <= v <= 2470:
            print(f"  :{i:<5}E={l[9:19].strip():>8} DE={l[19:21].strip()!r:<4} J={l[22:39].strip()!r} L={l[55:64].strip()!r}")
