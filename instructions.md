# Nuclear Data Evaluation Guidelines

## General Comment Section Ordering Policy

All `adopted.ens` files must follow the standardized ordering for general comments to ensure consistency across nuclear data evaluations. The required order is:

### 1. Isotope discovery
- Format: `Isotope discovery (reference): experimental details`
- Must be the first general comment section
- Example: `Isotope discovery (2012Th10): {+32}S(α,n){+35}Ar at Purdue (1940Ki12,1941Ki01,1941El04).`

### 2. {+A}X production:
- Format: `{+A}X production:` where A is mass number and X is element symbol
- Lists production methods and experimental details
- Should include all relevant production studies

### 3. {+A}X decay measurements:
- Format: `{+A}X decay measurements:`
- Covers half-life measurements, decay modes, and decay studies
- Include beta decay, electron capture, proton emission, etc.

### 4. {+A}X radius measurement:
- Format: `{+A}X radius measurement:` (singular)
- Covers nuclear radius determinations
- Include interaction cross-section studies and matter radius measurements

### 5. {+A}X mass measurements:
- Format: `{+A}X mass measurements:`
- Lists mass spectrometry and reaction Q-value studies
- Include direct mass measurements and systematic studies

### 6. Theoretical calculations:
- Format: `Theoretical calculations:`
- Lists theoretical predictions and model calculations
- Include shell model, ab initio calculations, and systematic predictions
- Should be the last general comment section

## Compliance Status

### Files Currently Compliant:
- Al35_adopted.ens ✅
- Ar35_adopted.ens ✅ 
- Ca35_adopted.ens ✅
- K35_adopted.ens ✅
- P35_adopted.ens ✅
- S35_adopted.ens ✅ (no general comments)
- Si35_adopted.ens ✅

### Files Requiring Correction:
- **Mg35_adopted.ens** ❌ - Production section appears before discovery section
- **Na35_adopted.ens** ❌ - Production section appears before discovery section  
- **Ne35_adopted.ens** ❌ - Missing discovery and production sections

## Implementation Notes

1. Not all sections are required for every isotope - include only sections with available data
2. Maintain the prescribed order even if some intermediate sections are missing
3. Use consistent formatting for section headers
4. Each section should contain chronologically ordered references when possible
5. Theoretical calculations should always be the final general comment section

## Quality Assurance

Evaluators should verify section ordering during the review process. Any deviations from this standard must be corrected before final submission.

---
*Last updated: June 5, 2025*
