---
name: xref-label-update
description: >
  Use this skill when updating cross-reference (XREF) labels in ENSDF
  adopted files after experimental datasets are added or removed. Handles
  systematic label shifting, new label insertion, deleted label removal,
  and preserves parenthetical notations such as (energy), (*), and (?).
  Covers both add-dataset and remove-dataset scenarios with 5%+ spot-check
  validation.
argument-hint: [adopted.ens] [add|remove] [dataset-label]
---

# Update ENSDF Cross-Reference (XREF) Labels

ENSDF 80-column data record and field definitions, structural rules, column positions, uncertainty notation, and spot-check policy: `.github/copilot-instructions.md`.

## Task Overview

Update cross-reference labels in ENSDF adopted file when experimental datasets are added or removed, causing existing dataset labels to shift.

## Scenario 1: Add Dataset

### Input
1. **File**: `[path/to/adopted.ens]`
2. **New dataset**: `[X]` = `[description]`
3. **Mapping**: e.g., assume [X]=`F`: F→G, G→H, H→I, I→J, J→K (A-E unchanged)

### Steps

#### 1. Update X-Records
Insert new dataset at appropriate position, shift subsequent labels, pad spaces to 80 characters.

#### 2. Alphabetically Shift Existing XREF Labels
Apply mapping — notations (energy), (asterisk), (question mark), (energy asterisk), (energy question) shift naturally with labels:
- `XREF=F` → `XREF=G`
- `XREF=BFGH` → `XREF=BGHI`
- `XREF=BFG(2103)HIJ` → `XREF=BGH(2103)IJK`
- `XREF=F(*)J` → `XREF=G(*)K`
- `XREF=H(7300*)J` → `XREF=I(7300*)K`

#### 3. Insert New XREF Label
For levels in new dataset, insert label alphabetically (no (notations) needed):
- `XREF=ABCDGHIJK` → `XREF=ABCDFGHIJK`
- `XREF=BGH(2103)IJK` → `XREF=BFGH(2103)IJK`

Omit column calibrate and line ruler checks. Only pad XREF line to 80 characters with spaces.

#### 4. Spot-Check
Verify randomly-selected 5%+ of XREF entries (at least 5):
- Check shift mapping applied correctly
- Verify new label inserted where needed
- Confirm alphabetical order
- Ensure all lines exactly 80 characters

### Example
```
New: XF = 9BE(37CA,34ARG)
Mapping: F→G, G→H, H→I, I→J, J→K (A-E unchanged)

Shift:
XREF=ABDFG(2103)HIJ → XREF=ABDGH(2103)IJK

Insert F for levels also existing in F dataset:
XREF=ABDGH(2103)IJK → XREF=ABDFGH(2103)IJK
```

## Scenario 2: Remove Dataset

### Input
1. **File**: `[path/to/adopted.ens]`
2. **Removed dataset**: `[X]` = `[description]`
3. **Mapping**: e.g., removed `B`: C→B, D→C, E→D, F→E, G→F, etc. (A unchanged)

### Steps

#### 1. Update X-Records
Remove dataset line, shift subsequent labels up, pad spaces to 80 characters.

#### 2. Shift XREF Labels
Apply shift mapping to each label present. Delete removed label (B) if present.

Examples:
- `XREF=ABC` → `XREF=AB` (had B, removed B, C→B)
- `XREF=ACD` → `XREF=ABC` (no B, just shift C→B, D→C)
- `XREF=C` → `XREF=B` (shift C→B)
- `XREF=ACDEFGH` → `XREF=ABCDEFG` (no B, shift all)
- `XREF=ACDEF(2420)GIK` → `XREF=ABCDE(2420)FHJ` (notations shift with labels)
- `XREF=FG(7520*)` → `XREF=EF(7520*)` (notations preserved)

#### 3. Validation
Omit column calibrate and line ruler checks. Only pad XREF line to 80 characters with spaces.

**CRITICAL:** This task ONLY updates XREF labels. Do NOT delete any data records (L-records, G-records, comment lines). Human evaluators handle data removal separately.

#### 4. Spot-Check
Verify randomly-selected 5%+ of XREF entries (at least 5):
- Check shift mapping applied correctly
- Verify removed label deleted where present
- Confirm alphabetical order
- Ensure all lines exactly 80 characters

### Example
```
Removed: XB = 36SI B-N DECAY (503 MS)
Mapping: C→B, D→C, E→D, F→E, G→F, H→G, I→H, J→I, K→J, L→K (A unchanged)

Original XREF:
XREF=ABCDE → XREF=ABDE (B removed, D→C, E→D)
XREF=ADEFG(2420)HIJ → XREF=ACDEF(2420)GHI (no B, shift down)
```

## Success Criteria (Both Scenarios)
- ✅ X-records updated (inserted/removed + shifted)
- ✅ XREF labels shifted per mapping
- ✅ New label inserted OR removed label deleted
- ✅ All lines 80 characters
- ✅ Spot-check passes (5%+ samples, minimum 5)
