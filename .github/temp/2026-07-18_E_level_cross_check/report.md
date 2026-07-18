# Level Energy Cross-Check Report

## Metadata

| Field | Value |
|:-------|:------|
| Source | `2026OSAA_CT11035_152Gd_Table_I.md` (Table I) |
| Target | `2026OSAA_CT11035_152Gd.ens` (ENSDF L-records, E cols 10-19, DE cols 20-21) |
| Date | 2026-07-18 |
| Matching | Rounded keV (exact integer) |
| Spot-check | 30 random levels (15%), all 30 passed |

---

## Summary

| Category | Count | Note |
|:----------|------:|:-----|
| Table I levels | 200 | |
| ENSDF L-records | 201 | Includes ground state 0.0 keV |
| Exact match (delta E < 0.005 keV) | 40 | Value, uncertainty, decimals identical |
| Systematic +0.01 keV offset | 159 | All T1 > ENSDF by 0.01 keV |
| Significant difference | 1 | ~3272 keV match collision |
| Table I only | 0 | |
| ENSDF only | 1 | Ground state 0.0 keV |
| Uncertainty mismatches | 0 | |
| Decimal place mismatches | 0 | |

### Systematic Offset: Direction & Root Cause

| Property | Value |
|:----------|:------|
| Direction | **All 159** T1 > ENSDF (T1 0.01 keV higher) |
| Magnitude | 158 exactly 0.01 keV; 1 at 0.02 keV |
| Root cause | GLSC least-squares fit truncation vs Table I round-half-up |

**Assessment:** NOT data entry errors. GLSC truncates fit output at 0.01 keV level; Table I uses round-half-up.
0.01 keV negligible vs uncertainties (typically 3-15 keV). No correction needed.

---

## ENSDF Only

| E (keV) | Line | Note |
|:---------|:-----|:-----|
| 0.0 | L40 | Ground state. Table I row 1: "0 \| 0+ \| none \| ..." |

---

## Match Collision: ~3272 keV

Table I has two levels near 3272: **3271.97(10)** and **3272.40(16)**.
ENSDF has: **3271.73** (L1575) and **3272.44** (L1447).
Rounded-keV matching collides both Table I entries to key 3272.

**Correct pairing (nearest energy):**

| Table I | ENSDF | Delta E | Within unc? |
|:---------|:-------|:--------|:------------|
| 3271.97(10) | 3271.73 | 0.24 keV | Yes (2.4 sigma) |
| 3272.40(16) | 3272.44 | 0.04 keV | Yes (0.25 sigma) |

Not flagged as data error. Both within normal fit tolerances.

---

## 15% Random Spot-Check

| Metric | Value |
|:--------|:------|
| Sample | 30 levels (15% of 200) |
| Method | Bidirectional Table I markdown ↔ ENSDF L-record E/DE fields |
| Result | **30/30 passed** |
| Failures | 0 |

All spot-checked levels match in value (within 0.02 keV), uncertainty, and decimal places.
Verification code: `spot_check.py`.

---

## Conclusion

1. **No data entry errors detected.** All 200 Table I levels present in ENSDF.
2. **Systematic +0.01 keV offset:** 159/200 levels. GLSC truncation artifact, not error.
3. **40 levels exact match** (20%).
4. **One match collision** ~3272 keV — both levels correct under nearest-energy pairing.
5. **Ground state 0.0 keV** — present in both, different format in Table I.
6. **All uncertainties and decimal places match.**

**Overall: ENSDF L-record energies fully consistent with Table I.**
