# 2025-10-28 cleanup (temporary workspace consolidation)

This dated folder groups prior ad‑hoc scripts, logs, and reports that were cluttering `.github/temp`. Nothing outside `.github/temp` was touched.

## Layout
- `scripts/` — single Python utilities gathered from the former temp root.
- `script_groups/` — prior working sets, preserved by original folder names and dates (no renames).
- `reports/` — markdown and text reports that document verification runs and results.
- `logs/` — log and rpt artifacts (unchanged content).

## Rationale
- Make the temp area navigable without losing provenance.
- Keep historical runs intact under `script_groups/` using their original names and timestamps.

## How to update this manifest later (optional)
Run in Windows PowerShell from the repo root:

```powershell
# Show a compact tree of this cleanup folder
Get-ChildItem -Path 'd:\X\ND\ENSDF\.github\temp\2025-10-28_cleanup' -Recurse |
  Select-Object FullName | Out-String -Width 4096

# Count files per top-level subfolder
'grouppath,count'; 'scripts','script_groups','reports','logs' | ForEach-Object {
  $p = "d:\X\ND\ENSDF\.github\temp\2025-10-28_cleanup\$_";
  $c = (Get-ChildItem -Path $p -Recurse -File | Measure-Object).Count;
  "$_,$c"
}
```

## Notes
- All moves were non-destructive; only locations changed.
- If you create new scratch scripts or logs, drop them into `scripts/` or `logs/` respectively to keep the temp area tidy.
