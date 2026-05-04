---
name: flag-expansion
description: >
  Use this skill when expanding flags in column 77 or flags in FLAG= continuation records in ENSDF files into individual cG or cL comment lines. Maps each flag character to its defined description in the dataset header. Clears column 77 flag characters from data records or deletes original FLAG= continuation lines after expansion.
argument-hint: [ENSDF file]
---

# ENSDF Flag Expansion (Generalized)

ENSDF 80-column data record and field definitions, structural rules, column positions, uncertainty notation, and spot-check policy: `.github/copilot-instructions.md`.

## 1. Objective
Systematically expand flags in column 77 or flags in `FLAG=` continuation records into individual `cG` or `cL` comments. The purpose is human review; **redundant comments are acceptable** — always add the new comment, even if a similar comment already exists.

## 2. Execution Procedure

### Step 1: Identify flags and their comment mappings
- Read the dataset header to find all flag definitions (e.g., colunn 77 or  `FLAG=A means E from ...`).
- Confirm which flags actually have occurrences: `grep 'FLAG=' file.ens`. Skip flags with zero occurrences.
- Locate all records with flag characters in column 77 or`FLAG=` continuation lines.

### Step 2: Expand — unconditionally
For **every** occurrence of a FLAG= line, **always**:
1. Add the new `cG`/`cL` comment immediately after the parent data record (before its existing comments).
2. Delete the `FLAG=` continuation line.

**Never suppress comment insertion** because a similar or related comment already exists. The expanded comments are for human review; the evaluator decides which to keep eventually.

**Comment ordering** (G-records): `E$ → RI$ → M$ → MR$`  
Insert new comments in the correct position relative to existing comment blocks — not blindly at the position of the deleted FLAG= line.

### Step 3: Handle multiple flags on the same record atomically
When a record has multiple `FLAG=` lines (e.g., `FLAG=A` and `FLAG=B`), generate a **single combined replacement** spanning all FLAG= lines. Generating independent ops per flag causes context exhaustion: after the first op removes its FLAG= line, the second op cannot find its original context.

If independent ops have already been generated and some fail, update the failed op's context to use post-expansion anchors (e.g., the comment line just added by the first op).

### Step 4: Verify
- Confirm 0 `FLAG=` lines remain in the file.
- For each expanded record, check the expected comment lines are present within that record's comment block (not the adjacent record's block — stop the search at the next data record).
- Count totals per comment type against expected numbers.
- Comment line spot-checks: compare with `line.rstrip() == expected_bare_string` (no `.ljust(80)` — comment lines do not need to be exactly 80 chars).

---