---
name: general-comments-ordering
description: "Organizes general comment sections in Adopted Dataset ENSDF files in the canonical sequence: Isotope Discovery, Production, Decay Measurements, Radius, Mass, Theoretical Calculations. Use when adding or reorganizing general comments at the beginning of an Adopted dataset file."
---

# Adopted Dataset Comments Ordering

ENSDF 80-column data record and field definitions, structural rules, column positions, and uncertainty notation: `.github/agents/ENSDF-Agent.agent.md`. Spot-check policy: `.github/copilot-instructions.md`.

## Canonical Sequence

Arrange general comments (non-record-specific) at the top of the Adopted Dataset file after Q-value comments and before any record-specific general comments. Follow this order:

1. **Isotope Discovery** — experimental details, discovery references
2. **Production** — methods and reaction studies
3. **Decay Measurements** — half-life, decay modes, branching ratios
4. **Radius Measurement** — nuclear radius determinations
5. **Mass Measurements** — mass spectrometry, Q-values, binding energy
6. **Theoretical Calculations** — nuclear structure calculations, shell model, etc. Prioritize works from the most recent years that calculated energy levels or level energies, spins (J), parities (π), and transition probabilities for this specific isotope.


**Within each section:** Group comments by NSR reference (Reverse-chronological order by key number).

---
