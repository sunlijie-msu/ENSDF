# Simple tool to see what changed in any file compared to yesterday
# Usage: .\what-changed.ps1 filename.ens
# Can be run from anywhere in the workspace

param([string]$file)

if (-not $file) {
    Write-Host "Usage: .\what-changed.ps1 filename.ens"
    exit
}

# Always work from the workspace root
$workspaceRoot = Split-Path -Parent $PSScriptRoot
Push-Location $workspaceRoot

try {
    $found = Get-ChildItem -Recurse -Filter $file | Select-Object -First 1
    if (-not $found) {
        Write-Host "File not found: $file"
        exit
    }

    # Get relative path from workspace root
    $relativePath = $found.FullName.Substring($workspaceRoot.Length + 1)
    
    # Show the actual changes
    git diff HEAD~1 $relativePath
}
finally {
    Pop-Location
}
