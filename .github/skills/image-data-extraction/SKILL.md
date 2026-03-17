---
name: image-data-extraction
description: Extract nuclear level scheme and gamma transition data from images or PDF figures for ENSDF entry. Handles level identification, spin-parity assignment extraction, gamma energy extraction, level energy calculation from gamma cascades, ascending energy ordering, and ENSDF uncertainty notation. Mandatory 5% random spot-check validation against source image before claiming completion.
argument-hint: [image or PDF file] [target ENSDF file]
---

# Image/PDF Data Extraction Prompt Instructions

## CRITICAL EXECUTION RULES

**Pay extreme attention to row and column alignment. Pay extreme attention not to overlook blank cells.**

**Plan systematically, execute carefully, validate rigorously.** Never guess or assume—flag unclear values for clarification. Every decimal place, digit, and blank cell matters.

**Double-check everything at least twice before claiming completion.**

---

## EXTRACTION OBJECTIVES

Extract all numerical data and uncertainties with absolute fidelity to the source image. Preserve every decimal place exactly—do not round, omit, alter, or add digits. Example: 10.0 is 10.0, not 10 or 10.00!

---

## CRITICAL CHARACTER RECOGNITION

**Exercise extreme caution with mathematical symbols and notation:**

- **±** (plus-minus) vs **+** (plus) vs **−** (minus) — verify exact symbol
- **>** (greater than) vs **≥** (greater than or equal) — verify exact symbol
- **<** (less than) vs **≤** (less than or equal) — verify exact symbol
- **Decimal points** (.) must be preserved with exact digit counts
- **1** vs **l** vs **|** — verify character identity
- Ensure that every +/- sign absolutely matches the original image.

**When uncertain about any character, flag for manual verification rather than guessing.**

---

## CRITICAL ENSDF ORDERING REQUIREMENTS

**ALL level energies in ASCENDING order** (lowest to highest)  
**ALL gamma energies within each level in ASCENDING order** (lowest to highest)

ENSDF parsing systems require strict ascending energy order — one incorrectly ordered record causes file rejection.

---

## LEVEL SCHEME EXTRACTION PROTOCOLS

### Level Identification Standards

- **Horizontal bars represent nuclear levels** with definitive energy positions
- **Spin-parity assignments** appear on the LEFT side of each horizontal bar
- **Level energies** may be explicitly labeled or calculated from gamma transition sums
- **Ground state** typically positioned at bottom (0.0 keV) unless otherwise specified
- **Excited states** arranged vertically by increasing excitation energy

### Gamma Transition Extraction Rules

- **Vertical arrows indicate gamma transitions** connecting nuclear levels
- **Gamma energies** are labeled in the MIDDLE of each transition arrow
- **Transition direction**: Arrows point FROM higher energy TO lower energy levels
- **Multiple transitions**: Each arrow represents a single gamma-ray emission

### Level Energy Calculation Protocol

When level energies are not explicitly provided:

1. **Start from ground state** (0.0 keV reference point)
2. **Sum gamma energies** along cascade pathways from ground to excited states
3. **Verify consistency** across multiple pathways to same level
4. **Cross-validate** energy sums for internal consistency
5. **Report calculated energies** with appropriate precision based on gamma energy precision

### Spin-Parity Assignment Standards

- **(3/2⁻)** → tentative assignment
- **5/2⁺** → confirmed assignment
- **7/2⁺?** → uncertain assignment
- **[9/2⁻]** → theoretical prediction
- **(3/2⁻,5/2⁻)** → ambiguous assignment

---

## ENSDF UNCERTAINTY NOTATION

**ENSDF uses fixed 80-column format with 2-column uncertainty fields (1-2 digits maximum). 3-digit uncertainties corrupt adjacent fields!**

Uncertainty digits align with the rightmost decimal digit of the stated value:

| Decimal Digits | ENSDF Notation | Meaning |
|----------------|----------------|---------|
| No decimal | 1234(5) | 1234 ± 5 |
| No decimal | 1234(56) | 1234 ± 56 |
| 1 decimal | 12.3(4) | 12.3 ± 0.4 |
| 1 decimal | 12.3(45) | 12.3 ± 4.5 |
| 2 decimals | 1.23(4) | 1.23 ± 0.04 |
| 2 decimals | 1.23(45) | 1.23 ± 0.45 |

**CONSTRAINTS:**
- Maximum 2-digit uncertainties for DE, DRI, DCC, DTI, DS fields
- 3-digit uncertainties FORBIDDEN (corrupts 80-column format)
- Asymmetric uncertainties in DT, DMR fields use +X-Y format (up to 6 characters)

---

## COMPARATIVE DATA MARKERS

**GT/LT for limits:**
- `<1.6` → RI=`1.6`, uncertainty field=`LT`
- `>5.2` → RI=`5.2`, uncertainty field=`GT`

---

## VALIDATION CHECKLIST

**Energy Ordering:**
- Level energies: 0.0 < 58.1 < 127.6 < 143.7... (ascending)
- Gamma energies per level: 113.2 < 158.9 < 162.2... (ascending)

**Extraction Workflow:**
1. Identify nuclear levels (horizontal bars, bottom to top)
2. Extract spin-parity assignments (left-side labels)
3. Map gamma transitions (vertical arrows and energy labels)
4. Calculate level energies by summing gamma pathways when needed
5. Organize data in ascending energy order
6. Cross-validate energy balance across all pathways
7. Verify completeness of extracted data

**Random Spot-Check Protocol (MANDATORY):**
- After extraction completion, randomly select 5-10 data points (levels, gammas, or uncertainties)
- Cross-verify selected samples against original source image
- Check for transcription errors, misaligned columns, or overlooked values
- If discrepancies found, perform systematic re-check of entire dataset
- Document spot-check results before claiming extraction completion
