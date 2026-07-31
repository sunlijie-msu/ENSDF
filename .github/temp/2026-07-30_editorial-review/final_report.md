# Editorial Review Report: 58Ca, 58Sc, 58Ti, 58V, 58Cr Datasets

**Action:** Check-Only. No edits applied.  
**Scope:** Comment records only (c, cL, cG, cB, cE, cN, cP, cQ).  
**Protocol:** `.github/skills/editorial-review-guidelines/SKILL.md`  
**Date:** 2026-07-30  

---

## Summary

| Isotope | Files Scanned | Issues Found |
|---------|--------------|--------------|
| 58Ca    | 2            | 4            |
| 58Sc    | 3            | 2            |
| 58Ti    | 4            | 9            |
| 58V     | 2            | 4            |
| 58Cr    | 6            | 5            |
| **Total** | **17**     | **24**       |

---

## Detailed Findings

| File | Line | Category | Current Text | Recommended | Rationale |
|------|------|----------|-------------|-------------|-----------|
| Ca58_adopted.ens | 9 | Superscript-Notation | `{+56Sc}` | `{+56}Sc` | Element symbol inside superscript braces; `{+n}` should wrap only mass number |
| Ca58_adopted.ens | 9 | Spelling | `neutrom` | `neutron` | Misspelling |
| Ca58_adopted.ens | 9 | Extra-Space | `from  mass` (double space) | `from mass` | Double space within comment text |
| Ca58_adopted.ens | 38 | Capitalization | `cL T$No experimental value has been reported` | `cL T$no experimental value has been reported` | Record-specific T$ comment should be lowercase after field identifier |
| Sc58_adopted.ens | 10 | Spelling | `superseeds` | `supersedes` | Misspelling |
| Sc58_adopted.ens | 20 | Spelling | `grand-daughter` | `granddaughter` | Incorrect hyphenation/spelling |
| Ti58_adopted.ens | 4 | Spelling | `evaluatord` | `evaluators` | Misspelling (typo in cQ comment) |
| Ti58_adopted.ens | 29 | Spelling | `superseeds` | `supersedes` | Misspelling |
| Ti58_adopted.ens | 39 | Spelling | `grand-daughter` | `granddaughter` | Incorrect hyphenation/spelling |
| Ti58_adopted.ens | 41 | Spelling | `superseeds` | `supersedes` | Misspelling |
| Ti58_adopted.ens | 55 | Dittography | `this is the possibly the reason` | `this is possibly the reason` | Duplicated word `the` |
| Ti58_adopted.ens | 65 | Capitalization | `cL T$Weighted average of 57 ms {I10}` | `cL T$weighted average of 57 ms {I10}` | Record-specific T$ comment should be lowercase after field identifier |
| Ti58_adopted.ens | 68 | Spelling | `grand-daughter` | `granddaughter` | Incorrect hyphenation/spelling |
| Ti58_beta_decay_12_ms.ens | 10 | Spelling | `grand-daughter` | `granddaughter` | Incorrect hyphenation/spelling |
| Ti58_beta_decay_12_ms.ens | 23 | Capitalization | `cL T$From Adopted Levels` | `cL T$from Adopted Levels` | Record-specific T$ comment should be lowercase |
| Ti58_9be_61v_58tig.ens | 11 | Hyphenation | `Gamma-ray energies` (adjective form correct, but `Gamma-ray` starts sentence) | `|g-ray energies` or `Gamma rays` | Noun `gamma rays` should not be hyphenated; prefer `|g` notation |
| V58_adopted.ens | 57 | Capitalization | `cL T$Weighted average of 185 ms {I10}` | `cL T$weighted average of 185 ms {I10}` | Record-specific T$ comment should be lowercase |
| V58_adopted.ens | 63 | Capitalization | `cG E$A 114 {I2} |g seen` | `cG E$a 114 {I2} |g seen` | Record-specific E$ comment should be lowercase |
| V58_beta_decay_58_ms.ens | 13 | Spelling | `grand-daughter` | `granddaughter` | Incorrect hyphenation/spelling |
| V58_beta_decay_58_ms.ens | 22 | Capitalization + Extra-Space-After-$ | `cN BR$ assumed %|b{+-}=100` | `cN BR$Assumed %|b{+-}=100` | cN always uppercase; space after `$` should be removed |
| Cr58_adopted.ens | 51 | Missing-Space | `{I13}in Coulomb Excitation` | `{I13} in Coulomb Excitation` | Space needed after `{I...}` uncertainty notation |
| Cr58_coulex.ens | 12 | Hyphenation | `Gamma-rays were detected` | `Gamma rays were detected` or `|g rays were detected` | Noun `gamma rays` not hyphenated |
| Cr58_coulex.ens | 18 | Spelling | `striped {+58}Cr ions` | `stripped {+58}Cr ions` | `stripped` = fully ionized; `striped` = marked with stripes |
| Cr58_238u_48ca_xg_208pb_48ca_xg.ens | 57 | Capitalization | `cL J$From figure 5 of 2006Zh42` | `cL J$from figure 5 of 2006Zh42` | Record-specific J$ comment should be lowercase |
| Cr58_238u_48ca_xg_208pb_48ca_xg.ens | 68 | Capitalization | `cL T$Estimated from broadened line shape` | `cL T$estimated from broadened line shape` | Record-specific T$ comment should be lowercase |

---

## Error Distribution by Category

| Category | Count |
|----------|-------|
| Spelling | 12 |
| Capitalization | 8 |
| Hyphenation | 2 |
| Superscript-Notation | 1 |
| Dittography | 1 |
| Extra-Space | 1 |
| Missing-Space | 1 |

---

## Notes

1. **DALI2 instrument name** — occurrences of `DALI2` in `Ca58_1h_59sc_2pg.ens` and `Ti58_1h_58ti_58tiPg.ens` are the detector array name, NOT bare uncertainty notation. No error.
2. **All files ASCII-clean** — no Unicode leakage found in any of the 17 files.
3. **cP comments** in `Cr58_beta_decay_191_ms.ens` (L24) and `V58_beta_decay_58_ms.ens` (L20) correctly uppercase per cN/cP exception.
4. **cN BR$** in `V58_beta_decay_58.ms.ens` is the only cN comment in the scope and has two concurrent issues (uppercase + extra space).
