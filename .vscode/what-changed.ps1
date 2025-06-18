# Simple tool to see what changed in any file compared to yesterday
# Usage: .\what-changed.ps1 filename.ens

param([string]$file)

if (-not $file) {
    Write-Host "Usage: .\what-changed.ps1 filename.ens"
    exit
}

$found = Get-ChildItem -Recurse -Filter $file | Select-Object -First 1
if (-not $found) {
    Write-Host "File not found: $file"
    exit
}

$path = $found.FullName.Replace((Get-Location).Path + "\", "")

# Show the actual changes
git diff HEAD~1 $path
