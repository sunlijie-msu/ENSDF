"""
MANDATORY SPOT CHECK FOR 173W DATA ENTRY
Per .github/copilot-instructions.md requirements
"""

import random

# Raw source data for verification
raw_data = """
165.2(3) 2042.9 8 7 21/2+ 19/2+ 100(11)
186.3(5) 2229.2 7 8 23/2+ 21/2+ 79(10)
351.4(4) 2229.2 7 7 23/2+ 21/2+ 18(6)
186.0(5) 2346.0 10 9 25/2− 23/2− 88(6)
205.5(3) 2434.7 8 7 25/2+ 21/2+ 70(9)
391.4(3) 2434.7 8 8 25/2+ 23/2+ 73(10)
210.4(3) 2556.4 9 10 27/2− 25/2− 100(6)
396.6(5) 2556.4 9 9 27/2− 25/2− - unmeasured
220.6(2) 2655.3 7 8 27/2+ 23/2+ 84(9)
425.9(2) 2655.3 7 7 27/2+ 23/2+ 84(12)
233.6(4) 2790.0 10 9 29/2− 25/2− 98(7)
444.2(5) 2790.0 10 10 29/2− 27/2− - unmeasured
243.0(2) 2898.3 8 7 29/2+ 21/2+ 88(9)
463.5(4) 2898.3 8 8 29/2+ 25/2+ 95(11)
254.8(3) 3044.8 9 10 31/2− 27/2− 74(4)
488.7(3) 3044.8 9 9 31/2− 27/2− - unmeasured
503.9(5) 3159.2 7 7 31/2+ 23/2+ 63(12)
274.1(5) 3318.9 10 9 33/2− 25/2− 55(3)
528.7(5) 3318.9 10 10 33/2− 29/2− 41(3)
290.6(6) 3609.5 9 10 35/2− 27/2− 53(3)
564.4(4) 3609.5 9 9 35/2− 31/2− 49(4)
306.2(7) 3915.7 10 9 37/2− 25/2− 35(2)
596.7(5) 3915.7 10 10 37/2− 33/2− 76(5)
320.4(5) 4236.1 9 10 39/2− 27/2− 44(2)
626.4(5) 4236.1 9 9 39/2− 35/2− 51(5)
334.7(6) 4570.8 10 9 41/2− 25/2− 28(2)
655.0(4) 4570.8 10 10 41/2− 37/2− 48(4)
348.9(4) 4919.7 9 10 43/2− 27/2− 32(2)
683.4(6) 4919.7 9 9 43/2− 39/2− 52(4)
362.8(5) 5282.4 10 9 45/2− 25/2− 21(3)
711.4(4) 5282.4 10 10 45/2− 41/2− 46(4)
377.4(2) 5659.8 9 10 47/2− 27/2− 16(3)
740.1(4) 5659.8 9 9 47/2− 43/2− 43(4)
392.2(3) 6051.8 10 9 49/2− 25/2− 6(1)
769.4(4) 6051.8 10 10 49/2− 45/2− 33(7)
406.2(4) 6457.7 9 10 51/2− 27/2− 5(1)
797.9(4) 6457.7 9 9 51/2− 47/2− 29(6)
"""

lines = [l for l in raw_data.strip().split('\n') if l.strip()]
total = len(lines)
sample_size = max(3, int(0.05 * total))  # 5% or minimum 3

print(f"Total entries: {total}")
print(f"Sample size (5%): {sample_size}")
print()

# Random selection
random.seed(2026)
sample_indices = sorted(random.sample(range(total), sample_size))

print("RANDOM SPOT CHECK SAMPLE:")
print("="*80)
for idx in sample_indices:
    line = lines[idx]
    parts = line.split()
    eg_raw = parts[0]
    ei = parts[1]
    bandi = parts[2]
    bandf = parts[4]
    jpi_i = parts[5]
    jpi_f = parts[6]
    ig_rest = parts[7:]
    
    print(f"\nRow {idx+1}/{total}: {line}")
    print(f"  Eg={eg_raw}, Ei={ei}, Band {bandi}→{bandf}, Jπ(i)={jpi_i}, Ig={' '.join(ig_rest)}")
    print(f"  ⚠ MANUAL VERIFICATION REQUIRED against ENSDF file")

print()
print("="*80)
print("BIDIRECTIONAL CHECK:")
print("Forward: Row 1 = 165.2(3), Ei=2042.9")
print("Backward: Row 37 (last) = 797.9(4), Ei=6457.7")
print("⚠ Verify both endpoints match file content")
