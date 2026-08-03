"""Generate exact old/new patch blocks by reading the real file, then simulate."""
import decimal

PATH = r"A34\S34\new\S34_34cl_ec_decay_31.99_m.ens"

def rnd(s):
    return str(int(decimal.Decimal(s).to_integral_value(rounding=decimal.ROUND_HALF_UP)))

def l_rec(E, J):
    return " 34S   L " + E.ljust(10) + "   " + J.ljust(17) + " " * 41

def g_rec(E, RI, DRI, M):
    return " 34S   G " + E.ljust(10) + "   " + RI.ljust(7) + DRI + " " + M.ljust(9) + " " * 39

def cg(text):
    return (" 34S  cG RI$other: " + text + ".").ljust(80)

with open(PATH, encoding="utf-8") as f:
    lines = f.read().splitlines()

def find_line(substr):
    for i, ln in enumerate(lines, 1):
        if ln.startswith(substr):
            return i, ln
    raise RuntimeError(f"not found: {substr}")

# --- exact anchor lines from file ---
_, cg3304 = find_line(" 34S  cG RI$other: 25.4")
_, l4115 = find_line(" 34S   L 4115")
_, cE4689 = find_line(" 34S  cE TI$0.034")
_, g2561 = find_line(" 34S   G 2561")
_, g2749 = find_line(" 34S   G 2749")
_, cg2749 = find_line(" 34S  cG RI$other: 0.049")

# --- build new blocks ---
L4075 = l_rec("4075", "1+")
G4074 = g_rec("4074", "0.00081", "LT", "D")
cG4074 = cg("<0.0023 (1975Va02)")
G1384 = g_rec("1384", "0.021", "LT", "")
G4877 = g_rec("4877", "0.00076", "LT", "")
cG4877 = cg("<0.0010 (1975Va02)")
L4890 = l_rec("4890", "2+")
G1586 = g_rec("1586", "0.018", "LT", "")
cG1586 = cg("<0.015 (1975Va02)")
G2762 = g_rec("2762", "0.011", "LT", "")
G4889 = g_rec("4889", "0.0015", "LT", "E2")
cG4889 = cg("<0.0010 (1975Va02)")

# --- patch A: insert level 4075 block between L3304 block and L4115 ---
oldA = cg3304 + "\n" + l4115
newA = cg3304 + "\n" + L4075 + "\n" + G4074 + "\n" + cG4074 + "\n" + l4115
# --- patch B: insert G1384 before G2561 ---
oldB = cE4689 + "\n" + g2561
newB = cE4689 + "\n" + G1384 + "\n" + g2561
# --- patch C: insert G4877 block + level 4890 block after cg2749 ---
oldC = cg2749
newC = cg2749 + "\n" + G4877 + "\n" + cG4877 + "\n" + L4890 + "\n" + G1586 + "\n" + cG1586 + "\n" + G2762 + "\n" + G4889 + "\n" + cG4889

# --- simulate ---
sim = "\n".join(lines)
for old, new, name in [(oldA, newA, "A"), (oldB, newB, "B"), (oldC, newC, "C")]:
    if sim.count(old) != 1:
        print(f"PATCH {name}: OLD occurrences={sim.count(old)}  <-- check!")
    sim = sim.replace(old, new, 1)
    print(f"PATCH {name}: applied, len now {len(sim.splitlines())} lines")

# verify all new records present and 80 chars
out = sim.split("\n")
new_keys = [" 34S   L 4075", " 34S   G 4074", " 34S   G 1384", " 34S   G 4877",
            " 34S   L 4890", " 34S   G 1586", " 34S   G 2762", " 34S   G 4889"]
for k in new_keys:
    hit = [l for l in out if l.startswith(k)]
    print(f"  {k}: {len(hit)} record(s), len={len(hit[0]) if hit else 'MISSING'}")
bad = [l for l in out if l[6:7] == " " and l[7:8] in ("L", "G") and len(l) != 80]
print("Bad-length L/G:", bad if bad else "none")

# write expected blocks to a sidecar for manual inspection
with open(r".github\temp\2026-08-02_e_round\patch_blocks.txt", "w", encoding="utf-8") as f:
    f.write("=== PATCH A old ===\n" + oldA + "\n=== PATCH A new ===\n" + newA + "\n")
    f.write("=== PATCH B old ===\n" + oldB + "\n=== PATCH B new ===\n" + newB + "\n")
    f.write("=== PATCH C old ===\n" + oldC + "\n=== PATCH C new ===\n" + newC + "\n")
print("sidecar written")
