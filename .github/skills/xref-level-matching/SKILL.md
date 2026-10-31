---
name: xref-level-matching
description: >
  Use this skill to validate every XREF list in an ENSDF adopted dataset against the actual levels in the referenced individual datasets. Identifies inconsistencies in level matching. CHECK-ONLY — reports findings without editing files.
argument-hint: [adopted.ens] [dataset.ens]
---

# XREF Level Matching: Adopted vs. Dataset Levels

XREF syntax and record layout: `.github/agents/ENSDF-Agent.agent.md`. An XREF record indicates that the referenced datasets also contain the same nuclear level as the corresponding adopted level.

Trace each adopted level through its XREF labels to the referenced dataset's level (the `(energy)` qualifier locates it); if a label gives no energy and no `*`, pair levels one-to-one to the most likely candidate level, preferring Jπ-compatible levels and excluding levels already located by an energy.

Classify each adopted label and dataset level (cite by energy and Jπ, no line numbers).
 - Wrong match: `(energy)` locates a dataset level although a closer compatible one stays unpaired.
 - Missing match: an adopted label or dataset level stays unpaired.
 - Redundant match: several adopted levels locate one dataset level without `*`; `*` on a single adopted level; repeated label.
 - Mismatch: paired level with incompatible Jπ or energy beyond combined uncertainties.
 - Malformed label: blank within the XREF text, double qualifier, or undefined dataset symbol.
 - Otherwise: match.

