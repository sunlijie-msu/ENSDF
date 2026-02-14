# Move all .ens files to their corresponding old folders and delete new folders in A58

$a58Path = "XUNDL\A58"

# Move .ens files to corresponding old folders
Get-ChildItem -Path $a58Path -Recurse -Filter "*.ens" | ForEach-Object {
    $fileName = $_.Name
    # Extract element prefix (e.g., Ti58, Ca58, Sc58)
    if ($fileName -match '^([A-Z][a-z]?\d+)') {
        $element = $matches[1]
        $oldFolder = Join-Path $a58Path "$element\old"
        
        if (Test-Path $oldFolder) {
            $destination = Join-Path $oldFolder $fileName
            Write-Host "Moving $fileName to $element\old\"
            Move-Item -Path $_.FullName -Destination $destination -Force
        } else {
            Write-Warning "Old folder not found for $element"
        }
    }
}

# Delete all "new" folders in A58
Get-ChildItem -Path $a58Path -Recurse -Directory -Filter "new" | ForEach-Object {
    Write-Host "Deleting $($_.FullName)"
    Remove-Item -Path $_.FullName -Recurse -Force
}

Write-Host "`nReorganization complete!"
