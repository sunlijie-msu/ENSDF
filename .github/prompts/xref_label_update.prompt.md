# Update ENSDF Cross-Reference (XREF) Labels

## Task Overview

Update cross-reference labels in ENSDF adopted file when a new experimental dataset is added, causing existing dataset labels to shift.

## Input
1. **File**: `[path/to/adopted.ens]`
2. **New dataset**: `[X]` = `[description]`
3. **Mapping**: e.g., assume [X]=`F`: F→G, G→H, H→I, I→J, J→K (A-E unchanged)

## Steps

### 1. Update X-Records
Insert new dataset, shift subsequent labels, pad spaces to 80 characters.

### 2. Shift Existing XREF Labels
Apply mapping - notations shift automatically with labels:
- `XREF=F` → `XREF=G`
- `XREF=BFGH` → `XREF=BGHI`
- `XREF=BFG(2103)HIJ` → `XREF=BGH(2103)IJK`
- `XREF=F(*)J` → `XREF=G(*)K`
- `XREF=H(7300*)J` → `XREF=I(7300*)K`

### 3. Insert New Label
For levels in new dataset, insert label alphabetically (no energy notation):
- `XREF=ABCDGHIJK` → `XREF=ABCDFGHIJK`
- `XREF=BGH(2103)IJK` → `XREF=BFGH(2103)IJK`

Pad XREF line to 80 characters.

### 4. Spot-Check
Verify randomly-selected 5%+ of XREF entries (at least 3):
- Check label maps to correct dataset
- Confirm alphabetical order

## Success Criteria
- ✅ X-records updated (new + shifted)
- ✅ XREF labels shifted per mapping
- ✅ New label inserted where needed
- ✅ All lines 80 characters
- ✅ Spot-check passes

## Example
```
New: XF = 9BE(37CA,34ARG)
Mapping: F→G, G→H, H→I, I→J, J→K (A-E unchanged)

Shift:
XREF=ABDFG(2103)HIJ → XREF=ABDGH(2103)IJK

Insert F for levels also existing in F dataset:
XREF=ABDGH(2103)IJK → XREF=ABDFGH(2103)IJK
```
