---
name: ensdf-header-setup
description: >
  Use this skill when preparing ENSDF files for a new mass chain evaluation
  cycle. Copies .old/.xundl files to new/, renames to .ens, creates the four
  standard folders (new/, old/, raw/, pdf/), updates the IDENTIFICATION
  record columns 66-80 to "ENSDF    YYYYMM", and inserts a new History (H)
  record.
argument-hint: [mass number] or [element symbol] or [file path]
---

# ENSDF File Identification and History Records Setup Workflow

## Purpose
Prepare `.old` and `.xundl` files for a new mass chain evaluation.

---

## Quick Start (for AI Agent)

```
1. Copy .old/.xundl → new/
2. Move .old/.xundl → old/
3. Rename in new/: .old/.xundl → .ens
4. Create raw/ and pdf/ folders
5. Update IDENTIFICATION record (line 1, cols 66-80)
6. Insert new History (H) record after IDENTIFICATION
```

---

## Folder Structure

```
El##/
├── new/    # Working .ens files
├── old/    # Original .old/.xundl (reference only)
├── raw/    # Raw data, figures, notes
└── pdf/    # Generated PDFs
```

---

## IDENTIFICATION and History Records

### IDENTIFICATION Record (Line 1)
- Cols 1-65: Dataset title and references (preserve unchanged)
- Cols 66-80: Replace with `ENSDF    YYYYMM` (e.g., `ENSDF    202609`)

### History (H) Record (Insert after IDENTIFICATION)
```
XXXXX  H TYP=FUL$AUT=LIJIE SUN AND JUN CHEN$CIT=ENSDF$CUT=30-Sep-2026$          
```
- Replace `XXXXX` with NUCID (e.g., ` 34AR`, ` 34CL`, ` 34S `)
- **Keep all existing H records unchanged below**

---

## Automated Workflow

### Step 1: Setup folders and copy files
```powershell
$mass = 34
$nuclides = @("Ne","Na","Mg","Al","Si","P","S","Cl","Ar","K","Ca")

foreach ($el in $nuclides) {
    $base = "D:\X\ND\ENSDF\A${mass}\${el}${mass}"
    @("new","old","raw","pdf") | ForEach-Object {
        if (!(Test-Path "$base\$_")) { New-Item -ItemType Directory -Path "$base\$_" -Force }
    }
    Get-ChildItem "$base\*.old","$base\*.xundl" -ErrorAction SilentlyContinue | ForEach-Object {
        Copy-Item $_.FullName "$base\new\"; Move-Item $_.FullName "$base\old\"
    }
    Get-ChildItem "$base\new\*.old","$base\new\*.xundl" -ErrorAction SilentlyContinue | 
        Rename-Item -NewName { $_.Name -replace '\.(old|xundl)$','.ens' }
}
```

### Step 2: Update headers
```powershell
python ".github\temp\update_headers.py" "D:\X\ND\ENSDF\A${mass}"
```

---

## Important Notes

1. **NEVER edit `.old` files** - reference copies only
2. **Preserve existing H records** - only INSERT new H record
3. **80-character lines** - all ENSDF records must be exactly 80 chars
4. **Validate**: `python .github/scripts/column_calibrate.py <file>`
