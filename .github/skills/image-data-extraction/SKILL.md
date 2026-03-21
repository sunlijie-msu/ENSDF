---
name: image-data-extraction
description: >
  Use this skill when extracting nuclear level scheme or gamma transition data
  from images, PDF figures, or level-scheme diagrams for ENSDF entry. Handles
  level identification, spin-parity extraction, gamma energy extraction, level
  energy calculation from gamma cascades, ascending energy ordering, and ENSDF
  uncertainty notation. Mandatory 15% random spot-check validation against the
  source image before claiming completion.
argument-hint: [image or PDF file] [target ENSDF file]
---

# Image and PDF Data Extraction

## Purpose

Extract nuclear level scheme and gamma transition data from images or PDF figures into ENSDF-formatted records.

## When to Use

- Extracting level energies and spin-parity assignments from level-scheme diagrams
- Reading gamma-ray energies and intensities from figure annotations
- Calculating level energies from gamma-ray cascade pathways
- Any image-to-ENSDF data transcription task

## Character Recognition

Exercise extreme caution with visually similar characters:

| Easily confused | Verify |
|:----------------|:-------|
| ± vs + vs − | Exact symbol |
| > vs ≥, < vs ≤ | Exact symbol |
| 1 vs l vs \| | Character identity |
| Decimal points | Exact digit count |

When uncertain about any character, flag for manual verification.

## Level Scheme Extraction

### Level Identification

- Horizontal bars represent nuclear levels with definitive energy positions
- Spin-parity assignments appear on the left side of each horizontal bar
- Ground state is typically at the bottom (0.0 keV)
- Excited states are arranged vertically by increasing excitation energy

### Gamma Transition Extraction

- Vertical arrows indicate gamma transitions connecting nuclear levels
- Gamma energies are labeled in the middle of each transition arrow
- Arrows point from higher energy to lower energy levels
- Each arrow represents a single gamma-ray emission

### Level Energy Calculation

When level energies are not explicitly provided:

1. Start from the ground state (0.0 keV reference point)
2. Sum gamma energies along cascade pathways
3. Verify consistency across multiple pathways to the same level
4. Cross-validate energy sums for internal consistency
5. Report calculated energies with precision matching the gamma energy precision

### Spin-Parity Notation

For full spin-parity rules, see `copilot-instructions.md` and the `spin-parity` skill.

## Energy Ordering

All level energies and gamma energies within each level must be in ascending order. See `copilot-instructions.md` Section 2 for the energy ordering requirement.

## Uncertainty Notation

For ENSDF uncertainty field rules (2-column maximum, GT/LT markers, scientific notation), see `copilot-instructions.md` Section 3.

## Validation Checklist

- [ ] Level energies in ascending order
- [ ] Gamma energies per level in ascending order
- [ ] All spin-parity assignments transcribed with exact parentheses
- [ ] Energy balance verified across all cascade pathways
- [ ] 15% random spot-check against source image completed

## Gotchas

- Level energies must always be in ascending order — one misordered record causes ENSDF file rejection
- AI models frequently misread subscripts/superscripts in low-resolution images — always cross-verify
- Decimal points can be confused with image artifacts — verify digit counts carefully
- When multiple pathways exist to the same level, energy sums may differ slightly due to rounding — flag discrepancies >1 keV
