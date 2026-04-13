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
$workspaceRoot = Split-Path (Split-Path $scriptDir -Parent) -Parent
$cssRelativePath = ".github/scripts/cambria-markdown-pdf.css"
$cssPath = Join-Path $workspaceRoot $cssRelativePath
$vscodeDir = Join-Path $workspaceRoot ".vscode"
$settingsPath = Join-Path $vscodeDir "settings.json"

if (-not (Test-Path $vscodeDir)) {
    New-Item -ItemType Directory -Path $vscodeDir | Out-Null
}

$css = @"
html, body, body.vscode-body {
  font-family: Cambria, "Times New Roman", serif !important;
  font-size: ${FontSizePt}pt !important;
  line-height: 1.45 !important;
}

body, body.vscode-body,
body.vscode-body p,
body.vscode-body li,
body.vscode-body div,
body.vscode-body span,
body.vscode-body table,
body.vscode-body th,
body.vscode-body td,
body.vscode-body blockquote,
body.vscode-body h1,
body.vscode-body h2,
body.vscode-body h3,
body.vscode-body h4,
body.vscode-body h5,
body.vscode-body h6 {
  font-family: Cambria, "Times New Roman", serif !important;
}

body.vscode-body p,
body.vscode-body li,
body.vscode-body div,
body.vscode-body span,
body.vscode-body table,
body.vscode-body th,
body.vscode-body td,
body.vscode-body blockquote {
  font-size: ${FontSizePt}pt !important;
}

body.vscode-body h1 { font-size: ${FontSizePt + 10}pt !important; }
body.vscode-body h2 { font-size: ${FontSizePt + 7}pt !important; }
body.vscode-body h3 { font-size: ${FontSizePt + 5}pt !important; }
body.vscode-body h4 { font-size: ${FontSizePt + 3}pt !important; }
body.vscode-body h5 { font-size: ${FontSizePt + 1}pt !important; }
body.vscode-body h6 { font-size: ${FontSizePt}pt !important; }

body.vscode-body code,
body.vscode-body pre {
  font-family: Consolas, "Courier New", monospace !important;
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

$settings["markdown-pdf.styles"] = @($cssPath)
$settings["markdown-pdf.stylesRelativePathFile"] = $false
$settings["markdown-pdf.includeDefaultStyles"] = $true
$settings["markdown-pdf.displayHeaderFooter"] = $false
$settings["markdown-pdf.pageBreak"] = $true
$settings["markdown-pdf.scale"] = 1.2

$settings | ConvertTo-Json -Depth 20 | Set-Content -Path $settingsPath -Encoding UTF8

$resolvedMarkdown = if ([System.IO.Path]::IsPathRooted($MarkdownFile)) {
    $MarkdownFile
} else {
    Join-Path $workspaceRoot $MarkdownFile
}

$pdfPath = [System.IO.Path]::ChangeExtension($resolvedMarkdown, ".pdf")

Write-Host "Configured Markdown PDF for Cambria at ${FontSizePt}pt."
Write-Host "CSS: $cssPath"
Write-Host "Settings: $settingsPath"
Write-Host "Markdown file: $resolvedMarkdown"
Write-Host "Expected PDF output after export: $pdfPath"
Write-Host "Next step in VS Code: open the Markdown file and run 'Markdown PDF: Export (pdf)'."