$excel = New-Object -ComObject Excel.Application
$excel.Visible = $false
$workbook = $excel.Workbooks.Open("d:\X\ND\ENSDF\Statistics.xlsx")

foreach ($worksheet in $workbook.Worksheets) {
    Write-Host "`n=== Sheet: $($worksheet.Name) ==="
    $usedRange = $worksheet.UsedRange
    $rowCount = $usedRange.Rows.Count
    $colCount = $usedRange.Columns.Count
    
    for ($row = 1; $row -le $rowCount; $row++) {
        $rowData = @()
        for ($col = 1; $col -le $colCount; $col++) {
            $cell = $worksheet.Cells.Item($row, $col)
            $rowData += $cell.Text
        }
        Write-Host ($rowData -join " | ")
    }
}

$workbook.Close($false)
$excel.Quit()
[System.Runtime.Interopservices.Marshal]::ReleaseComObject($excel) | Out-Null
