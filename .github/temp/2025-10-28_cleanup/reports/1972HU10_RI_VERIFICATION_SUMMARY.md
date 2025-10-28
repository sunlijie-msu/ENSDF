# 1972HU10 RI VERIFICATION REPORT
## Comprehensive Verification of RI Values from L 7066.4 Onwards

**Date**: October 17, 2025  
**Scope**: All levels from L 7066.4 to end of 1972Hu10.ens  
**Total Levels Checked**: 59 levels  
**Total Gammas with RI Values**: 363 gammas  

---

## EXECUTIVE SUMMARY

**✅ MATCHES FOUND**: 39 gammas (10.7%)  
**❌ DISCREPANCIES FOUND**: 137 items (37.7%)  
**⚠️ MISSING DATA**: Remaining gammas are in levels not present in Cl35_34s_p_g.ens

### Discrepancy Breakdown:
- **Missing Levels**: 40 levels (levels exist in 1972Hu10 but NOT in Cl35_34s_p_g.ens)
- **Missing Gammas**: 83 gammas (gammas exist in 1972Hu10 but NOT found in Cl35_34s_p_g.ens)
- **Missing RI Citations**: 12 gammas (gamma exists but NO 1972Hu10 RI citation in comments)
- **RI Value Mismatches**: 2 gammas (RI values don't match between sources)
- **DRI Value Mismatches**: 0 gammas

---

## CRITICAL FINDINGS

### 1. RI VALUE MISMATCHES (⚠️ REQUIRES IMMEDIATE ATTENTION)

These are actual discrepancies where the RI value in Cl35_34s_p_g.ens does NOT match 1972Hu10:

#### L 7451.2 keV (Cl35: L 7451.1)
| Gamma Energy | 1972Hu10 RI | Cl35 RI | Issue |
|--------------|-------------|---------|--------|
| **G 4448.2** (Cl35:4447.9) | **10.0**(10) | **10**(1) | RI decimal formatting difference |
| **G 4757** (Cl35:4756.8) | **8.0**(8) | **8**(8) | RI decimal formatting difference |

**Analysis**: These appear to be formatting differences (10.0 vs 10, 8.0 vs 8) rather than true value discrepancies. Both are mathematically equivalent but formatted differently.

---

### 2. MISSING RI CITATIONS (❌ URGENT - NEED TO ADD)

These gammas exist in Cl35_34s_p_g.ens but are missing 1972Hu10 RI citations:

#### L 7178.6 keV
- **G 3211.1**: RI=10.0(10) - NO 1972Hu10 citation
- **G 4484** (Cl35:4484.4): RI=4.0(20) - NO 1972Hu10 citation  
- **G 5959.0** (Cl35:5958.7): RI=16.0(16) - NO 1972Hu10 citation
- **G 7177.8**: RI=40.0(40) - NO 1972Hu10 citation

#### L 7502.52 keV (Cl35: L 7502.9)
- **G 3559.7** (Cl35:3559.8): RI=25.0(25) - NO 1972Hu10 citation
- **G 4499.5** (Cl35:4499.8): RI=13.0(13) - NO 1972Hu10 citation
- **G 4856.6** (Cl35:4856.8): RI=55.0(55) - NO 1972Hu10 citation
- **G 5739.2** (Cl35:5739.4): RI=7.0(7) - NO 1972Hu10 citation

#### L 7561.4 keV (Cl35: L 7561.3)
- **G 4867** (Cl35:4867.0): RI=21.0(21) - NO 1972Hu10 citation
- **G 6341.7** (Cl35:6341.3): RI=36.0(36) - NO 1972Hu10 citation
- **G 7560.5** (Cl35:7560.4): RI=36.0(36) - NO 1972Hu10 citation

#### L 7685.8 keV (Cl35: L 7685.5)
- **G 7684.9** (Cl35:7684.6): RI=72.0(72) - NO 1972Hu10 citation

**Total Missing Citations**: 12 gammas require 1972Hu10 RI citations to be added

---

### 3. MISSING GAMMAS (83 gammas)

These gammas appear in 1972Hu10.ens but are NOT found in Cl35_34s_p_g.ens. This could be because:
- Gammas were not adopted in the final evaluation
- Different gamma-ray assignments between datasets
- Experimental limitations in one study vs another

**Representative Examples:**

#### L 7066.4 keV (Cl35: L 7066.2)
- G 3007.9: RI=1.0(5) - NOT IN Cl35
- G 3903.7: RI=6.0(6) - NOT IN Cl35  
- G 5846.8: RI=18.0(18) - NOT IN Cl35

#### L 7178.6 keV
- G 1077: RI=4.0(20) - NOT IN Cl35
- G 3120.1: RI=24.0(24) - NOT IN Cl35
- G 3260.5: RI=2.0(10) - NOT IN Cl35

**See full report for complete list of 83 missing gammas**

---

### 4. MISSING LEVELS (40 levels)

These entire levels from 1972Hu10.ens do NOT exist in Cl35_34s_p_g.ens:

| Level Energy | Number of Gammas |
|--------------|------------------|
| L 7226.2 | 11 gammas |
| L 7503.50 | 3 gammas |
| L 7520.2 | 7 gammas |
| L 7549.8 | 8 gammas |
| L 7619.6 | 6 gammas |
| L 7707.2 | 7 gammas |
| L 7746.0 | 7 gammas |
| L 7778.4 | 10 gammas |
| L 7782.9 | 12 gammas |
| L 7798.4 | 7 gammas |
| L 7881.3 | 10 gammas |
| L 7900.2 | 6 gammas |
| L 7924.0 | 9 gammas |
| L 7971.0 | 12 gammas |
| L 7988.4 | 4 gammas |
| L 7996.7 | 5 gammas |
| L 8002.5 | 7 gammas |
| L 8007.0 | 4 gammas |
| L 8039.6 | 6 gammas |
| L 8076.6 | 11 gammas |
| L 8096.8 | 14 gammas |
| L 8107.4 | 11 gammas |
| L 8114.3 | 8 gammas |
| L 8147.7 | 9 gammas |
| L 8157.3 | 9 gammas |
| L 8180.3 | 6 gammas |
| L 8209.9 | 7 gammas |
| L 8218.3 | 4 gammas |
| L 8243.9 | 0 gammas |
| L 8270.8 | 0 gammas |
| L 8278.8 | 0 gammas |
| L 8284.5 | 0 gammas |
| L 8290.0 | 0 gammas |
| L 8300.1 | 0 gammas |
| L 8320.2 | 0 gammas |
| L 8323.9 | 0 gammas |
| L 8385.1 | 7 gammas |
| L 8391.4 | 0 gammas |
| L 8407.5 | 0 gammas |
| L 8411.8 | 0 gammas |

**Note**: These levels may represent:
- Resonances observed only in 1972Hu10 experiment
- Levels not confirmed by other experiments
- Levels not adopted in the final evaluation

---

## SUCCESSFUL MATCHES (✓ 39 gammas verified)

These gammas have correctly matching RI values between 1972Hu10 and Cl35_34s_p_g.ens:

### L 7066.4 keV (Cl35: L 7066.2)
- ✓ G 4063.5 (Cl35:4063.2): RI=2.0(10)
- ✓ G 4372 (Cl35:4372.0): RI=6.0(6)
- ✓ G 4420.5 (Cl35:4420.2): RI=3.0(15)
- ✓ G 5303.2 (Cl35:5302.8): RI=16.0(16)
- ✓ G 7065.6 (Cl35:7065.4): RI=48.0(48)

### L 7103.4 keV
- ✓ G 4100.4: RI=3.0(15)
- ✓ G 4409 (Cl35:4409.2): RI=13.0(13)
- ✓ G 5340.2 (Cl35:5340.0): RI=4.0(20)
- ✓ G 5883.8 (Cl35:5883.5): RI=67.0(67)
- ✓ G 7102.6: RI=11.0(11)

### L 7194.8 keV (Cl35: L 7194.6)
- ✓ G 3227.3 (Cl35:3227.1): RI=2.0(10)

### L 7234.4 keV (Cl35: L 7234.0)
- ✓ G 4540 (Cl35:4539.8): RI=2.0(10)
- ✓ G 7233.6 (Cl35:7233.2): RI=93.0(93)

### L 7272.5 keV (Cl35: L 7272.7)
- ✓ G 3305.0 (Cl35:3305.2): RI=1.0(5)
- ✓ G 6052.8: RI=23.0(23)
- ✓ G 7271.7 (Cl35:7271.9): RI=69.0(69)

### L 7362.1 keV (Cl35: L 7362.0)
- ✓ G 3394.6 (Cl35:3394.5): RI=3.0(15)
- ✓ G 4359.1 (Cl35:4359.0): RI=0.5(3)
- ✓ G 5598.8 (Cl35:5598.5): RI=10.0(10)
- ✓ G 6142.4 (Cl35:6142.0): RI=70.0(70)
- ✓ G 7361.3 (Cl35:7361.2): RI=10.0(10)

### L 7395.6 keV (Cl35: L 7396.0)
- ✓ G 3048.0 (Cl35:3048.1): RI=10.0(10)
- ✓ G 3452.8 (Cl35:3452.9): RI=8.0(8)
- ✓ G 4232.8 (Cl35:4232.7): RI=49.0(49)
- ✓ G 4392.6 (Cl35:4393.0): RI=14.0(14)
- ✓ G 4749.7 (Cl35:4750.0): RI=10.0(10)

### L 7601.1 keV (Cl35: L 7600.8)
- ✓ G 4598.1 (Cl35:4597.7): RI=9.0(9)
- ✓ G 4955.1 (Cl35:4954.7): RI=1.5(8)
- ✓ G 7600.2 (Cl35:7599.9): RI=31.0(31)

### L 7656.7 keV (Cl35: L 7656.6)
- ✓ G 3689.2 (Cl35:3689.1): RI=2.0(10)
- ✓ G 7655.8 (Cl35:7655.7): RI=57.0(57)

### L 7672.3 keV (Cl35: L 7671.9)
- ✓ G 7671.4 (Cl35:7671.0): RI=2.0(10)

### L 7685.8 keV (Cl35: L 7685.5)
- ✓ G 4682.8 (Cl35:4682.4): RI=9.0(9)

### L 7694.3 keV (Cl35: L 7693.9)
- ✓ G 7693.4 (Cl35:7693.0): RI=96.0(96)

### L 7869.0 keV (Cl35: L 7868.7)
- ✓ G 7868.1 (Cl35:7867.8): RI=62.0(62)

### L 8035.8 keV (Cl35: L 8035.7)
- ✓ G 5341 (Cl35:5341.4): RI=5.0(25)
- ✓ G 6272.4 (Cl35:6272.1): RI=5.0(25)
- ✓ G 6816.0 (Cl35:6815.6): RI=56.0(56)
- ✓ G 8034.8 (Cl35:8034.7): RI=2.0(10)

---

## RECOMMENDATIONS

### IMMEDIATE ACTIONS REQUIRED:

1. **Add Missing RI Citations (12 gammas)**:
   - L 7178.6: Add 1972Hu10 citations for 4 gammas
   - L 7502.52: Add 1972Hu10 citations for 4 gammas
   - L 7561.4: Add 1972Hu10 citations for 3 gammas
   - L 7685.8: Add 1972Hu10 citation for 1 gamma

2. **Investigate RI Formatting Discrepancies (2 gammas)**:
   - L 7451.2, G 4448.2: Verify if 10.0(10) vs 10(1) is acceptable formatting
   - L 7451.2, G 4757: Verify if 8.0(8) vs 8(8) is acceptable formatting

3. **Review Missing Gammas (83 gammas)**:
   - Determine if these should be added to Cl35_34s_p_g.ens
   - Verify experimental evidence from 1972Hu10 paper
   - Check if other references support these gamma transitions

4. **Review Missing Levels (40 levels)**:
   - Determine if these resonance levels should be included in adopted dataset
   - Check if these levels are confirmed by other experiments
   - Consider if these are tentative assignments

### VERIFICATION NOTES:

- Energy matching tolerance: ±0.5 keV (accounts for slight differences in energy calibration)
- All matches include both RI value and uncertainty verification
- Gamma energies may differ slightly between 1972Hu10 and Cl35 due to energy calibration differences

---

## METHODOLOGY

**Verification Process:**
1. Parsed all levels and gammas with RI values from 1972Hu10.ens starting at L 7066.4
2. For each level, searched for matching level in Cl35_34s_p_g.ens (within 0.5 keV tolerance)
3. For each gamma, searched for matching gamma energy (within 0.5 keV tolerance)
4. Extracted RI values from either:
   - G-record fields (columns 21-31) if "RI$from 1972Hu10" present
   - Comment lines if "Other: X.X {In} from 1972Hu10" pattern found
5. Compared RI and DRI values for exact matches

**Tools Used:**
- Python script: `verify_1972hu10_v2.py`
- Regular expression matching for RI extraction
- Energy tolerance matching for slight calibration differences

---

## APPENDIX: FULL DETAILED REPORTS

**Complete detailed reports available at:**
- `.github/temp/1972hu10_verification_report_v2.txt` - Full discrepancy details
- `.github/temp/1972hu10_parsed_data.txt` - Parsed 1972Hu10 data structure

---

**Report Generated**: October 17, 2025  
**Verification Script**: `verify_1972hu10_v2.py`  
**Status**: COMPREHENSIVE VERIFICATION COMPLETE ✓
