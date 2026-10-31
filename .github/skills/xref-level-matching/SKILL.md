---
name: xref-level-matching
description: >
  Use this skill to generate the level-by-level matching table between an ENSDF adopted dataset and the individual datasets referenced by its XREF labels, and to identify possible mismatches in level matching. CHECK-ONLY — reports findings without editing files.
argument-hint: [adopted.ens] [dataset.ens ...]
---

# XREF Level Matching: Adopted vs. Dataset Levels

XREF syntax and record layout: `.github/agents/ENSDF-Agent.agent.md`. An XREF record indicates that the referenced datasets also contain the same nuclear level as the corresponding adopted level.

Trace each adopted level through its XREF labels (`-(…)` cites every dataset except those listed) to the referenced dataset's level (the `(energy)` qualifier locates it); if a label gives no energy and no `*`, pair levels one-to-one to the most likely candidate level, preferring Jπ-compatible levels and excluding levels already located by an energy.

Classify each adopted label and dataset level (cite by energy and Jπ, no line numbers).
 - Wrong match: `X(energy)` names a dataset X level although a compatible level closer to the adopted energy matches no adopted level.
 - Missing match: an adopted label or dataset level stays unpaired (a wrong match always leaves a dataset level unpaired; report both).
 - Redundant match: several adopted levels locate one dataset level without `*`; `*` on a single adopted level; repeated label.
 - Mismatch: paired level with incompatible Jπ (state whether an adopted comment notes it) or energy beyond combined uncertainties.
 - Malformed label: blank within the XREF text, double qualifier, or undefined dataset symbol.
 - Otherwise: match.

Output the level-by-level matching table: one row per adopted level and per unpaired dataset level (energy, Jπ, XREF label, counterpart energy, Jπ, class). 

