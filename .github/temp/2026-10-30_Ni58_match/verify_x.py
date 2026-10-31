def L(p): return [l.rstrip("\n").ljust(80) for l in open(p, encoding="utf-8", errors="replace")]
NI = L(r"XUNDL/A58/Ni58/new/Ni58_adopted.ens")
print("--- Ni58 :1372-1382 ---")
for n in range(1372, 1383): print(f"  :{n:<5}{NI[n-1].rstrip()}")
for lab in ["H(*)", "K(", "C(9245", "C(9193"]:
    hits = [i for i, l in enumerate(NI, 1) if lab in l]
    print(f"  {lab:<9} count={len(hits):<3} {hits}")
print("\n--- Ni58 :905-920 ---")
for n in range(905, 921): print(f"  :{n:<5}{NI[n-1].rstrip()}")
