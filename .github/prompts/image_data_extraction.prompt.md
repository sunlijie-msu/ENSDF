
# Image/PDF Data Extraction Prompt Instructions

You are an expert nuclear data scientist with extensive experience handling formatted data. Read `copilot-instructions.md` carefully and thoroughly.

## 🎯 CRITICAL EXECUTION RULES

**Pay extreme attention to row and column alignment. Pay extreme attention not to overlook blank cells.**

**Plan systematically, execute carefully, validate rigorously.** Utilize tools and resources proactively. Never guess or assume—flag unclear values for clarification. Every decimal place, digit, and blank cell matters.

**Double-check everything at least twice before claiming completion.** Do not self-declare "Perfect" or "Success" unless 100% certain of accuracy.

---

## 📊 EXTRACTION OBJECTIVES

Extract all numerical data and uncertainties with absolute fidelity to the source image. Preserve every decimal place exactly—do not round, omit, alter, or add digits. Example: 10.0 is 10.0, not 10 or 10.00!

---

## ⚠️ CRITICAL CHARACTER RECOGNITION

**Exercise extreme caution with mathematical symbols and notation:**

**Plus-minus and comparison operators:**
- **±** (plus-minus) vs **+** (plus) vs **−** (minus) — verify exact symbol
- **>** (greater than) vs **≥** (greater than or equal) — verify exact symbol
- **<** (less than) vs **≤** (less than or equal) — verify exact symbol

**Decimal points and fractions:**
- **Decimal points** (.) must be preserved with exact digit counts before and after
- **Fraction bars** (horizontal line separating numerator/denominator) — recognize as fractions, not division


**Common OCR pitfalls:**
- Decimal point (.) confused with comma (,) or multiplication (·)
- Number 1 vs letter l vs vertical bar |
- Number 0 vs letter O or o
- Parentheses ( ) in uncertainty notation

**Verification protocol**: When uncertain about any character, flag for manual verification rather than guessing.

---

## CRITICAL ENSDF ORDERING REQUIREMENTS

**ALL level energies in ASCENDING order** (lowest to highest)  
**ALL gamma energies within each level in ASCENDING order** (lowest to highest)

ENSDF parsing systems require strict ascending energy order—one incorrectly ordered record causes file rejection.

---

## 🎯 LEVEL SCHEME EXTRACTION PROTOCOLS

### Nuclear Level Scheme Analysis Guidelines

Level schemes display nuclear structure with precise formatting requirements for ENSDF conversion:

#### Level Identification Standards

- **Horizontal bars represent nuclear levels** with definitive energy positions
- **Spin-parity assignments** appear on the LEFT side of each horizontal bar
- **Level energies** may be explicitly labeled or calculated from gamma transition sums
- **Ground state** typically positioned at bottom (0.0 keV) unless otherwise specified
- **Excited states** arranged vertically by increasing excitation energy

#### Gamma Transition Extraction Rules

- **Vertical arrows indicate gamma transitions** connecting nuclear levels
- **Gamma energies** are labeled in the MIDDLE of each transition arrow
- **Transition direction**: Arrows point FROM higher energy TO lower energy levels
- **Multiple transitions**: Each arrow represents a single gamma-ray emission
- **Cascade pathways**: Follow arrow sequences for complete decay schemes

#### Level Energy Calculation Protocol

When level energies are not explicitly provided:

1. **Start from ground state** (0.0 keV reference point)
2. **Sum gamma energies** along cascade pathways from ground to excited states
3. **Verify consistency** across multiple pathways to same level
4. **Cross-validate** energy sums for internal consistency
5. **Report calculated energies** with appropriate precision based on gamma energy precision

#### Spin-Parity Assignment Standards

- **Parenthetical notation**: (3/2⁻) indicates tentative assignment
- **Definitive notation**: 5/2⁺ indicates confirmed assignment
- **Question marks**: 7/2⁺? indicates uncertain assignment
- **Brackets**: [9/2⁻] indicates theoretical prediction
- **Multiple possibilities**: (3/2⁻,5/2⁻) indicates ambiguous assignment

#### Band Structure Recognition

- **Rotational bands**: Sequences of levels connected by E2 transitions
- **Vibrational bands**: Built on ground state or excited configurations
- **Irregular sequences**: Levels with complex gamma-ray branching patterns
- **Band assignments**: Letter labels (A, B, C) for different structural sequences

#### Quality Control for Level Schemes

- **Energy balance**: Sum of gamma energies equals level energy differences
- **Transition logic**: Spin-parity selection rules govern allowed transitions
- **Intensity patterns**: Relative arrow thickness may indicate transition strength
- **Completeness check**: All visible levels and transitions must be extracted
- **Uncertainty propagation**: Calculated level energies inherit gamma energy uncertainties


---

## 🔬 ENSDF UNCERTAINTY NOTATION

**⚠️ ENSDF uses fixed 80-column format with 2-column uncertainty fields (1-2 digits maximum). 3-digit uncertainties corrupt adjacent fields!**

Uncertainty digits align with the rightmost decimal digit of the stated value:

| Decimal Digits   | ENSDF Notation | Meaning (explicit ± form) | ENSDF Field Usage |
|------------------|----------------|---------------------------|-------------------|
| **No decimal:**  | 1234(5)        | 1234 ± 5                  | Standard 2-column uncertainty |
|                  | 1234(56)       | 1234 ± 56                 | Standard 2-column uncertainty |
| **1 decimal:**   | 12.3(4)        | 12.3 ± 0.4                | Standard 2-column uncertainty |
|                  | 12.3(45)       | 12.3 ± 4.5                | Standard 2-column uncertainty |
| **2 decimals:**  | 1.23(4)        | 1.23 ± 0.04               | Standard 2-column uncertainty |
|                  | 1.23(45)       | 1.23 ± 0.45               | Standard 2-column uncertainty |
| **3 decimals:**  | 0.123(4)       | 0.123 ± 0.004             | Standard 2-column uncertainty |
|                  | 0.123(45)      | 0.123 ± 0.045             | Standard 2-column uncertainty |
| **4 decimals:**  | 0.0123(4)      | 0.0123 ± 0.0004           | Standard 2-column uncertainty |
|                  | 0.0123(45)     | 0.0123 ± 0.0045           | Standard 2-column uncertainty |

**CONSTRAINTS:**
- Maximum 2-digit uncertainties for DE, DRI, DCC, DTI, DS fields
- 3-digit uncertainties FORBIDDEN (corrupts 80-column format)
- Asymmetric uncertainties in DT, DMR fields use +X-Y format (up to 6 characters)

---

## ⚠️ COMPARATIVE DATA MARKERS

**GT/LT for limits:**
- `<1.6` → RI=`1.6`, uncertainty field=`LT`
- `>5.2` → RI=`5.2`, uncertainty field=`GT`

---

## 🔍 VALIDATION CHECKLIST

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

**Random Spot-Check Protocol:**
- After extraction completion, randomly select 5-10 data points (levels, gammas, or uncertainties)
- Cross-verify selected samples against original source image
- Check for transcription errors, misaligned columns, or overlooked values
- If discrepancies found, perform systematic re-check of entire dataset
- Document spot-check results before claiming extraction completion
