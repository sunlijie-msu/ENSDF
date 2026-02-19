param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string]$OldFile,

    [Parameter(Mandatory = $true, Position = 1)]
    [string]$NewFile
)

$ErrorActionPreference = 'Stop'

$oldPath = (Resolve-Path -LiteralPath $OldFile).Path
$newPath = (Resolve-Path -LiteralPath $NewFile).Path

$compare = Compare-Object `
    (Get-Content -LiteralPath $oldPath) `
    (Get-Content -LiteralPath $newPath)

$psRemoved = @($compare | Where-Object SideIndicator -eq '<=').Count
$psAdded = @($compare | Where-Object SideIndicator -eq '=>').Count
$psTotal = $compare.Count

$previousErrorPreference = $ErrorActionPreference
$ErrorActionPreference = 'Continue'
$gitOutput = & git diff --no-index --numstat -- $oldPath $newPath 2>$null
$gitExitCode = $LASTEXITCODE
$ErrorActionPreference = $previousErrorPreference

$gitAdded = $null
$gitDeleted = $null
$gitStatus = 'unavailable'

if ($gitOutput) {
    $firstLine = ($gitOutput -split "`r?`n" | Where-Object { $_.Trim() -ne '' } | Select-Object -First 1)
    if ($firstLine) {
        $parts = $firstLine -split "`t"
        if ($parts.Count -ge 2) {
            if ($parts[0] -match '^\d+$') { $gitAdded = [int]$parts[0] }
            if ($parts[1] -match '^\d+$') { $gitDeleted = [int]$parts[1] }
            $gitStatus = 'ok'
        }
    }
}

if ($gitStatus -ne 'ok') {
    if ($gitExitCode -eq 0 -or $gitExitCode -eq 1) {
        $gitStatus = 'no-numstat-output'
    }
    else {
        $gitStatus = "git-error($gitExitCode)"
    }
}

[PSCustomObject]@{
    OldFile       = $oldPath
    NewFile       = $newPath
    PowerShellTotal   = $psTotal
    PowerShellRemoved = $psRemoved
    PowerShellAdded   = $psAdded
    GitAdded      = $gitAdded
    GitDeleted    = $gitDeleted
    GitStatus     = $gitStatus
    GitExitCode   = $gitExitCode
} | Format-List
