import re
def L(p): return [x.rstrip("\n").ljust(80) for x in open(p, encoding="utf-8", errors="replace")]
B = r"XUNDL/A58/Ni58/new/"
N = L(B + "Ni58_54fe_16o_12c.ens")
D = L(B + "Ni58_58ni_a_aP.ens")
C = L(B + "Ni58_58ni_p_pP_pol_p_pP_p_pPg.ens")
F = L(B + "Ni58_58ni_e_eP.ens")
LO = L(B + "Ni58_54fe_7li_t.ens")
AD = L(B + "Ni58_adopted.ens")

def nums(src, lo, hi, tag):
    out = []
    for l in src:
        if l[5] == " " and l[6] == " " and l[7] == "L":
            try: v = float(l[9:19].split()[0])
            except: continue
            if lo <= v <= hi: out.append(v)
    print(f"  {tag}: {out}")

print("--- dataset level energies near the disputed adopted levels ---")
nums(N, 6800, 7600, "N 54Fe(16O,12C) 6800-7600")
nums(D, 8000, 9900, "D 58Ni(a,a') 8000-9900 (top of file)")
nums(C, 9300, 9400, "C 58Ni(p,p') 9300-9400")
nums(F, 8150, 8300, "F 58Ni(e,e') 8150-8300")
nums(LO, 2700, 2900, "L 54Fe(7Li,t) 2700-2900")

print("\n--- adopted XREF lines for the flagged levels ---")
for target in ("7210.4", "18000", "8203", "2775.39", "9336", "9327.3"):
    for i, l in enumerate(AD):
        if l[5] == " " and l[6] == " " and l[7] == "L" and l[9:19].strip() == target:
            print(f"   L {l[9:19].strip():>8} : {AD[i+1].rstrip()[:70]}")
            break

print("\n--- N dataset: highest level below 7210 ---")
alln = sorted(float(l[9:19].split()[0]) for l in N if l[5] == " " and l[6] == " " and l[7] == "L" and l[9:19].strip())
low = [x for x in alln if x < 7210]
print("   N levels below 7210.4:", low[-3:], " above:", [x for x in alln if x > 7210][:3])
print("\n--- D dataset: top 5 levels ---")
alld = sorted(float(l[9:19].split()[0]) for l in D if l[5] == " " and l[6] == " " and l[7] == "L" and l[9:19].strip())
print("   ", alld[-5:])
