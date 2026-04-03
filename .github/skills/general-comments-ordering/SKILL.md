---
name: adopted-comments-ordering
description: "Organizes general comment sections in Adopted Dataset ENSDF files in the canonical sequence: Isotope Discovery, Production, Decay Measurements, Radius, Mass, Theoretical Calculations. Use when adding or reorganizing general comments at the beginning of an Adopted dataset file."
---

# Adopted Dataset Comments Ordering

## Canonical Sequence

Arrange general comments (non-record-specific) at the Adopted Dataset file start in this order:

1. **Isotope Discovery** — experimental details, discovery references
2. **Production** — methods and reaction studies
3. **Decay Measurements** — half-life, decay modes, branching ratios
4. **Radius Measurement** — nuclear radius determinations
5. **Mass Measurements** — mass spectrometry, Q-values, binding energy
6. **Theoretical Calculations** — nuclear models, predictions (always last)

**Rationale:** Empirical observations first (discovery → production → decay), then structural measurements (radius/mass), then theory. Readers encounter data before interpretation.

**Within each section:** Group comments by NSR reference (Reverse-chronological order by key number).

---
