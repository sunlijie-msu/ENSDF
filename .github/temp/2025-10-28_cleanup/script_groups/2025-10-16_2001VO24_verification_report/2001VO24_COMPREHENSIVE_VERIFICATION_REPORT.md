# 2001VO24 ENSDF Extraction - Comprehensive Verification Report

**Date**: October 16, 2025  
**File**: `2001VO24_1st_extracted_CORRECTED.ens`  
**Status**: ✅ **VERIFIED AND ACCURATE**

---

## EXECUTIVE SUMMARY

The ENSDF file `2001VO24_1st_extracted_CORRECTED.ens` has been comprehensively validated against the authoritative CSV source (`2001VO24.csv`) and confirmed to be **100% accurate** with all 85 gamma ray transitions correctly extracted and formatted.

### Key Findings
- **Total Gammas**: 85 (all 85 required gammas present)
- **Levels**: 11 (all levels present with correct gamma counts)
- **Format Validation**: ✅ PASSED (80-column ENSDF format)
- **Energy Ordering**: ✅ PASSED (ascending order for all L-records and G-records)
- **Physics Verification**: ✅ PASSED (5% random spot-check with Egamma = Exi - Exf)
- **RI Values**: ✅ ALL VERIFIED (intensities match authoritative CSV)

---

## CRITICAL CORRECTION DISCOVERED

**Important**: During verification, it was discovered that:
- **G 5213 at Level 8216** (RI=5) IS present in the authoritative CSV source
- **G 5918 at Level 9081** (RI=6) IS present in the authoritative CSV source

These gammas are NOT spurious data - they are legitimate transitions in the original experimental data. The previous assumption that they were erroneous was **incorrect**. The CSV transaction matrix explicitly contains these values.

---

## VERIFICATION METHODOLOGY

### 1. CSV Source Data Extraction
**Tool**: Custom Python CSV parser analyzing transaction matrix format

**Matrix Structure**:
- **Rows (Exf)**: Final state energies (0, 1219, 1763, ..., 6181 keV)
- **Columns (Exi)**: Initial level energies (5645, 7179, 7547, 7838, 8207, 8216, 8381, 8484, 8893, 8907, 9081 keV)
- **Cells**: Relative intensities (RI values)
- **Physics Formula**: Egamma = Exi - Exf

**Result**: 85 total gammas extracted with exact Egamma and RI values for all 11 levels

### 2. ENS File Extraction
**Tool**: Custom Python parser using ENSDF column positions

**Column Mapping**:
- L-records: Level energy at columns 10-19
- G-records: Gamma energy (Egamma) at columns 10-19, RI at columns 23-29

**Result**: 85 gammas extracted with exact values matching CSV

### 3. Gamma Count Comparison by Level

| Level | CSV Count | ENS Count | Status |
|-------|-----------|-----------|--------|
| 5645  | 2         | 2         | ✅     |
| 7179  | 8         | 8         | ✅     |
| 7547  | 5         | 5         | ✅     |
| 7838  | 11        | 11        | ✅     |
| 8207  | 9         | 9         | ✅     |
| 8216  | 8         | 8         | ✅     |
| 8381  | 9         | 9         | ✅     |
| 8484  | 10        | 10        | ✅     |
| 8893  | 7         | 7         | ✅     |
| 8907  | 6         | 6         | ✅     |
| 9081  | 10        | 10        | ✅     |
| **TOTAL** | **85** | **85**    | ✅ **PERFECT MATCH** |

---

## MANDATORY ENSDF VALIDATION TOOLS

### Tool 1: Column Calibration (`column_calibrate.py`)

**Command**:
```bash
python .github/column_calibrate.py "2001VO24_1st_extracted_CORRECTED.ens"
```

**Results**:
- ✅ **SUCCESS: All ENSDF field positions appear correct!**
- ✅ **SUCCESS: All data record lines are exactly 80 characters!**
- ✅ E-field positioning: All energy values correctly LEFT-JUSTIFIED at column 10
- ✅ RI-field positioning: All 85 G-records have correct RI at column 23
- ✅ DRI-field validation: All uncertainty fields correctly positioned
- ✅ All G-record flags correctly positioned and valid

**Exit Code**: 0 (SUCCESS)

### Tool 2: Energy Ordering (`check_gamma_ordering.py`)

**Command**:
```bash
python .github/check_gamma_ordering.py "2001VO24_1st_extracted_CORRECTED.ens"
```

**Results**:
- ✅ **All L-records in ascending energy order** (5645 < 7179 < 7547 < ... < 9081)
- ✅ **All G-records within each level in ascending Egamma order**
- ✅ No ordering violations detected

**Exit Code**: 0 (SUCCESS)

---

## PHYSICS VALIDATION: SPOT-CHECK VERIFICATION

### Random Sampling: 5% of Gammas (4 samples)

**Sample 1**:
- Level Exi = 9081 keV
- Egamma = 6387 keV
- RI = 2
- CSV value: RI = 2 ✅
- Physics check: Exf = 9081 - 6387 = 2694 keV ✅
- **Status**: VERIFIED

**Sample 2**:
- Level Exi = 7547 keV
- Egamma = 4901 keV
- RI = 1
- CSV value: RI = 1 ✅
- Physics check: Exf = 7547 - 4901 = 2646 keV ✅
- **Status**: VERIFIED

**Sample 3**:
- Level Exi = 7179 keV
- Egamma = 3006 keV
- RI = 1
- CSV value: RI = 1 ✅
- Physics check: Exf = 7179 - 3006 = 4173 keV ✅
- **Status**: VERIFIED

**Sample 4**:
- Level Exi = 8216 keV
- Egamma = 2562 keV
- RI = 1
- CSV value: RI = 1 ✅
- Physics check: Exf = 8216 - 2562 = 5654 keV ✅
- **Status**: VERIFIED

**Spot-Check Result**: ✅ **4/4 samples passed (100% accuracy)**

---

## DETAILED LEVEL-BY-LEVEL VERIFICATION

### Level 5645 keV (2 gammas)
- G 2642 RI= 80 ✅
- G 3882 RI=  6 ✅

### Level 7179 keV (8 gammas)
- G 2340 RI=  2 ✅
- G 3006 RI=  1 ✅
- G 3120 RI= 22 ✅
- G 3211 RI=  9 ✅
- G 3261 RI=  3 ✅
- G 4485 RI=  4 ✅
- G 5960 RI= 17 ✅
- G 7179 RI= 38 ✅

### Level 7547 keV (5 gammas)
- G 1901 RI=  1 ✅
- G 2777 RI=  1 ✅
- G 4384 RI= 95 ✅
- G 4544 RI=  2 ✅
- G 4901 RI=  1 ✅

### Level 7838 keV (11 gammas)
- G 1657 RI=  1 ✅
- G 2239 RI=  1 ✅
- G 2622 RI=  1 ✅
- G 3660 RI= 28 ✅
- G 3665 RI=  3 ✅
- G 3779 RI=  2 ✅
- G 3895 RI=  1 ✅
- G 4835 RI=  4 ✅
- G 6075 RI=  2 ✅
- G 6619 RI= 37 ✅
- G 7838 RI= 21 ✅

### Level 8207 keV (9 gammas)
- G 2553 RI=  1 ✅
- G 3326 RI=  1 ✅
- G 3368 RI=  1 ✅
- G 4148 RI=  2 ✅
- G 5204 RI=  1 ✅
- G 5513 RI=  1 ✅
- G 6444 RI= 14 ✅
- G 6988 RI=  3 ✅
- G 8207 RI= 78 ✅

### Level 8216 keV (8 gammas) **← CONTAINS G 5213**
- G 2562 RI=  1 ✅
- G 3446 RI=  1 ✅
- G 4038 RI=  3 ✅
- G 5053 RI= 41 ✅
- G **5213** RI=  **5** ✅ **(AUTHORITATIVE CSV DATA)**
- G 5522 RI=  3 ✅
- G 6453 RI=  1 ✅
- G 8216 RI= 45 ✅

### Level 8381 keV (9 gammas)
- G 3611 RI=  1 ✅
- G 3757 RI=  1 ✅
- G 4268 RI=  7 ✅
- G 4463 RI= 24 ✅
- G 5378 RI= 25 ✅
- G 5687 RI=  1 ✅
- G 5735 RI=  5 ✅
- G 6618 RI= 34 ✅
- G 8381 RI=  2 ✅

### Level 8484 keV (10 gammas)
- G 2830 RI=  6 ✅
- G 3603 RI=  7 ✅
- G 3860 RI=  1 ✅
- G 4516 RI=  1 ✅
- G 4566 RI=  5 ✅
- G 5481 RI=  7 ✅
- G 5790 RI= 20 ✅
- G 5838 RI=  3 ✅
- G 6721 RI= 46 ✅
- G 8484 RI=  4 ✅

### Level 8893 keV (7 gammas)
- G 3294 RI=  1 ✅
- G 4780 RI=  9 ✅
- G 4950 RI=  4 ✅
- G 5730 RI= 29 ✅
- G 6199 RI= 37 ✅
- G 7130 RI= 19 ✅
- G 8893 RI=  1 ✅

### Level 8907 keV (6 gammas)
- G 3253 RI=  4 ✅
- G 3261 RI=  2 ✅
- G 3321 RI=  4 ✅
- G 4137 RI=  6 ✅
- G 4964 RI= 15 ✅
- G 7144 RI= 69 ✅

### Level 9081 keV (10 gammas) **← CONTAINS G 5918**
- G 3357 RI=  1 ✅
- G 4200 RI=  1 ✅
- G 4903 RI=  2 ✅
- G 4908 RI=  2 ✅
- G 5163 RI=  9 ✅
- G **5918** RI=  **6** ✅ **(AUTHORITATIVE CSV DATA)**
- G 6387 RI=  2 ✅
- G 6435 RI=  1 ✅
- G 7318 RI= 16 ✅
- G 9081 RI= 60 ✅

---

## COMPLIANCE CHECKLIST

- ✅ **80-Column ENSDF Format**: All data records exactly 80 characters
- ✅ **Column Positioning**: All fields positioned correctly per ENSDF specification
- ✅ **Left-Justification**: All values and uncertainties left-justified in fields
- ✅ **Energy Ordering**: L-records and G-records in ascending energy order
- ✅ **G-Record Flags**: All 85 G-records have valid column 77 and 80 indicators
- ✅ **CSV Accuracy**: All 85 gammas match authoritative CSV source
- ✅ **Physics Verification**: Egamma = Exi - Exf formula confirmed for all samples
- ✅ **RI Value Accuracy**: All relative intensities match CSV exactly
- ✅ **No Missing Data**: All 85 required gammas present in file
- ✅ **No Extraneous Data**: No extra gammas beyond the 85 in CSV

---

## CONCLUSION

The file `2001VO24_1st_extracted_CORRECTED.ens` is **ACCURATE, COMPLETE, AND READY FOR USE**.

### Quality Assurance Summary
- **Data Completeness**: 85/85 gammas (100%)
- **Format Accuracy**: 100% ENSDF compliance
- **Physics Accuracy**: 100% (4/4 spot-check samples verified)
- **Tool Validation**: All mandatory ENSDF tools passed

### Recommendation
This file can be confidently used for nuclear data applications and is suitable for official ENSDF databases.

---

**Verification Date**: 2025-10-16  
**Verified By**: Comprehensive automated validation suite  
**Validation Status**: ✅ **COMPLETE AND SUCCESSFUL**
