---
name: small-data-entry
description: >
  Use this skill for one 1964Gl04 resonance table at a time, matching direct
  resonance decays to an ENSDF adopted file by Ep(lab) and validating the
  resulting G-record or cG comment entries.
argument-hint: [SOURCE_TABLE TARGET_FILE]
---

# Small Data Entry

ENSDF 80-column data record and field definitions, structural rules, column positions, and uncertainty notation: `.github/agents/ENSDF-Agent.agent.md`. Spot-check policy: `.github/copilot-instructions.md`.

## When
Use this skill for a single resonance table from 1964Gl04 or an equivalent small one-table data entry pass.

## Goal
- Read the source table and match by `E_p(lab)` in the `S` field.
- Enter only direct resonance transitions labeled `(r) -> final level`.
- Exclude secondary decays unless explicitly requested.
- Exclude ambiguous rows unless explicitly requested.

## Core rules

For each included row:
1. Convert `E_gamma` and its uncertainty from MeV to keV exactly.
2. Find the matching final level in the adopted file.
3. Match the transition to an existing `G` record if possible.

If a matching `G` record exists:
- Do not overwrite existing `G` record energy or intensity fields.
- Add the 1964Gl04 intensity to `cG RI$other:`.
- Add `cG E$other:` only if 1964Gl04 gives an explicit `E_gamma` uncertainty.
- Keep comment order: `E$`, then `RI$`, then general comments.

If no matching `G` record exists:
- Insert a new `G` record in ascending energy order.
- Enter `E`, `DE`, `RI`, and `DRI` from 1964Gl04.
- Put `?` in column 80.
- Add `cG E,RI$from 1964Gl04...` for the new transition.
- Do not add `cG E$other:` or `cG RI$other:` for the same 1964Gl04 source values, because they are already primary in the new `G` record.

## Comment templates

```text
cG E$other: 3070 {I30} (1964Gl04)
cG RI$other: 8 {I2} (1964Gl04)
cG RI$other: 6.6 (1983Wa27), 8 {I2} (1964Gl04)
cG E,RI$from 1964Gl04, but not observed in later work.
```

## Safeguards
- Never shift unrelated fields.
- Never move the `T1/2` field or subsequent columns when editing `L` records.
- Keep all data records exactly 80 characters.
- Keep the leading blank in column 1.
- Preserve ascending gamma order within the level block.

## Validation
For each new or changed data record:

```powershell
python .github/scripts/ensdf_1line_ruler.py --line "<exact 80-char line>"
```

After the block update:

```powershell
python .github/scripts/column_calibrate.py "<target-file>"
python .github/scripts/check_gamma_ordering.py "<target-file>"
```

For multi-row data-entry passes, also do both QA checks before closing:
1. Bidirectional mapping check
   - Count all direct `(r) -> level` source rows.
   - Count all mapped target transitions.
   - Confirm the counts match and that each target transition maps back to one source row.
2. Random spot check
   - Use a reproducible random sample.
   - Minimum 5 samples.
   - Verify source value, uncertainty, and target ENSDF entry for every sampled item.

## Done when
- Only `(r) -> final level` transitions were entered.
- Every 1964Gl04 intensity for an existing `G` record appears in `cG RI$other:`.
- Every 1964Gl04 energy with an explicit uncertainty for an existing `G` record appears in `cG E$other:`.
- Every missing transition was added as a new `G` record with `?` in column 80 and `cG E,RI$from 1964Gl04...`.
- Validation passes.
- Bidirectional mapping check passes.
- Random spot check passes with 100% success.
