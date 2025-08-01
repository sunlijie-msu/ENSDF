# PowerShell wrapper for check_gamma_ordering.py
# This script makes it easier to use wildcards in PowerShell

param(
    [Parameter(Mandatory=$true)]
    [string]$Pattern,
    
    [switch]$Verbose,
    [switch]$Summary
)

# Build file list
$files = Get-ChildItem $Pattern | ForEach-Object { $_.FullName }

if ($files.Count -eq 0) {
    Write-Host "❌ No files found matching pattern: $Pattern" -ForegroundColor Red
    exit 1
}

# Build arguments
$arguments = @()
$arguments += $files

if ($Verbose) { $arguments += "--verbose" }
if ($Summary) { $arguments += "--summary" }

# Run the Python script
& python .github/check_gamma_ordering.py @arguments
