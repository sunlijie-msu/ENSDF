#!/usr/bin/env python3
"""Comprehensive verification of 2001VO24 data in Cl35_34s_p_g.ens"""

# 2001VO24 L 7547 (matches p_g.ens L 7548.9) from CSV
csv_data = {
    "1901": 1,      # Exf=5646
    "4384": 95,     # Exf=3163
    "4544": 2,      # Exf=3003
    "4901": 1,      # Exf=2646
    "7070": 1,      # Exf=477 (NEW - not in current p_g.ens)
}

# p_g.ens L 7548.9 gammas (current state)
pg_data = {
    "1903": 0.6,    # from 1976Me12, has 2001Vo24: 1
    "1963": 0.1,    # from 1976Me12, NO 2001Vo24 data
    "2778.9": 1.3,  # from 1976Me12, NO 2001Vo24 data
    "4385.6": 95,   # from 1976Me12: 94, has 2001Vo24: 95 ✓
    "4545.8": 1.8,  # from 1972Hu10: 2.0, has 2001Vo24: 2 ✓
    "4902.8": 0.5,  # from 1976Me12: 0.68, has 2001Vo24: 1 ✓
    "5785.4": 0.3,  # from 1976Me12: 0.33, NO 2001Vo24 data
    "7548.0": 0.2,  # from 1976Me12: 0.27, NO 2001Vo24 data
}

print("=" * 70)
print("VERIFICATION: 2001VO24 L 7547 vs p_g.ens L 7548.9")
print("=" * 70)

# Match gammas
print("\nMATCHING ANALYSIS:")
print("-" * 70)
print(f"{'CSV Egamma':<15} {'CSV RI':<10} {'p_g.ens Egamma':<18} {'p_g.ens RI':<15} {'Status':<15}")
print("-" * 70)

for csv_eg, csv_ri in csv_data.items():
    csv_eg_int = int(csv_eg)
    
    # Find matching transition in pg_data
    # Check energy within ±30 keV tolerance (accounting for resolution)
    matched = False
    for pg_eg, pg_ri in pg_data.items():
        pg_eg_float = float(pg_eg)
        energy_diff = abs(csv_eg_int - pg_eg_float)
        
        if energy_diff < 30:  # Within 30 keV tolerance
            matched = True
            ri_match = "✓" if csv_ri == int(pg_ri) else f"MISMATCH: {int(pg_ri)}"
            print(f"{csv_eg:<15} {csv_ri:<10} {pg_eg:<18} {pg_ri:<15} {ri_match:<15}")
            break
    
    if not matched:
        print(f"{csv_eg:<15} {csv_ri:<10} {'NO MATCH':<18} {'-':<15} {'⚠ MISSING':<15}")

print("\n" + "=" * 70)
print("MISSING TRANSITIONS IN p_g.ens:")
print("-" * 70)

# Find gammas in p_g.ens that are NOT in CSV
print("p_g.ens-only gammas (should verify if data is valid):")
for pg_eg, pg_ri in pg_data.items():
    pg_eg_int = float(pg_eg)
    found = False
    for csv_eg in csv_data.keys():
        if abs(pg_eg_int - int(csv_eg)) < 30:
            found = True
            break
    if not found:
        print(f"  G {pg_eg}: RI={pg_ri} keV (from 1976Me12 or other sources, NOT in 2001Vo24)")

print("\nCSV-only gammas (should be ADDED to p_g.ens if appropriate):")
for csv_eg, csv_ri in csv_data.items():
    csv_eg_int = int(csv_eg)
    found = False
    for pg_eg in pg_data.keys():
        if abs(csv_eg_int - float(pg_eg)) < 30:
            found = True
            break
    if not found:
        print(f"  G {csv_eg}: RI={csv_ri} (NEW in 2001Vo24, NOT in current p_g.ens) ⚠")
        exf = 7547 - csv_eg_int
        print(f"         → Final level: Exf={exf} keV")

print("\n" + "=" * 70)
print("DATA INTEGRITY CHECK:")
print("-" * 70)

# Check if RI values that we already added are correct
print("\nRI values in p_g.ens comments with 2001Vo24 source:")
ri_checks = [
    ("G 1903", 1, "1 (2001Vo24)"),
    ("G 4385.6", 95, "95 (2001Vo24)"),
    ("G 4545.8", 2, "2 (2001Vo24)"),
    ("G 4902.8", 1, "1 (2001Vo24)"),
]

for gamma, expected_ri, comment_format in ri_checks:
    status = "✓ CORRECT" if expected_ri > 0 else "? NEEDS VERIFICATION"
    print(f"  {gamma}: Expected RI={expected_ri}, Format: {comment_format} {status}")

print("\n" + "=" * 70)
