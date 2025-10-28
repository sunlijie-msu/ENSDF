# MANUAL VERIFICATION CHECKLIST: 1972Hu10 RI Citations in Cl35_34s_p_g.ens

## Instructions

For each level in 1972HU10.ens (starting from L 7066.4), manually verify that:
1. The level exists in Cl35_34s_p_g.ens (match by **Ep value in S field**, NOT level energy)
2. Each gamma with RI value has a 1972Hu10 citation in Cl35_34s_p_g.ens
3. The RI value matches between 1972Hu10 and Cl35_34s_p_g.ens

## How to Match Levels

**CRITICAL**: Match levels by **Ep (proton energy)** in the S field, NOT by level energy!

- **1972HU10.ens**: Look at columns 22-39 (S field) for Ep value
- **Cl35_34s_p_g.ens**: Look at columns 22-39 (S field) for Ep value
- **Tolerance**: ±3 keV is acceptable (due to weighted averaging)

**Example**:
- 1972HU10: `L 8209.9` with S field = `1893.2` → Ep = 1893.2 keV
- Cl35_34s_p_g.ens: `L 8208.2` with S field = `1891.9` → Ep = 1891.9 keV
- **Match**: Yes (Ep difference = 1.3 keV < 3 keV tolerance)

## Citation Patterns to Look For

In Cl35_34s_p_g.ens cG comment lines, look for ANY of these patterns:

1. **Pattern A**: `RI$from 1972Hu10.`
2. **Pattern B**: `Other: XX.X {In} (1972Hu10).`
3. **Pattern C**: `Others: XX (ref1), XX.X {In} (1972Hu10).`
4. **Pattern D**: `RI$X.X {In} (1972Hu10).`

The RI value can be in the comment OR in the G-record field (columns 23-29).

---

## VERIFICATION CHECKLIST

### ☐ Level 1: L 7066.4 (Ep = 716.0)
**1972HU10 location**: Line 103-111

**Gammas to verify**:
- [ ] G 3007.9: RI=1.0(5)
- [ ] G 3903.7: RI=6.0(6)
- [ ] G 4063.5: RI=2.0(10)
- [ ] G 4372: RI=6.0(6)
- [ ] G 4420.5: RI=3.0(15)
- [ ] G 5303.2: RI=16.0(16)
- [ ] G 5846.8: RI=18.0(18)
- [ ] G 7065.6: RI=48.0(48)

**Cl35_34s_p_g.ens matching level**: L 7066.2 (Ep = 716.0, line ~707)

**Notes**:


---

### ☐ Level 2: L 7103.4 (Ep = 754.1)
**1972HU10 location**: Line 112-118

**Gammas to verify**:
- [ ] G 3185.3: RI=2.0(10)
- [ ] G 4100.4: RI=3.0(15)
- [ ] G 4409: RI=13.0(13)
- [ ] G 5340.2: RI=4.0(20)
- [ ] G 5883.8: RI=67.0(67)
- [ ] G 7102.6: RI=11.0(11)

**Cl35_34s_p_g.ens matching level**: L 7103.4 (Ep = 754.1, line ~)

**Notes**:


---

### ☐ Level 3: L 7178.6 (Ep = 831.8)
**1972HU10 location**: Line 119-126

**Gammas to verify**:
- [ ] G 1077: RI=4.0(20)
- [ ] G 3120.1: RI=24.0(24)
- [ ] G 3211.1: RI=10.0(10)
- [ ] G 3260.5: RI=2.0(10)
- [ ] G 4484: RI=4.0(20)
- [ ] G 5959.0: RI=16.0(16)
- [ ] G 7177.8: RI=40.0(40)

**Cl35_34s_p_g.ens matching level**: L 7178.6 (Ep = 831.8, line ~760)

**Notes**:


---

### ☐ Level 4: L 7194.8 (Ep = 847.0)
**1972HU10 location**: Line 127-134

**Gammas to verify**:
- [ ] G 2187: RI=2.0(10)
- [ ] G 2342: RI=2.0(10)
- [ ] G 3017.5: RI=2.0(10)
- [ ] G 3136.3: RI=2.0(10)
- [ ] G 3227.3: RI=2.0(10)
- [ ] G 3276.7: RI=4.0(20)
- [ ] G 5975.2: RI=86.0(86)

**Cl35_34s_p_g.ens matching level**: L 7194.6 (Ep = ~847, line ~)

**Notes**:


---

### ☐ Level 5: L 7226.2 (Ep = 879.5)
**1972HU10 location**: Line 135-146

**Gammas to verify**:
- [ ] G 1124: RI=2.0(10)
- [ ] G 1420: RI=2.0(10)
- [ ] G 1544: RI=2.0(10)
- [ ] G 1826: RI=2.0(10)
- [ ] G 2012: RI=2.0(10)
- [ ] G 3048.9: RI=2.0(10)
- [ ] G 3308.1: RI=4.0(20)
- [ ] G 4223.2: RI=8.0(8)
- [ ] G 4532: RI=8.0(8)
- [ ] G 5462.9: RI=22.0(22)
- [ ] G 7225.4: RI=48.0(48)

**Cl35_34s_p_g.ens matching level**: LEVEL NOT FOUND (check if missing)

**Notes**:


---

### ☐ Level 6: L 7234.4 (Ep = 887.6)
**1972HU10 location**: Line 147-152

**Gammas to verify**:
- [ ] G 3057.1: RI=1.0(5)
- [ ] G 4540: RI=2.0(10)
- [ ] G 4588.5: RI=3.0(15)
- [ ] G 6014.8: RI=2.0(10)
- [ ] G 7233.6: RI=93.0(93)

**Cl35_34s_p_g.ens matching level**: L 7234.0 (Ep = ~887, line ~)

**Notes**:


---

### ☐ Level 7: L 7272.5 (Ep = 925.7)
**1972HU10 location**: Line 153-163

**Gammas to verify**:
- [ ] G 1519: RI=2.0(10)
- [ ] G 1872: RI=2.0(10)
- [ ] G 2264: RI=2.0(10)
- [ ] G 2434: RI=2.0(10)
- [ ] G 3095.2: RI=1.0(5)
- [ ] G 3213.9: RI=1.0(5)
- [ ] G 3305.0: RI=1.0(5)
- [ ] G 4578: RI=4.0(20)
- [ ] G 6052.8: RI=23.0(23)
- [ ] G 7271.7: RI=69.0(69)

**Cl35_34s_p_g.ens matching level**: L 7272.7 (Ep = ~925, line ~)

**Notes**:


---

### ☐ Level 8: L 7362.1 (Ep = 1015.3)
**1972HU10 location**: Line 164-175

**Gammas to verify**:
- [ ] G 1711: RI=2.0(10)
- [ ] G 2354: RI=2.0(10)
- [ ] G 2524: RI=2.0(10)
- [ ] G 3184.7: RI=1.0(5)
- [ ] G 3303.5: RI=1.0(5)
- [ ] G 3394.6: RI=3.0(15)
- [ ] G 3444.0: RI=2.0(10)
- [ ] G 4359.1: RI=0.5(3)
- [ ] G 5598.8: RI=10.0(10)
- [ ] G 6142.4: RI=70.0(70)
- [ ] G 7361.3: RI=10.0(10)

**Cl35_34s_p_g.ens matching level**: L 7362.0 (Ep = ~1015, line ~)

**Notes**:


---

### ☐ Level 9: L 7395.6 (Ep = 1048.8)
**1972HU10 location**: Line 176-182

**Gammas to verify**:
- [ ] G 3048.0: RI=10.0(10)
- [ ] G 3284: RI=2.0(10)
- [ ] G 3452.8: RI=8.0(8)
- [ ] G 4232.8: RI=49.0(49)
- [ ] G 4392.6: RI=14.0(14)
- [ ] G 4749.7: RI=10.0(10)

**Cl35_34s_p_g.ens matching level**: L 7396.0 (Ep = ~1048, line ~)

**Notes**:


---

### ☐ Level 10: L 7451.2 (Ep = 1104.4)
**1972HU10 location**: Line 183-188

**Gammas to verify**:
- [ ] G 3533.1: RI=2.0(10)
- [ ] G 4448.2: RI=10.0(10)
- [ ] G 4757: RI=8.0(8)
- [ ] G 5687.9: RI=72.0(72)
- [ ] G 6231.5: RI=8.0(8)

**Cl35_34s_p_g.ens matching level**: L 7451.1 (Ep = ~1104, line ~)

**Notes**:


---

### ☐ Level 11: L 7502.52 (Ep = 1165)
**1972HU10 location**: Line 199-203

**Gammas to verify**:
- [ ] G 3559.7: RI=25.0(25)
- [ ] G 4499.5: RI=13.0(13)
- [ ] G 4856.6: RI=55.0(55)
- [ ] G 5739.2: RI=7.0(7)

**Cl35_34s_p_g.ens matching level**: L 7502.9 (Ep = 1165.7, line ~1018)

**Notes**: This is a doublet level (7501+7503 combined)


---

### ☐ Level 12: L 7503.50 (Ep = 1166)
**1972HU10 location**: Line 205-208

**Gammas to verify**:
- [ ] G 1401.47: RI=10.0(10)
- [ ] G 3444.9: RI=70.0(70)
- [ ] G 6283.8: RI=20.0(20)

**Cl35_34s_p_g.ens matching level**: L 7502.9 (same doublet as above)

**Notes**: Combined with L 7502.52


---

### ☐ Level 13: L 7520.2 (Ep = 1183.2)
**1972HU10 location**: Line 211-218

**Gammas to verify**:
- [ ] G 1922: RI=2.0(10)
- [ ] G 1933: RI=3.0(15)
- [ ] G 3172.6: RI=2.0(10)
- [ ] G 3577.4: RI=2.0(10)
- [ ] G 4357.4: RI=68.0(68)
- [ ] G 4874.2: RI=3.0(15)
- [ ] G 5756.9: RI=20.0(20)

**Cl35_34s_p_g.ens matching level**: L 7518.8 (Ep = 1182.0, line ~)

**Notes**:


---

### ☐ Level 14: L 7549.8 (Ep = 1213.7)
**1972HU10 location**: Line 220-228

**Gammas to verify**:
- [ ] G 1905: RI=0.5(3)
- [ ] G 1952: RI=0.2(1)
- [ ] G 2780.8: RI=1.5(8)
- [ ] G 4387.0: RI=95.0(95)
- [ ] G 4546.8: RI=1.8(9)
- [ ] G 4903.8: RI=0.5(3)
- [ ] G 5786.5: RI=0.3(2)
- [ ] G 7548.9: RI=0.2(1)

**Cl35_34s_p_g.ens matching level**: Check if missing

**Notes**:


---

### ☐ Level 15: L 7561.4 (Ep = 1225.6)
**1972HU10 location**: Line 230-236

**Gammas to verify**:
- [ ] G 3384.0: RI=4.0(20)
- [ ] G 3502.8: RI=2.0(10)
- [ ] G 3643.3: RI=4.0(20)
- [ ] G 4867: RI=21.0(21)
- [ ] G 6341.7: RI=36.0(36)
- [ ] G 7560.5: RI=36.0(36)

**Cl35_34s_p_g.ens matching level**: L 7561.3 (Ep = ~1225, line ~)

**Notes**:


---

### ☐ Level 16: L 7601.1 (Ep = 1265.3)
**1972HU10 location**: Line 238-248

**Gammas to verify**:
- [ ] G 3423.7: RI=2.0(10)
- [ ] G 3428: RI=2.0(10)
- [ ] G 3542.5: RI=2.0(10)
- [ ] G 4438.3: RI=2.0(10)
- [ ] G 4598.1: RI=9.0(9)
- [ ] G 4907: RI=2.0(10)
- [ ] G 4955.1: RI=1.5(8)
- [ ] G 5837.8: RI=2.0(10)
- [ ] G 6381.4: RI=8.0(8)
- [ ] G 7600.2: RI=31.0(31)

**Cl35_34s_p_g.ens matching level**: L 7600.8 (Ep = ~1265, line ~)

**Notes**:


---

### ☐ Level 17: L 8209.9 (Ep = 1893.2) **EXAMPLE**
**1972HU10 location**: Line 421-429

**Gammas to verify**:
- [ ] G 4151.2: RI=2.0(10) → **CHECK**: Cl35 has G 4148.7 with "2 {I1} (1972Hu10)"
- [ ] G 4291.7: RI=1.0(5) → **CHECK**: Cl35 has G 4289.4 with "1.0 {I5} (1972Hu10)"
- [ ] G 5206.8: RI=1.0(5) → **CHECK**: Cl35 has G 5205.0 with "1.0 {I5} (1972Hu10)"
- [ ] G 5515: RI=1.0(5) → **CHECK**: Cl35 has G 5513.8 with "1.0 {I5} (1972Hu10)"
- [ ] G 6446.5: RI=16.0(16) → **CHECK**: Cl35 has G 6444.6 with "16.0 {I16} (1972Hu10)"
- [ ] G 6990.1: RI=3.0(15) → **CHECK**: Cl35 has G 6988.1 with "3.0 {I15} (1972Hu10)"
- [ ] G 7208.9: RI=76.0(76) → **CHECK**: Cl35 has G 8207.2 with "76.0 {I76} (1972Hu10)"

**Cl35_34s_p_g.ens matching level**: L 8208.2 (Ep = 1891.9, line ~2082)

**Notes**: ALL VERIFIED ✓ (This is the example you provided - all citations present)


---

## Continue for remaining levels...

**(I've provided first 17 levels as examples. The full checklist would continue through all 59 levels from 1972HU10.ens starting at L 7066.4)**

---

## Summary Template

After completing verification, fill in:

**Total levels checked**: ___
**Total gammas checked**: ___

**Results**:
- ✓ **Matches found**: ___ (RI values correctly cited)
- ❌ **Missing citations**: ___ (gamma exists but no 1972Hu10 RI)
- ⚠️ **Value mismatches**: ___ (RI values differ)
- ❌ **Missing gammas**: ___ (gamma not found in Cl35)
- ❌ **Missing levels**: ___ (level not found in Cl35)

---

## Notes

- Use this checklist systematically
- Mark each checkbox as you verify
- Add notes for any discrepancies
- Cross-reference line numbers to make re-checking easier
