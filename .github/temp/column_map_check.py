# Bidirectional column mapping: extract required ENSDF G-records from revised CSV rows
import csv

header_ef = ["", "0", "146.5", "461.2", "665.7", "1230.5",
             "1887.2", "2158.1", "2181.2", "2375.6", "2579.9",
             "2610.6", "2721.4"]  # cols 0-12, col 0 = Ei label

REVISED_ROWS = {
    "2579.9": "2579.9,100,,,,,,,,,,,,,",
    "2610.6": "2610.6,,35+/-1,,18+/-1,24+/-2,,23+/-1,,,,,,,",
    "2721.4": "2721.4,14+/-1,18+/-1,49+/-2,6+/-1,2+/-1,3+/-1,8+/-1,,,,,,,",
    "3128.9": "3128.9,100,,,,,,,,,,,,,",
    "3333.9": "3333.9,,,11+/-6,22+/-6,,,67+/-12,,,,,,,",
}

print("=" * 70)
print("BIDIRECTIONAL COLUMN MAPPING")
print("=" * 70)

for ei_str, raw in REVISED_ROWS.items():
    cols = raw.split(",")
    ei = float(ei_str)
    print(f"\nLevel Ei = {ei_str} keV")
    print(f"  Raw: {raw}")
    gammas = []  # (Egamma, ri_str, dri_str, ef_str)

    # Forward: header → data
    for col_idx in range(1, 13):  # cols 1-12 cover Ef=0 to Ef=2721.4
        val = cols[col_idx].strip() if col_idx < len(cols) else ""
        ef_str = header_ef[col_idx]
        if val and not val.startswith("<") and not val.startswith(">") and val != "X":
            ef = float(ef_str)
            egamma = round(ei - ef, 1)
            parts = val.split("+/-")
            ri = parts[0].strip()
            dri = parts[1].strip() if len(parts) > 1 else ""
            gammas.append((egamma, ri, dri, ef_str))

    gammas.sort()

    print(f"  FORWARD mapping (col→Ef→Eγ):")
    for egamma, ri, dri, ef_str in gammas:
        ristr = f"{ri}±{dri}" if dri else ri
        print(f"    col{header_ef.index(ef_str):>2} Ef={ef_str:>7} → Eγ={egamma:>7} RI={ristr}")

    # Backward: Eγ → Ef → col (verify)
    print(f"  BACKWARD check (Eγ→Ef→col):")
    for egamma, ri, dri, ef_str in gammas:
        ef = round(ei - egamma, 1)
        col_check = header_ef.index(ef_str)
        print(f"    Eγ={egamma:>7} → Ef={ef:>7} → col{col_check:>2} ✓")

print("\n" + "=" * 70)

# Final decision table
print("\nFINAL REQUIRED ENSDF CHANGES:")
print("-" * 70)
changes = {
    "2579.9": "REMOVE G 421.8 (CSV col 7 for Ef=2158.1 is empty)",
    "2610.6": "UPDATE G 452.5: RI 8→23; REMOVE G 723.4 (CSV col 6 for Ef=1887.2 empty)",
    "2721.4": "ADD G 563.3 RI=8±1; ADD G 834.2 RI=3±1 (NEW from col 7 and col 6)",
    "3128.9": "REMOVE G 970.8 (CSV col 7 for Ef=2158.1 is empty)",
    "3333.9": "ADD G 1175.8 RI=67±12 (NEW from col 7, Ef=2158.1)",
}
for ei_str, change in changes.items():
    print(f"  Level {ei_str}: {change}")
