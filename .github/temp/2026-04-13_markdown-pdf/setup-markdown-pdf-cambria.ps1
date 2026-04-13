param(
    [string]$MarkdownFile = "XUNDL/Folder_Lijie_Sun.md",
    [double]$FontSizePt = 14
)

function ConvertTo-Hashtable {
  param([Parameter(ValueFromPipeline = $true)]$InputObject)

  if ($null -eq $InputObject) {
    return $null
  }

  if ($InputObject -is [System.Collections.IDictionary]) {
    $hash = @{}
    foreach ($key in $InputObject.Keys) {
      $hash[$key] = ConvertTo-Hashtable $InputObject[$key]
    }
    return $hash
  }

  if ($InputObject -is [System.Collections.IEnumerable] -and -not ($InputObject -is [string])) {
    $items = @()
    foreach ($item in $InputObject) {
      $items += ConvertTo-Hashtable $item
    }
    return $items
  }

  if ($InputObject -is [psobject] -and $InputObject.PSObject.Properties.Count -gt 0) {
    $hash = @{}
    foreach ($property in $InputObject.PSObject.Properties) {
      $hash[$property.Name] = ConvertTo-Hashtable $property.Value
    }
    return $hash
  }

  return $InputObject
}

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$workspaceRoot = Split-Path (Split-Path (Split-Path $scriptDir -Parent) -Parent) -Parent
$cssRelativePath = ".github/temp/2026-04-13_markdown-pdf/cambria-markdown-pdf.css"
$cssPath = Join-Path $workspaceRoot $cssRelativePath
$vscodeDir = Join-Path $workspaceRoot ".vscode"
$settingsPath = Join-Path $vscodeDir "settings.json"

if (-not (Test-Path $vscodeDir)) {
    New-Item -ItemType Directory -Path $vscodeDir | Out-Null
}

$css = @"
body {
  font-family: Cambria, "Times New Roman", serif;
  font-size: ${FontSizePt}pt;
  line-height: 1.4;
}

p, li, table, th, td, blockquote {
  font-family: Cambria, "Times New Roman", serif;
}

code, pre {
  font-family: Consolas, "Courier New", monospace;
}
"@

Set-Content -Path $cssPath -Value $css -Encoding UTF8

$settings = @{}
if (Test-Path $settingsPath) {
    $raw = Get-Content -Path $settingsPath -Raw
    if ($raw.Trim()) {
    $settingsObject = $raw | ConvertFrom-Json
    $settings = ConvertTo-Hashtable $settingsObject
    }
}

$settings["markdown-pdf.styles"] = @($cssRelativePath)
$settings["markdown-pdf.includeDefaultStyles"] = $true
$settings["markdown-pdf.displayHeaderFooter"] = $false
$settings["markdown-pdf.pageBreak"] = $true

$settings | ConvertTo-Json -Depth 20 | Set-Content -Path $settingsPath -Encoding UTF8

$resolvedMarkdown = if ([System.IO.Path]::IsPathRooted($MarkdownFile)) {
    $MarkdownFile
} else {
    Join-Path $workspaceRoot $MarkdownFile
}

Write-Host "Configured Markdown PDF for Cambria at ${FontSizePt}pt."
Write-Host "CSS: $cssPath"
Write-Host "Settings: $settingsPath"
Write-Host "Markdown file: $resolvedMarkdown"
Write-Host "Next step in VS Code: open the Markdown file and run 'Markdown PDF: Export (pdf)'."