---
description: Run the ens2pdf.py Python wrapper to convert ENSDF .ens files to PDF using the McMaster-MSU Java NDS tool. Supports single files, element-level batches, and glob patterns. Optionally opens the result.
name: ens2pdf
argument-hint: "File name, element symbol, or glob pattern (e.g. Si35_adopted, Si, Si35_*sig)"
mode: ask
---

Convert ENSDF `.ens` files to PDF using the `ens2pdf.py` Python wrapper script.

## Usage

Provide this command for the requested conversion pattern:

```bash
# Convert single file by name
python .github/scripts/ens2pdf.py Si35_adopted

# Convert with full file path
python .github/scripts/ens2pdf.py "finished/Si35/new/Si35_adopted.ens"

# Convert all files for an element
python .github/scripts/ens2pdf.py Si

# Convert files matching pattern
python .github/scripts/ens2pdf.py "Si35_*sig"

# Convert and open in VS Code (default)
python .github/scripts/ens2pdf.py Si35_adopted --open

# Convert and open in system viewer
python .github/scripts/ens2pdf.py Si35_adopted --open --system
```

#### PDF Generation

```powershell
# Single element
Set-Location "D:\X\ND\Files"
$element = "Al"
Get-ChildItem "D:\X\ND\A35\finished\${element}35\new\*.ens" | ForEach-Object {
    java -jar "D:\X\ND\McMaster-MSU-Java-NDS\McMaster_MSU_JAVA_NDS_v3.0_01May2025.jar" $_.FullName "$($_.BaseName).pdf"
}

# All elements
$elements = @("Al", "Ar", "Ca", "K", "Mg", "Na", "Ne", "P", "Si")
foreach ($element in $elements) {
    Get-ChildItem "D:\X\ND\A35\finished\${element}35\new\*adopted.ens" | ForEach-Object {
        java -jar "D:\X\ND\McMaster-MSU-Java-NDS\McMaster_MSU_JAVA_NDS_v3.0_01May2025.jar" $_.FullName "$($_.BaseName).pdf"
    }
}
```

## Options

| Flag | Effect |
|------|--------|
| *(none)* | Convert and save PDF, no viewer opened |
| `--open` | Open result in VS Code after conversion |
| `--open --system` | Open result in the system default PDF viewer |

## Notes

- The script resolves partial names and glob patterns against the workspace file tree.
- Multiple files matched by a pattern are converted sequentially.
- The underlying Java tool is `McMaster_MSU_JAVA_NDS_v3.0_01May2025.jar`; ensure it is present at `D:\X\ND\McMaster-MSU-Java-NDS\`.
