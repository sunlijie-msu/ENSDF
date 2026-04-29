---
name: ri-100-average-revision
description: >
  Use this skill when reviewing RI=100 gamma transitions in ENSDF adopted
  files. Replaces unnecessary RI=100 averaging with source adoption from the most
  precise dataset, updates G-record RI/DRI when needed, rewrites cG RI$
  comments, and validates the result.
argument-hint: [adopted.ens]
---

# RI=100 Average Revision in Adopted ENSDF Files
ENSDF 80-column data record and field definitions, structural rules, column positions, uncertainty notation, and spot-check policy: `.github/copilot-instructions.md`.

## Use When
- A `cG RI$` comment averages multiple RI=100 values
- Multiple datasets normalize the same gamma to 100 and one source must be adopted
- The adopted G-record `RI`/`DRI` may need to follow a single source instead of an unnecessary average

## Core Rule
RI=100 values are normalization references, not just normal intensities. Do **not** average them. Choose one source by comparing **absolute uncertainties implied by ENSDF notation**, not raw `{I...}` digits.

## Workflow
1. Find G records with `RI=100`, `100.0`, or `100.00` whose `cG RI$` comment uses weighted or unweighted averaging.
2. Extract every quoted RI source and convert each uncertainty to its absolute value from ENSDF last-digit notation.
3. Adopt the source with the smallest absolute uncertainty. If the G-record `RI` precision or `DRI` reflects averaging rather than that source, update the fields to match the adopted source.
4. Rewrite the `cG RI$` block as `from SOURCE.` plus `Other:` or `Others:` for the remaining datasets.
5. Preserve comment order: `cG E$` -> `cG RI$` -> `cG M$` -> `cG MR$` -> other identifiers.
6. Validate each changed G record with `ensdf_1line_ruler.py`, then run file-level validation.

## Decision Notes
- If only one dataset quotes RI=100, no special handling is needed.
- If two sources have equal absolute uncertainty, rewrite the `cG RI$` block as `from SOURCE1 and SOURCE2`.
- If the task edits only comments, skip ruler and column validation only when no G-record field changes are made.

## Completion Criteria
- No `cG RI$` comment averages RI=100 values.
- Each RI=100 case cites one adopted source and lists the remaining sources as alternates.
- Any changed G-record `RI`/`DRI` fields match the adopted source.
- Targeted RI=100 checks and file-level validation pass.