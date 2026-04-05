---
name: value-occurrence-check
description: >
  Use this skill when checking consistency of nuclear level energies across
  multiple occurrences in a gamma-ray transition CSV table. Verifies that
  energy, uncertainty, and J-π are identical wherever a level appears as
  both an initial (Ei) and final (Ef) state. Mandates explicit column
  mapping including blank cells and bidirectional forward/backward
  verification.
argument-hint: [CSV or table file]
---

# Value Occurrence Check

ENSDF 80-column data record and field definitions, structural rules, column positions, uncertainty notation, and spot-check policy: `.github/copilot-instructions.md`.

## Purpose

Verify that every nuclear level energy appearing multiple times in a gamma-ray transition table has consistent energy, uncertainty, and J-π across all occurrences.

## When to Use

- Before entering CSV table data into ENSDF records
- When a gamma-ray transition table lists levels as both initial (Ei) and final (Ef) states
- To catch transcription errors or inconsistent J-π assignments across table entries

## Method

### Step 1: Column Mapping

Follow the bidirectional column mapping protocol from `copilot-instructions.md` Section 5:

1. List all header columns explicitly, including blank positions
2. Count blank cells as positional placeholders
3. Forward verification: header → data
4. Backward verification: data → header

### Step 2: Occurrence Scan

For every unique level energy in the table:

1. Collect all rows where it appears as Ei or Ef
2. Compare energy value character-for-character across occurrences
3. Compare uncertainty character-for-character
4. Compare J-π character-for-character

### Step 3: Report Inconsistencies

For each mismatch:

```
LEVEL: 1175.3 keV
  Row 7:  Ef=1175.3(1), Jπf=5/2-     ✓
  Row 26: Ei=1175.3(1), Jπi=5/2-     ✓
  Row 49: Ei=1175.3(2), Jπi=5/2-     ✗ uncertainty mismatch (1 vs 2)
```

### Step 4: Validate Completeness

- Ground state (0 keV) appears only as Ef
- Every level energy has been checked
- 100% of occurrences verified before claiming completion

## Data Fidelity

Preserve every decimal place exactly — do not round, omit, alter, or add digits. 10.0 remains 10.0, not 10 or 10.00. See `copilot-instructions.md` Section 4 for numerical exactness rules.

## Gotchas

- Blank cells are the primary cause of misaligned column mapping — count them meticulously
- AI models frequently fail at lower-right table corners — apply extra scrutiny there
- Forward-only counting leads to off-by-one errors — always verify bidirectionally
