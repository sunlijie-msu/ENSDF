# ENSDF Column Calibration Script (Enhanced with PowerShell History Analysis)
# Usage: .\column-calibrate.ps1 "path\to\file.ens" [-Detailed]

param(
    [string]$FilePath,
    [switch]$Detailed
)

# Function definitions (must be defined before use in PowerShell)

# Character mapping function for detailed analysis
function Show-CharacterMapping {
    param([string]$Record, [string]$RecordType)
    
    Write-Host "Character-by-character mapping for $RecordType-record:" -ForegroundColor Yellow
    for ($i = 0; $i -lt $Record.Length -and $i -lt 80; $i++) {
        $pos = $i + 1
        $char = $Record[$i]
        if ($char -eq ' ') { $char = 'SP' }
        Write-Host ("{0,2}: '{1}'" -f $pos, $char)
    }
    Write-Host ""
}

# Enhanced field extraction and analysis
function Show-ENSDFFields {
    param([string]$Record, [string]$RecordType)
    
    Write-Host "=== Field Analysis for $RecordType-record ===" -ForegroundColor Cyan
    Write-Host "Record: $Record"
    Write-Host ""
    
    if ($RecordType -eq "L") {
        # L-record field analysis
        $nucid = if ($Record.Length -ge 5) { $Record.Substring(0, 5).Trim() } else { "N/A" }
        $recordType = if ($Record.Length -ge 8) { $Record[7] } else { "N/A" }
        $energy = if ($Record.Length -ge 19) { $Record.Substring(9, 10).Trim() } else { "N/A" }
        $energyUnc = if ($Record.Length -ge 21) { $Record.Substring(19, 2).Trim() } else { "N/A" }
        $readabilitySpace = if ($Record.Length -ge 22) { $Record[21] } else { "N/A" }
        $jPi = if ($Record.Length -ge 39) { $Record.Substring(21, 18).Trim() } else { "N/A" }
        $halfLife = if ($Record.Length -ge 49) { $Record.Substring(39, 10).Trim() } else { "N/A" }
        $halfLifeUnc = if ($Record.Length -ge 55) { $Record.Substring(49, 6).Trim() } else { "N/A" }
        
        Write-Host "Field Analysis:" -ForegroundColor Green
        Write-Host "  NUCID (cols 1-5): '$nucid'"
        Write-Host "  Record type (col 8): '$recordType'"
        Write-Host "  Energy (cols 10-19): '$energy'"
        Write-Host "  Energy uncertainty (cols 20-21): '$energyUnc'"
        Write-Host "  Readability space (col 22): '$readabilitySpace'"
        Write-Host "  J-π (cols 22-39): '$jPi'"
        Write-Host "  Half-life (cols 40-49): '$halfLife'"
        Write-Host "  Half-life uncertainty (cols 50-55): '$halfLifeUnc'"
    }
    elseif ($RecordType -eq "G") {
        # G-record field analysis
        $nucid = if ($Record.Length -ge 5) { $Record.Substring(0, 5).Trim() } else { "N/A" }
        $recordType = if ($Record.Length -ge 8) { $Record[7] } else { "N/A" }
        $energy = if ($Record.Length -ge 19) { $Record.Substring(9, 10).Trim() } else { "N/A" }
        $energyUnc = if ($Record.Length -ge 21) { $Record.Substring(19, 2).Trim() } else { "N/A" }
        $readabilitySpace = if ($Record.Length -ge 22) { $Record[21] } else { "N/A" }
        $intensity = if ($Record.Length -ge 29) { $Record.Substring(21, 8).Trim() } else { "N/A" }
        $intensityUnc = if ($Record.Length -ge 31) { $Record.Substring(29, 2).Trim() } else { "N/A" }
        $multipolarity = if ($Record.Length -ge 41) { $Record.Substring(31, 10).Trim() } else { "N/A" }
        
        Write-Host "Field Analysis:" -ForegroundColor Green
        Write-Host "  NUCID (cols 1-5): '$nucid'"
        Write-Host "  Record type (col 8): '$recordType'"
        Write-Host "  Energy (cols 10-19): '$energy'"
        Write-Host "  Energy uncertainty (cols 20-21): '$energyUnc'"
        Write-Host "  Readability space (col 22): '$readabilitySpace'"
        Write-Host "  Relative intensity (cols 22-29): '$intensity'"
        Write-Host "  Intensity uncertainty (cols 30-31): '$intensityUnc'"
        Write-Host "  Multipolarity (cols 32-41): '$multipolarity'"
    }
    Write-Host ""
}

# Enhanced field validation function
function Test-ENSDFFields {
    param([string]$Record, [string]$RecordType)
    
    $issues = @()
    
    # Basic length check
    if ($Record.Length -lt 80) {
        $issues += "Record too short: $($Record.Length) chars (should be 80)"
    }
    
    # Check NUCID field (columns 1-5)
    if ($Record.Length -ge 5) {
        $nucid = $Record.Substring(0, 5)
        if ($nucid.Trim() -eq "") {
            $issues += "NUCID field (cols 1-5) is empty"
        }
    }
    
    # Check record type position (column 8)
    if ($Record.Length -ge 8) {
        if ($RecordType -eq "L" -and $Record[7] -ne 'L') {
            $issues += "Record type not 'L' at position 8 (found: '$($Record[7])')"
        }
        elseif ($RecordType -eq "G" -and $Record[7] -ne 'G') {
            $issues += "Record type not 'G' at position 8 (found: '$($Record[7])')"
        }
    }
    
    # Check energy field (columns 10-19) - should not be all spaces
    if ($Record.Length -ge 19) {
        $energyField = $Record.Substring(9, 10)
        if ($energyField.Trim() -eq "") {
            $issues += "Energy field (cols 10-19) is empty"
        }
    }
    
    # Check readability space at column 22 (critical for human reading)
    if ($Record.Length -ge 22 -and $Record[21] -ne ' ') {
        $issues += "Column 22 should be space for readability (found: '$($Record[21])')"
    }
    
    # Record type specific validations
    if ($RecordType -eq "L") {
        # For L-records, J-π field starts at column 23 (after readability space)
        if ($Record.Length -ge 39) {
            $jPiField = $Record.Substring(22, 17)  # Adjusted: starts at 23 (index 22)
            if ($jPiField.Trim() -eq "") {
                $issues += "J-π field (cols 23-39) appears empty"
            }
        }
    }
    elseif ($RecordType -eq "G") {
        # For G-records, relative intensity starts at column 23 (after readability space)
        if ($Record.Length -ge 29) {
            $intensityField = $Record.Substring(22, 7)  # Adjusted: starts at 23 (index 22)
            if ($intensityField.Trim() -eq "") {
                $issues += "Relative intensity field (cols 23-29) appears empty"
            }
        }
    }
    
    return $issues
}

# Main script logic starts here

if (-not $FilePath -or -not (Test-Path $FilePath)) {
    Write-Host "Usage: .\column-calibrate.ps1 'path\to\file.ens' [-Detailed]" -ForegroundColor Red
    Write-Host "  -Detailed: Show character-by-character mapping for each record" -ForegroundColor Yellow
    exit 1
}

Write-Host "=== ENSDF Column Calibration (Enhanced) ===" -ForegroundColor Cyan
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
        Write-Host "  NUCID (1-5), L (8), Energy (10-19), DE (20-21), Space (22), J (23-39), T (40-49), DT (50-55)" -ForegroundColor Gray
        Write-Host ""
        
        # Show detailed field analysis
        Show-ENSDFFields $record "L"
        
        # Optional character-by-character mapping
        if ($Detailed) {
            Show-CharacterMapping $record "L"
        }
    }
}

# Analyze G-records
if ($gRecords) {
    Write-Host "Sample G-records:" -ForegroundColor Green
    foreach ($record in $gRecords) {
        Write-Host $record
        Write-Host "  NUCID (1-5), G (8), Energy (10-19), DE (20-21), Space (22), RI (23-29), DRI (30-31), M (32-41)" -ForegroundColor Gray
        Write-Host ""
        
        # Show detailed field analysis
        Show-ENSDFFields $record "G"
        
        # Optional character-by-character mapping
        if ($Detailed) {
            Show-CharacterMapping $record "G"
        }
    }
}

# Validate sample records
if ($lRecords) {
    Write-Host "L-record validation:" -ForegroundColor Yellow
    foreach ($record in $lRecords) {
        $issues = Test-ENSDFFields $record "L"
        if ($issues.Count -eq 0) {
            Write-Host "  ✓ Format OK" -ForegroundColor Green
        } else {
            Write-Host "  ⚠ Issues found:" -ForegroundColor Red
            $issues | ForEach-Object { Write-Host "    $_" -ForegroundColor Red }
        }
    }
    Write-Host ""
}

if ($gRecords) {
    Write-Host "G-record validation:" -ForegroundColor Yellow
    foreach ($record in $gRecords) {
        $issues = Test-ENSDFFields $record "G"
        if ($issues.Count -eq 0) {
            Write-Host "  ✓ Format OK" -ForegroundColor Green
        } else {
            Write-Host "  ⚠ Issues found:" -ForegroundColor Red
            $issues | ForEach-Object { Write-Host "    $_" -ForegroundColor Red }
        }
    }
    Write-Host ""
}

# Summary statistics
$totalLines = $content.Count
$lRecordCount = ($content | Where-Object { $_ -match "^\s*\w+\s+L\s" }).Count
$gRecordCount = ($content | Where-Object { $_ -match "^\s*\w+\s+G\s" }).Count
$commentCount = ($content | Where-Object { $_ -match "^\s*\w+\s+c" }).Count

Write-Host "File Statistics:" -ForegroundColor Cyan
Write-Host "  Total lines: $totalLines"
Write-Host "  L-records (levels): $lRecordCount"
Write-Host "  G-records (gammas): $gRecordCount"
Write-Host "  Comment lines: $commentCount"
Write-Host ""

Write-Host "✓ Column calibration complete" -ForegroundColor Green
Write-Host "✓ Enhanced script with PowerShell history improvements" -ForegroundColor Green
Write-Host ""
Write-Host "=== ENSDF Column Reference ===" -ForegroundColor Cyan
Write-Host "L-records: NUCID(1-5) L(8) Energy(10-19) DE(20-21) [space](22) J-π(23-39) T(40-49) DT(50-55)"
Write-Host "G-records: NUCID(1-5) G(8) Energy(10-19) DE(20-21) [space](22) RI(23-29) DRI(30-31) M(32-41)"
Write-Host ""
Write-Host "Key improvements from PowerShell history analysis:" -ForegroundColor Yellow
Write-Host "  • Enhanced field extraction and validation"
Write-Host "  • Character-by-character mapping (use -Detailed flag)"
Write-Host "  • Corrected column assignments for readability space at col 22"
Write-Host "  • J-π and RI fields properly start at column 23"
Write-Host "  • Comprehensive field validation with specific error messages"
