---
name: xref-level-matching
description: >
  Use this skill to validate every XREF list in an ENSDF adopted dataset against
  the actual levels in the referenced individual datasets. Identifies inconsistencies in level matching. CHECK-ONLY — reports findings without editing files.
argument-hint: [adopted.ens] [dataset.ens]
---

# XREF Level Matching: Adopted vs. Dataset Levels

XREF syntax and record layout: `.github/agents/ENSDF-Agent.agent.md`. An XREF record indicates that the referenced datasets also contain the same nuclear level as the corresponding adopted level.

Trace level by level: each adopted level, through its XREF labels (located by the label energy when given), to the cited dataset's level; assign levels globally one-to-one by energy and Jπ, never by nearest energy.

Report per adopted level (energy, Jπ; no line numbers): match; mismatch (energy or Jπ inconsistent); wrong match (a better dataset level exists); missing match (label without level, or level without label); redundant match (level claimed by several adopted levels without `*`).

