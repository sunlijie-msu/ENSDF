# ENSDF Column Calibration Script
# Usage: .\column-calibrate.ps1 "path\to\file.ens"

param([string]$FilePath)

if (-not $FilePath -or -not (Test-Path $FilePath)) {
    Write-Host "Usage: .\column-calibrate.ps1 'path\to\file.ens'" -ForegroundColor Red
    exit 1
}

Write-Host "=== ENSDF Column Calibration ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Column Ruler (1-80):" -ForegroundColor Yellow
Write-Host "12345678901234567890123456789012345678901234567890123456789012345678901234567890"
Write-Host "         1         2         3         4         5         6         7         8"
Write-Host ""

# Extract sample records
$content = Get-Content $FilePath
$lRecords = $content | Where-Object { $_ -match "^\s*\w+\s+L\s" } | Select-Object -First 2
$gRecords = $content | Where-Object { $_ -match "^\s*\w+\s+G\s" } | Select-Object -First 2

# Analyze L-records
if ($lRecords) {
    Write-Host "Sample L-records:" -ForegroundColor Green
    foreach ($record in $lRecords) {
        Write-Host $record
        Write-Host "  NUCID (1-5), L (8), Energy (10-19), DE (20-21), J (22-39), T (40-49), DT (50-55)" -ForegroundColor Gray
        Write-Host ""
    }
}

# Analyze G-records
if ($gRecords) {
    Write-Host "Sample G-records:" -ForegroundColor Green
    foreach ($record in $gRecords) {
        Write-Host $record
        Write-Host "  NUCID (1-5), G (8), Energy (10-19), DE (20-21), RI (22-29), DRI (30-31), M (32-41)" -ForegroundColor Gray
        Write-Host ""
    }
}

# Character mapping function (optional detailed analysis)
function Show-CharacterMapping {
    param([string]$Record)
    
    Write-Host "Character mapping:" -ForegroundColor Yellow
    for ($i = 0; $i -lt $Record.Length -and $i -lt 80; $i++) {
        $pos = $i + 1
        $char = $Record[$i]
        if ($char -eq ' ') { $char = 'SP' }
        Write-Host ("{0,2}: {1}" -f $pos, $char)
    }
}

Write-Host "✓ Column calibration complete" -ForegroundColor Green
Write-Host "✓ Script saved as column-calibrate.ps1" -ForegroundColor Green
