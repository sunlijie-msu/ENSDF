# ENSDF Field Alignment Fix - Reconstruction Strategy

**Date**: 2025-10-06  
**Target File**: `Cl35_34s_p_g.ens` (2432 lines, 1108 G-records)

## Problem Summary

Fixed two critical ENSDF G-record field positioning issues:
1. **RI field**: 1075 G-records had RI starting at column 22 instead of 23 (missing separator space)
2. **M field**: 58 G-records had M starting at column 32 instead of 33 (missing separator space)

## The ONLY Correct Solution: Line Reconstruction Strategy

### Core Principle
**NEVER use insert/remove approach** - it either shifts all subsequent fields or corrupts adjacent field data.

**ALWAYS use reconstruction** - extract field content from current position, rebuild line with correct spacing.

### Generic Template
```python
# For field that should be at columns START_COL to END_COL
# But currently starts at (START_COL - 1) due to missing separator

# STEP 1: Extract parts
part1 = line[:START_COL-2]          # Everything BEFORE separator (cols 1 to START_COL-2)
part2 = ' '                         # Separator space at column START_COL-1
part3 = line[START_COL-2:START_COL-2+FIELD_LEN]  # Field content from current position
part4 = line[START_COL-1+FIELD_LEN:]             # Everything AFTER field (UNCHANGED!)

# STEP 2: Reconstruct
fixed_line = part1 + part2 + part3 + part4

# STEP 3: Pad/trim to 80 chars, add newline
fixed_line = fixed_line[:80].ljust(80) + '\n'
```

### Critical Index Calculations
- **Column N in ENSDF docs** = **Index N-1 in Python** (0-based indexing)
- **part1 endpoint**: `START_COL-2` (last char before separator position)
- **part3 start**: `START_COL-2` (where field currently starts)
- **part3 end**: `START_COL-2+FIELD_LEN` (extract exact field length)
- **part4 start**: `START_COL-1+FIELD_LEN` (CRITICAL: preserves all subsequent fields)

### Why part4 Must Start at (START_COL-1+FIELD_LEN)
```
Original line structure (WRONG - missing space):
  Cols: ...21|22 23 24 25 26 27 28|29 30 31...
  Data: ...  |R  I  _  V  A  L  U  |E  D  R...
           ↑ Should be space but has 'R'

After inserting space at col 22 (index 21), field content shifts:
  New:  ...  | _ R  I  _  V  A  L  |U  E  D  R...
           ↑ Space inserted
           
To preserve "D R..." at original position (col 30+):
  part4 must start at index 29 (col 30)
  
Formula: START_COL-1+FIELD_LEN = 23-1+7 = 29 ✓
```

## Applied Fixes

### RI Field Fix (Columns 23-29, 7 characters)
- **Missing separator**: Column 22
- **Field length**: 7 characters (columns 23-29)
- **Records affected**: 1075 G-records

```python
part1 = line[:21]      # Cols 1-21 (indices 0-20)
part2 = ' '            # Col 22 (index 21) - SEPARATOR SPACE
part3 = line[21:28]    # Cols 22-28 → 23-29 (7 chars: RI content)
part4 = line[29:]      # Cols 30+ (DRI, M, MR, C, Q UNCHANGED)
```

**Index verification**:
- part1: `[:21]` = chars at indices 0-20 = columns 1-21 ✓
- part2: Single space at column 22 ✓
- part3: `[21:28]` = 7 chars from indices 21-27 = current cols 22-28 ✓
- part4: `[29:]` = indices 29+ = columns 30+ (DRI field starts at col 30) ✓

### M Field Fix (Columns 33-41, 9 characters)
- **Missing separator**: Column 32
- **Field length**: 9 characters (columns 33-41)
- **Records affected**: 58 G-records

```python
part1 = line[:31]      # Cols 1-31 (indices 0-30) - includes DRI field
part2 = ' '            # Col 32 (index 31) - SEPARATOR SPACE
part3 = line[31:40]    # Cols 32-40 → 33-41 (9 chars: M content)
part4 = line[41:]      # Cols 42+ (MR, DMR, CC, TI, C, Q UNCHANGED)
```

**Index verification**:
- part1: `[:31]` = chars at indices 0-30 = columns 1-31 ✓
- part2: Single space at column 32 ✓
- part3: `[31:40]` = 9 chars from indices 31-39 = current cols 32-40 ✓
- part4: `[41:]` = indices 41+ = columns 42+ (MR field starts at col 42) ✓

## Failed Approaches (DO NOT USE - ARCHIVED FOR LEARNING)

### Approach 1: Insert Space + Remove Trailing Character
**File**: `fix_ri_alignment.py` (FAILED)

**Logic**: Insert space at col 22, remove character at end of line to maintain 80-char length

**Problem**: Shifts ALL subsequent fields (DRI, M, MR, C, Q) right by 1 column

**Why it fails**:
```
Original: ...E|RIVALUE|D M1+E2   0.42 ... C S
Insert @22: ...E| RIVALUE|D M1+E2   0.42 ... C S (81 chars)
Remove @80: ...E| RIVALUE|D M1+E2   0.42 ... C   (80 chars - lost 'S'!)
                      ↑         ↑
               RI now correct, but DRI shifted from col 30 to col 31!
```

### Approach 2-3: Insert Space + Remove Compensating Character at Index 29/31/32
**Files**: `fix_ri_alignment_correct.py` (FAILED multiple times)

**Logic**: Insert space at col 22, remove character at various positions to prevent shifting

**Problem**: Corrupted adjacent field data (deleted 'L' from 'LT', digits from '10', etc.)

**Why it fails**:
```
Original: ...E|RIVALUE| LT M1+E2...
Insert @22: ...E| RIVALUE| LT M1+E2... (81 chars)
Remove @29: ...E| RIVALUE|LT M1+E2...  (80 chars - deleted space from DRI!)
Remove @31: ...E| RIVALUE| T M1+E2...  (80 chars - deleted 'L' from 'LT'!)
```

**Correct diagnosis**: The problem isn't about WHERE to remove - it's that removing ANY character from existing fields corrupts data!

## Scripts in This Archive

### Diagnostic Tools
- **scan_ri_col22.py**: Finds G-records where column 22 != space (RI misalignment)
- **scan_m_col33.py**: Finds G-records where column 32 != space (M misalignment)

### Failed Fixes (Learning Reference)
- **fix_ri_alignment.py**: Insert/remove trailing char approach - shifts all fields
- **fix_ri_alignment_correct.py**: Insert/remove compensating char approach - corrupts data

### Successful Fixes
- **fix_ri_truly_correct.py**: RI field reconstruction - 1075 records fixed ✓
- **fix_m_field_alignment.py**: M field reconstruction - 58 records fixed ✓

## Validation Results

**After RI Fix**:
```
RI field positioning errors: 0
DRI field: All correct
M field: All correct
MR field: All correct
```

**After M Fix**:
```
M field positioning errors: 0
All multipolarity values correctly LEFT-JUSTIFIED at column 33
MR field: All correct
All subsequent fields preserved
```

## Critical Lessons Learned

1. **NEVER use insert/remove approach** for fixed-width format field repositioning
2. **Reconstruction is the ONLY safe method** - extract, reposition, preserve rest
3. **Don't trust validation tools blindly** - manually verify with custom diagnostic scans
4. **Archive ALL attempts** (successes AND failures) for learning reference
5. **part4 start index calculation is CRITICAL** - off-by-one errors corrupt adjacent fields
6. **Verify immediately after each fix** with custom scan before claiming success
7. **Field preservation is non-negotiable** - subsequent fields must remain at original positions

## Future Applications

Use this reconstruction strategy for ANY ENSDF field repositioning task:

1. **Identify the problem**: Which field is at wrong column?
2. **Create diagnostic scan**: `scan_[field]_col[N].py` to quantify issues
3. **Calculate indices precisely**:
   - part1: Everything before separator
   - part2: Separator space
   - part3: Field content from CURRENT position
   - part4: Everything after field from ORIGINAL position
4. **Implement with dry-run validation**
5. **Test with manual scan before applying**
6. **Verify field preservation with spot-checks**
7. **Archive scripts to legacy folder**

## Contact & Maintenance

This archive documents the field alignment fix process for ENSDF G-records in Cl35_34s_p_g.ens (2025-10-06).

**Reconstruction strategy is the DEFINITIVE solution** - all future field positioning fixes should follow this pattern.
