---
name: xref-label-update
description: >
  Use this skill when updating XREF labels in ENSDF adopted files after
  datasets are added or removed. Handles systematic label shifting and
  parenthetical notations such as (energy), (*), and (?).
argument-hint: [adopted.ens] [add|remove] [dataset-label]
---
# Update ENSDF Cross-Reference (XREF) Labels

ENSDF 80-column data record and field definitions, structural rules, column positions, and uncertainty notation: `.github/agents/ENSDF-Agent.agent.md`. Spot-check policy: `.github/copilot-instructions.md`.

## Scenario 1: Add Dataset(s)

Before editing, compare complete old/new X-record lists. Build one `old label → new label` map; use final positions, not sequential shifts. For multiple insertions, insert all new labels in one pass.

### Steps

#### 1. Update X-Records
Replace index with final X-record list. Pad each record to 80 characters.

#### 2. Alphabetically Shift Existing XREF Labels
Apply mapping — notations `(energy)`, `(*)`, `(?)` travel with their labels:
- `XREF=BFGH` → `XREF=BGHI`
- `XREF=BFG(2103)HIJ` → `XREF=BGH(2103)IJK`
- `XREF=F(*)J` → `XREF=G(*)K`
- `XREF=H(7300*)J` → `XREF=I(7300*)K`

#### 3. Insert New XREF Labels
Match each new dataset L-record to adopted levels before insertion. Insert labels alphabetically; use `Label(source-energy)` when source/adopted energies differ, and retain source `?`/`*` only when present in the source record:
- `XREF=ABCDGHIJK` → `XREF=ABCDFGHIJK`
- `XREF=ABCDFG` → `XREF=ABCDE(3326)FG`

## Scenario 2: Remove Dataset

Determine shift mapping (e.g., removed `B`: C→B, D→C, E→D, and so on; A unchanged).

### Steps

#### 1. Update X-Records
Remove dataset line, shift subsequent labels up, pad spaces to 80 characters.

#### 2. Shift XREF Labels
Apply mapping; delete removed label if present:
- `XREF=ABC` → `XREF=AB` (B removed; C→B)
- `XREF=ACD` → `XREF=ABC` (no B; C→B, D→C)
- `XREF=ACDEF(2420)GIK` → `XREF=ABCDE(2420)FHJ` (notations travel with labels)

## Scenario 3: Swap Two Adjacent Dataset Labels (e.g., G↔H)

**Key insight:** A bidirectional swap requires care — lines containing **both** labels are textually unchanged after the swap (set {G,H} → {H,G} = {G,H} in sorted order). Only lines containing one label but not the other need text changes.

### Steps

#### 1. Update X-Records
Swap the dataset descriptions on the two X-record lines (labels XG/XH stay; only the text content swaps).

#### 2. Identify XREF Lines That Actually Change
- **Both labels present** (e.g., `XREF=...GH...`): **no change needed** — sorted result is identical.
- **Only one label present** (e.g., `XREF=...G...` without H): change that label to its swap partner.
- Parenthetical notations `(energy)`, `(*)`, `(?)` travel with their label.

#### 3. Apply Changes
Example (swapping G↔H):
- `XREF=ACDEFGHIJK` → unchanged (both present)
- `XREF=ACDEF(2420)GIK` → `XREF=ACDEF(2420)HIK` (G→H, H absent)
- `XREF=ACEG(4474)JK` → `XREF=ACEH(4474)JK` (G→H, H absent)
- `XREF=FG(7520*)` → `XREF=FH(7520*)` (G→H, H absent)

**NEVER** apply G→H then H→G in two passes — this creates double-shifting. Identify all changes first, then apply atomically.

## Validation
Skip column calibrate and line ruler checks. Pad XREF line to 80 chars only.

**CRITICAL:** This task ONLY updates XREF labels. Do NOT modify data records. Human evaluators handle data editing separately.

## Spot-Check (Both Scenarios)

Verify 5%+ of XREF entries (at least 5):
- Shift mapping applied correctly; no double-shifting
- New label inserted or removed label deleted as needed
- Alphabetical label order preserved
- All XREF lines exactly 80 characters

## Implementation Pitfalls

**Continuation records:** Some L-records have `dL`, `2 L`, or similar continuation lines between the L-record and the XREF line. The `replace_string_in_file` context must include the continuation record; do not assume L-record directly precedes XREF.

**Repeated XREF content:** Adjacent levels can share identical XREF line content (e.g., doublet pairs). Use L-record + XREF + next-L-record context to identify each entry uniquely; avoid using the preceding XREF line as context since it may change in the same batch.

**Partial-run false flags:** After partial batch application, a shift-check script may falsely flag already-correct lines (e.g., the new L label caught again by an L→M rule). Verify remaining changes manually rather than re-running the full script output.
