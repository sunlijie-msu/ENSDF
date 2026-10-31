---
name: xref-token-integrity
description: >
  Use this skill to validate every XREF token in an ENSDF adopted dataset against
  the actual level lists of the cited individual datasets. Detects phantom energies,
  fabricated levels, unmarked shared peaks, and malformed tokens.
  CHECK-ONLY — reports findings without editing files.
argument-hint: [adopted.ens] [dataset folder]
---

# XREF Token Integrity: Adopted vs. Dataset Levels

XREF syntax and record layout: `.github/agents/ENSDF-Agent.agent.md`. This skill adds the verification procedure: a token is a provenance claim, so the dataset must actually contain that level.

| # | Check (per token, after merging `XREF=`/`XREF+=`) | Failure |
|:--|:--|:--|
| 1 | One letter + optional `(...)`; no embedded spaces; order A–Z, a–z, `#` | malformed token |
| 2 | Parenthetical energy exists in that dataset (±2 keV) | phantom energy |
| 3 | Bare letter: a dataset level lies within max(10 keV, 2σ_combined) | fabricated level |
| 4 | Two adopted levels may share one dataset level only if every such token carries `*`; each `*` sits on ≥2 levels | unmarked ambiguity |
| 5 | Letter appears in the adopted key list (`XX...` header lines) | wrong letter |

Pitfalls: parse `E`-notation (`17.42E3` with DE 25 → ±250 keV); blank DE is not zero; integer-energy datasets need the 10 keV floor; report `file:line` for both sides.
