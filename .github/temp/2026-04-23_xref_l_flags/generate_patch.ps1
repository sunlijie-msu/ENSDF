$src = 'A34/Cl34/new/Cl34_adopted.ens'
$out = '.github/temp/2026-04-23_xref_l_flags/remaining_flags.patch.txt'
$lines = Get-Content $src
$sb = New-Object System.Text.StringBuilder
[void]$sb.AppendLine('*** Begin Patch')
for ($i = 1; $i -lt $lines.Count; $i++) {
    if ($lines[$i] -match '^ 34CLX L XREF=L\s*$') {
        $prev = $lines[$i - 1]
        if ($prev -match '^ 34CL  L ' -and $prev.Length -eq 80 -and $prev.Substring(76, 1) -eq ' ') {
            $new = $prev.Substring(0, 76) + 'L' + $prev.Substring(77, 3)
            [void]$sb.AppendLine('*** Update File: d:\X\ND\ENSDF\A34\Cl34\new\Cl34_adopted.ens')
            if ($i -ge 2) {
                [void]$sb.AppendLine($lines[$i - 2])
            }
            [void]$sb.AppendLine('-' + $prev)
            [void]$sb.AppendLine('+' + $new)
            [void]$sb.AppendLine($lines[$i])
            if ($i + 1 -lt $lines.Count) {
                [void]$sb.AppendLine($lines[$i + 1])
            }
        }
    }
}
[void]$sb.AppendLine('*** End Patch')
Set-Content -Path $out -Value $sb.ToString()
Write-Output $out
