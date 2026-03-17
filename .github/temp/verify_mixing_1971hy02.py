"""
Cross-check 1971Hy02 mixing ratios:
  Source: A34/Cl34/raw/1971HY02_mixing.md
  Target 1: A34/Cl34/raw/1971HY02.ens  (raw processed file)
  Target 2: A34/Cl34/new/Cl34_33s_p_g.ens (adopted file, cG MR$ comments)

Usage: python .github/temp/verify_mixing_1971hy02.py
"""

import random
import re

# ---------------------------------------------------------------------------
# 1. Source table (1971HY02_mixing.md Table V)
# ---------------------------------------------------------------------------
SOURCE = [
    # (Ei_MeV, Ef_MeV, Egamma_MeV, delta_text)
    (6.167, 0.146,  6.021, "+0.02±0.03"),
    (6.167, 1.230,  4.937, "0.0±0.01"),
    (6.167, 3.982,  2.185, "+0.05±0.06 or -1.3±0.2"),
    (6.167, 4.075,  2.092, "-0.03±0.05 or >7"),
    (6.206, 3.545,  2.661, "0.0±0.02"),
    (6.206, 3.601,  2.605, "+0.03±0.05"),
    (6.226, 2.722,  3.504, "+0.05±0.05"),
    (6.226, 3.771,  2.455, "-0.03±0.05"),
    (3.601, 2.722,  0.879, "-0.01±0.04"),
    (3.601, 0.146,  3.455, "-0.07±0.04"),
    (3.545, 0.146,  3.399, "+0.06±0.05"),
    (2.722, 0.461,  2.261, "+0.03±0.05 or +2.3±0.5"),
]

# Expected ENSDF notation after applying the Rose-Brink (1967) sign flip.
# In ENSDF comment format: |d=VAL {IUNC}
ENSDF_EXPECTED = [
    ("-0.02", "3"),
    ("0.00", "1"),
    ("-0.05", "6", "or |d=+1.3 {I2}"),
    ("+0.03", "5", "or |d<-7"),
    ("0.00", "2"),
    ("-0.03", "5"),
    ("-0.05", "5"),
    ("+0.03", "5"),
    ("+0.01", "4"),
    ("+0.07", "4"),
    ("-0.06", "5"),
    ("-0.03", "5", "or |d=-2.3 {I5}"),
]

# ---------------------------------------------------------------------------
# 2. Parse 1971HY02.ens
# ---------------------------------------------------------------------------
def parse_raw_ens(path):
    """Return list of (Ei_keV, Eg_keV, mr_text) for cG M,MR$ lines."""
    entries = []
    current_ei = None
    current_eg = None
    with open(path, encoding="utf-8") as f:
        for line in f:
            if len(line) < 9:
                continue
            rt = line[7:8]
            if rt == "L":
                e = line[9:19].strip()
                if e:
                    try:
                        current_ei = float(e)
                    except ValueError:
                        pass
            elif rt == "G":
                e = line[9:19].strip()
                if e:
                    try:
                        current_eg = float(e)
                    except ValueError:
                        pass
            # Check for cG MR$ or cG M,MR$ lines
            col6 = line[5:6]
            rec = line[7:10] if len(line) > 10 else ""
            if "cG" in line[:10] and ("M,MR$" in line or "MR$" in line[:20]):
                entries.append((current_ei, current_eg, line.rstrip()))
    return entries


# ---------------------------------------------------------------------------
# 3. Parse Cl34_33s_p_g.ens for cG MR$ lines citing 1971Hy02
# ---------------------------------------------------------------------------
def parse_adopted_ens(path):
    """Return list of (level_energy, gamma_energy, mr_text, linenum) for
    cG MR$ or cG M,MR$ lines that reference 1971Hy02."""
    entries = []
    current_ei = None
    current_eg = None
    with open(path, encoding="utf-8") as f:
        for lnum, line in enumerate(f, 1):
            if len(line) < 9:
                continue
            rt = line[7:8]
            if rt == "L" and line[5:6] == " ":
                e = line[9:19].strip()
                if e:
                    try:
                        current_ei = float(e)
                    except ValueError:
                        pass
            elif rt == "G" and line[5:6] == " ":
                e = line[9:19].strip()
                if e:
                    try:
                        current_eg = float(e)
                    except ValueError:
                        pass
            # cG lines
            if "cG" in line[:10] and "1971Hy02" in line:
                if "MR$" in line or "M,MR$" in line:
                    entries.append((current_ei, current_eg, line.rstrip(), lnum))
    return entries


# ---------------------------------------------------------------------------
# 4. Run cross-check
# ---------------------------------------------------------------------------
def main():
    raw_path = "A34/Cl34/raw/1971HY02.ens"
    adopted_path = "A34/Cl34/new/Cl34_33s_p_g.ens"

    print("=" * 70)
    print("MIXING RATIO CROSS-CHECK: 1971Hy02")
    print("=" * 70)
    print(f"\nSource table rows: {len(SOURCE)}")

    # Parse files
    raw_entries = parse_raw_ens(raw_path)
    adopted_entries = parse_adopted_ens(adopted_path)

    print(f"1971HY02.ens MR entries: {len(raw_entries)}")
    print(f"Cl34_33s_p_g.ens cG MR$ (1971Hy02) entries: {len(adopted_entries)}")

    # ---------------------------------------------------------------------------
    # Check A: Source → 1971HY02.ens
    # ---------------------------------------------------------------------------
    print("\n" + "─" * 70)
    print("CHECK A: 1971HY02_mixing.md → 1971HY02.ens")
    print("─" * 70)

    errors_a = 0
    for i, (Ei, Ef, Eg, delta) in enumerate(SOURCE):
        Ei_kev = Ei * 1000
        Eg_kev = Eg * 1000
        # Find matching raw entry by Ei and Eg (within ±3 keV)
        match = None
        for (ei, eg, txt) in raw_entries:
            if ei is not None and eg is not None:
                if abs(ei - Ei_kev) < 5 and abs(eg - Eg_kev) < 5:
                    match = (ei, eg, txt)
                    break
        if match is None:
            print(f"  [MISSING] Row {i+1}: Ei={Ei} MeV, Eg={Eg} MeV ({delta}) — NOT FOUND in 1971HY02.ens")
            errors_a += 1
        else:
            # Verify delta values, including alternate solutions when present.
            exp = ENSDF_EXPECTED[i]
            val_ok = exp[0] in match[2]
            unc_ok = f"{{I{exp[1]}}}" in match[2]
            alt_ok = True if len(exp) < 3 else exp[2] in match[2]
            status = "✓ PASS" if (val_ok and unc_ok and alt_ok) else "✗ FAIL"
            if not (val_ok and unc_ok and alt_ok):
                errors_a += 1
            print(f"  {status} Row {i+1}: Ei={Ei}, Ef={Ef}, Eg={Eg} → {delta}")
            if not val_ok:
                print(f"         EXPECTED: |d={exp[0]} {{I{exp[1]}}}")
                print(f"         FOUND:    {match[2][20:]}")
            if val_ok and unc_ok and not alt_ok:
                print(f"         EXPECTED ALT: {exp[2]}")
                print(f"         FOUND:        {match[2][20:]}")

    print(f"\nCheck A: {len(SOURCE) - errors_a}/{len(SOURCE)} PASS, {errors_a} errors")

    # ---------------------------------------------------------------------------
    # Check B: Source → Cl34_33s_p_g.ens cG MR$ comments
    # ---------------------------------------------------------------------------
    print("\n" + "─" * 70)
    print("CHECK B: 1971HY02_mixing.md → Cl34_33s_p_g.ens cG MR$ comments")
    print("─" * 70)

    errors_b = 0
    row_to_adopted = {}
    for i, (Ei, Ef, Eg, delta) in enumerate(SOURCE):
        Ei_kev = Ei * 1000
        Eg_kev = Eg * 1000
        match = None
        for (ei, eg, txt, lnum) in adopted_entries:
            if ei is not None and eg is not None:
                if abs(ei - Ei_kev) < 5 and abs(eg - Eg_kev) < 5:
                    match = (ei, eg, txt, lnum)
                    break
        if match is None:
            print(f"  [MISSING] Row {i+1}: Ei={Ei} MeV, Eg={Eg} MeV ({delta}) — NOT FOUND in Cl34_33s_p_g.ens")
            errors_b += 1
        else:
            exp = ENSDF_EXPECTED[i]
            val_ok = exp[0] in match[2]
            unc_ok = f"{{I{exp[1]}}}" in match[2]
            alt_ok = True if len(exp) < 3 else exp[2] in match[2]
            status = "✓ PASS" if (val_ok and unc_ok and alt_ok) else "✗ FAIL"
            if not (val_ok and unc_ok and alt_ok):
                errors_b += 1
            row_to_adopted[i] = match
            print(f"  {status} Row {i+1} line {match[3]}: Ei={Ei}, Ef={Ef}, Eg={Eg} → {delta}")
            if not val_ok or not unc_ok:
                print(f"         EXPECTED: |d={exp[0]} {{I{exp[1]}}}")
                print(f"         FOUND:    {match[2][20:]}")
            if val_ok and unc_ok and not alt_ok:
                print(f"         EXPECTED ALT: {exp[2]}")
                print(f"         FOUND:        {match[2][20:]}")

    print(f"\nCheck B: {len(SOURCE) - errors_b}/{len(SOURCE)} PASS, {errors_b} errors")

    # ---------------------------------------------------------------------------
    # Check C: No extra entries (entries in raw or adopted not in source)
    # ---------------------------------------------------------------------------
    print("\n" + "─" * 70)
    print("CHECK C: No spurious entries (1971HY02.ens count vs source)")
    print("─" * 70)
    print(f"  Source rows: {len(SOURCE)}")
    print(f"  1971HY02.ens entries: {len(raw_entries)}")
    print(f"  Cl34_33s_p_g.ens entries: {len(adopted_entries)}")
    if len(raw_entries) == len(SOURCE):
        print("  ✓ PASS: 1971HY02.ens count matches source")
    else:
        print(f"  ✗ FAIL: Count mismatch ({len(raw_entries)} vs {len(SOURCE)})")
    if len(adopted_entries) == len(SOURCE):
        print("  ✓ PASS: Cl34_33s_p_g.ens count matches source")
    else:
        print(f"  ✗ FAIL: Count mismatch ({len(adopted_entries)} vs {len(SOURCE)})")

    # ---------------------------------------------------------------------------
    # Random spot-check (5%, min 5)
    # ---------------------------------------------------------------------------
    print("\n" + "─" * 70)
    n = len(SOURCE)
    sample_size = max(5, round(0.05 * n + 0.5))
    random.seed(20260317)
    indices = random.sample(range(n), sample_size)
    print(f"RANDOM SPOT-CHECK (seed=20260317, {sample_size}/{n} = {100*sample_size//n}%)")
    print("─" * 70)
    spot_pass = 0
    for idx in sorted(indices):
        Ei, Ef, Eg, delta = SOURCE[idx]
        exp = ENSDF_EXPECTED[idx]
        # Verify in adopted
        match_adopted = row_to_adopted.get(idx)
        if match_adopted:
            val_ok = exp[0] in match_adopted[2]
            unc_ok = f"{{I{exp[1]}}}" in match_adopted[2]
            alt_ok = True if len(exp) < 3 else exp[2] in match_adopted[2]
            ok = val_ok and unc_ok and alt_ok
        else:
            ok = False
        flag = "✓ PASS" if ok else "✗ FAIL"
        if ok:
            spot_pass += 1
        print(f"  {flag} Row {idx+1}: Ei={Ei}, Ef={Ef}, Eg={Eg} MeV")
        print(f"         Source: δ={delta}")
        expected_str = f"|d={exp[0]} {{I{exp[1]}}}"
        print(f"         Expected ENSDF: {expected_str}")
        if match_adopted:
            print(f"         Adopted line {match_adopted[3]}: {match_adopted[2][20:]}")
        else:
            print(f"         NOT FOUND in adopted file")

    print(f"\nSpot-check: {spot_pass}/{sample_size} PASS")

    # ---------------------------------------------------------------------------
    # Summary
    # ---------------------------------------------------------------------------
    total_errors = errors_a + errors_b
    print("\n" + "=" * 70)
    print("FINAL SUMMARY")
    print("=" * 70)
    print(f"  Check A (source→raw): {errors_a} errors")
    print(f"  Check B (source→adopted): {errors_b} errors")
    print(f"  Check C (counts): {'OK' if len(raw_entries)==len(SOURCE) and len(adopted_entries)==len(SOURCE) else 'MISMATCH'}")
    print(f"  Spot-check: {spot_pass}/{sample_size} PASS")
    if total_errors == 0 and spot_pass == sample_size:
        print("\n  ✓ ALL CHECKS PASSED — mixing ratio data is correct and complete")
    else:
        print(f"\n  ✗ {total_errors} errors found — investigate before claiming completion")


if __name__ == "__main__":
    main()
